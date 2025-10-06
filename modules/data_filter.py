"""
Módulo responsável pela aplicação de filtros nos dados
"""
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
from utils.logger import logger

class DataFilter:
    """Aplica filtros e transformações em DataFrames"""
    
    def __init__(self):
        pass
    
    def select_columns(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Seleciona apenas colunas específicas do DataFrame
        
        Args:
            df: DataFrame original
            columns: Lista de nomes de colunas a manter
            
        Returns:
            DataFrame filtrado
        """
        if not columns:
            return df
        
        # Mantém apenas colunas que existem no DataFrame
        available_columns = [col for col in columns if col in df.columns]
        
        if not available_columns:
            logger.warning("Nenhuma coluna selecionada encontrada no DataFrame")
            return df
        
        return df[available_columns].copy()
    
    def filter_by_date_range(self, df: pd.DataFrame, 
                            date_column: str,
                            start_date: datetime = None,
                            end_date: datetime = None) -> pd.DataFrame:
        """
        Filtra DataFrame por intervalo de datas
        
        Args:
            df: DataFrame a filtrar
            date_column: Nome da coluna de data
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            DataFrame filtrado
        """
        if date_column not in df.columns:
            logger.warning(f"Coluna '{date_column}' não encontrada")
            return df
        
        filtered_df = df.copy()
        
        try:
            # Converte coluna para datetime se necessário
            if not pd.api.types.is_datetime64_any_dtype(filtered_df[date_column]):
                filtered_df[date_column] = pd.to_datetime(filtered_df[date_column], errors='coerce')
            
            # Aplica filtro de data inicial
            if start_date:
                filtered_df = filtered_df[filtered_df[date_column] >= pd.to_datetime(start_date)]
            
            # Aplica filtro de data final
            if end_date:
                filtered_df = filtered_df[filtered_df[date_column] <= pd.to_datetime(end_date)]
            
            logger.info(f"Filtro de data aplicado: {len(filtered_df)} registros mantidos")
            return filtered_df
        
        except Exception as e:
            logger.error(f"Erro ao filtrar por data: {e}")
            return df
    
    def filter_by_value_range(self, df: pd.DataFrame,
                             value_column: str,
                             min_value: float = None,
                             max_value: float = None) -> pd.DataFrame:
        """
        Filtra DataFrame por intervalo de valores
        
        Args:
            df: DataFrame a filtrar
            value_column: Nome da coluna numérica
            min_value: Valor mínimo (opcional)
            max_value: Valor máximo (opcional)
            
        Returns:
            DataFrame filtrado
        """
        if value_column not in df.columns:
            logger.warning(f"Coluna '{value_column}' não encontrada")
            return df
        
        filtered_df = df.copy()
        
        try:
            # Converte para numérico se necessário
            if not pd.api.types.is_numeric_dtype(filtered_df[value_column]):
                filtered_df[value_column] = pd.to_numeric(filtered_df[value_column], errors='coerce')
            
            # Aplica filtro mínimo
            if min_value is not None:
                filtered_df = filtered_df[filtered_df[value_column] >= min_value]
            
            # Aplica filtro máximo
            if max_value is not None:
                filtered_df = filtered_df[filtered_df[value_column] <= max_value]
            
            logger.info(f"Filtro de valor aplicado: {len(filtered_df)} registros mantidos")
            return filtered_df
        
        except Exception as e:
            logger.error(f"Erro ao filtrar por valor: {e}")
            return df
    
    def filter_by_text(self, df: pd.DataFrame,
                      column: str,
                      search_text: str,
                      case_sensitive: bool = False) -> pd.DataFrame:
        """
        Filtra DataFrame por texto em uma coluna
        
        Args:
            df: DataFrame a filtrar
            column: Nome da coluna
            search_text: Texto a buscar
            case_sensitive: Se deve diferenciar maiúsculas/minúsculas
            
        Returns:
            DataFrame filtrado
        """
        if column not in df.columns or not search_text:
            return df
        
        try:
            filtered_df = df.copy()
            filtered_df[column] = filtered_df[column].astype(str)
            
            if case_sensitive:
                mask = filtered_df[column].str.contains(search_text, na=False)
            else:
                mask = filtered_df[column].str.contains(search_text, case=False, na=False)
            
            return filtered_df[mask]
        
        except Exception as e:
            logger.error(f"Erro ao filtrar por texto: {e}")
            return df
    
    def remove_duplicates(self, df: pd.DataFrame, 
                         subset: List[str] = None) -> pd.DataFrame:
        """
        Remove linhas duplicadas
        
        Args:
            df: DataFrame
            subset: Lista de colunas para considerar na duplicação
            
        Returns:
            DataFrame sem duplicatas
        """
        try:
            original_count = len(df)
            deduplicated_df = df.drop_duplicates(subset=subset, keep='first')
            removed_count = original_count - len(deduplicated_df)
            
            if removed_count > 0:
                logger.info(f"Removidas {removed_count} linhas duplicadas")
            
            return deduplicated_df
        
        except Exception as e:
            logger.error(f"Erro ao remover duplicatas: {e}")
            return df
    
    def sort_dataframe(self, df: pd.DataFrame,
                      by_columns: List[str],
                      ascending: bool = True) -> pd.DataFrame:
        """
        Ordena DataFrame por colunas específicas
        
        Args:
            df: DataFrame a ordenar
            by_columns: Lista de colunas para ordenação
            ascending: Se True, ordena crescente
            
        Returns:
            DataFrame ordenado
        """
        try:
            # Filtra apenas colunas existentes
            valid_columns = [col for col in by_columns if col in df.columns]
            
            if not valid_columns:
                return df
            
            return df.sort_values(by=valid_columns, ascending=ascending)
        
        except Exception as e:
            logger.error(f"Erro ao ordenar DataFrame: {e}")
            return df