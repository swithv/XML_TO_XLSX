"""
Funções auxiliares diversas
"""
import re
from datetime import datetime
from typing import Any, Dict, List

def clean_filename(filename: str) -> str:
    """
    Remove caracteres especiais de nomes de arquivos
    
    Args:
        filename: Nome do arquivo
        
    Returns:
        Nome limpo
    """
    # Remove caracteres especiais, mantém apenas alfanuméricos, ponto e hífen
    clean = re.sub(r'[^\w\s\-.]', '', filename)
    clean = re.sub(r'\s+', '_', clean)
    return clean

def format_currency(value: float, currency: str = "R$") -> str:
    """
    Formata valor como moeda
    
    Args:
        value: Valor numérico
        currency: Símbolo da moeda
        
    Returns:
        String formatada
    """
    try:
        return f"{currency} {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return f"{currency} 0,00"

def parse_date(date_string: str) -> datetime:
    """
    Converte string em datetime, tentando múltiplos formatos
    
    Args:
        date_string: String com data
        
    Returns:
        Objeto datetime ou None se falhar
    """
    formats = [
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%Y-%m-%d',
        '%d/%m/%Y'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except:
            continue
    
    return None

def get_nested_value(data: Dict, key_path: str, default: Any = None) -> Any:
    """
    Busca valor em dicionário aninhado usando notação de ponto
    Exemplo: 'emit.CNPJ' busca data['emit']['CNPJ']
    
    Args:
        data: Dicionário para buscar
        key_path: Caminho das chaves separado por ponto
        default: Valor padrão se não encontrar
        
    Returns:
        Valor encontrado ou default
    """
    keys = key_path.split('.')
    value = data
    
    try:
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    except:
        return default

def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Converte valor para float de forma segura
    
    Args:
        value: Valor a converter
        default: Valor padrão se falhar
        
    Returns:
        Float convertido
    """
    try:
        if isinstance(value, str):
            # Remove pontos de milhares e substitui vírgula por ponto
            value = value.replace('.', '').replace(',', '.')
        return float(value)
    except:
        return default

def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Trunca texto adicionando reticências
    
    Args:
        text: Texto a truncar
        max_length: Comprimento máximo
        
    Returns:
        Texto truncado
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."