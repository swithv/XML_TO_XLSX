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
# Caminhos expandidos para maior compatibilidade
DEFAULT_XML_FIELDS = {
    'Número da Nota': [
        'nfeProc.NFe.infNFe.ide.nNF',
        'NFe.infNFe.ide.nNF',
        'nfe.infNFe.ide.nNF',
        'infNFe.ide.nNF',
        'ide.nNF',
        'nNF',
        'numero'
    ],
    'Data de Emissão': [
        'nfeProc.NFe.infNFe.ide.dhEmi',
        'NFe.infNFe.ide.dhEmi',
        'nfe.infNFe.ide.dhEmi',
        'infNFe.ide.dhEmi',
        'ide.dhEmi',
        'ide.dEmi',
        'dhEmi',
        'dEmi',
        'dataEmissao'
    ],
    'CNPJ Emitente': [
        'nfeProc.NFe.infNFe.emit.CNPJ',
        'NFe.infNFe.emit.CNPJ',
        'nfe.infNFe.emit.CNPJ',
        'infNFe.emit.CNPJ',
        'emit.CNPJ',
        'emitente.CNPJ',
        'emitente.cnpj'
    ],
    'Nome Emitente': [
        'nfeProc.NFe.infNFe.emit.xNome',
        'NFe.infNFe.emit.xNome',
        'nfe.infNFe.emit.xNome',
        'infNFe.emit.xNome',
        'emit.xNome',
        'emitente.xNome',
        'emitente.nome'
    ],
    'CNPJ Destinatário': [
        'nfeProc.NFe.infNFe.dest.CNPJ',
        'NFe.infNFe.dest.CNPJ',
        'nfe.infNFe.dest.CNPJ',
        'infNFe.dest.CNPJ',
        'dest.CNPJ',
        'destinatario.CNPJ',
        'destinatario.cnpj'
    ],
    'Nome Destinatário': [
        'nfeProc.NFe.infNFe.dest.xNome',
        'NFe.infNFe.dest.xNome',
        'nfe.infNFe.dest.xNome',
        'infNFe.dest.xNome',
        'dest.xNome',
        'destinatario.xNome',
        'destinatario.nome'
    ],
    'Valor Total': [
        'nfeProc.NFe.infNFe.total.ICMSTot.vNF',
        'NFe.infNFe.total.ICMSTot.vNF',
        'nfe.infNFe.total.ICMSTot.vNF',
        'infNFe.total.ICMSTot.vNF',
        'total.ICMSTot.vNF',
        'ICMSTot.vNF',
        'vNF',
        'valorTotal',
        'valorNF'
    ],
    'Valor Produtos': [
        'nfeProc.NFe.infNFe.total.ICMSTot.vProd',
        'NFe.infNFe.total.ICMSTot.vProd',
        'nfe.infNFe.total.ICMSTot.vProd',
        'infNFe.total.ICMSTot.vProd',
        'total.ICMSTot.vProd',
        'ICMSTot.vProd',
        'vProd',
        'valorProdutos'
    ],
    'Chave NFe': [
        'nfeProc.protNFe.infProt.chNFe',
        'protNFe.infProt.chNFe',
        'nfeProc.NFe.infNFe.@Id',
        'NFe.infNFe.@Id',
        'nfe.infNFe.@Id',
        'infNFe.@Id',
        'chNFe',
        'chave'
    ],
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