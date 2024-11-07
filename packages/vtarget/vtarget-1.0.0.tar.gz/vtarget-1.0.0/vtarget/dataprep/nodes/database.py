import json

import numpy as np
import pandas as pd
import snowflake.connector
from google.cloud import bigquery
from google.oauth2 import service_account
from pymongo import MongoClient
from sqlalchemy import create_engine, text

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.database_connection.utilities import database_utilities
from vtarget.utils.bq_to_pandas_type import bq_to_pandas_type
from vtarget.utils.dtype_optimizer import dtype_optimizer


class Database:
    def exec(self, flow_id, node_key, pin, settings):

        script = []
        script.append("\n# DATABASE")

        try:
            # * Valida que existan todos los campos requeridos y que no estén vacíos dependiendo del tipo de conexion
            checked, msg = database_utilities.check_fields(settings, tier="data")
            if not checked:
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

            prefix: str = ""
            deploy_enabled: bool = settings["deploy_enabled"] if "deploy_enabled" in settings else False

            if deploy_enabled:
                prefix = "deploy_"

            source = settings[f"{prefix}source"]

            if source == "postgresql" or source == "mysql" or source == "sqlite" or source == "mariadb" or source == "oracle":
                table: str = settings[f"{prefix}table"] if (f"{prefix}table" in settings and settings[f"{prefix}table"] is not None) else None
                query: str = settings[f"{prefix}query"] if (f"{prefix}query" in settings and settings[f"{prefix}query"] is not None) else None

                connection = database_utilities.get_url_connection(flow_id, settings, with_database=True)
                engine = create_engine(connection)
                if not source in ["oracle"]:
                    table = f'"{table}"'
                df = pd.read_sql(text(query if query else f"SELECT * FROM {table}"), con=engine.connect())
                engine.dispose()

            elif source == "sqlserver_2000":
                import pyodbc

                table: str = settings[f"{prefix}table"] if (f"{prefix}table" in settings and settings[f"{prefix}table"] is not None) else None
                query: str = settings[f"{prefix}query"] if (f"{prefix}query" in settings and settings[f"{prefix}query"] is not None) else None

                connection = database_utilities.get_url_connection(flow_id, settings, True)
                try:
                    engine = pyodbc.connect(connection)
                except Exception as e:
                    # TODO: Agregar a la lista de opciones de la vista
                    settings[f"{prefix}source"] = "sqlserver_2000_v2"
                    connection = database_utilities.get_url_connection(flow_id, settings, True)
                    engine = pyodbc.connect(connection)
                cursor = engine.cursor()
                cursor.execute(query if query else f"SELECT * FROM [{table}]")
                results = np.array(cursor.fetchall())
                column_names = [str(column[0]) for column in cursor.description]
                df = pd.DataFrame(results, columns=column_names)
                cursor.close()
                engine.close()

            elif source == "bigquery":
                service_account_host = settings[f"{prefix}service_account_host"]
                database = settings[f"{prefix}database"]
                project = settings[f"{prefix}project"]
                table: str = settings[f"{prefix}table"] if (f"{prefix}table" in settings and settings[f"{prefix}table"] is not None) else None
                query: str = settings[f"{prefix}query"] if (f"{prefix}query" in settings and settings[f"{prefix}query"] is not None) else None

                with open(service_account_host) as file:
                    service_account_host = json.load(file)
                    credentials = service_account.Credentials.from_service_account_info(service_account_host)
                    client = bigquery.Client(credentials=credentials)
                    if table is not None:
                        table_ref = client.dataset(database, project=project).table(table)
                        table_type = client.get_table(table_ref).table_type
                        schema = client.get_table(table_ref).schema
                        client.close()

                        if table_type == "TABLE":
                            rows = client.list_rows(table_ref)
                            df = rows.to_dataframe()
                        elif table_type == "VIEW":
                            query = f"SELECT * FROM `{project}.{database}.{table}`"
                            query_job = client.query(query)
                            df = query_job.to_dataframe()
                        
                        df = bq_to_pandas_type.convert_dataframe(df, schema=schema)

                            # batch_size = 2000000
                            # total_results = 0
                            # df_batches = []
                            # while True:
                            #     credentials = service_account.Credentials.from_service_account_info(service_account_host)
                            #     client = bigquery.Client(credentials=credentials)
                            #     query = f"""SELECT
                            #         sucursal,
                            #         rut,
                            #         cliente,
                            #         direccion,
                            #         comuna,
                            #         ciudad,
                            #         vendedor,
                            #         cod_vendedor,
                            #         dia_visita,
                            #         frecuencia_visita,
                            #         fecha_programada,
                            #         supervisor,
                            #         region,
                            #         tipo,
                            #         nro_pedido,
                            #         fecha_pedido,
                            #         codigo_vendedor_realizado,
                            #         codigo_vendedor_asignado_hoy
                            #     FROM
                            #         espol-data.vistas.cartera_clientes_atendidos
                            #     WHERE
                            #         region IS NOT NULL AND
                            #         tipo IS NOT NULL AND
                            #         nro_pedido IS NOT NULL AND
                            #         fecha_pedido IS NOT NULL AND
                            #         codigo_vendedor_realizado IS NOT NULL
                            #     LIMIT {batch_size}
                            #     OFFSET {total_results}
                            #     """
                            #     query_job = client.query(query)
                            #     results = query_job.result(max_results=batch_size)

                            #     df_batch = results.to_dataframe()
                            #     df_batches.append(df_batch)

                            #     total_results += batch_size
                            #     if len(df_batch) < batch_size:
                            #         break

                            #     client.close()

                            # df = pd.concat(df_batches, ignore_index=True)
                    elif query is not None:
                        query_job = client.query(query)
                        df = query_job.to_dataframe()
                    else:
                        msg = app_message.dataprep["nodes"]["database_utilities"]["check_optional_fields"](node_key)
                        return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

            elif source == "snowflake":
                table: str = settings[f"{prefix}table"] if (f"{prefix}table" in settings and settings[f"{prefix}table"] is not None) else None
                query: str = settings[f"{prefix}query"] if (f"{prefix}query" in settings and settings[f"{prefix}query"] is not None) else None

                user = settings[f"{prefix}user"]
                database = settings[f"{prefix}database"]
                project = settings[f"{prefix}project"]
                account = settings[f"{prefix}account"]
                password = settings[f"{prefix}password"]

                connection = snowflake.connector.connect(user=user, password=password, account=account, database=project, schema=database)
                cursor = connection.cursor()
                cursor.execute(query if query else f'SELECT * FROM "{table}"')
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(results, columns=column_names)
                connection.close()
                cursor.close()

            elif source == "mongodb":
                mongo_client = settings[f"{prefix}mongo_client"]
                database = settings[f"{prefix}database"]
                table = settings[f"{prefix}table"]

                client = MongoClient(mongo_client)
                db = client[database]
                collection = db[table]
                data = list(collection.find())
                df = pd.DataFrame(data)
                client.close()

            else:
                msg = app_message.dataprep["nodes"]["database"]["source_required"](node_key)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
        
        # Intenta optmizar los tipos de datos
        try:
            dtype_optimizer.optimize(df)
        except Exception as e:
            print("Error al intentar optimizar tipo de datos", str(e))
        
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
