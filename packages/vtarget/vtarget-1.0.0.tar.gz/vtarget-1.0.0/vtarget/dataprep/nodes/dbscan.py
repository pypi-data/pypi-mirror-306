import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from sklearn.cluster import DBSCAN

class DbScan:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# DBSCAN")

        variables: list[str] = settings["variables"] if "variables" in settings and settings["variables"] else []
        algorithm: str = settings["algorithm"] if "algorithm" in settings else "auto"
        metric: str = settings["metric"] if "metric" in settings else "euclidean"
        epsilon: float = settings["epsilon"] if "epsilon" in settings else 0.5
        min_samples: float = settings["min_samples"] if "min_samples" in settings and settings["min_samples"] else 5

        if not variables:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            X = df[variables].values
            dbscan = DBSCAN(algorithm=algorithm, eps=epsilon, min_samples=min_samples, metric=metric).fit(X)
            df["label"] = dbscan.labels_
            
            script.append(f"X = df[{variables}].values")
            script.append(f"dbscan = DBSCAN(algorithm={algorithm}, eps={epsilon}, min_samples={min_samples}, metric={metric}).fit(X)")
            script.append(f'df["label"] = dbscan.labels_')
            
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
