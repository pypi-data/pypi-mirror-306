import numpy as np
import pandas as pd


class DataFrameTypesOptimizer:

    def _optimize_numeric_types(self, df: pd.DataFrame):
        """Optimiza los tipos numéricos en el DataFrame utilizando downcast y conversiones adicionales."""
        for col in df.select_dtypes(include=[np.number]).columns:
            col_data = df[col]
            if col_data.dtype in ['float64', 'float32']:
                if col_data.max() < np.finfo(np.float32).max and col_data.min() > np.finfo(np.float32).min:
                    df[col] = col_data.astype('float32')
                elif col_data.max() < np.finfo(np.float16).max and col_data.min() > np.finfo(np.float16).min:
                    df[col] = col_data.astype('float16')
                    
            elif col_data.dtype in ['int64', 'int32', 'int16']:
                if col_data.max() < np.iinfo(np.int32).max and col_data.min() > np.iinfo(np.int32).min:
                    df[col] = col_data.astype('int32')
                elif col_data.max() < np.iinfo(np.int16).max and col_data.min() > np.iinfo(np.int16).min:
                    df[col] = col_data.astype('int16')
                elif col_data.max() < np.iinfo(np.int8).max and col_data.min() > np.iinfo(np.int8).min:
                    df[col] = col_data.astype('int8')

    def _optimize_categorical_types(self, df: pd.DataFrame):
        """Optimiza las columnas categóricas en el DataFrame."""
        for col in df.select_dtypes(include=['object']).columns:
            col_data = df[col]
            
            # Solo convierte si hay menos de un porcentaje específico de valores únicos
            if col_data.nunique() / len(col_data) < 0.1:  # Ajusta este umbral según sea necesario
                df[col] = col_data.astype('category')

    def optimize(self, df: pd.DataFrame):
        """Aplica la optimización de tipos de datos en el DataFrame."""
        self._optimize_numeric_types(df)
        # self._optimize_categorical_types(df)
        return df

dtype_optimizer = DataFrameTypesOptimizer()