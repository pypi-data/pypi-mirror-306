import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
import networkx as nx
from community import community_louvain

class Louvain:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        out: pd.DataFrame = pd.DataFrame()
        stats: pd.DataFrame = pd.DataFrame()
        
        script.append("\n# LOUVAIN")
        
        source: str = settings["source"] if "source" in settings else None
        target: str = settings["target"] if "target" in settings else None
        weight: str | None = settings["weight"] if "weight" in settings else None
        resolution: float = settings["resolution"] if "resolution" in settings else 1
        seed: float = settings["seed"] if "seed" in settings else None

        if not source:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        
        if not target:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            G: nx.Graph = nx.from_pandas_edgelist(df, source=source, target=target)
            
            partition = community_louvain.best_partition(G, resolution=resolution, random_state=seed) # con el param resolution menor a 1 fuerzo a buscar grupos más pequeños
            values = list(partition.values())
            
            # DF con cada nodo y su comunidad
            out = pd.DataFrame({'node': G.nodes, 'community': values})
            # Asigna un tipo por nodo
            out['type'] = source
            mask = out['node'].isin(df[source])
            out.loc[~mask, 'type'] = target
            
            grouped = out.copy().groupby(['community','type']).count().reset_index()
            
            print("\ngrouped")
            print(grouped)
            print(grouped.columns)
            print(grouped.index)
            
            stats = pd.pivot_table(grouped, index='community', columns='type', values='node').reset_index().rename_axis(None, axis=1)
            print("\nstats")
            print(stats.index)
            print(stats.columns)
            print(stats.dtypes)
            print(stats)
            
        except Exception as e:
            print(e)
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": out, "Stats": stats},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": out, "Stats": stats}
