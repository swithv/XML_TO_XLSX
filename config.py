"""
Configurações e constantes do projeto
"""
import os
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# Configurações de upload
MAX_FILE_SIZE_MB = 200
ALLOWED_EXTENSIONS = ['.xml', '.zip']

# Mapeamento de campos XML padrão para NFe (Nota Fiscal Eletrônica)
# Ajuste conforme o tipo de XML que você trabalha
DEFAULT_XML_FIELDS = {
    'Número da Nota': ['nNF', 'numero', 'nfe.infNFe.ide.nNF'],
    'Data de Emissão': ['dhEmi', 'dataEmissao', 'nfe.infNFe.ide.dhEmi'],
    'CNPJ Emitente': ['emit.CNPJ', 'emitente.cnpj', 'nfe.infNFe.emit.CNPJ'],
    'Nome Emitente': ['emit.xNome', 'emitente.nome', 'nfe.infNFe.emit.xNome'],
    'CNPJ Destinatário': ['dest.CNPJ', 'destinatario.cnpj', 'nfe.infNFe.dest.CNPJ'],
    'Nome Destinatário': ['dest.xNome', 'destinatario.nome', 'nfe.infNFe.dest.xNome'],
    'Valor Total': ['vNF', 'valorTotal', 'nfe.infNFe.total.ICMSTot.vNF', 'total.ICMSTot.vNF'],
    'Valor Produtos': ['vProd', 'valorProdutos', 'nfe.infNFe.total.ICMSTot.vProd', 'total.ICMSTot.vProd'],
    'Chave NFe': ['chNFe', 'chave', 'nfe.infNFe.@Id', 'protNFe.infProt.chNFe'],
}

# Configurações de formatação Excel
EXCEL_CONFIG = {
    'header_style': {
        'font_bold': True,
        'bg_color': '#4472C4',
        'font_color': '#FFFFFF',
        'border': 1
    },
    'money_format': 'R$ #,##0.00',
    'date_format': 'DD/MM/YYYY HH:MM:SS',
    'column_width': 20
}

# Configurações do Dashboard
DASHBOARD_CONFIG = {
    'chart_height': 400,
    'chart_template': 'plotly_white',
    'currency_symbol': 'R$'
}

# Mensagens do sistema
MESSAGES = {
    'upload_success': '✅ Arquivos carregados com sucesso!',
    'upload_error': '❌ Erro ao carregar arquivos.',
    'processing': '⏳ Processando arquivos...',
    'export_success': '✅ Excel gerado com sucesso!',
    'no_files': '⚠️ Nenhum arquivo foi carregado.',
    'invalid_xml': '⚠️ XML inválido ou mal formatado.'
}