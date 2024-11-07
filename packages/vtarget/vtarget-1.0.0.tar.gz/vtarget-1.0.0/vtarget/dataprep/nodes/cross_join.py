import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class CrossJoin:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        
        # Validar que exista df de entrada en el puerto Tgt
        if "Tgt" not in pin:
            msg = app_message.dataprep["nodes"]["missing_df"](node_key, "Tgt")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
            
        # Validar que exista df de entrada en el puerto Src
        if "Src" not in pin:
            msg = app_message.dataprep["nodes"]["missing_df"](node_key, "Src")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        script.append("\n# CROSS_JOIN")
        df_T: pd.DataFrame = pin["Tgt"].copy() if "Tgt" in pin else pd.DataFrame()
        df_S: pd.DataFrame = pin["Src"].copy() if "Src" in pin else pd.DataFrame()
        
        # Advertir si el dataframe está vacío
        if df_T.empty:
            msg = app_message.dataprep["nodes"]["empty_df"](node_key, "Tgt")
            bug_handler.default_node_log(flow_id, node_key, msg, bug_level="warning", console_level="warn")

        # Advertir si el dataframe está vacío
        if df_S.empty:
            msg = app_message.dataprep["nodes"]["empty_df"](node_key, "Src")
            bug_handler.default_node_log(flow_id, node_key, msg, bug_level="warning", console_level="warn")

        # Validar que exista columnas seleccionadas en la config de ambos Dataframes
        selected_T: list = settings["tgt"] if "tgt" in settings and settings["tgt"] else None
        selected_S: list = settings["src"] if "src" in settings and settings["src"] else None
        
        if not selected_T:
            msg = app_message.dataprep["nodes"]["empty_entry_list"](node_key, "Target")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        if not selected_S:
            msg = app_message.dataprep["nodes"]["empty_entry_list"](node_key, "Source")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        df_T = df_T[selected_T]
        script.append("df_T = df_T[{}]".format(selected_T))
        
        df_S = df_S[selected_S]
        script.append("df_S = df_S[{}]".format(selected_S))

        try:
            df = pd.merge(df_T, df_S, how="cross")  # , validate="many_to_one")
            script.append("df = pd.merge(df_T, df_S, how='cross')")
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
