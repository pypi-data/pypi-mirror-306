import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from sklearn.cluster import KMeans

class Kmeans:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# KEMANS")

        variables: list[str] = settings["variables"] if "variables" in settings and settings["variables"] else []
        algorithm: str = settings["algorithm"] if "algorithm" in settings else "auto"
        init: str = settings["init"] if "init" in settings else "k-means++"
        n_init: any = settings["random_state"] if "random_state" in settings else 'auto'
        n_clusters: float = settings["n_clusters"] if "n_clusters" in settings else 8
        random_state: float = settings["random_state"] if "random_state" in settings else None

        if not variables:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            X = df[variables].values
            kmeans  = KMeans(algorithm=algorithm, n_clusters=n_clusters, random_state=random_state, init=init, n_init=n_init).fit(X)
            df["label"] = kmeans.labels_
            
            script.append(f"X = df[{variables}].values")
            script.append(f"kmeans  = KMeans(algorithm={algorithm}, n_clusters={n_clusters}, random_state={random_state}, init={init}, n_init={n_init}).fit(X)")
            script.append(f'df["label"] = kmeans.labels_')
            
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
