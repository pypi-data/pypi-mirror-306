import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.database_connection.utilities import database_utilities

import re

import snowflake.connector
from google.oauth2 import service_account
from pymongo import MongoClient
from snowflake.connector.pandas_tools import write_pandas
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError


class DatabaseWrite:
    def exec(self, flow_id, node_key, pin, settings):

        df: pd.DataFrame = pin["In"].copy()
        script = []
        script.append("\n# DATABASE WRITE")

        try:
            # * Valida que existan todos los campos requeridos y que no estén vacíos dependiendo del tipo de conexion
            checked, msg = database_utilities.check_fields(settings, tier="write_data", node_key=node_key)
            if not checked:
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

            prefix: str = ""
            deploy_enabled: bool = settings["deploy_enabled"] if "deploy_enabled" in settings else False

            if deploy_enabled:
                prefix = "deploy_"

            source = settings[f"{prefix}source"]

            if source == "postgresql" or source == "mysql" or source == "sqlite" or source == "mariadb" or source == "oracle":
                table = settings[f"{prefix}table"]
                save_type = settings[f"{prefix}save_type"]
                connection = database_utilities.get_url_connection(flow_id, settings, with_database=True)
                reset_seq = False
                
                engine = create_engine(connection)
                with engine.connect() as con:
                    if save_type == "truncate":
                        save_type = "append"
                        con.execute(text(f'TRUNCATE "{table}" CASCADE'))
                        reset_seq = True
                        con.commit()
                engine.dispose()

                engine = create_engine(connection)
                with engine.connect() as con:
                    df.to_sql(name=table, con=con, if_exists=save_type, index=False)
                    con.commit()
                engine.dispose()
                
                if reset_seq:
                    engine = create_engine(connection)
                    with engine.connect() as con:
                        for seq, col in con.execute(
                            text(
                                f"""
                                    SELECT
                                        CONCAT(t.table_name,'_',c.column_name,'_seq') AS seq,
                                        c.column_name AS col
                                    FROM 
                                        information_schema.tables t
                                    JOIN 
                                        information_schema.columns c ON t.table_name = c.table_name
                                    WHERE
                                        t.table_name = '{table}'
                                        AND c.column_default LIKE 'nextval%'
                                """
                            )
                        ).fetchall():
                            con.execute(text(f'SELECT SETVAL(\'{seq}\', MAX(public."{table}"."{col}")) FROM "{table}"'))
                        con.commit()
                    engine.dispose()

            elif source == "sqlserver_2000":
                import pyodbc

                table = settings[f"{prefix}table"]
                save_type = settings[f"{prefix}save_type"]

                connection = database_utilities.get_url_connection(flow_id, settings, True)
                try:
                    engine = pyodbc.connect(connection)
                except Exception as e:
                    # TODO: Agregar a la lista de opciones de la vista
                    settings[f"{prefix}source"] = "sqlserver_2000_v2"
                    connection = database_utilities.get_url_connection(flow_id, settings, True)
                    engine = pyodbc.connect(connection)
                cursor = engine.cursor()
                # Preparación de datos
                columns_name = ", ".join(df.columns)
                values = ", ".join(["?" for _ in df.columns])
                params = iter(np.asarray(df).tolist())
                # Limpia o no la tabla seleccionada de la base de datos

                if save_type in ["replace", "truncate"]:  # TODO: Intentar manejar estos casos
                    cursor.execute(f"TRUNCATE TABLE {table}")
                # Inserción
                cursor.executemany(f"INSERT INTO {table} ({columns_name}) VALUES ({values})", params)
                cursor.commit()
                cursor.close()
                engine.close()

            elif source == "bigquery":
                service_account_host = settings[f"{prefix}service_account_host"]
                database = settings[f"{prefix}database"]
                project = settings[f"{prefix}project"]
                table = settings[f"{prefix}table"]
                save_type = settings[f"{prefix}save_type"]

                if save_type == "truncate":
                    save_type = "replace"  # TODO: Intentar manejar estos casos

                with open(service_account_host) as file:
                    service_account_host = json.load(file)
                    credentials = service_account.Credentials.from_service_account_info(service_account_host)
                    df.to_gbq(
                        f"{database}.{table}",
                        project_id=project,
                        if_exists=save_type,
                        credentials=credentials,
                    )

            elif source == "snowflake":
                table = settings[f"{prefix}table"]
                user = settings[f"{prefix}user"]
                database = settings[f"{prefix}database"]
                project = settings[f"{prefix}project"]
                account = settings[f"{prefix}account"]
                password = settings[f"{prefix}password"]
                save_type = settings[f"{prefix}save_type"]

                connection = snowflake.connector.connect(user=user, password=password, account=account, database=project, schema=database)
                write_pandas(
                    connection,
                    df,
                    table,
                    project,
                    database,
                    overwrite=save_type in ["replace", "truncate"],  # TODO: Intentar manejar estos casos
                    auto_create_table=False,
                )
                connection.close()

            elif source == "mongodb":
                mongo_client = settings[f"{prefix}mongo_client"]
                database = settings[f"{prefix}database"]
                table = settings[f"{prefix}table"]
                save_type = settings[f"{prefix}save_type"]

                client = MongoClient(mongo_client)
                db = client[database]
                collection = db[table]
                if save_type in ["replace", "truncate"]:  # TODO: Intentar manejar estos casos
                    collection.drop()
                collection.insert_many(df.to_dict("records"), ordered=True)
                client.close()

            else:
                msg = app_message.dataprep["nodes"]["database_write"]["source_required"](node_key)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        except ProgrammingError as e:
            # Utiliza expresiones regulares para extraer el nombre de la columna y la tabla desde el mensaje de error
            column_match = re.search(r'column "(.*?)" of relation', str(e.orig))
            table_match = re.search(r'relation "(.*?)" does not exist', str(e.orig))

            column_name = column_match.group(1) if column_match else None
            table_name = table_match.group(1) if table_match else None

            if column_name and table_name:
                msg = app_message.dataprep["nodes"]["database_write"]["no_column_in_table"](node_key, column_name, table_name)
            else:
                msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))

            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": df}
