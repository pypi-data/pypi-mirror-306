import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message

class Merge:
    def __init__(self):
        self.script = []

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        edf = pd.DataFrame()
        pout_struct = {"L": edf, "J": edf, "R": edf, "F": edf}

        if "iL" not in pin or "iR" not in pin:
            msg = app_message.dataprep["nodes"]["merge"]["input_port"](node_key)
            bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
            return pout_struct

        self.script.append("\n# MERGE")

        # * Dataframes de entrada
        df_iL: pd.DataFrame = pin["iL"].copy() if "iL" in pin else pd.DataFrame()
        df_iR: pd.DataFrame = pin["iR"].copy() if "iR" in pin else pd.DataFrame()
        
        # * Advertir si el dataframe está vacío
        if df_iL.empty:
            msg = app_message.dataprep["nodes"]["empty_df"](node_key, "iL")
            bug_handler.default_node_log(flow_id, node_key, msg, bug_level="warning", console_level="warn")

        # * Advertir si el dataframe está vacío
        if df_iR.empty:
            msg = app_message.dataprep["nodes"]["empty_df"](node_key, "iR")
            bug_handler.default_node_log(flow_id, node_key, msg, bug_level="warning", console_level="warn")
        
        # * Columnas de salida
        left_columns: list[str] = settings["left_columns"] if "left_columns" in settings else []
        right_columns: list[str] = settings["right_columns"] if "right_columns" in settings else []
        
        # * Limpiar columnas seleccionadas dejando solo las válidas
        valid_left_columns : list = [ x for x in left_columns if x in df_iL.columns ]
        valid_right_columns : list = [ x for x in right_columns if x in df_iR.columns ]
        
        # * Validar que exista columnas seleccionadas en la config de ambos Dataframes
        if not valid_left_columns:
            msg = app_message.dataprep["nodes"]["empty_entry_list"](node_key, "Left")
            bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
            return pout_struct
        
        if not valid_right_columns:
            msg = app_message.dataprep["nodes"]["empty_entry_list"](node_key, "Right")
            bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
            return pout_struct

        try:
            df_iL: pd.DataFrame = df_iL[valid_left_columns].copy()
            df_iR: pd.DataFrame = df_iR[valid_right_columns].copy()
            self.script.append("df_iL = df_iL[{}].copy()".format(valid_left_columns))
            self.script.append("df_iR = df_iR[{}].copy()".format(valid_right_columns))

            left_on: list[str] = [x["left"] for x in settings["items"] if "left" in x and x["left"]]
            right_on: list[str] = [x["right"] for x in settings["items"] if "right" in x and x["right"]]
            
            # * Limpiar columnas del merge dejando solo las válidas
            valid_left_on : list[str] = [ x for x in left_on if x in df_iL.columns ]
            valid_right_on : list[str] = [ x for x in right_on if x in df_iR.columns ]
            
            # * Validar que ambos array sean del mismo largo
            if len(left_on) != len(right_on):
                msg = app_message.dataprep["nodes"]["merge"]["not_equal_len"](node_key)
                bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
                return pout_struct

            # * Validar que las columnas del merge sean del mismo tipo
            for idx, l_col in enumerate(valid_left_on):
                r_col = valid_right_on[idx]
                if df_iL[l_col].dtype != df_iR[r_col].dtype:
                    # msg = app_message.dataprep["nodes"]["merge"]["not_equal_len"](node_key)
                    msg = f"You are trying to merge on {df_iL[l_col].dtype} and {df_iR[r_col].dtype} columns"
                    bug_handler.default_node_log(flow_id, node_key, msg, console_level="warn", bug_level="warning")
            
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
            return pout_struct

        if "L" in settings["outputs"]:
            pout_struct["L"] = self.apply_join(flow_id, node_key, "left", df_iL, df_iR, valid_left_on, valid_right_on)
        if "J" in settings["outputs"]:
            pout_struct["J"] = self.apply_join(flow_id, node_key, "inner", df_iL, df_iR, valid_left_on, valid_right_on)
        if "R" in settings["outputs"]:
            pout_struct["R"] = self.apply_join(flow_id, node_key, "right", df_iL, df_iR, valid_left_on, valid_right_on)
        if "F" in settings["outputs"]:
            pout_struct["F"] = self.apply_join(flow_id, node_key, "outer", df_iL, df_iR, valid_left_on, valid_right_on)

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": pout_struct,
                "config": json.dumps(settings, sort_keys=True),
                "script": self.script,
            },
        )

        script_handler.script += self.script
        self.script = []
        return pout_struct

    def apply_join(self, flow_id, node_key, how, df_iL, df_iR, left_on, right_on):
        try:
            self.script.append(f"# {how}")
            if how == "outer":
                df_out = pd.merge(
                    df_iL,
                    df_iR,
                    left_on=left_on,
                    right_on=right_on,
                    how="outer",
                    indicator=True,
                )
                # Campo _merge viene como category, lo cambio a object (str)
                df_out["merge_type"] = df_out["_merge"].astype(str)
                del df_out["_merge"]
                self.script.append("df_{} = pd.merge(df_iL, df_iR, left_on={}, right_on={}, how='outer', indicator=True)".format(how, left_on, right_on))
            else:
                df_out = pd.merge(df_iL, df_iR, left_on=left_on, right_on=right_on, how=how, indicator=False)
                self.script.append("df_{} = pd.merge(df_iL, df_iR, left_on={}, right_on={}, how='{}',indicator=False)".format(how, left_on, right_on, how))
        except Exception as e:
            print(e)
            print(e.__class__.__name__)
            print(', '.join(e.args))
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
            return pd.DataFrame()
        return df_out
