import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
import numpy as np
from ast import literal_eval

class Replace:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        
        script.append("\n# REPLACE")
        
        all: bool = settings["all"] if "all" in settings else False
        columns: list[str] = settings["columns"] if "columns" in settings else []
        old_value: str = settings["old_value"] if "old_value" in settings else ''
        new_value: str = settings["new_value"] if "new_value" in settings else ''
        

        if not all and not columns:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        
        # Parse numeric values
        try:
            new_value = literal_eval(new_value)
            old_value = literal_eval(old_value)
        except Exception as e:
            pass
        
        try:
            if old_value == 'nan':
                old_value = np.nan
            elif old_value == 'empty':
                old_value = ''
                
            if new_value == 'nan':
                new_value = np.nan
            elif new_value == 'empty':
                new_value = ''
                
            if all:
                if old_value == 'null' or old_value == '':
                    df.fillna(new_value, inplace=True)
                else:
                    df.replace(old_value, new_value, inplace = True)
            else:
                for col in columns:
                    if old_value == 'null' or old_value == '':
                        df[col].fillna(new_value, inplace=True)
                    else:
                        print(df[col].dtype)
                        df[col].replace(old_value, new_value, inplace=True)
            
        except Exception as e:
            print(e)
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
