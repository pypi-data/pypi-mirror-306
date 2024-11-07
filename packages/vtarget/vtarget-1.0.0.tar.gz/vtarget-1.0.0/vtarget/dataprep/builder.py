from vtarget.language.app_message import app_message


class Builder:
    import pandas as pd

    def __init__(self):
        # self.compute_node_counter = 0
        self.nodes: dict = {}
        self.script: str = ""
        self.init_script()  # resetea el script
        self.cur_node_key: str = None
        self.dumpings = 0
        self.execution = 0
        self.runnable = False
        # self.ultra = None

    def init_pipeline(self):
        from vtarget.dataprep.pipeline import Pipeline

        self.pipeline = Pipeline()

    def init_script(self):
        from vtarget.handlers.script_handler import script_handler

        # Headers del script
        script_handler.script.append("#!/usr/bin/env python")
        script_handler.script.append("# coding: utf-8\n")
        script_handler.script.append("import pandas as pd")
        script_handler.script.append("import numpy as np")

    def set_nodes(self, flow_id: str, data: dict):
        from vtarget.handlers.bug_handler import bug_handler

        self.nodes = {}  # Diccionario con los nodos del flujo cuya clave es el atributo "key" del nodo
        for idx, nd in enumerate(data["nodeDataArray"]):
            if not ("isGroup" in nd and nd["isGroup"]) and (
                nd["type"] not in ["Comment"]
            ):  # and (nd["categoryId"] not in ["chart"]):  # no es grupo  # no es comment  # no es chart
                self.nodes[nd["key"]] = {
                    "idx": idx,
                    "key": nd["key"],
                    "skip": False,
                    "name": nd["name"],
                    "type": nd["type"],
                    "output": None,
                    "loaded": False,
                    "childs": [],
                    "parents": [],
                    "disabled": True if "meta" in nd and "disabled" in nd["meta"] and nd["meta"]["disabled"] else False,
                }

        # * Recorre los links para obtener los padres e hijos por nodo
        for ld in data["linkDataArray"]:
            # if "_chart" in ld["to"]:
            #     continue

            # ! Valida que el nodo existe
            if ld["to"] not in self.nodes:
                # TODO: Agregar al diccionario
                msg = f'link {ld["key"]} to {ld["to"]}: hace referencia a nodo inexistente ({ld["to"]})'
                bug_handler.default_node_log(flow_id, None, msg, console_level="trace", bug_level="warning", success=True)
                continue

            # ! Valida que el nodo existe
            if ld["from"] not in self.nodes:
                # TODO: Agregar al diccionario
                msg = f'link {ld["key"]} from {ld["from"]}: hace referencia a nodo inexistente ({ld["from"]})'
                bug_handler.default_node_log(flow_id, None, msg, console_level="trace", bug_level="warning", success=True)
                continue

            # * Agrega los padres
            parent = {"from": ld["from"], "frompid": ld["frompid"], "topid": ld["topid"]}
            if not self.nodes[ld["to"]]["parents"]:
                self.nodes[ld["to"]]["parents"] = [parent]
            else:
                self.nodes[ld["to"]]["parents"].append(parent)

            # * Agrega los hijos
            child = {"to": ld["to"], "topid": ld["topid"], "frompid": ld["frompid"], "to_idx": self.nodes[ld["to"]]["idx"]}
            if not self.nodes[ld["from"]]["childs"]:
                self.nodes[ld["from"]]["childs"] = [child]
            else:
                self.nodes[ld["from"]]["childs"].append(child)

    def reset_childs_recursive(self, flow_id: str, node_key: str, reseted_nodes: list):
        """Resetea todos los nodos hijos cuando cambia la configuración de un padre"""

        import gc

        from vtarget.handlers.cache_handler import cache_handler

        for child in self.nodes[node_key]["childs"]:
            if child["to"] in cache_handler.settings[flow_id]:
                print(node_key, "reset_childs_recursive")
                del cache_handler.settings[flow_id][child["to"]]
                reseted_nodes.append(child["to"])
            self.reset_childs_recursive(flow_id, child["to"], reseted_nodes)
        gc.collect()
        return reseted_nodes

    def set_skip_childs_recursive(self, flow_id: str, node_key: str, data: dict):
        """Setea a True el parámetro para saltar (no-procesar) los nodos hijos cuando existe un error"""

        for child in self.nodes[node_key]["childs"]:
            child_idx = child["to_idx"]
            child_key = child["to"]
            # Habilita flag para saltarse el nodo
            self.nodes[child_key]["skip"] = True
            # Resetea el df completo almacenado en RAM
            self.nodes[child_key]["output"] = None
            # Resetea el nodo de gojs
            for port_name in data["nodeDataArray"][child_idx]["meta"]["ports_map"]["pout"]:
                data["nodeDataArray"][child_idx]["meta"]["ports_map"]["pout"][port_name]["head"] = []
                data["nodeDataArray"][child_idx]["meta"]["ports_map"]["pout"][port_name]["rows"] = 0
                data["nodeDataArray"][child_idx]["meta"]["ports_map"]["pout"][port_name]["cols"] = 0

            data["nodeDataArray"][child_idx]["meta"]["has_error"] = False  # Limpia flag de error
            data["nodeDataArray"][child_idx]["meta"]["skipped"] = True  # Marcar como saltado
            print("=================> se saltará el nodo", child_key)
            self.set_skip_childs_recursive(flow_id, child_key, data)
        return True

    def check_childs_loaded(self, node_key: str):
        """Checkea si todos los hijos están listos"""

        loaded = True
        for child in self.nodes[node_key]["childs"]:
            if not self.nodes[child["to"]]["loaded"]:
                loaded = False
                break
        return loaded

    def dump_parents(self, flow_id, node_key):
        """Manda a almacenar y liberar los padres que ya están listos"""

        import time

        from vtarget.handlers.cache_handler import cache_handler

        if not cache_handler.dump_enabled:
            return

        t = time.time()
        if not self.nodes[node_key]["loaded"]:
            return
        for parent in self.nodes[node_key]["parents"]:
            if self.check_childs_loaded(parent["from"]):
                cache_handler.dump(flow_id, parent["from"])
        if len(self.nodes[node_key]["childs"]) == 0:
            cache_handler.dump(flow_id, node_key)
        self.dumpings += time.time() - t

    def stop_model(self):
        self.runnable = False

    def analyzer(
        self,
        data: dict,
        reset_cache: bool,
        flow_id: str,
        flow_name: str,
        disable_all_write_nodes: bool,
        disable_all_email_nodes: bool,
        deploy_enabled: bool = False,
    ):
        import gc
        import json
        import time
        from typing import Any, Dict

        import pandas as pd

        from vtarget.dataprep.types import NodeType
        from vtarget.handlers.bug_handler import bug_handler
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.handlers.event_handler import event_handler
        from vtarget.handlers.log_handler import log_handler
        from vtarget.handlers.script_handler import script_handler
        import math

        print("deploy_enabled", deploy_enabled)

        self.runnable = True
        self.dumpings = 0
        self.execution = 0

        # * Reseteo de variables singleton para cada ejecución
        log_handler.log = []
        bug_handler.bug = []
        script_handler.script = []

        # * Si se corre el flujo reseteando la cache
        if reset_cache:
            msg = app_message.dataprep["builder"]["reset_cache"](flow_name)
            bug_handler.default_node_log(flow_id, None, msg, console_level="trace", bug_level="info", success=True)
            cache_handler.reset(flow_id)

        # * Inicializa la caché para el flujo si es que aún no existe
        cache_handler.load_settings(flow_id)
        if flow_id not in cache_handler.cache:
            cache_handler.cache[flow_id] = dict()

        cache_nodes_keys = list(cache_handler.cache[flow_id].keys())
        msg = app_message.dataprep["builder"]["nodes_in_cache"](str(len(cache_nodes_keys)))
        bug_handler.default_node_log(flow_id, None, msg, console_level="trace", bug_level="info", success=True)

        # * Hace una copia local de los nodos y su metadata
        self.set_nodes(flow_id, data)

        completed_nodes: list = []
        num_nodes_ok: int = 0  # conteo del número de nodos procesados
        attemps: int = 0  # contador de intentos del while para procesar el flujo completo
        t1 = time.time()  # inicializa el tiempo total de procesamiento de los nodos

        # * Itera mientras no estén todos los nodos procesados (prop loaded == True)
        while self.runnable and num_nodes_ok < len(self.nodes):
            # print(num_nodes_ok, "<", len(self.nodes))
            attemps += 1
            for node_key, node_data in self.nodes.items():
                node_idx: int = self.nodes[node_key]["idx"]

                if not self.runnable:
                    msg = app_message.dataprep["builder"]["stopped_flow"]
                    bug_handler.default_node_log(flow_id, None, msg, console_level="error", bug_level="warning", success=True)
                    break

                # * Salta los nodos que ya han sido procesados
                if self.nodes[node_key]["loaded"]:
                    continue

                # * Salta los nodos output y email cuando el check de deshabilitar está activado
                if (disable_all_write_nodes and (node_data["type"] in [NodeType.OUTPUTDATA.value, NodeType.EXCEL.value, NodeType.DATABASEWRITE.value])) or (
                    disable_all_email_nodes and (node_data["type"] in [NodeType.EMAIL.value])
                ):

                    if node_data["type"] in [NodeType.EMAIL.value]:
                        msg = app_message.dataprep["builder"]["not_send"](node_key)
                    else:
                        msg = app_message.dataprep["builder"]["skip_writing"](node_key)
                    bug_handler.default_node_log(flow_id, None, msg, console_level="trace", bug_level="info", success=True)

                    # * Se establece como loaded = True para que no entre nuevamente en caso que el while haga mas de un intento
                    self.nodes[node_key]["loaded"] = True
                    data["nodeDataArray"][node_idx]["meta"]["skipped"] = False
                    self.dump_parents(flow_id, node_key)
                    # * Agrega nodo a lista de completados
                    if node_key not in completed_nodes:
                        num_nodes_ok += 1
                        completed_nodes.append(node_key)
                    continue

                # * Omitir el procesamiento de nodos saltados por un error en el nodo padre
                if self.nodes[node_key]["skip"]:
                    # TODO: Pancho aquí te falto traducción
                    # * Se establece como loaded = True para que no entre nuevamente en caso que el while haga mas de un intento
                    self.nodes[node_key]["loaded"] = True
                    bug_handler.console("Nodo {} saltado".format(node_key), "trace", flow_id)
                    # * Agrega nodo a lista de completados
                    if node_key not in completed_nodes:
                        num_nodes_ok += 1
                        completed_nodes.append(node_key)
                    continue

                # * Omitir el procesamiento de nodos deshabilitados desde la vista
                if self.nodes[node_key]["disabled"]:
                    # TODO: Pancho aquí te falto traducción
                    # * Se establece como loaded = True para que no entre nuevamente en caso que el while haga mas de un intento
                    self.nodes[node_key]["loaded"] = True
                    self.nodes[node_key]["output"] = True  # Marcar con salida para forzar el error en el/los nodos hijos que no estén deshabilitados
                    bug_handler.console("Nodo {} dehabilitado".format(node_key), "trace", flow_id)
                    # * Agrega nodo a lista de completados
                    if node_key not in completed_nodes:
                        num_nodes_ok += 1
                        completed_nodes.append(node_key)
                    continue

                # * --------------------------------------------------
                # * Determina si el nodo puede ser procesado
                # * --------------------------------------------------
                ready_to_exec = False  # * Solo es verdadero cuando todos los nodos padres han sido procesados
                has_any_disabled_parent = False  # * Verdadero si algun nodo padre está deshabilitado
                to_load_input_port: Dict[str, Dict[str, Any]] = {}
                # * Almacena los df del mapeo de los puertos de entrada
                input_port: Dict[str, pd.DataFrame] = {}

                # * Si el nodo no posee padres, se puede procesar
                if not node_data["parents"]:
                    # * Nodos de entrada pueden procesarse inmediatamente ya que no tienen registro de nodos padres
                    if node_data["type"] in [
                        NodeType.INPUTDATA.value,
                        NodeType.DFMAKER.value,
                        NodeType.DATABASE.value,
                        NodeType.SOURCE.value,
                        NodeType.DATETIMERANGE.value,
                        NodeType.APIREST.value,
                    ]:
                        ready_to_exec = True
                    else:
                        # * Error si el nodo no tiene registro de padres, pero debería tenerlos
                        msg = app_message.dataprep["builder"]["parent_without_entry"](node_key)
                        bug_handler.default_node_log(flow_id, None, msg, console_level="trace", bug_level="info", success=True)

                        # * Se establece como loaded = True para que no entre nuevamente en caso que el while haga mas de un intento
                        self.nodes[node_key]["loaded"] = True
                        self.dump_parents(flow_id, node_key)
                        # * Agrega nodo a lista de completados
                        if node_key not in completed_nodes:
                            num_nodes_ok += 1
                            completed_nodes.append(node_key)

                        # * Saltar rama del nodo
                        self.set_skip_childs_recursive(flow_id, node_key, data)
                        continue

                else:  # * Si el nodo tiene padres
                    # * Verificar que todos los padres tienen sus salidas cargadas (que han sido procesados)
                    ready_to_exec = True  # inicializo la carga en verdadero
                    for parent in node_data["parents"]:
                        # * Si el nodo padre posee salida
                        if self.nodes[parent["from"]]["output"] != None:
                            # Almacena temporalmente la salida del padre para cargarla posteriomente como entrada del nodo hijo
                            to_load_input_port[parent["topid"]] = {"node_key": parent["from"], "port_name": parent["frompid"]}
                            # * Revisar si el padre ha sido desabilitado
                            if self.nodes[parent["from"]]["disabled"]:
                                bug_handler.console(f"NODO {node_key} tiene nodo padre deshabilitado {parent['from']}", "-", flow_id)
                                has_any_disabled_parent = True
                        else:
                            # *Si al menos un padre no está procesado, entonces termina la iteración
                            ready_to_exec = False
                            break

                # * --------------------------------------------------
                # * Si el nodo se puede procesar, inicia el procesamiento
                # * --------------------------------------------------
                if ready_to_exec:
                    # * Si se puede procesar, pero uno de sus padres está deshabilitado
                    if has_any_disabled_parent:
                        # * Se establece como loaded = True para que no entre nuevamente en caso que el while haga mas de un intento
                        self.nodes[node_key]["loaded"] = True
                        msg = app_message.dataprep["builder"]["parent_disabled"](node_key)
                        bug_handler.default_node_log(flow_id, node_key, msg, console_level="error", bug_level="error", success=True)

                        # * Marcar nodo con error
                        data["nodeDataArray"][node_idx]["meta"]["has_error"] = True  # * Marca nodo como error
                        self.set_skip_childs_recursive(flow_id, node_key, data)  # * Saltar rama del nodo
                        # * Agrega nodo a lista de completados
                        if node_key not in completed_nodes:
                            num_nodes_ok += 1
                            completed_nodes.append(node_key)
                        continue
                    
                    node_name: str = node_data["name"]
                    has_error: bool = False
                    self.cur_node_key = node_key

                    node_settings = cache_handler.settings[flow_id][node_key] if node_key in cache_handler.settings[flow_id] else dict()
                    node_in_cache = len(node_settings) > 0 and node_key in cache_handler.cache[flow_id]

                    # * --------------------------------------------------
                    # * Si el nodo actual está en caché y su config no ha cambiado, entonces no lo procesa
                    # * --------------------------------------------------
                    if (
                        node_in_cache
                        and "config" in node_settings
                        and node_settings["config"] == json.dumps(data["nodeDataArray"][node_idx]["meta"]["config"], sort_keys=True)
                        and (
                            "ports_config" not in node_settings  # no existe ports_config en cache
                            or (
                                "ports_config" in node_settings  # existe ports_config en cache
                                and node_settings["ports_config"]
                                == json.dumps(
                                    data["nodeDataArray"][node_idx]["meta"]["ports_config"],
                                    sort_keys=True,
                                )  # y ports_config no ha cambiado
                            )
                        )
                    ):
                        data["nodeDataArray"][node_idx]["meta"]["readed_from_cache"] = True
                        data["nodeDataArray"][node_idx]["meta"]["processed"] = True
                        script_handler.script += node_settings["script"]
                    # * --------------------------------------------------
                    # * De lo contrario, procesa y actualiza los valores de los df de salida
                    # * --------------------------------------------------
                    else:
                        if node_data["type"] not in [
                            NodeType.INPUTDATA.value,
                            NodeType.DFMAKER.value,
                            NodeType.DATABASE.value,
                            NodeType.SOURCE.value,
                            NodeType.DATETIMERANGE.value,
                            NodeType.APIREST.value,
                        ]:
                            # * Recorre los puertos del entrada del nodo
                            for _, pin_name in enumerate(data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"]):
                                if "dtypes" in data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"][pin_name] and pin_name in to_load_input_port:
                                    # * Carga salida del padre desde caché
                                    to_load = to_load_input_port[pin_name]
                                    cache_handler.load(flow_id, to_load["node_key"], to_load["port_name"])
                                    parent_key = to_load["node_key"]
                                    parent_port = to_load["port_name"]
                                    parent_cache = (
                                        cache_handler.cache[flow_id][parent_key] if flow_id in cache_handler.cache and parent_key in cache_handler.cache[flow_id] else dict()
                                    )

                                    # * Actualiza los dtypes de la entrada del nodo con el dataframe de la salida del nodo anterior
                                    if parent_cache and "pout" in parent_cache and parent_port in parent_cache["pout"]:
                                        input_port[pin_name] = parent_cache["pout"][parent_port]
                                        dtypes_list = data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"][pin_name]["dtypes"]

                                        # * nuevo dtypes de entrada
                                        u_dtypes = self.update_inputs_dtypes(node_name, node_key, dtypes_list, input_port[pin_name])
                                        data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"][pin_name]["dtypes"] = u_dtypes

                        # * --------------------------------------------------
                        # * Verifica si el nodo existe en caché, pero su config se modificó
                        # * --------------------------------------------------
                        bug_handler.console(f"PROCESANDO NODO {node_key}", "-", flow_id)
                        if node_settings and (
                            (
                                "config" in node_settings and node_settings["config"] != json.dumps(data["nodeDataArray"][node_idx]["meta"]["config"], sort_keys=True)
                            )  # node config ha cambiado
                            or (
                                "ports_config" in node_settings  # existe ports_config en cache
                                # and "ports_config" in data["nodeDataArray"][node_idx]["meta"]
                                and node_settings["ports_config"] != json.dumps(data["nodeDataArray"][node_idx]["meta"]["ports_config"], sort_keys=True)
                            )  # node ports_config ha cambiado
                        ):
                            # * Resetea la rama completa del nodo y envia lista de nodos a la vista
                            reseted_nodes = self.reset_childs_recursive(flow_id, node_key, [node_key])
                            event_handler.emit_queue.put(
                                {
                                    "name": "dataprep.reseted_nodes",
                                    "data": {
                                        "flow_id": flow_id,
                                        "reseted_nodes": reseted_nodes,
                                    },
                                }
                            )

                        t = time.time()

                        # ! Agrega parametro de despliegue a la config de cada nodo
                        if "meta" in data["nodeDataArray"][node_idx] and "config" in data["nodeDataArray"][node_idx]["meta"]:
                            data["nodeDataArray"][node_idx]["meta"]["config"]["deploy_enabled"] = deploy_enabled

                        # * Procesa todos los nodos excepto los de tipo chart
                        if "categoryId" in data["nodeDataArray"][node_idx] and data["nodeDataArray"][node_idx]["categoryId"] != "chart":
                            # ! resetea paginacion a 1
                            if "ports_config" in data["nodeDataArray"][node_idx]["meta"] and data["nodeDataArray"][node_idx]["meta"]["ports_config"] is not None:
                                for port in data["nodeDataArray"][node_idx]["meta"]["ports_config"]:
                                    data["nodeDataArray"][node_idx]["meta"]["ports_config"][port]["page"] = 1

                            # * Ejecucion individual de cada nodo
                            data["nodeDataArray"][node_idx] = self.pipeline.exec(flow_id, data["nodeDataArray"][node_idx], input_port)
                        else:
                            print(f'{data["nodeDataArray"][node_idx]["type"]} no se procesa')

                        self.execution += time.time() - t
                        # print(self.execution)

                        has_error = (
                            next(
                                (x for x in bug_handler.bug if x["node_key"] == node_key and x["level"] == "error"),
                                None,
                            )
                            != None
                        )

                        data["nodeDataArray"][node_idx]["meta"]["processed"] = True
                        data["nodeDataArray"][node_idx]["meta"]["has_error"] = has_error

                        # * Envía nodos procesado a la vista
                        event_handler.emit_queue.put(
                            {
                                "name": "dataprep.node_processed",
                                "data": {
                                    "flow_id": flow_id,
                                    "key": node_key,
                                    "node": json.dumps(data["nodeDataArray"][node_idx], default=str),
                                    "progress": math.floor(((num_nodes_ok + 1) / len(self.nodes)) * 100) if len(self.nodes) > 0 else 0,
                                    # 'log': log_handler.log, # TODO: Hacer el log del nodo correspondiente
                                },
                            }
                        )

                    # * Establece que el nodo se ha procesado y se ha generado una salida
                    self.nodes[node_key]["output"] = True
                    # * Se establece como loaded = True para que no entre nuevamente en caso que el while haga mas de un intento
                    self.nodes[node_key]["loaded"] = True
                    self.dump_parents(flow_id, node_key)
                    # * Agrega nodo a lista de completados
                    if node_key not in completed_nodes:
                        num_nodes_ok += 1
                        completed_nodes.append(node_key)

                    # * Verifica si el nodo fue procesado con error
                    data["nodeDataArray"][node_idx]["meta"]["skipped"] = False
                    if has_error:
                        print("\n\n\n----------- has_error", has_error)
                        cache_handler.delete_node(flow_id, node_key)
                        data["nodeDataArray"][node_idx]["meta"]["has_error"] = True  # * Marca nodo como error
                        self.set_skip_childs_recursive(flow_id, node_key, data)  # * Saltar rama del nodo

        # * --------------------------------------------------
        # * Fin del while y for principal
        # * --------------------------------------------------

        cache_nodes_keys = list(cache_handler.settings[flow_id].keys())
        msg = app_message.dataprep["builder"]["save_cache"](len(cache_nodes_keys))
        bug_handler.default_node_log(flow_id, None, msg, console_level="debug", bug_level="info", success=True)

        msg = app_message.dataprep["builder"]["processed_flow"](str(round(time.time() - t1, 3)))
        bug_handler.default_node_log(flow_id, None, msg, console_level="debug", bug_level="info", success=True)

        print(self.dumpings, "dumpings")
        print(self.execution, "execution")

        # Una vez que acaba la ejecución del flujo se conforma el script
        self.script = "\n".join(script_handler.script)
        cache_handler.dump_settings(flow_id)
        del self.nodes
        gc.collect()

        return data

    # ---------------------------------------------------------------------------------------
    # Actualiza los dtypes utilizando el df que se está recibiendo de entrada
    # y compara con lo que se tenía en la configuración, manejando tanto la
    # creación de campos que antes no existían, como la eliminación de campos que fueron eliminados

    def update_inputs_dtypes(self, node_name, node_key, current_dtypes, input_df: pd.DataFrame):
        res = input_df.dtypes.to_frame("dtypes")
        res = res["dtypes"].astype(str).reset_index()
        updated_dtypes = {}
        for i, x in res.iterrows():
            updated_dtypes[x["index"]] = {
                "dtype": x["dtypes"],
                "selected": True,
                "order": i,
            }

        return updated_dtypes
        """
        if not len(current_dtypes):
            return current_dtypes

        # Si hay que crear campos nuevos se agregarán al final
        try:
            max_order =  max(list(map(lambda x: x['order'], current_dtypes.values())))
        except Exception as e:
            print('Error (builder): ', e)
            bug_handler.append({'flow_id':flow_id, 'success': False, 'node_key': None, 'level': 'error',
                                        'msg': 'No fue obtener el max de la lista de dtypes', 'exception': str(e)})
            return current_dtypes

        for i,x in res.iterrows():
            if x['index'] in current_dtypes: # si el campo en la salida está en el pin de entrada, sólo actualizo el tipo de dato
                if node_name != 'Select': # los select, al permitir cambiar los datatypes no deben actualizarse
                    current_dtypes[x['index']]['dtype'] = x['dtypes']
            else: # si el campo no está, es porque se editó el flujo en algun punto intermedio y se debe crear el campo
                # del current_dtypes[x['index']]
                max_order += 1
                current_dtypes[x['index']] = {'dtype': x['dtypes'], 'selected': True, 'order': max_order}
                print('previamente no existía el campo "{}" en el nodo "{}", se agrega'.format(x['index'], node_name))
                bug_handler.append({'flow_id':flow_id, 'success': True, 'node_key': node_key, 'level': 'info',
                                        'msg': 'Campo "{}" no existía en el nodo "{}" previamente, se agrega'.format(x['index'], node_name), 'exception': ''})
                # print('Campo "{}" no existe en nodo "{}" será omitido'.format(x['index'], node_name))
        # print('\n\n\ncurrent_dtypes:\n')
        # print(current_dtypes)
        # Extraigo los campos que antes existían y ya no
        removed_fields = list(set(current_dtypes.keys()) - set(res['index'].tolist()))
        # Remuevo los campos que ya no existen
        # current_dtypes = dict(filter(lambda i: i[0] in res['index'].tolist(), current_dtypes.items()))
        for rf in removed_fields:
            to_remove = current_dtypes[rf]
            # print(rf, to_remove)
            bug_handler.append({'flow_id':flow_id, 'success': True, 'node_key': node_key, 'level': 'warning',
                                        'msg': 'Ya no existe el campo "{}" en el nodo "{}", se elimina de sus dtypes'.format(rf, node_name), 'exception': ''})
            del current_dtypes[rf]

        # print('\ncurrent_dtypes (modified):')
        # print(current_dtypes)
        return current_dtypes
        """

    def remove_flow_from_cache(self, flow_id: str):
        """DEPRECATED"""
        import gc

        from vtarget.handlers.cache_handler import cache_handler

        if flow_id in cache_handler.settings:
            print("remove_flow_from_cache")
            del cache_handler.settings[flow_id]
        gc.collect()

    def remove_nodes_from_cache(self, flow_id: str, node_keys: list[str]):
        import gc

        from vtarget.handlers.cache_handler import cache_handler

        removeds = []
        if flow_id in cache_handler.settings:
            for node_key in node_keys:
                if node_key in cache_handler.settings[flow_id]:
                    if node_key not in removeds:
                        removeds.append(node_key)
                    del cache_handler.settings[flow_id][node_key]
                    print("remove_nodes_from_cache")
        if flow_id in cache_handler.cache:
            for node_key in node_keys:
                if node_key in cache_handler.cache[flow_id]:
                    if node_key not in removeds:
                        removeds.append(node_key)
                    del cache_handler.cache[flow_id][node_key]

        cache_handler.dump_settings(flow_id)
        print(removeds)
        gc.collect()
        return removeds

    # Actualiza node['meta']['ports_map']['pout'][port_name]['summary']
    def load_detailed_view(self, flow_id: str, node_key: str, port_name: str):
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.utils.utilities import utilities

        # NOTE: No sé cuantas veces se ejecuta esta carga
        cache_handler.load(flow_id, node_key, port_name)
        if flow_id in cache_handler.cache and node_key in cache_handler.cache[flow_id]:
            df = cache_handler.cache[flow_id][node_key]["pout"][port_name]
            return utilities.viz_summary(df)
        return {}

    # Actualiza node['meta']['ports_map']['pout'][port_name]['describe']
    def load_column_view(self, flow_id: str, node_key: str, port_name: str):
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.utils.utilities import utilities

        # NOTE: No sé cuantas veces se ejecuta esta carga
        cache_handler.load(flow_id, node_key, port_name)
        if flow_id in cache_handler.cache and node_key in cache_handler.cache[flow_id]:
            df = cache_handler.cache[flow_id][node_key]["pout"][port_name]
            return utilities.get_central_tendency_measures(df)
        return {}

    def modify_node(self, flow_id: str, node_key: str, node: dict, port_name: str):
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.utils.utilities import utilities

        try:
            cache_handler.load(flow_id, node_key, port_name)
            if flow_id in cache_handler.cache and node_key in cache_handler.cache[flow_id]:
                cached_node = cache_handler.cache[flow_id][node_key]
                if "pout" in cached_node and port_name in cached_node["pout"]:
                    port_df = cached_node["pout"][port_name]
                    port_config = utilities.get_table_config(node["meta"], port_name)
                    head = utilities.get_head_of_df_as_list(port_df, port_config, flow_id, node_key, port_name)
                    node["meta"]["ports_map"]["pout"][port_name]["head"] = head
                else:
                    msg = app_message.dataprep["builder"]["exec_flow"]
                    return {
                        "flow_id": flow_id,
                        "node_key": node_key,
                        "node": node,
                        "success": False,
                        "error": msg,
                    }
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return {
                "flow_id": flow_id,
                "node_key": node_key,
                "node": node,
                "success": False,
                "error": str(e),
            }

        return {"flow_id": flow_id, "node_key": node_key, "node": node, "success": True}

    def run_node(self, flow_id: str, node_key: str, node: dict, links_to: list):
        if "CHART" in node_key.upper():
            return

        import json
        from typing import Dict

        import pandas as pd

        from vtarget.handlers.bug_handler import bug_handler
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.handlers.event_handler import event_handler

        print("run node", node_key)

        # Resetea los bug
        bug_handler.bug = []

        # Incializa la caché para el nodo si es que aún no existe
        cache_handler.load_settings(flow_id)

        # Almancena los df del mapeo de los puertos de entrada
        input_port: Dict[str, pd.DataFrame] = {}

        # Cargar la cache de los padres en los puertos de entrada del nodo
        for ld in links_to:
            if "_chart" in ld["to"]:
                continue
            parent_port = ld["frompid"]
            parent_key = ld["from"]
            node_port = ld["topid"]

            cache_handler.load(flow_id, parent_key, parent_port)  # carga la cache del padre
            parent_cache = cache_handler.cache[flow_id][parent_key] if flow_id in cache_handler.cache and parent_key in cache_handler.cache[flow_id] else dict()

            if parent_cache and "pout" in parent_cache and parent_port in parent_cache["pout"]:
                input_port[node_port] = parent_cache["pout"][parent_port]  # actualiza pin del nodo con la salida correspondiente del padre

        # ! restea paginacion a 1
        if "ports_config" in node["meta"] and node["meta"]["ports_config"] is not None:
            for port in node["meta"]["ports_config"]:
                node["meta"]["ports_config"][port]["page"] = 1

        node = self.pipeline.exec(flow_id, node, input_port)

        # Valida si la ejecucion del nodo tuvo algun error
        has_error = (
            next(
                (x for x in bug_handler.bug if x["node_key"] == node_key and x["level"] == "error"),
                None,
            )
            != None
        )
        node["meta"]["skipped"] = False
        node["meta"]["processed"] = True
        node["meta"]["has_error"] = has_error

        event_handler.emit_queue.put(
            {
                "name": "dataprep.node_processed",
                "data": {"flow_id": flow_id, "key": node_key, "node": json.dumps(node, default=str), "progress": 100},
            }
        )

        if has_error:
            cache_handler.delete_node(flow_id, node_key)

        # TODO: deberia guardarse el resultado en cache
        cache_handler.dump_settings(flow_id)

        return {
            "flow_id": flow_id,
            "key": node_key,
            "node": json.dumps(node, default=str),
        }


if __name__ == "__main__":
    b = Builder()
    m = b.load_model()
    print(m)
