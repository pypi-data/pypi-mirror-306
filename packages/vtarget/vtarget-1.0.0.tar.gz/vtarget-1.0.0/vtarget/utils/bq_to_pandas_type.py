import pandas as pd
from google.cloud.bigquery.schema import SchemaField

class BigQueryToPandasTypeConverter:
    def _get_column_types(self, schema: list | list[SchemaField]):
        """Obtiene los tipos de datos de la tabla en BigQuery."""
        return {field.name: field.field_type for field in schema}

    def _try_cast_to_numeric(self, series):
        """Intenta convertir una serie a tipo numérico."""
        try:
            return pd.to_numeric(series, errors='coerce').astype(int)
        except Exception:
            return series

    def _try_cast_to_float(self, series):
        """Intenta convertir una serie a tipo flotante."""
        try:
            return pd.to_numeric(series, errors='coerce').astype(float)
        except Exception:
            return series

    def _try_cast_to_datetime(self, series):
        """Intenta convertir una serie a tipo datetime."""
        try:
            return pd.to_datetime(series, errors='coerce')
        except Exception:
            return series

    def _try_cast_to_bool(self, series):
        """Intenta convertir una serie a tipo booleano."""
        try:
            return series.astype(bool)
        except Exception:
            return series

    def _try_cast_based_on_type(self, series, bq_type):
        """Intenta convertir la serie basada en el tipo de dato de BigQuery."""
        if bq_type in ['INTEGER', 'INT64', 'NUMERIC', 'BIGNUMERIC']:
            return self._try_cast_to_numeric(series)
        elif bq_type in ['FLOAT', 'FLOAT64']:
            return self._try_cast_to_float(series)
        elif bq_type in ['DATE', 'DATETIME', 'TIMESTAMP']:
            return self._try_cast_to_datetime(series)
        elif bq_type in ['BOOLEAN', 'BOOL']:
            return self._try_cast_to_bool(series)
        else:
            return series  # Retorna la serie sin cambios si el tipo no está manejado

    def convert_dataframe(self, df: pd.DataFrame, schema: list | list[SchemaField]):
        """Aplica la conversión de tipos de datos en función del esquema de BigQuery."""
        column_types = self._get_column_types(schema)
        for column in df.columns:
            if column in column_types:
                bq_type = column_types[column]
                df[column] = self._try_cast_based_on_type(df[column], bq_type)
        return df
    
bq_to_pandas_type = BigQueryToPandasTypeConverter()