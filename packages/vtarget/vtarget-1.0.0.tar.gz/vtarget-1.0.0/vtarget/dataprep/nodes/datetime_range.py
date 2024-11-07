import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class DatetimeRange:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pd.DataFrame()
        script.append("\n# DATETIME RANGE")

        start_date: str = settings["start_date"] if "start_date" in settings else None
        end_date: str = settings["end_date"] if "end_date" in settings else None
        frequency: str = settings["frequency"] if "frequency" in settings else None

        if not start_date:
            msg = app_message.dataprep["nodes"]["datetime_range"]["start_date_required"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        if not end_date:
            msg = app_message.dataprep["nodes"]["datetime_range"]["end_date_required"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        if not frequency:
            msg = app_message.dataprep["nodes"]["datetime_range"]["frequency_is_required"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        if start_date and end_date and frequency:
            try:
                df["date_range"] = pd.date_range(start=start_date, end=end_date, freq=frequency)
                script.append(f"df['date_range'] = pd.date_range(start='{start_date}', end='{end_date}', freq='{frequency}'")

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
            msg = app_message.dataprep["nodes"]["datetime_range"]["properties_not_provided"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
