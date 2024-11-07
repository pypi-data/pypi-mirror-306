import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.utilities import utilities


class Switch:
    def __init__(self):
        # self.functionApply = ["is null", "is not null", "in", "not in"]
        # self.noValueRequired = ["is empty", "is not empty"]
        self.noValueRequired = ["is null", "is not null", "is empty", "is not empty", "True", "False", "is_infinity", "is_not_infinity"]

    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# SWITCH")

        cases: list = settings["cases"] if "cases" in settings and settings["cases"] else []
        default_value: str | None = settings["default_value"] if "default_value" in settings else ""
        default_value_field: str | None = settings["default_value_field"] if "default_value_field" in settings and settings["default_value_field"] else None
        new_column: str = settings["new_column"] if "new_column" in settings and settings["new_column"] else "new_column"

        if default_value == None and default_value_field == None:
            msg = app_message.dataprep["nodes"]["switch"]["default_value"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg)

        try:
            conditions = []
            outputs = []
            script.append("conditions = []")
            script.append("outputs = []")
            for caseIdx, case in enumerate(cases):
                script.append(f"\n# Case {caseIdx + 1}")

                output: str | None = case["output"] if "output" in case else ""
                output_field: str | None = case["output_field"] if "output_field" in case and case["output_field"] else None

                if output == None and output_field == None:
                    msg = app_message.dataprep["nodes"]["switch"]["no_return_value"](node_key, caseIdx + 1)
                    return bug_handler.default_node_log(flow_id, node_key, msg)

                query = ""
                script.append(f'query{caseIdx + 1} = ""')
                case_conditions: list = case["conditions"] if "conditions" in case else []
                if not case_conditions:
                    msg = app_message.dataprep["nodes"]["switch"]["no_conditions"](node_key, caseIdx + 1)
                    return bug_handler.default_node_log(flow_id, node_key, msg)

                for condIdx, condition in enumerate(case_conditions):
                    script.append(f"# Condition {condIdx + 1}")
                    rule: str = f" {condition['rule']} " if "rule" in condition else ""
                    field: str = condition["field"] if "field" in condition and condition["field"] else None
                    operator: str = condition["operator"] if "operator" in condition and condition["operator"] else None

                    value: str | None = utilities.check_and_add_flow_vars(flow_id, condition["value"]) if "value" in condition else ""
                    value_field: str | None = condition["value_field"] if "value_field" in condition and condition["value_field"] else None

                    # Validar campos requeridos para la condicion
                    if condIdx > 0 and not rule:
                        msg = app_message.dataprep["nodes"]["switch"]["missing_condition_prop"](node_key, "Rule", caseIdx + 1, condIdx + 1)
                        return bug_handler.default_node_log(flow_id, node_key, msg)

                    if not field:
                        msg = app_message.dataprep["nodes"]["switch"]["missing_condition_prop"](node_key, "Column", caseIdx + 1, condIdx + 1)
                        return bug_handler.default_node_log(flow_id, node_key, msg)

                    if not operator:
                        msg = app_message.dataprep["nodes"]["switch"]["missing_condition_prop"](node_key, "Operator", caseIdx + 1, condIdx + 1)
                        return bug_handler.default_node_log(flow_id, node_key, msg)

                    # * Operaciones que no requieren value
                    if operator in self.noValueRequired:
                        if operator == "is null":
                            value = f"pd.isnull(df['{field}'])"

                        elif operator == "is not null":
                            value = f"pd.notnull(df['{field}'])"

                        elif "empty" in operator:
                            value = f'df["{field}"] == ""' if operator == "is empty" else f'df["{field}"] != ""'

                        elif operator == "is_infinity":
                            value = f"(df['{field}'] == np.inf) | (df['{field}'] == -np.inf)"

                        elif operator == "is_not_infinity":
                            value = f"(df['{field}'] != np.inf) & (df['{field}'] != -np.inf)"

                        # TODO: Revisar casos bools
                        elif operator == "True":
                            value = f"df['{field}'] == True"
                        elif operator == "False":
                            value = f"df['{field}'] == False"

                        query += f"{rule}({value})"

                    # * Operaciones que REQUIEREN value o value_field
                    else:
                        # * Validar value y value_field para los operadores que lo requieren
                        if value == None and value_field == None:
                            msg = app_message.dataprep["nodes"]["switch"]["missing_condition_prop"](node_key, "Value", caseIdx + 1, condIdx + 1)
                            return bug_handler.default_node_log(flow_id, node_key, msg)
                        
                        # * si existe value_field
                        if value_field:
                            if value_field not in df.columns:
                                msg = app_message.dataprep["nodes"]["switch"]["no_column_in_df"](node_key, value_field)
                                return bug_handler.default_node_log(flow_id, node_key, msg)

                            query += f"{rule}(df['{field}'] {operator} df['{value_field}'])"

                        # * si existe value
                        else:
                            if operator == "in":
                                # TODO: Hay que quitar los astype cuando se solucione el problema en el dtypes al pasar a string
                                df[field] = df[field].astype(str)
                                value = f"df['{field}'].str.contains('{value}')"
                                query += f"{rule}({value})"

                            elif operator == "not in":
                                # TODO: Hay que quitar los astype cuando se solucione el problema en el dtypes al pasar a string
                                df[field] = df[field].astype(str)
                                value = f"~df['{field}'].str.contains('{value}')"
                                query += f"{rule}({value})"

                            else:
                                # Parse numeric values
                                # try:
                                #     new_value = literal_eval(new_value)
                                # except Exception as e:
                                #     pass
                                # ? Agregar comillas si el tipo de la columna es string o datetime
                                value = "'{}'".format(value) if (pd.api.types.is_string_dtype(df[field].dtype) or pd.api.types.is_datetime64_any_dtype(df[field].dtype)) else value
                                query += f"{rule}(df['{field}'] {operator} {value})"

                        script.append(f'query{caseIdx + 1} = "{query}"')

                case_output = df[output_field] if output_field in df.columns else output

                # Si la salida es una columna del DF, tratar como string
                if isinstance(case_output, pd.Series):
                    case_output = case_output.astype(str)

                outputs.append(case_output)
                conditions.append(eval(query))

                output_str = "df['" + output_field + "']" if output_field else "'" + output + "'"
                script.append(f"outputs.append({output_str})")
                script.append(f"conditions.append(eval(query))")

            switch_default_value = df[default_value_field] if default_value_field in df.columns else default_value
            
            # Si el valor por defecto es una columna, tratar como string
            if isinstance(switch_default_value, pd.Series):
                switch_default_value = switch_default_value.astype(str)

            df[new_column] = np.select(conditions, outputs, default=switch_default_value)

            try:
                # Limpiar posibles valores nan devueltos como string
                df[new_column].replace(["nan", "NaN", "NAN", "nat", "NaT", "NAT"], "", inplace=True)
            except Exception as e:
                print(new_column, e)

            # try parse to datetime
            try:
                df[new_column] = pd.to_datetime(df[new_column], format="mixed")
            except Exception as e:
                # try parse to numeric
                try:
                    df[new_column] = pd.to_numeric(df[new_column])
                except Exception as e:
                    print(new_column, e)

            default_value_str = "df['" + default_value_field + "']" if default_value_field else "'" + default_value + "'"
            script.append("\n# Output")
            script.append(f'df["{new_column}"] = np.select(conditions, outputs, default={default_value_str})')

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
