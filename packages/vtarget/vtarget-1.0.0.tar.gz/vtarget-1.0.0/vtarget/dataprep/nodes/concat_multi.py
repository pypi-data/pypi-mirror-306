import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message

class Concat_Multi:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        script.append("\n# CONCAT MULTI")
        
        inputs: list = settings["inputs"] if "inputs" in settings else []
        if not inputs:
            msg = app_message.dataprep["nodes"]["required_prop"](node_key, "inputs")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        
        dfs_to_concat: list[pd.DataFrame] = []
        script.append(f"dfs_to_concat = []")
        for input in inputs:
            port: str = input["port"] if "port" in input else None
            fields: list[str] = input["fields"] if "fields" in input else []
            
            if not port or not fields:
                continue
            
            # * Validar que exista df de entrada en el puerto
            if fields and port not in pin:
                msg = app_message.dataprep["nodes"]["missing_df"](node_key, port)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
            
            df_port: pd.DataFrame = pin[port].copy() if port in pin else pd.DataFrame()
            # * Advertir si el dataframe está vacío
            if df_port.empty:
                msg = app_message.dataprep["nodes"]["empty_df"](node_key, port)
                bug_handler.default_node_log(flow_id, node_key, msg, bug_level="warning", console_level="warn")
                
            # * Limpiar columnas seleccionadas dejando solo las válidas
            valid_fields : list = [ x for x in fields if x in df_port.columns ]
            
            # * Validar que exista columnas seleccionadas en la config de ambos Dataframes
            if not valid_fields:
                msg = app_message.dataprep["nodes"]["empty_entry_list"](node_key, port)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

            df_port = df_port[valid_fields]
            dfs_to_concat.append(df_port)
            
            script.append(f"\n#Port {port}")
            script.append(f"df_{port} = df_{port}[{valid_fields}]")
            script.append(f"dfs_to_concat.append(df_{port})")

        try:
            df = pd.concat(dfs_to_concat, ignore_index=True)
            script.append("\n#Concat all")
            script.append("df_out = pd.concat(dfs_to_concat, ignore_index=True)")
            
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
