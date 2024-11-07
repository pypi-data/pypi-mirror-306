import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Split:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# SPLIT")

        # field, separator, split_type
        field: str = settings["field"] if "field" in settings and settings["field"] != "" else None
        separator: str = settings["separator"] if "separator" in settings and settings["separator"] != "" else None
        split_type: str = settings["split_type"] if "split_type" in settings and settings["split_type"] != "" else None
        n_divisions: int = settings["n_divisions"] if "n_divisions" in settings and settings["n_divisions"] > 0 else None

        if not field:
            msg = app_message.dataprep["nodes"]["required_prop"](node_key, "Field")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        if not separator or not split_type:
            msg = app_message.dataprep["nodes"]["required_prop"](node_key, "Separator" if not separator else "Split Type")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            if split_type == "column":
                new_cols = df[field].str.split(separator, expand=True, n=n_divisions).fillna("")
                new_cols.columns = [f"{field}_{i}" for i in range(new_cols.shape[1])]
                df = pd.concat([df, new_cols], axis=1)

                script.append("new_cols = df['{}'].str.split('{}', expand=True, n={})".format(field, separator, n_divisions))
                script.append("new_cols.columns = [f'" + field + "_{i}' for i in range(new_cols.shape[1])]")
                script.append("df = pd.concat([df, new_cols], axis=1)")

            elif split_type == "row":
                df_split = df[field].str.split(separator, expand=True).stack().reset_index(level=1, drop=True).rename(f"{field}_value_split")
                df = df.join(df_split).reset_index(drop=True)

                script.append(f"df_split = df['{field}'].str.split('{separator}', expand=True).stack().reset_index(level=1, drop=True).rename('{field}_value_split')")
                script.append("df = df.join(df_split).reset_index(drop=True)")
            else:
                print("Error")

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
