import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message

class Concat:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        
        # * Validar que exista df de entrada en el puerto A
        if "A" not in pin:
            msg = app_message.dataprep["nodes"]["missing_df"](node_key, "A")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
            
        # * Validar que exista df de entrada en el puerto B
        if "B" not in pin:
            msg = app_message.dataprep["nodes"]["missing_df"](node_key, "B")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        script.append("\n# CONCAT")
        df_A: pd.DataFrame = pin["A"].copy() if "A" in pin else pd.DataFrame()
        df_B: pd.DataFrame = pin["B"].copy() if "B" in pin else pd.DataFrame()

        # * Advertir si el dataframe está vacío
        if df_A.empty:
            msg = app_message.dataprep["nodes"]["empty_df"](node_key, "A")
            bug_handler.default_node_log(flow_id, node_key, msg, bug_level="warning", console_level="warn")

        # * Advertir si el dataframe está vacío
        if df_B.empty:
            msg = app_message.dataprep["nodes"]["empty_df"](node_key, "B")
            bug_handler.default_node_log(flow_id, node_key, msg, bug_level="warning", console_level="warn")

        selected_A: list = settings["a"] if "a" in settings and settings["a"] else []
        selected_B: list = settings["b"] if "b" in settings and settings["b"] else []
        
        # * Limpiar columnas seleccionadas dejando solo las válidas
        valid_columns_A : list = [ x for x in selected_A if x in df_A.columns ]
        valid_columns_B : list = [ x for x in selected_B if x in df_B.columns ]
        
        # * Validar que exista columnas seleccionadas en la config de ambos Dataframes
        if not valid_columns_A:
            msg = app_message.dataprep["nodes"]["empty_entry_list"](node_key, "A")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        
        if not valid_columns_B:
            msg = app_message.dataprep["nodes"]["empty_entry_list"](node_key, "B")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        
        df_A = df_A[valid_columns_A]
        script.append("df_A = df_A[{}]".format(valid_columns_A))
        
        df_B = df_B[valid_columns_B]
        script.append("df_B = df_B[{}]".format(valid_columns_B))

        try:
            df = pd.concat([df_A, df_B], ignore_index=True)
            script.append("df = pd.concat([df_A, df_B], ignore_index=True)")
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
