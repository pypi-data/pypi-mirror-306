import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Rolling:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# ROLLING")

        column: str = settings["column"] if "column" in settings else None
        window: int = settings["window"] if "window" in settings else 1
        operation = settings["operation"] if "operation" in settings else None

        if not column:
            msg = app_message.dataprep["nodes"]["rolling"]["column_required"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        if not operation:
            msg = app_message.dataprep["nodes"]["rolling"]["operation_required"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        if column and operation:
            try:
                obj = df[column].rolling(window=window, min_periods=0, closed="right")
                script.append(f"obj = df['{column}'].rolling(window={window}, min_periods=0, closed='right')")

                if operation == "sum":
                    df["rolling"] = obj.sum()
                    script.append("\n# Sum")
                    script.append(f'df["rolling"] = obj.sum()')
                elif operation == "mean":
                    df["rolling"] = obj.mean()
                    script.append("\n# Mean")
                    script.append(f'df["rolling"] = obj.mean()')
                elif operation == "median":
                    df["rolling"] = obj.median()
                    script.append("\n# Median")
                    script.append(f'df["rolling"] = obj.median()')
                elif operation == "min":
                    df["rolling"] = obj.min()
                    script.append("\n# Min")
                    script.append(f'df["rolling"] = obj.min()')
                elif operation == "max":
                    df["rolling"] = obj.max()
                    script.append("\n# Max")
                    script.append(f'df["rolling"] = obj.max()')
                    
                df.reset_index(drop=True, inplace=True)

            except Exception as e:
                msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
                return bug_handler.default_node_log(flow_id, node_key, msg, str(e))

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
        else:
            msg = app_message.dataprep["nodes"]["rolling"]["properties_not_provided"](node_key) 
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
