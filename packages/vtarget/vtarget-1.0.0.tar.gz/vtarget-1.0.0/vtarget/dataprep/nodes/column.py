import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Column:
    def __init__(self):
        self.script = []

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        df = pin["In"].copy()

        self.script.append("\n# COLUMN")
        if "items" not in settings or not settings["items"]:
            msg = app_message.dataprep["nodes"]["column"]["no_columns_selected"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        
        # Obtener df con las columnas seleccionadas y su orden, dtypes actualizados, lista con los nuevos nombres de las columnas
        df, _, rename_cols = self.select_types_and_fields(flow_id, node_key, df, settings["items"])

        # Si hay alguna columna para renombrar en las seleccionadas
        if rename_cols:
            try:
                df = df.rename(columns=rename_cols)
            except Exception as e:
                msg = app_message.dataprep["nodes"]["column"]["rename_columns"](node_key)
                return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
            
            self.script.append("\n# Rename columns")
            self.script.append("df = df.rename(columns={})".format(rename_cols))

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": self.script,
            },
        )

        script_handler.script += self.script.copy()
        self.script = []

        return {"Out": df}

    def select_types_and_fields(self, flow_id: str, node_key: str, df: pd.DataFrame, dtypes: dict):
        """Retorna el df con las columnas seleccionadas y el orden dado

        Args:
            flow_id (str): id del flujo
            node_key (str): id del nodo
            df (pd.DataFrame): dataframe de entrada
            dtypes (dict): configuracion de las columnas (selected, order)

        Returns:
            tuple: df, dtypes, rename_cols
        """
        
        # https://pbpython.com/pandas_dtypes.html
        # Obtener solo las columnas seleccionadas de la lista inicial (selected==True)
        selected = dict(
            filter(
                lambda x: True if "selected" in x[1] and x[1]["selected"] else False,
                dtypes.items(),
            )
        )

        # Existe la posibilidad de que ya no existan columnas que previamente fueron creadas
        available_cols = []
        removed_cols = []
        for field, _ in selected.items():
            if field in df.columns:
                available_cols.append(field)
            else:
                removed_cols.append(field)
                del dtypes[field]  # dado que no existe la eliminamos de dtypes
                msg = app_message.dataprep["nodes"]["column"]["column_not_in_df"](node_key, field)
                bug_handler.default_node_log(flow_id, node_key, msg, console_level="warn", bug_level="warning", success=True)

        # Remover las columnas que ya no existen
        for del_key in removed_cols:
            del selected[del_key]

        # Mantener solamente columnas existentes y seleccionadas
        df = df[available_cols]
        
        self.script.append("df = df[{}]".format(available_cols))

        # Diccionario para el renombrado de columnas
        rename_cols = {}
        for field, _ in selected.items():
            if "rename" in dtypes[field] and dtypes[field]["rename"]:
                rename_cols[field] = dtypes[field]["rename"]

        # Ordena las columnas segun el orden dado en la configuracion del nodo
        order_cols = list(dict(sorted(selected.items(), key=lambda item: item[1]["order"])).keys())

        return df[order_cols], dtypes, rename_cols
