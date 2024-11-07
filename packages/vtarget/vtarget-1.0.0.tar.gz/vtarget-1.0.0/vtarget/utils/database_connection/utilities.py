from vtarget.language.app_message import app_message
from vtarget.utils.database_connection.field_validation import FIELD_VALIDATION_DATABASE
from vtarget.utils.encrypter import encrypter, DECRYPT_KEY

class Utilities:
    def __init__(self):
        pass

    def check_fields(self, data: dict = dict(), tier: str = str(), node_key: str = str()) -> tuple:
        """
        Método que retorna si los datos entregados en conjunto con el nivel son válidos
        """

        prefix: str = ""  # Se usa para obtener claves y valores en modo deploy
        if "deploy_enabled" in data and data["deploy_enabled"]:
            prefix = "deploy_"

        source: str = data[f"{prefix}source"] if (f"{prefix}source" in data and data[f"{prefix}source"] is not None) else None
        # Valida que venga el recurso de conexión
        if not source:
            return False, app_message.dataprep["nodes"]["database_utilities"]["source_required"](node_key)

        # Valida que el recurso de conexión exista en el arreglo
        if not (source in FIELD_VALIDATION_DATABASE and tier in FIELD_VALIDATION_DATABASE[source]):
            return False, app_message.dataprep["nodes"]["database_utilities"]["check_missing_source"](node_key)

        fields: list = FIELD_VALIDATION_DATABASE[source][tier]["required"]

        # Valida que cada campo tenga valor
        for field in fields:
            field = prefix + field
            if not field in data:
                return False, app_message.dataprep["nodes"]["database_utilities"]["check_fields_to_connection"](node_key, field)

            value: any = data[field]
            if not value:
                return False, app_message.dataprep["nodes"]["database_utilities"]["check_empty_fields"](node_key, field)

        if "optional" in FIELD_VALIDATION_DATABASE[source][tier]:
            # Se recorren los arreglos de claves
            for _list in FIELD_VALIDATION_DATABASE[source][tier]["optional"]:
                flag: bool = False

                # Se recorren las claves
                for field in _list:
                    field = prefix + field
                    # Valida que el campo exista en la data y que tenga un valor
                    if field in data and data[field]:
                        flag = True
                        break

                # En caso que no exista ninguna clave con valor, da error
                if not flag:
                    # return False, "(check_fields) Falló la validación de variables opcionales"
                    return False, app_message.dataprep["nodes"]["database_utilities"]["check_optional_fields"](node_key)

        return True, ""

    def get_url_connection(self, flow_id: str, data: dict, with_database: bool = False) -> str:
        """
        Método que retorna el string de conexión para cada base de datos
        """

        prefix: str = ""  # Se usa para obtener claves y valores en modo deploy
        if "deploy_enabled" in data and data["deploy_enabled"]:
            prefix = "deploy_"

        if data[f"{prefix}source"] == "sqlite":
            return f"sqlite:///{data[f'{prefix}path']}"

        if data[f"{prefix}source"] == "postgresql":
            PASS: str = data[f"{prefix}password"] if (f"{prefix}password" in data and data[f"{prefix}password"] is not None) else ""
            # password: str = ":" + data[f"{prefix}password"] if (f"{prefix}password" in data and data[f"{prefix}password"] is not None) else ""
            port: str = ":" + str(data[f"{prefix}port"]) if (f"{prefix}port" in data and data[f"{prefix}port"] is not None) else ""
            database: str = "/" + data[f"{prefix}database"] if with_database else ""

            DECRYPTEDPASS = ":" + encrypter.decrypt(PASS, DECRYPT_KEY) if PASS is not None and DECRYPT_KEY is not None else ""

            return f"postgresql://{data[f'{prefix}user']}{DECRYPTEDPASS}@{data[f'{prefix}host']}{port}" + database

        if data[f"{prefix}source"] == "sqlserver_2000":
            # ['SQL Server', 'SQL Server Native Client 11.0', 'ODBC Driver 17 for SQL Server']
            PASS: str = data[f"{prefix}password"] if (f"{prefix}password" in data and data[f"{prefix}password"] is not None) else ""
            database: str = f'Database={data[f"{prefix}database"]};' if with_database else ""

            DECRYPTEDPASS = (encrypter.decrypt(PASS, DECRYPT_KEY)) if PASS is not None and DECRYPT_KEY is not None else ""

            return "DRIVER={SQL Server};" + f'USER={data[f"{prefix}user"]};PASSWORD={DECRYPTEDPASS};' + database + f'SERVER={data[f"{prefix}host"]};PORT={data[f"{prefix}port"]};'

        if data[f"{prefix}source"] == "sqlserver_2000_v2":
            # ['SQL Server', 'SQL Server Native Client 11.0', 'ODBC Driver 17 for SQL Server']
            PASS: str = data[f"{prefix}password"] if (f"{prefix}password" in data and data[f"{prefix}password"] is not None) else ""
            database: str = f'Database={data[f"{prefix}database"]};' if with_database else ""

            DECRYPTEDPASS = (encrypter.decrypt(PASS, DECRYPT_KEY)) if PASS is not None and DECRYPT_KEY is not None else ""

            return "DRIVER={SQL Server};" + f'UID={data[f"{prefix}user"]};PWD={DECRYPTEDPASS};' + database + f'SERVER={data[f"{prefix}host"]};PORT={data[f"{prefix}port"]};'

        if data[f"{prefix}source"] == "mysql" or data[f"{prefix}source"] == "mariadb":
            PASS: str = data[f"{prefix}password"] if (f"{prefix}password" in data and data[f"{prefix}password"] is not None) else ""
            # password: str = ":" + data[f"{prefix}password"] if (f"{prefix}password" in data and data[f"{prefix}password"] is not None) else ""
            port: str = ":" + str(data[f"{prefix}port"]) if (f"{prefix}port" in data and data[f"{prefix}port"] is not None) else ""
            database: str = "/" + data[f"{prefix}database"] if with_database else ""

            DECRYPTEDPASS = ":" + encrypter.decrypt(PASS, DECRYPT_KEY) if PASS is not None and DECRYPT_KEY is not None else ""

            return f"mysql+pymysql://{data[f'{prefix}user']}{DECRYPTEDPASS}@{data[f'{prefix}host']}{port}" + database

        if data[f"{prefix}source"] == "oracle":
            PASS: str = data[f"{prefix}password"] if (f"{prefix}password" in data and data[f"{prefix}password"] is not None) else ""
            # password: str = ":" + data[f"{prefix}password"] if (f"{prefix}password" in data and data[f"{prefix}password"] is not None) else ""
            port: str = ":" + str(data[f"{prefix}port"]) if (f"{prefix}port" in data and data[f"{prefix}port"] is not None) else ""
            database: str = "/" + data[f"{prefix}database"] if with_database else ""
            service_name: str = "?service_name=" + data[f"{prefix}service_name"] if data[f"{prefix}service_name"] is not None or len(data[f"{prefix}service_name"]) > 0 else ""

            DECRYPTEDPASS = ":" + encrypter.decrypt(PASS, DECRYPT_KEY) if PASS is not None and DECRYPT_KEY is not None else ""

            return f"oracle+oracledb://{data[f'{prefix}user']}{DECRYPTEDPASS}@{data[f'{prefix}host']}{port}{service_name}"


database_utilities = Utilities()
