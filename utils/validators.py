"""
Validadores de arquivos e dados
"""
import os
from pathlib import Path
from typing import List, Tuple
import config
from utils.logger import logger

def validate_file_extension(filename: str, allowed_extensions: List[str] = None) -> bool:
    """
    Valida se a extensão do arquivo é permitida
    
    Args:
        filename: Nome do arquivo
        allowed_extensions: Lista de extensões permitidas
        
    Returns:
        True se válido, False caso contrário
    """
    if allowed_extensions is None:
        allowed_extensions = config.ALLOWED_EXTENSIONS
    
    ext = Path(filename).suffix.lower()
    return ext in allowed_extensions

def validate_file_size(file_size: int, max_size_mb: int = None) -> bool:
    """
    Valida o tamanho do arquivo
    
    Args:
        file_size: Tamanho do arquivo em bytes
        max_size_mb: Tamanho máximo permitido em MB
        
    Returns:
        True se válido, False caso contrário
    """
    if max_size_mb is None:
        max_size_mb = config.MAX_FILE_SIZE_MB
    
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes

def validate_xml_content(xml_string: str) -> Tuple[bool, str]:
    """
    Valida se o conteúdo é um XML válido
    
    Args:
        xml_string: String contendo o XML
        
    Returns:
        Tupla (is_valid, error_message)
    """
    try:
        # Verifica se tem tag de abertura e fechamento
        if not xml_string.strip().startswith('<?xml') and not xml_string.strip().startswith('<'):
            return False, "Arquivo não parece ser um XML válido"
        
        # Tenta fazer parse básico
        import xml.etree.ElementTree as ET
        ET.fromstring(xml_string)
        return True, ""
    
    except ET.ParseError as e:
        return False, f"Erro de parse XML: {str(e)}"
    except Exception as e:
        return False, f"Erro ao validar XML: {str(e)}"

def validate_uploaded_files(uploaded_files) -> Tuple[bool, List[str]]:
    """
    Valida uma lista de arquivos enviados pelo Streamlit
    
    Args:
        uploaded_files: Lista de arquivos do st.file_uploader
        
    Returns:
        Tupla (all_valid, error_messages)
    """
    errors = []
    
    if not uploaded_files:
        return False, ["Nenhum arquivo foi enviado"]
    
    for file in uploaded_files:
        # Valida extensão
        if not validate_file_extension(file.name):
            errors.append(f"❌ {file.name}: extensão não permitida")
            continue
        
        # Valida tamanho
        if hasattr(file, 'size') and not validate_file_size(file.size):
            errors.append(f"❌ {file.name}: arquivo muito grande")
            continue
    
    return len(errors) == 0, errors