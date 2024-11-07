# TODO: Importar el language acá
from typing import TypedDict, Any, Callable


class __AppMessage:
    class DataprepDict(TypedDict):
        class DataprepNodesDict(TypedDict):
            api_rest: Any
            code: Any
            column: Any
            dtype: Any
            datetime_fill: Any
            datetime_range: Any
            concat: Any
            cross_join: Any
            cumsum: Any
            cut: Any
            database_write: Any
            database: Any
            datetime_extract: Any
            datetime_formatter: Any
            describe: Any
            df_maker: Any
            email: Any
            excel: Any
            filter: Any
            group_by: Any
            input_data: Any
            inter_row: Any
            merge: Any
            pivot: Any
            rolling: Any
            sample: Any
            split: Any
            switch: Any
            database_utilities: Any
            deploy_enabled: Callable[[str], str]
            exception: Callable[[str, str], str]
            missing_column: Callable[[str], str]
            empty_list: Callable[[str, str], str]
            missing_specific_column: Callable[[str, str], str]
            empty_df: Callable[[str, str], str]
            empty_entry_list: Callable[[str, str], str]
            missing_df: Callable[[str, str], str]
            required_prop: Callable[[str, str], str]

        nodes: DataprepNodesDict

        class DataprepBuilderDict(TypedDict):
            reset_cache: Callable[[str], str]
            nodes_in_cache: Callable[[int], str]
            not_send: Callable[[str], str]
            skip_writing: Callable[[str], str]
            parent_without_entry: Callable[[str], str]
            save_cache: Callable[[int], str]
            processed_flow: Callable[[float], str]
            stopped_flow: str
            exec_flow: str
            max_rows: Callable[[str, int], str]

        builder: DataprepBuilderDict

    dataprep: DataprepDict

    class DatavizDict(TypedDict):
        pass

    dataviz: DatavizDict

    class AutotsDict(TypedDict):
        pass

    autots: AutotsDict

    class AutomlDict(TypedDict):
        pass

    automl: AutomlDict

    class HandlersDict(TypedDict):
        pass

    handlers: HandlersDict

    class UtilsDict(TypedDict):
        pass

    utils: UtilsDict

    class WorkerDict(TypedDict):
        pass

    worker: WorkerDict

    class ServiceDict(TypedDict):
        pass

    service: ServiceDict

    def __init__(self, languaje):
        if languaje == "es":
            self.dataprep = self.dataprep_spanish()
            self.dataviz = self.dataviz_spanish()
            self.autots = self.autots_spanish()
            self.automl = self.automl_spanish()
            self.handlers = self.handlers_spanish()
            self.utils = self.utils_spanish()
            self.worker = self.worker_spanish()
            self.service = self.service_spanish()
        else:
            self.dataprep = self.dataprep_english()
            self.dataviz = self.dataviz_english()
            self.autots = self.autots_english()
            self.automl = self.automl_english()
            self.handlers = self.handlers_english()
            self.utils = self.utils_english()
            self.worker = self.worker_english()
            self.service = self.service_english()

    # ===================================
    # Spanish
    # ===================================
    def dataprep_spanish(self) -> DataprepDict:
        return {
            "nodes": {
                "api_rest": {
                    "no_method": lambda node_key: f"({node_key}): Debes seleccionar un método de envío",
                    "no_url": lambda node_key: f"({node_key}): Debes seleccionar una URL",
                },
                "code": {
                    "no_vtg_codeout": lambda node_key: f"({node_key}): Debes llamar a la función vtg_codeout(Df) con tu DataFrame de salida",
                },
                "column": {
                    "no_columns_selected": lambda node_key: f"({node_key}): No hay columnas seleccionadas",
                    "rename_columns": lambda node_key: f"({node_key}): No fue posible renombrar las columnas",
                    "column_not_in_df": lambda node_key, column: f"({node_key}): La columna '{column}' no existe en el Dataframe",
                },
                "dtype": {
                    "no_columns_selected": lambda node_key: f"({node_key}): No hay columnas seleccionadas",
                    "rename_columns": lambda node_key: f"({node_key}): No fue posible renombrar las columnas",
                    "column_not_in_df": lambda node_key, column: f"({node_key}): La columna '{column}' no existe en el Dataframe",
                    "change_dtype": lambda node_key, column, dtype: f"({node_key}): No fue posible transformar el tipo de dato de la columna '{column}' a '{dtype}'",
                    "unknow_dtype": lambda node_key, column, dtype: f"({node_key}): Tipo de dato '{dtype}' desconocido. Columna '{column}' se mantiene como string",
                },
                "datetime_fill": {
                    "time_column_required": lambda node_key: f"({node_key}): La columna 'Tiempo' es obligatoria",
                    "key_column_required": lambda node_key: f"({node_key}): Se requiere la lista de columnas clave",
                    "frequency_column_required": lambda node_key: f"({node_key}): Se requiere 'Frecuencia'",
                    "properties_not_provided": lambda node_key: f"({node_key}): Debes proporcionar todas las propiedades",
                },
                "datetime_range": {
                    "start_date_required": lambda node_key: f"({node_key}): Se requiere el campo 'Fecha Inicio'",
                    "end_date_required": lambda node_key: f"({node_key}): Se requiere 'Fecha Fin'",
                    "frequency_is_required": lambda node_key: f"({node_key}): Se requiere 'Frecuencia'",
                    "properties_not_provided": lambda node_key: f"({node_key}): Debes proporcionar todas las propiedades",
                },
                "concat": {
                    "input_port_A": lambda node_key, col: f"({node_key}): La columna '{col}' no existe en Dataframe A",
                    "input_port_B": lambda node_key, col: f"({node_key}): La columna '{col}' no existe en Dataframe B",
                },
                "cross_join": {},
                "cumsum": {
                    "aggregation_required": lambda node_key: f"({node_key}): Debes seleccionar al menos un método de agregación",
                },
                "cut": {
                    "no_cutting_parameter": lambda node_key: f"({node_key}): No hay parámetro de corte",
                    "no_type_cut": lambda node_key: f"({node_key}): El tipo de corte no existe",
                },
                "database_write": {
                    "source_required": lambda node_key: f"({node_key}): Debes seleccionar un recurso de conexión",
                    "no_column_in_table": lambda node_key, column, table: f'({node_key}): La columna "{column}" no existe en la tabla "{table}"',
                },
                "database": {
                    "source_required": lambda node_key: f"({node_key}): Debes seleccionar un recurso de conexión",
                },
                "datetime_extract": {},
                "datetime_formatter": {
                    "pattern_quotes": lambda node_key: f"({node_key}): Usa comillas en el patrón personalizado",
                    "pattern_required": lambda node_key: f"({node_key}): Debes seleccionar al menos un formato",
                },
                "describe": {},
                "df_maker": {},
                "email": {
                    "config_required": lambda node_key, fields: f"({node_key}): Todos los campos deben ser completados. Campos faltantes {fields}",
                    "failed_send": lambda node_key: f"({node_key}): No fue posible realizar el envío de email",
                    "size_max": lambda node_key: f"({node_key}): No es posible enviar el correo ya que el tamaño de los archivos adjuntos supera el límite máximo",
                },
                "excel": {
                    "failed_generate": lambda node_key: f"({node_key}): No fue posible generar el archivo excel",
                    "output_path": lambda node_key: f"({node_key}): Seleccione directorio de salida",
                },
                "filter": {
                    "rules": lambda node_key: f"({node_key}): Debes crear una regla",
                    "unknow_rule": lambda node_key, rule: f"({node_key}): No se reconoce la regla '{rule}'",
                    "failed_condition": lambda node_key: f"({node_key}): No fue posible procesar la condición",
                    "unknow_column": lambda node_key, field: f"({node_key}): No existe la columna '{field}' en el Dataframe de entrada",
                    "unknow_operator": lambda node_key, operator: f"({node_key}): Operador '{operator}' no reconocido ",
                },
                "group_by": {
                    "missing_props": lambda node_key: f"({node_key}): Alguna de las propiedades para el método de agregación no ha sido proporcionada",
                },
                "input_data": {
                    "url_not_valid": lambda node_key, path: f"({node_key}): Url '{path}' no existe o no es válida",
                    "missing_extension": lambda node_key: f"({node_key}): No existe extensión del archivo",
                    "file_not_exist": lambda node_key, path: f"({node_key}): Archivo '{path}' no existe en disco",
                    "unknow_format": lambda node_key, format: f"({node_key}): Formato '{format}' no reconocido",
                    "end_start_spaces": lambda node_key: f"({node_key}): Archivo fuente contiene espacios al inicio o final del nombre de una o más columnas. Se ha corregido para la lectura",
                    "wrong_sheet_name": lambda node_key, sheet_name: f"({node_key}): No se encontró una hoja con el nombre '{sheet_name}'",
                },
                "inter_row": {
                    "fillna": lambda node_key: f"({node_key}): La función 'fillna', debes especificar el valor para los nulos",
                },
                "merge": {
                    "input_port": lambda node_key: f"({node_key}): Puerto entrada iL o iR no conectado",
                    "input_port_il": lambda node_key, col: f"({node_key}): La columna '{col}' no existe en Dataframe iL",
                    "input_port_iR": lambda node_key, col: f"({node_key}): La columna '{col}' no existe en Dataframe iR",
                    "not_equal_len": lambda node_key,: f"({node_key}): Campos de la izquierda y derecha del Merge deben ser del mismo largo",
                },
                "pivot": {
                    "incompleted_fields": lambda node_key, missing: f"({node_key}): Faltan campos de la configuración. Campos faltantes: {missing}",
                },
                "rolling": {
                    "column_required": lambda node_key: f"({node_key}): Column is required",
                    "operation_required": lambda node_key: f"({node_key}): Operation is required",
                    "properties_not_provided": lambda node_key: f"({node_key}): Algunas de las propiedades no han sido proporcionadas",
                },
                "sample": {
                    "sample_size": lambda node_key: f"({node_key}) Debes ingresar un tamaño de muestra válida mayor a 0",
                },
                "split": {
                    "default_value": lambda node_key: f"({node_key}): No existe Valor o Columna por defecto",
                },
                "switch": {
                    "default_value": lambda node_key: f"({node_key}): Default Value no existe o es vacío",
                    "no_column_in_df": lambda node_key, column: f"({node_key}): La columna '{column}' no existe en el Dataframe",
                    "no_conditions": lambda node_key, caseIdx: f"({node_key}): No existe condiciones para el caso {caseIdx}",
                    "no_return_value": lambda node_key, caseIdx: f"({node_key}): No existe valor de salida para el caso {caseIdx}",
                    "no_value_or_field": lambda node_key, caseIdx, conditionIdx: f"({node_key}): No existe valor para la condición {conditionIdx} del caso {caseIdx}",
                    "missing_condition_prop": lambda node_key, prop, caseIdx, conditionIdx: f"({node_key}): No existe {prop} para la condición {conditionIdx} del caso {caseIdx}",
                },
                "database_utilities": {
                    "source_required": lambda node_key: f"({node_key}): Debes seleccionar un recurso de conexión",
                    "check_missing_source": lambda node_key: f"({node_key}): El recurso de conexión no se encuentra",
                    "check_fields_to_connection": lambda node_key, field: f"({node_key}): Falta la columna '{field}' para establecer la conexión",
                    "check_empty_fields": lambda node_key, field: f"({node_key}): La columna '{field}' se encuentra vacía",
                    "check_optional_fields": lambda node_key: f"({node_key}): Faltan campos para establecer conexión",
                },
                "deploy_enabled": lambda node_key: f"({node_key}): El deploy_mode está habilitado, pero deploy_path no existe en la configuración del nodo",
                "exception": lambda node_key, error: f"({node_key}) Error: " + error,
                "missing_column": lambda node_key: f"({node_key}): Debes seleccionar al menos una columna",
                "empty_list": lambda node_key, name: f"({node_key}): Debes seleccionar al menos una opción de la lista de '{name}'",
                "missing_specific_column": lambda node_key, column: f"({node_key}): Debes seleccionar la columna '{column}'",
                "empty_df": lambda node_key, name: f"({node_key}): Dataframe de entrada {name} está vacío",
                "empty_entry_list": lambda node_key, port: f"({node_key}): Debes seleccionar al menos un campo en la entrada '{port}'",
                "missing_df": lambda node_key, name: f"({node_key}): No existe dataframe de entrada {name}",
                "required_prop": lambda node_key, prop: f"({node_key}): El campo '{prop}' es obligatorio",
            },
            "builder": {
                "reset_cache": lambda flow_name: f"Caché reseteada en flujo '{flow_name}'",
                "nodes_in_cache": lambda q_nodes: f"'{q_nodes}' Nodos en caché",
                "not_send": lambda node_key: f"Se omite envío para nodo '{node_key}'",
                "skip_writing": lambda node_key: f"Se omite escritura de archivo para nodo '{node_key}'",
                "parent_without_entry": lambda node_key: f"Se omite nodo '{node_key}' sin entrada padre",
                "parent_disabled": lambda node_key: f"Nodo '{node_key}' no puede procesarse, uno de los nodos padres está deshabilitado",
                "save_cache": lambda q_nodes: f"Se almacenaron '{q_nodes}' nodos en caché",
                "processed_flow": lambda seconds: f"Flujo procesado en '{seconds}' segundos",
                "stopped_flow": "La ejecución del flujo ha sido interrumpida",
                "exec_flow": "El flujo aún no se ha ejecutado",
                "max_rows": lambda node_key, max_rows: f"({node_key}): Se ha exedido el máximo de filas permitido ({f'{max_rows:_}'.replace('_','.')})",
            },
        }

    def dataviz_spanish(self) -> DatavizDict:
        return {
            "data_source_reader": {
                "not_memory_flow": lambda node_key, flow_name: f"La fuente de datos del nodo '{node_key}' en el flujo '{flow_name}' No está en memoria. Por favor ejecuta el flujo en el módulo Dataprep",
                "no_such_file": lambda file_path: f"No se encuentró el archivo '{file_path}'",
                "unspecified_extension": f"El archivo debe tener alguna extensión",
                "invalid_extension": lambda extensions: f"Las extensiones permitidas son: '{extensions}'",
            },
            "data_frame_operator": {
                "specified_operation": "Operación no especificada. Por favor selecciona alguna operación para la métrica.",
                "invalid_operation": lambda operation, operation_dict: f"La operación '{operation}' es inválida'. Operaciones permitidas: '{operation_dict}'",
                "field_numeric": lambda operation, field_name: f"La operación '{operation}' requiere que el campo '{field_name}' sea númerico",
            },
            "items": {
                "scatter": {
                    "non_numeric_xaxis": "La variable del eje x debe ser numérica",
                    "non_numeric_yaxis": "La variable del eje y debe ser numérica",
                }
            },
        }

    def autots_spanish(self) -> AutotsDict:
        return {
            "autots": {
                "not_train": "Aún no se ha realizado el entrenamiento",
                "not_path": lambda pickle: f"{pickle}: Ruta no existe",
            },
            "train": {},
            "exception": lambda error: f"Error: " + error,
        }

    def automl_spanish(self) -> AutomlDict:
        return {
            "automl": {
                "not_train": "Aún no se ha realizado el entrenamiento",
                "not_path": lambda pickle: f"{pickle}: Ruta no existe",
            },
            "exception": lambda error: f"Error: " + error,
        }

    def handlers_spanish(self) -> HandlersDict:
        return {
            "cache_handler": {
                "node_cache_saved": lambda node_key: f"({node_key}) Almacenado en cache",
                "node_ram_saved": lambda node_key: f"({node_key}) Almacenado en RAM",
            },
            "exception": lambda error: f"Error: " + error,
        }

    def utils_spanish(self) -> UtilsDict:
        return {
            "utilities": {
                "sort_column_not_in_df": "Algunas columnas de orden no existen en la tabla de resultados",
                "var_not_in_df": lambda prop: f"La columna '{prop}' no existe en el Dataframe",
                "duplicated_columns": lambda columns: f"Se han corregido las siguientes columnas duplicadas: {columns}. Revise la configuración del nodo",
                "empty_labels": "Se han corregido algunos nombres de columna vacíos en el dataframe de entrada",
            },
            "exception": lambda error: f"Error: " + error,
        }

    def worker_spanish(self) -> WorkerDict:
        return {
            "listener": {
                "automl": {
                    "get_interaction": {
                        "missing_property": lambda prop: f"Falta la propiedad '{prop}'",
                    },
                    "load_source": {
                        "not_path": f"Falta la ruta del archivo",
                    },
                    "load_voutput": {
                        "not_flow_cache": f"Flujo no cargado en caché",
                    },
                    "set_cache": {
                        "not_flow_cache": f"Flujo no cargado en caché",
                        "not_source": f"No existe fuente de datos",
                    },
                    "start_training": {
                        "var_not_in_data": lambda prop: f"La variable '{prop}' no está en la data",
                    },
                },
                "autots": {
                    "get_interaction": {
                        "missing_property": lambda prop: f"Falta la propiedad '{prop}'",
                    },
                    "load_source": {
                        "not_path": f"Falta la ruta del archivo",
                    },
                    "load_voutput": {
                        "not_flow_cache": f"Flujo no cargado en caché",
                    },
                    "set_cache": {
                        "not_flow_cache": f"Flujo no cargado en caché",
                        "not_source": f"No existe fuente de datos",
                        "processing_error": lambda error: f"Error al intentar procesar: " + error,
                    },
                    "start_training": {
                        "var_not_in_data": lambda prop: f"La variable '{prop}' no está en la data",
                    },
                },
                "dataprep": {
                    "node_output": {
                        "var_not_in_data": lambda prop: f"La variable '{prop}' no está en la data",
                    },
                },
            },
            "exception": lambda error: f"Error: " + error,
            "unexpected_error": "Ha ocurrido un error inesperado",
        }

    def service_spanish(self) -> ServiceDict:
        return {
            "socket_listeners": {
                "dataprep": {
                    "database_connections": {
                        "get_databases": {
                            "get_database_error": lambda db, error: f"Error al obtener las Bases de Datos desde '{db}'\nError: {error}",
                        },
                        "get_projects": {
                            "get_project_error": lambda db, error: f"Error al obtener los Proyectos desde '{db}'\nError: {error}",
                        },
                        "get_tables": {
                            "get_table_error": lambda db, error: f"Error al obtener las Tablas desde '{db}'\nError: {error}",
                        },
                        "get_warehouses": {
                            "get_warehouse_error": lambda db, error: f"Error al obtener los Almacenes desde '{db}'\nError: {error}",
                        },
                        "unknow_source": "El recurso no coincide con ninguno de la lista",
                    }
                }
            },
            "http_listeners": {
                "auth_listener": {
                    "connection_error": "Error al conectarse al servicio de autenticación, verifique su conexión e inténtelo nuevamente más tarde",
                },
            },
            "exception": lambda error: f"Error: " + error,
        }

    # ===================================
    # English
    # ===================================
    def dataprep_english(self) -> DataprepDict:
        return {
            "nodes": {
                "api_rest": {
                    "no_method": lambda node_key: f"({node_key}): You must select a sending method",
                    "no_url": lambda node_key: f"({node_key}): You must select a URL",
                },
                "code": {
                    "no_vtg_codeout": lambda node_key: f"({node_key}): You must invoke the vtg_codeout(Df) function with your output DataFrame",
                },
                "column": {
                    "no_columns_selected": lambda node_key: f"({node_key}): No columns selected",
                    "rename_columns": lambda node_key: f"({node_key}): Could not rename columns",
                    "column_not_in_df": lambda node_key, column: f"({node_key}): Column '{column}' does not exist in the Dataframe",
                },
                "dtype": {
                    "no_columns_selected": lambda node_key: f"({node_key}): No columns selected",
                    "rename_columns": lambda node_key: f"({node_key}): Could not rename columns",
                    "column_not_in_df": lambda node_key, column: f"({node_key}): Column '{column}' does not exist in Dataframe",
                    "change_dtype": lambda node_key, column, dtype: f"({node_key}): It was not possible to transform the column '{column}' data type to '{dtype}'",
                    "unknow_dtype": lambda node_key, column, dtype: f"({node_key}): Unknown data type '{dtype}' in '{column}', it will be maintained as string",
                },
                "datetime_fill": {
                    "time_column_required": lambda node_key: f"({node_key}): 'Time' column is required",
                    "key_column_required": lambda node_key: f"({node_key}): Key columns list is required",
                    "frequency_column_required": lambda node_key: f"({node_key}): 'Frequency' column is required",
                    "properties_not_provided": lambda node_key: f"({node_key}): You must provide all properties",
                },
                "datetime_range": {
                    "start_date_required": lambda node_key: f"({node_key}): Start Date field is required",
                    "end_date_required": lambda node_key: f"({node_key}): End Date field is required",
                    "frequency_is_required": lambda node_key: f"({node_key}): Frequency field is required",
                    "properties_not_provided": lambda node_key: f"({node_key}): You must provide all properties",
                },
                "concat": {
                    "input_port_A": lambda node_key, col: f"({node_key}): Column '{col}' not contained in 'A' Dataframe columns",
                    "input_port_B": lambda node_key, col: f"({node_key}): Column '{col}' not contained in 'B' Dataframe columns",
                },
                "cross_join": {},
                "cumsum": {
                    "aggregation_required": lambda node_key: f"({node_key}): You must select at least one aggregation method",
                },
                "cut": {
                    "no_cutting_parameter": lambda node_key: f"({node_key}): There is no cutting parameter",
                    "no_type_cut": lambda node_key: f"({node_key}): The type of cut does not exist",
                },
                "database_write": {
                    "source_required": lambda node_key: f"({node_key}): You must select a connection resource",
                    "no_column_in_table": lambda node_key, column, table: f'({node_key}): Column "{column}" does not exist in table "{table}"',
                },
                "database": {
                    "source_required": lambda node_key: f"({node_key}): You must select a connection resource",
                },
                "datetime_extract": {},
                "datetime_formatter": {
                    "pattern_quotes": lambda node_key: f"({node_key}): Use quotes in custom pattern",
                    "pattern_required": lambda node_key: f"({node_key}): You must select at least one format",
                },
                "describe": {},
                "df_maker": {},
                "email": {
                    "config_required": lambda node_key, fields: f"({node_key}): All fields must be completed. Missing fields {fields}",
                    "failed_send": lambda node_key: f"({node_key}): Email was not sent",
                    "size_max": lambda node_key: f"({node_key}): Unable to send the email, the size of the attachments exceeds the maximum limit",
                },
                "excel": {
                    "failed_generate": lambda node_key: f"({node_key}): It was not possible to generate the excel file",
                    "output_path": lambda node_key: f"({node_key}): Select output directory",
                },
                "filter": {
                    "rules": lambda node_key: f"({node_key}): You must create a Rule",
                    "unknow_rule": lambda node_key, rule: f"({node_key}): The rule is not recognized '{rule}'",
                    "failed_condition": lambda node_key: f"({node_key}): Condition could not be processed",
                    "unknow_column": lambda node_key, field: f"({node_key}): Column '{field}' does not exist in the input Dataframe",
                    "unknow_operator": lambda node_key, operator: f"({node_key}): Operator '{operator}' not recognized",
                },
                "group_by": {"missing_props": lambda node_key: f"({node_key}): Some of the properties of aggregate method have not been provided"},
                "input_data": {
                    "url_not_valid": lambda node_key, path: f"({node_key}): Url '{path}' does not exist or does not valid",
                    "missing_extension": lambda node_key: f"({node_key}): Does not exist extension",
                    "file_not_exist": lambda node_key, path: f"({node_key}): File '{path}' does not exist on disk",
                    "unknow_format": lambda node_key, format: f"({node_key}): Format '{format}' not recognized",
                    "end_start_spaces": lambda node_key: f"({node_key}): Source file contains spaces at the beginning or end of the name of one or more columns. It has been corrected for reading",
                    "wrong_sheet_name": lambda node_key, sheet_name: f"({node_key}): Worksheet named '{sheet_name}' not found",
                },
                "inter_row": {
                    "fillna": lambda node_key: f"({node_key}): 'fillna' function, must specify the value for nulls",
                },
                "merge": {
                    "input_port": lambda node_key: f"({node_key}): iL or iR input port not connected",
                    "input_port_il": lambda node_key, col: f"({node_key}): Column '{col}' not contained in 'iL' Dataframe columns",
                    "input_port_iR": lambda node_key, col: f"({node_key}): Column '{col}' not contained in 'iR' Dataframe columns",
                    "not_equal_len": lambda node_key,: f"({node_key}): len(Left Merge columns) must be equal to len(Right Merge columns)",
                },
                "pivot": {
                    "incompleted_fields": lambda node_key, missing: f"({node_key}): Empty fields in setting: '{missing}'",
                },
                "rolling": {
                    "column_required": lambda node_key: f"({node_key}): Column is required",
                    "operation_required": lambda node_key: f"({node_key}): Operation is required",
                    "properties_not_provided": lambda node_key: f"({node_key}): Empty properties",
                },
                "sample": {"sample_size": lambda node_key: f"({node_key}) You must enter a valid sample size greater than 0"},
                "split": {
                    "default_value": lambda node_key: f"({node_key}): Default value does not exist",
                },
                "switch": {
                    "default_value": lambda node_key: f"({node_key}): Default Value does not exist or is empty",
                    "no_column_in_df": lambda node_key, column: f"({node_key}): The column '{column}' does not exist in the Dataframe",
                    "no_return_value": lambda node_key, caseIdx: f"({node_key}): Return value does not exist for case {caseIdx}",
                    "no_conditions": lambda node_key, caseIdx: f"({node_key}): Condition list does not exist for case {caseIdx}",
                    "no_value_or_field": lambda node_key, caseIdx, conditionIdx: f"({node_key}): Value does not exist for condition {conditionIdx} of case {caseIdx}",
                    "missing_condition_prop": lambda node_key, prop, caseIdx, conditionIdx: f"({node_key}): {prop} does not exist for condition {conditionIdx} of case {caseIdx}",
                },
                "database_utilities": {
                    "source_required": lambda node_key: f"({node_key}): Select a connection resource",
                    "check_missing_source": lambda node_key: f"({node_key}): Connection resource not found",
                    "check_fields_to_connection": lambda node_key, field: f"({node_key}): Empty Column: '{field}'",
                    "check_empty_fields": lambda node_key, field: f"({node_key}): Empty Column: '{field}'",
                    "check_optional_fields": lambda node_key: f"({node_key}): Empty fields to establish connection",
                },
                "deploy_enabled": lambda node_key: f"({node_key}): 'deploy_mode' is enabled, but 'deploy_path' does not exist in the node configuration",
                "exception": lambda node_key, error: f"({node_key}) Error: " + error,
                "missing_column": lambda node_key: f"({node_key}): At least one column must be selected",
                "empty_list": lambda node_key, name: f"({node_key}): Must select at least one option from the '{name}' list",
                "missing_specific_column": lambda node_key, column: f"({node_key}): Must select the column '{column}'",
                "empty_df": lambda node_key, name: f"({node_key}): Input dataframe {name} is empty",
                "empty_entry_list": lambda node_key, port: f"({node_key}): You must keep at least one field in the entry '{port}'",
                "missing_df": lambda node_key, name: f"({node_key}): Input dataframe {name} does not exist",
                "required_prop": lambda node_key, prop: f"({node_key}): The '{prop}' field is required",
            },
            "builder": {
                "reset_cache": lambda flow_name: f"Reset cache in flow '{flow_name}'",
                "nodes_in_cache": lambda q_nodes: f"'{q_nodes}' Cached nodes",
                "not_send": lambda node_key: f"Sending is skipped for node '{node_key}'",
                "skip_writing": lambda node_key: f"File write skipped for node '{node_key}'",
                "parent_without_entry": lambda node_key: f"Node '{node_key}' is omitted without parent entry",
                "parent_disabled": lambda node_key: f"Node '{node_key}' cannot be processed, some of the parent nodes are disabled",
                "save_cache": lambda q_nodes: f"'{q_nodes}' nodes were cached",
                "processed_flow": lambda seconds: f"Stream processed in '{seconds}' seconds",
                "stopped_flow": f"Flow execution has been stopped",
                "exec_flow": "Flow has not run yet",
                "max_rows": lambda node_key, max_rows: f"({node_key}): Maximum number of rows allowed has been exceeded ({f'{max_rows:_}'.replace('_','.')})",
            },
        }

    def dataviz_english(self) -> DatavizDict:
        return {
            "data_source_reader": {
                "not_memory_flow": lambda node_key, flow_name: f"The data source of node '{node_key}' in flow '{flow_name}' is not in memory. Please Run the flow in the Dataprep module",
                "no_such_file": lambda file_path: f"File '{file_path}' cannot be found",
                "unspecified_extension": f"The file must have some extension",
                "invalid_extension": lambda extensions: f"The allowed extensions are: '{extensions}'",
            },
            "data_frame_operator": {
                "specified_operation": "Unspecified operation. Please select some operation for the metric.",
                "invalid_operation": lambda operation, operation_dict: f"The operation '{operation}' is invalid'. Allowed operations: '{operation_dict}'",
                "field_numeric": lambda operation, field_name: f"Operation '{operation}' requires field '{field_name}' to be numeric",
            },
            "items": {
                "scatter": {
                    "non_numeric_xaxis": "The x-axis variable must be numeric",
                    "non_numeric_yaxis": "The y-axis variable must be numeric",
                }
            },
        }

    def autots_english(self) -> AutotsDict:
        return {
            "autots": {
                "not_train": "Training has not been done yet",
                "not_path": lambda pickle: f"{pickle}: Route does not exist",
            },
            "train": {},
            "exception": lambda error: f"Error: " + error,
        }

    def automl_english(self) -> AutomlDict:
        return {
            "automl": {
                "not_train": "Training has not been done yet",
                "not_path": lambda pickle: f"{pickle}: Route does not exist",
            },
            "exception": lambda error: f"Error: " + error,
        }

    def handlers_english(self) -> HandlersDict:
        return {
            "cache_handler": {
                "node_cache_saved": lambda node_key: f"({node_key}) Stored in cache",
                "node_ram_saved": lambda node_key: f"({node_key}) Stored in RAM",
            },
            "exception": lambda error: f"Error: " + error,
        }

    def utils_english(self) -> UtilsDict:
        return {
            "utilities": {
                "sort_column_not_in_df": "Some order columns do not exist in results table",
                "var_not_in_df": lambda prop: f"Column '{prop}' is not in the Dataframe",
                "duplicated_columns": lambda columns: f"Fixed the following duplicate columns: {columns}. Check node configuration",
                "empty_labels": "Fixed some empty column names in the input dataframe",
            },
            "exception": lambda error: f"Error: " + error,
        }

    def worker_english(self) -> WorkerDict:
        return {
            "listener": {
                "automl": {
                    "get_interaction": {
                        "missing_property": lambda prop: f"Property '{prop}' is missing",
                    },
                    "load_source": {
                        "not_path": f"File path is missing",
                    },
                    "load_voutput": {
                        "not_flow_cache": f"Flow not loaded in cache",
                    },
                    "set_cache": {
                        "not_flow_cache": f"Flow not loaded in cache",
                        "not_source": f"There is no data source",
                    },
                    "start_training": {
                        "var_not_in_data": lambda prop: f"The variable '{prop}' is not in the data",
                    },
                },
                "autots": {
                    "get_interaction": {
                        "missing_property": lambda prop: f"Property '{prop}' is missing",
                    },
                    "load_source": {
                        "not_path": f"File path is missing",
                    },
                    "load_voutput": {
                        "not_flow_cache": f"Flow not loaded in cache",
                    },
                    "set_cache": {
                        "not_flow_cache": f"Flow not loaded in cache",
                        "not_source": f"There is no data source",
                        "processing_error": lambda error: f"Error trying to process: " + error,
                    },
                    "start_training": {
                        "var_not_in_data": lambda prop: f"The variable '{prop}' is not in the data",
                    },
                },
                "dataprep": {
                    "node_output": {
                        "var_not_in_data": lambda prop: f"The variable '{prop}' is not in the data",
                    },
                },
            },
            "exception": lambda error: f"Error: " + error,
            "unexpected_error": "An unexpected error has occurred",
        }

    def service_english(self) -> ServiceDict:
        return {
            "socket_listeners": {
                "dataprep": {
                    "database_connections": {
                        "get_databases": {
                            "get_database_error": lambda db, error: f"Error obtaining Databases from '{db}'\nError: {error}",
                        },
                        "get_projects": {
                            "get_project_error": lambda db, error: f"Error getting Projects from '{db}'\nError: {error}",
                        },
                        "get_tables": {
                            "get_table_error": lambda db, error: f"Error getting Tables from '{db}'\nError: {error}",
                        },
                        "get_warehouses": {
                            "get_warehouse_error": lambda db, error: f"Error getting Stores from '{db}'\nError: {error}",
                        },
                        "unknow_source": "The resource does not match any in the list",
                    }
                }
            },
            "http_listeners": {
                "auth_listener": {
                    "connection_error": "Error connecting to the authentication service, please check your connection and try again later",
                },
            },
            "exception": lambda error: f"Error: " + error,
        }


app_message = __AppMessage("es")
