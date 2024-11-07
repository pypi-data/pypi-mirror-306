import json
import os
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils import normpath
from vtarget.utils.dtype_optimizer import dtype_optimizer


class InputData:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        script.append("\n# INPUT")

        encoding: str = settings["encoding"] if "encoding" in settings else "ISO-8859-1"
        dtype = str if "as_string" in settings and settings["as_string"] == True else None
        delimiter: str = settings["delimiter"] if "delimiter" in settings and settings["delimiter"] else None
        header: str = None if "has_header" in settings and settings["has_header"] == False else "infer"
        file_path = settings["file_path"] if "file_path" in settings else ""

        is_external = file_path.startswith("http://") or file_path.startswith("https://")
        if file_path and not is_external:
            file_path = normpath(file_path)

        # !! Deploy mode habilitado
        deploy_enabled: bool = settings["deploy_enabled"] if "deploy_enabled" in settings else False

        if deploy_enabled:
            if "deploy_file_path" not in settings or not settings["deploy_file_path"]:
                msg = app_message.dataprep["nodes"]["deploy_enabled"](node_key)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

            file_path = settings["deploy_file_path"] if "deploy_file_path" in settings else ""

            is_external = file_path.startswith("http://") or file_path.startswith("https://")
            if file_path and not is_external:
                file_path = normpath(file_path)

        if not is_external:
            # * check file exists
            file_exists = os.path.exists(file_path)

            if not file_exists:
                msg = app_message.dataprep["nodes"]["input_data"]["file_not_exist"](node_key, file_path)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

            # * get file extension
            _, file_ext = os.path.splitext(file_path)
            file_ext = file_ext[1:]

        else:
            # * check if url exist
            resp = requests.get(file_path)
            if resp.status_code not in range(200, 300):
                msg = app_message.dataprep["nodes"]["input_data"]["url_not_valid"](node_key, file_path)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

            # * get file extension from node config
            file_ext = settings["extension"] if "extension" in settings else ""
            if deploy_enabled:
                file_ext = settings["deploy_extension"] if "deploy_extension" in settings else ""

            # * si la ext no existe en la config, intentar extraer del nombre del archivo
            if not file_ext:
                url_path = urlparse(file_path)
                _, file_ext = os.path.splitext(Path(url_path.path))
                file_ext = file_ext[1:]

            # * Error si no es posible extraer la extension dela archivo
            if not file_ext:
                msg = app_message.dataprep["nodes"]["input_data"]["missing_extension"](node_key)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            bug_handler.console('Leyendo fuente "{}"...'.format(file_path), "trace", flow_id)
            if file_ext in ["csv", "txt"]:
                df = pd.read_csv(
                    file_path,
                    dtype=dtype,
                    encoding=encoding,
                    delimiter=delimiter,
                    header=header,
                )
                dtype_str = "str" if dtype != None else None
                header_str = f"'{header}'" if header else None

                script.append(f"df = pd.read_csv('{file_path}', dtype={dtype_str}, encoding='{encoding}', delimiter='{delimiter}', header={header_str})")

                # add prefix to df columns
                if header is None:
                    df.columns = [f"col_{name}" for name in df.columns]
                    script.append('df.columns = [f"col_{name}" for name in df.columns]')

            elif file_ext == "json":
                orient = settings["orient"] if "orient" in settings else "columns"
                df = pd.read_json(file_path, orient=orient, encoding=encoding)
                script.append(f"df = pd.read_json('{file_path}', orient='{orient}', encoding='{encoding}')")

            elif file_ext in ["xls", "xlsx", "xlsm", "xlsb"]:
                sheet_name = settings["sheet_name"] if "sheet_name" in settings else 0
                if deploy_enabled:
                    sheet_name = settings["deploy_sheet_name"] if "deploy_sheet_name" in settings else sheet_name

                try:
                    df = pd.read_excel(file_path, dtype=dtype, sheet_name=sheet_name, engine=None)
                except Exception as e:
                    if str(e.args[0]).startswith("Worksheet named"):
                        msg = app_message.dataprep["nodes"]["input_data"]["wrong_sheet_name"](node_key, sheet_name)
                    else:
                        msg = f"{e.__class__.__name__}: {' '.join(map(str, e.args))}"
                    return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
                dtype_str = "str" if dtype != None else None
                script.append(f"df = pd.read_excel('{file_path}', dtype={dtype_str}, sheet_name='{sheet_name}')")

            else:
                msg = app_message.dataprep["nodes"]["input_data"]["unknow_format"](node_key, file_ext)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

            df.columns = [str(c) for c in df.columns]

            # revisar si algun nombre de columna tiene espacio al inicio o al final
            if True in [c.startswith((" ", "\t")) or c.endswith((" ", "\t")) for c in df.columns]:
                df.columns = [c.strip() for c in df.columns]
                msg = app_message.dataprep["nodes"]["input_data"]["end_start_spaces"](node_key)
                bug_handler.default_node_log(flow_id, node_key, msg, console_level="warn", bug_level="warning")

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str,e.args))})")
        
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
