"""
Módulo responsável por fazer parse de XMLs e converter em DataFrames
"""
import xmltodict
import pandas as pd
from typing import List, Tuple, Dict, Any
import config
from utils.logger import logger
from utils.helpers import get_nested_value, safe_float, parse_date

class XMLParser:
    """Converte arquivos XML em DataFrames pandas"""
    
    def __init__(self):
        self.field_mapping = config.DEFAULT_XML_FIELDS
    
    def parse_multiple_xmls(self, xml_files: List[Tuple[str, bytes]]) -> pd.DataFrame:
        """
        Converte múltiplos XMLs em um único DataFrame
        
        Args:
            xml_files: Lista de tuplas (nome_arquivo, conteúdo_xml)
            
        Returns:
            DataFrame consolidado
        """
        all_data = []
        
        for filename, xml_content in xml_files:
            try:
                parsed_data = self._parse_single_xml(filename, xml_content)
                if parsed_data:
                    all_data.append(parsed_data)
            except Exception as e:
                logger.error(f"Erro ao processar {filename}: {e}")
                continue
        
        if not all_data:
            return pd.DataFrame()
        
        # Converte lista de dicts em DataFrame
        df = pd.DataFrame(all_data)
        
        # Adiciona informações de processamento
        df['_arquivo_origem'] = df['_arquivo_origem'].astype(str)
        df['_data_processamento'] = pd.Timestamp.now()
        
        logger.info(f"DataFrame criado com {len(df)} registros e {len(df.columns)} colunas")
        return df
    
    def _parse_single_xml(self, filename: str, xml_content: bytes) -> Dict[str, Any]:
        """
        Faz parse de um único XML
        
        Args:
            filename: Nome do arquivo
            xml_content: Conteúdo do XML em bytes
            
        Returns:
            Dicionário com dados extraídos
        """
        try:
            # Converte bytes para string
            xml_string = xml_content.decode('utf-8', errors='ignore')
            
            # Parse XML para dicionário
            xml_dict = xmltodict.parse(xml_string)
            
            # Extrai dados baseado no mapeamento de campos
            extracted_data = self._extract_fields(xml_dict)
            
            # Adiciona metadados
            extracted_data['_arquivo_origem'] = filename
            
            return extracted_data
        
        except Exception as e:
            logger.error(f"Erro ao parsear {filename}: {e}")
            return None
    
    def _extract_fields(self, xml_dict: Dict) -> Dict[str, Any]:
        """
        Extrai campos específicos do XML baseado no mapeamento
        
        Args:
            xml_dict: Dicionário convertido do XML
            
        Returns:
            Dicionário com campos extraídos
        """
        data = {}
        
        # Para cada campo no mapeamento, tenta encontrar o valor
        for field_name, possible_paths in self.field_mapping.items():
            value = None
            
            # Tenta cada path possível até encontrar um valor
            for path in possible_paths:
                value = get_nested_value(xml_dict, path)
                if value is not None:
                    break
            
            # Processa o valor encontrado
            if value is not None:
                # Converte valores monetários
                if 'valor' in field_name.lower() or 'total' in field_name.lower():
                    value = safe_float(value)
                
                # Converte datas
                elif 'data' in field_name.lower():
                    parsed_date = parse_date(str(value))
                    value = parsed_date if parsed_date else value
            
            data[field_name] = value
        
        return data
    
    def get_available_fields(self, sample_xml: bytes) -> List[str]:
        """
        Analisa um XML de amostra e retorna todos os campos disponíveis
        Útil para o usuário escolher quais campos incluir
        
        Args:
            sample_xml: Conteúdo de um XML de exemplo
            
        Returns:
            Lista de campos encontrados
        """
        try:
            xml_string = sample_xml.decode('utf-8', errors='ignore')
            xml_dict = xmltodict.parse(xml_string)
            
            # Extrai todas as chaves do XML (de forma recursiva)
            fields = self._get_all_keys(xml_dict)
            return sorted(list(set(fields)))
        
        except Exception as e:
            logger.error(f"Erro ao analisar campos disponíveis: {e}")
            return []
    
    def _get_all_keys(self, d: Any, parent_key: str = '', sep: str = '.') -> List[str]:
        """
        Extrai todas as chaves de um dicionário aninhado recursivamente
        
        Args:
            d: Dicionário a analisar
            parent_key: Chave pai (para recursão)
            sep: Separador de níveis
            
        Returns:
            Lista de chaves com caminho completo
        """
        keys = []
        
        if isinstance(d, dict):
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                keys.append(new_key)
                
                if isinstance(v, (dict, list)):
                    keys.extend(self._get_all_keys(v, new_key, sep))
        
        elif isinstance(d, list) and d:
            # Analisa primeiro item da lista
            keys.extend(self._get_all_keys(d[0], parent_key, sep))
        
        return keys