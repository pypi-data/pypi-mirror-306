import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Quality:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        out = pd.DataFrame()
        script.append("\n# QUALITY")

        try:
            cols = []
            for col in df.columns:
                empty = (df[col].values == '').sum() #or df[col].isnull().sum()
                isna = df[col].isna().sum()
                isnull = df[col].isnull().sum()
                unique = len(df[col].unique().tolist())
                duplicated = df[col].duplicated().sum()
                cols.append({ 
                         "column": col, 
                         "nulls": isnull,
                         "nulls_pct": round(isnull / len(df), 4),
                         "nans": isna,
                         "nans_pct": round(isna / len(df), 4),
                         "emptys": empty,
                         "emptys_pct": round(empty / len(df), 4),
                         "uniques": unique,
                         "uniques_pct": round(unique / len(df), 4),
                         "duplicateds": duplicated,
                         "duplicateds_pct": round(duplicated / len(df), 4),
                         })
                
            out = pd.DataFrame.from_dict(cols)
            
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
