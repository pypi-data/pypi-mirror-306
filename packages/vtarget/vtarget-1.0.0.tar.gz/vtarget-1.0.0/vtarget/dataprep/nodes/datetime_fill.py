import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class DatetimeFill:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# DATETIME FILL")

        time_column: str = settings["time_column"] if "time_column" in settings else None
        key_columns: list = settings["key_columns"] if "key_columns" in settings else []
        frequency = settings["frequency"] if "frequency" in settings else None
        msg = ''

        if not time_column:
            msg = app_message.dataprep["nodes"]["datetime_fill"]["time_column_required"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        if not key_columns:
            msg = app_message.dataprep["nodes"]["datetime_fill"]["key_column_required"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        if not frequency:
            msg = app_message.dataprep["nodes"]["datetime_fill"]["frequency_column_required"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        if time_column and key_columns and frequency:
            try:
                df = df.set_index([time_column] + key_columns).unstack(fill_value=0).asfreq(frequency, fill_value=0).stack().sort_index(level=1).reset_index()
                script.append(f"df = df.set_index({[time_column] + key_columns}).unstack(fill_value=0).asfreq('{frequency}', fill_value=0).stack().sort_index(level=1).reset_index()")
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
            msg = app_message.dataprep["nodes"]["datetime_fill"]["properties_not_provided"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
