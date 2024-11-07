import copy
import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.utilities import utilities


class Dtype:
    def __init__(self):
        self.script = []

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        df: pd.DataFrame = pin["In"].copy()
        self.script.append("\n# DTYPE")

        if "items" not in settings or not settings["items"]:
            msg = app_message.dataprep["nodes"]["dtype"]["no_columns_selected"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        df, _, rename_cols = self.select_types_and_fields(flow_id, node_key, df, settings["items"])

        # Si hay alguna columna para renombrar en las seleccionadas
        if rename_cols:
            try:
                df = df.rename(columns=rename_cols)
            except Exception as e:
                msg = app_message.dataprep["nodes"]["dtype"]["rename_columns"](node_key)
                return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")

            self.script.append("\n# Rename columns")
            self.script.append("df = df.rename(columns={})".format(rename_cols))

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": self.script.copy(),
            },
        )

        script_handler.script += self.script.copy()
        self.script = []
        return {"Out": df}

    # Retorna el df con las columnas seleccionadas y el tipo de dato
    def select_types_and_fields(self, flow_id: str, node_key: str, df: pd.DataFrame, new_dtypes: dict):
        # https://pbpython.com/pandas_dtypes.html
        selected_dtypes = copy.deepcopy(new_dtypes)
        # ? Para nodos de tipo DTYPE usar todos los campos, sin importar si estan o no en la config
        if "dtype" in node_key.lower():  # aas
            all_dtypes = utilities.get_dtypes_of_df(df)  # ? Todos los dtypes del Dataframe
            selected_dtypes = copy.deepcopy(all_dtypes)
        # ? Para nodos de tipo SELECTE obtener solo los campos seleccionados de la lista total de campos (selected==True)
        elif "select" in node_key.lower():
            selected_dtypes = dict(filter(lambda x: True if "selected" in x[1] and x[1]["selected"] else False, new_dtypes.items()))

        # Existe la posibilidad de que ya no existan columnas que previamente fueron creadas
        available_cols = []  # para nodo de tipo select
        removed_cols = []  # para nodo de tipo select

        for field, x in selected_dtypes.items():
            if field in df.columns:
                available_cols.append(field)
            else:
                removed_cols.append(field)
                msg = app_message.dataprep["nodes"]["dtype"]["column_not_in_df"](node_key, field)
                bug_handler.default_node_log(flow_id, node_key, msg, console_level="warn", bug_level="warning", success=True)

        # Remover las columnas que ya no existen
        for del_key in removed_cols:
            del selected_dtypes[del_key]

        # Mantener solamente columnas existentes y seleccionadas
        df: pd.DataFrame = df[available_cols]
        self.script.append("df = df[{}]".format(available_cols))
        self.script.append("\n# DATA TYPES")

        # Diccionario para el renombrado de variables
        rename_cols = {}
        standard_dtypes = ["str", "object", "bool", "category", "int8", "int16", "int32", "int64", "float16", "float32", "float64"]

        for field, x in selected_dtypes.items():
            # renombrar columnas
            if field in new_dtypes and "rename" in new_dtypes[field] and new_dtypes[field]["rename"]:
                rename_cols[field] = new_dtypes[field]["rename"]

            # orden de las columnas
            if field in new_dtypes and "order" in new_dtypes[field]:
                selected_dtypes[field]["order"] = new_dtypes[field]["order"]

            # nuevo tipo de dato desde la config (new_dtypes)
            newtype = new_dtypes[field]["dtype"] if field in new_dtypes and "dtype" in new_dtypes[field] and new_dtypes[field]["dtype"] else x["dtype"]

            # saltar cambio si el tipo sigue siendo el mismo
            if df[field].dtype == newtype:
                continue

            if newtype in standard_dtypes:
                df, status = self.select_change_col_dtype(flow_id, node_key, df.copy(), field, newtype)
                if not status:  # Si hubo un error se mantiene como texto (object)
                    new_dtypes[field]["dtype"] = "object"

            elif newtype in ["datetime64[ns]"]:
                try:
                    df = df.copy()
                    df[field] = pd.to_datetime(df[field], format="mixed")
                    self.script.append(f"df['{field}'] = pd.to_datetime(df['{field}'], format='mixed')")

                except Exception as e:
                    msg = app_message.dataprep["nodes"]["dtype"]["change_dtype"](node_key, field, newtype)
                    bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
                    # Si hubo un error se mantiene como texto (object)
                    new_dtypes[field]["dtype"] = "object"

            elif newtype in ["timedelta64[ns]"]:
                try:
                    df = df.copy()
                    df[field] = pd.to_timedelta(df[field])
                    self.script.append(f"df['{field}'] = pd.to_timedelta(df['{field}'])")
                except Exception as e:
                    msg = app_message.dataprep["nodes"]["dtype"]["change_dtype"](node_key, field, newtype)
                    bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
                    # Si hubo un error se mantiene como texto (object)
                    new_dtypes[field]["dtype"] = "object"

            else:
                msg = app_message.dataprep["nodes"]["dtype"]["unknow_dtype"](node_key, field, newtype)
                bug_handler.default_node_log(flow_id, node_key, msg, console_level="warn", bug_level="warning")
                new_dtypes[field]["dtype"] = "object"

        # Ordena las columnas segun el orden dado en la configuracion del nodo
        order_cols = list(dict(sorted(selected_dtypes.items(), key=lambda item: item[1]["order"])).keys())
        return df[order_cols], new_dtypes, rename_cols

    # Cambia el tipo de dato y maneja los errores que podrían salir en el intento
    def select_change_col_dtype(self, flow_id: str, node_key: str, df: pd.DataFrame, field: str, dtype: str):
        try:
            if dtype == 'bool' and df[field].dtype == 'object':
                df[field] = df[field].astype(str).str.lower()
                df_T = df[(df[field].str.lower() == 'true'.lower()) | (df[field].str.lower() == 'false'.lower())].copy()
                if not df_T.empty:
                    d = { 'true': 1, 'false': 0, '1': 1, '0': 0, '': 0 }
                    df[field] = df[field].map(d)
                    
            df[field] = df[field].astype(dtype)
        except Exception as e:
            msg = app_message.dataprep["nodes"]["dtype"]["change_dtype"](node_key, field, dtype)
            bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
            return df, False
        else:
            dtype_ = dtype if isinstance(dtype, str) else dtype.__name__
            self.script.append("df['{0}'] = df['{0}'].astype('{1}')".format(field, dtype_))
            return df, True
