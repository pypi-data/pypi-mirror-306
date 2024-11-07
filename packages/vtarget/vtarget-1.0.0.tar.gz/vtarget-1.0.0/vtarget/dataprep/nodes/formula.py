import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.utilities import utilities


class Formula:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# FORMULA")

        # Agrego los modulos y alias al entorno de variables globales
        imports_code: str = settings["imports"] if "imports" in settings and settings["imports"] else ""
        used_modules = utilities.find_imports(imports_code)
        globals().update(utilities.import_modules(used_modules))

        formulas: list = settings["items"] if "items" in settings else []

        for i, item in enumerate(formulas):
            col_name: str = ""
            if not item["field"]:  # crea una columna nueva
                col_name = item["new_column_name"] if "new_column_name" in item and item["new_column_name"] else f"x_{i}"
            else:  # actualiza la misma columna seleccionada
                col_name = item["field"]

            if "sentence" not in item:
                continue

            try:
                sentence = utilities.check_and_add_flow_vars(flow_id, item["sentence"], datetime_as_str=False)
                print(sentence)
                df[col_name] = eval(sentence)
                script.append("df.loc[:, '{}'] = {}".format(col_name, sentence))
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
