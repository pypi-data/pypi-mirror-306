import json
from contextlib import redirect_stdout
from io import StringIO

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.utilities import utilities
from vtarget.utils.dtype_optimizer import dtype_optimizer


class Code:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        code_snippet: str = utilities.check_and_add_flow_vars(flow_id, settings["code"], datetime_as_str=False) if "code" in settings else ""
        node_type: str = "CODE" if "code" in node_key.lower() else "SOURCE"
        script.append(f"\n# {node_type}")

        # Agrego los modulos y alias al entorno de variables globales
        used_modules = utilities.find_imports(code_snippet)
        globals().update(utilities.import_modules(used_modules))

        def vtg_codeout(x):
            global vtg_df, vtg_metacode
            vtg_df = x.copy()

        loc = {f"df_{k.lower()}": v.copy() for k, v in pin.items()}
        loc["vtg_codeout"] = vtg_codeout
        stdout = ""

        try:
            out = StringIO()
            with redirect_stdout(out):
                # NOTE: Antes estaba como exec(code_snippet, None, loc).
                # NOTE: Tener en cuenta en caso de que se encuentre algun fallo
                exec(code_snippet, loc)
            stdout = out.getvalue()

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            default = bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
            default["STDOUT"] = stdout
            default["STDOUT"] += str(e)
            return default
        else:
            script.append(code_snippet)
            df_out = globals()["vtg_df"] if "vtg_df" in globals() else []
            globals()["vtg_df"] = []
            if not isinstance(df_out, pd.DataFrame):
                msg = app_message.dataprep["nodes"]["code"]["no_vtg_codeout"](node_key)
                default = bug_handler.default_node_log(flow_id, node_key, msg, "", "error")
                default["STDOUT"] = stdout
                return default

        df_out.reset_index(inplace=True, drop=True)
        
        # Intenta optmizar los tipos de datos
        try:
            if node_type == "SOURCE":
                dtype_optimizer.optimize(df_out)
        except Exception as e:
            print("Error al intentar optimizar tipo de datos", str(e))
        
        cache_handler.update_node(
            flow_id,
            node_key,
            {"pout": {"Out": df_out}, "config": json.dumps(settings, sort_keys=True), "script": script},
        )

        script_handler.script += script
        return {"Out": df_out, "STDOUT": stdout}

    # def find_imports(self, code_snippet):
    #     # Busco los modulos que tienen la forma ['import * as *']
    #     matchs = re.findall("import (.*?) as (.*?)$", code_snippet, flags=re.MULTILINE)
    #     # print(matchs)
    #     out = [{"name": m[0].strip(), "alias": m[1].strip(), "objects": []} for m in matchs]
    #     # print(out)
    #     # Busco los ['from * import *', 'import *']
    #     # modules = []
    #     for node in ast.iter_child_nodes(ast.parse(code_snippet)):
    #         if isinstance(node, ast.ImportFrom):
    #             objects = [node.names[i].name for i in range(len(node.names))]
    #             if not node.names[0].asname:  # excluding the 'as' part of import
    #                 # modules.append(node.module)
    #                 out.append({"name": node.module, "alias": None, "objects": objects})
    #         elif isinstance(node, ast.Import):  # excluding the 'as' part of import
    #             if not node.names[0].asname:
    #                 out.append({"name": node.names[0].name, "alias": None, "objects": []})
    #                 # modules.append(node.names[0].name)
    #     return out
