import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class KeepCol:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df_Src: pd.DataFrame = pin["Src"].copy()
        df_Val: pd.DataFrame = pin["Val"].copy()
        out = pd.DataFrame()
        script.append("\n# KEEP_COL")
        
        column: str = settings["column"] if "column" in settings else ''
        
        if not column:
            msg = app_message.dataprep["nodes"]["required_prop"](node_key, "column")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            out = df_Src[df_Val[column]]
            
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": out},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": out}
