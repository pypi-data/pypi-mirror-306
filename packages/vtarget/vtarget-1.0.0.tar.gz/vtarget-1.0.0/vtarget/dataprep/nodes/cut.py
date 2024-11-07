import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Cut:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()

        script.append("\n# CUT")

        field: str = settings["field"] if "field" in settings else None
        last_n: float = settings["last_n"] if "last_n" in settings else None
        first_n: float = settings["first_n"] if "first_n" in settings else None
        n_to_last: float = settings["n_to_last"] if "n_to_last" in settings else None

        if not field:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        if not first_n and not last_n and not n_to_last:
            msg = app_message.dataprep["nodes"]["cut"]["no_cutting_parameter"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            if first_n:
                df["first_n"] = df[field].str[:first_n]
            elif last_n:
                df["last_n"] = df[field].str[-last_n:]
            elif n_to_last:
                df["n_to_last"] = df[field].str[n_to_last:]
            else:
                msg = app_message.dataprep["nodes"]["cut"]["no_type_cut"](node_key)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

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
