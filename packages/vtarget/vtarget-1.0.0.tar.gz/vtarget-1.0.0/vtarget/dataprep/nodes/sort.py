import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Sort:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# SORT")

        sorts = settings["items"] if "items" in settings and settings["items"] else []

        if sorts:
            setting_list = list(
                map(
                    lambda x: (x["field"], int(x["ascending"])),
                    [item for item in sorts if "field" in item and item["field"]],
                )
            )
            if setting_list:
                columns, order = zip(*setting_list)
            else:
                msg = app_message.dataprep["nodes"]["missing_column"](node_key)
                return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        else:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            by = list(columns)
            ascs = list(map(bool, list(order)))
            df = df.sort_values(by=by, ascending=ascs).reset_index(drop=True)
            script.append("df_{} = df.sort_values(by={}, ascending={}).reset_index(drop=True)".format(node_key, by, ascs))
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
