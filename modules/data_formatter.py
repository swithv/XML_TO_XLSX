"""
Módulo responsável pela formatação e limpeza de dados
"""
import pandas as pd
import re
from typing import List
from utils.logger import logger
from utils.helpers import safe_float, safe_string

class DataFormatter:
    """Formata e limpa dados do DataFrame"""
    
    def __init__(self):
        pass
    
    def format_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica formatações gerais ao DataFrame
        
        Args:
            df: DataFrame a formatar
            
        Returns:
            DataFrame formatado
        """
        if df.empty:
            return df
        
        formatted_df = df.copy()
        
        # Formata cada coluna baseado em seu tipo/nome
        for column in formatted_df.columns:
            try:
                # Formata valores monetários
                if self._is_monetary_column(column):
                    formatted_df[column] = self._format_monetary_values(formatted_df[column])
                
                # Formata CPF/CNPJ
                elif 'cnpj' in column.lower() or 'cpf' in column.lower():
                    formatted_df[column] = formatted_df[column].apply(self._format_document)
                
                # Formata datas
                elif 'data' in column.lower() or pd.api.types.is_datetime64_any_dtype(formatted_df[column]):
                    formatted_df[column] = pd.to_datetime(formatted_df[column], errors='coerce')
                
                # Limpa strings
                elif formatted_df[column].dtype == 'object':
                    formatted_df[column] = formatted_df[column].apply(self._clean_string)
            
            except Exception as e:
                logger.warning(f"Erro ao formatar coluna {column}: {e}")
                continue
        
        return formatted_df
    
    def _is_monetary_column(self, column_name: str) -> bool:
        """Verifica se coluna contém valores monetários"""
        monetary_keywords = ['valor', 'total', 'preco', 'preço', 'custo', 'desconto']
        return any(keyword in column_name.lower() for keyword in monetary_keywords)
    
    def _format_monetary_values(self, series: pd.Series) -> pd.Series:
        """
        Formata valores monetários para float
        
        Args:
            series: Serie com valores
            
        Returns:
            Serie formatada
        """
        def convert_value(val):
            # Trata None e strings "None"
            if pd.isna(val) or val is None or str(val).strip() in ["None", ""]:
                return 0.0
            return safe_float(val, 0.0)
        
        return series.apply(convert_value)
    
    def _format_document(self, doc: str) -> str:
        """
        Formata CPF ou CNPJ
        
        Args:
            doc: Documento sem formatação
            
        Returns:
            Documento formatado
        """
        if pd.isna(doc) or doc is None or str(doc).strip() in ["None", ""]:
            return ""
        
        # Remove tudo que não é número
        doc = re.sub(r'\D', '', str(doc))
        
        # Formata CNPJ (14 dígitos)
        if len(doc) == 14:
            return f"{doc[:2]}.{doc[2:5]}.{doc[5:8]}/{doc[8:12]}-{doc[12:]}"
        
        # Formata CPF (11 dígitos)
        elif len(doc) == 11:
            return f"{doc[:3]}.{doc[3:6]}.{doc[6:9]}-{doc[9:]}"
        
        return doc
    
    def _clean_string(self, text) -> str:
        """
        Remove espaços extras e caracteres especiais de strings
        
        Args:
            text: Texto a limpar
            
        Returns:
            Texto limpo
        """
        if pd.isna(text) or text is None or str(text).strip() == "None":
            return ""
        
        text = str(text).strip()
        text = re.sub(r'\s+', ' ', text)  # Remove espaços múltiplos
        return text
    
    def fill_missing_values(self, df: pd.DataFrame, strategy: str = 'empty') -> pd.DataFrame:
        """
        Preenche valores faltantes
        
        Args:
            df: DataFrame
            strategy: Estratégia ('empty', 'zero', 'mean', 'forward')
            
        Returns:
            DataFrame com valores preenchidos
        """
        filled_df = df.copy()
        
        try:
            # Primeiro, substitui string "None" por NaN
            filled_df = filled_df.replace(['None', 'none', 'NONE'], pd.NA)
            
            if strategy == 'empty':
                # Preenche com strings vazias para texto, 0 para números
                for column in filled_df.columns:
                    if pd.api.types.is_numeric_dtype(filled_df[column]):
                        filled_df[column] = filled_df[column].fillna(0)
                    else:
                        filled_df[column] = filled_df[column].fillna('')
            
            elif strategy == 'zero':
                filled_df = filled_df.fillna(0)
            
            elif strategy == 'mean':
                # Média apenas para colunas numéricas
                numeric_columns = filled_df.select_dtypes(include=['number']).columns
                filled_df[numeric_columns] = filled_df[numeric_columns].fillna(
                    filled_df[numeric_columns].mean()
                )
            
            elif strategy == 'forward':
                filled_df = filled_df.fillna(method='ffill')
            
            return filled_df
        
        except Exception as e:
            logger.error(f"Erro ao preencher valores faltantes: {e}")
            return df
    
    def rename_columns(self, df: pd.DataFrame, mapping: dict = None) -> pd.DataFrame:
        """
        Renomeia colunas do DataFrame
        
        Args:
            df: DataFrame
            mapping: Dicionário {nome_antigo: nome_novo}
            
        Returns:
            DataFrame com colunas renomeadas
        """
        if not mapping:
            return df
        
        try:
            return df.rename(columns=mapping)
        except Exception as e:
            logger.error(f"Erro ao renomear colunas: {e}")
            return df
    
    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Padroniza nomes de colunas (remove espaços, acentos, etc)
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame com colunas padronizadas
        """
        try:
            new_columns = []
            for col in df.columns:
                # Remove acentos e caracteres especiais
                new_col = col.strip()
                new_col = re.sub(r'[^\w\s]', '', new_col)
                new_col = re.sub(r'\s+', '_', new_col)
                new_columns.append(new_col)
            
            df.columns = new_columns
            return df
        
        except Exception as e:
            logger.error(f"Erro ao padronizar nomes de colunas: {e}")
            return df