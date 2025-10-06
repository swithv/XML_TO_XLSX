"""
Sistema de logging para rastreamento e debugging
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(name: str = "xml_converter") -> logging.Logger:
    """
    Configura e retorna um logger personalizado
    
    Args:
        name: Nome do logger
        
    Returns:
        Instância do logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evita duplicação de handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formato personalizado
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

# Instância global do logger
logger = setup_logger()

def log_operation(operation: str, details: str = ""):
    """
    Registra uma operação no log
    
    Args:
        operation: Nome da operação
        details: Detalhes adicionais
    """
    logger.info(f"{operation} {details}")

def log_error(error: Exception, context: str = ""):
    """
    Registra um erro no log
    
    Args:
        error: Exceção capturada
        context: Contexto do erro
    """
    logger.error(f"{context} | Erro: {str(error)}", exc_info=True)