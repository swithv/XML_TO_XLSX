"""
Aplicação Principal - Conversor XML para XLSX
Escritório de Contabilidade
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import config
from modules.upload_handler import UploadHandler
from modules.xml_parser import XMLParser
from modules.data_filter import DataFilter
from modules.data_formatter import DataFormatter
from modules.excel_exporter import ExcelExporter
from modules.dashboard_builder import DashboardBuilder
from utils.logger import logger
from utils.validators import validate_uploaded_files

# Configuração da página
st.set_page_config(
    page_title="Conversor XML → XLSX",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhor aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4472C4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Inicializa variáveis de sessão"""
    if 'df_processed' not in st.session_state:
        st.session_state.df_processed = None
    if 'xml_files' not in st.session_state:
        st.session_state.xml_files = []
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False

def main():
    """Função principal da aplicação"""
    
    # Inicializa estado
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📊 Conversor XML → XLSX</h1>', unsafe_allow_html=True)
    st.markdown("**Sistema profissional para conversão de Notas Fiscais Eletrônicas**")
    st.divider()
    
    # Sidebar com configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Opções de processamento
        st.subheader("Processamento")
        remove_duplicates = st.checkbox("Remover duplicatas", value=False)
        include_summary = st.checkbox("Incluir aba de resumo no Excel", value=True)
        
        st.divider()
        
        # Filtros opcionais
        st.subheader("Filtros (Opcional)")
        enable_filters = st.checkbox("Ativar filtros", value=False)
        
        filter_start_date = None
        filter_end_date = None
        filter_min_value = None
        filter_max_value = None
        
        if enable_filters:
            st.caption("Filtro por Data")
            col1, col2 = st.columns(2)
            with col1:
                filter_start_date = st.date_input("De:", value=None)
            with col2:
                filter_end_date = st.date_input("Até:", value=None)
            
            st.caption("Filtro por Valor")
            col3, col4 = st.columns(2)
            with col3:
                filter_min_value = st.number_input("Mín:", value=0.0, step=100.0)
            with col4:
                filter_max_value = st.number_input("Máx:", value=0.0, step=100.0)
        
        st.divider()
        
        # Informações
        st.subheader("ℹ️ Sobre")
        st.info("""
        **Formatos aceitos:**
        - Arquivos XML individuais
        - Arquivos ZIP com múltiplos XMLs
        
        **Tamanho máximo:** 200 MB
        """)
    
    # Área principal - Upload
    st.header("1️⃣ Upload de Arquivos")
    
    uploaded_files = st.file_uploader(
        "Arraste seus arquivos XML ou ZIP aqui",
        type=['xml', 'zip'],
        accept_multiple_files=True,
        help="Você pode enviar múltiplos arquivos de uma vez"
    )
    
    # Processa upload
    if uploaded_files:
        # Valida arquivos
        is_valid, errors = validate_uploaded_files(uploaded_files)
        
        if not is_valid:
            for error in errors:
                st.error(error)
            return
        
        # Botão de processamento
        if st.button("🚀 Processar Arquivos", type="primary", use_container_width=True):
            process_files(uploaded_files, remove_duplicates, enable_filters,
                         filter_start_date, filter_end_date, 
                         filter_min_value, filter_max_value)
    
    # Exibe resultados se processamento completo
    if st.session_state.processing_complete and st.session_state.df_processed is not None:
        display_results(include_summary)

def process_files(uploaded_files, remove_duplicates, enable_filters,
                 start_date, end_date, min_value, max_value):
    """
    Processa os arquivos enviados
    
    Args:
        uploaded_files: Arquivos do upload
        remove_duplicates: Se deve remover duplicatas
        enable_filters: Se filtros estão ativados
        start_date, end_date: Filtros de data
        min_value, max_value: Filtros de valor
    """
    try:
        with st.spinner("⏳ Processando arquivos..."):
            # 1. Upload e extração
            progress_bar = st.progress(0, text="Extraindo arquivos...")
            upload_handler = UploadHandler()
            xml_files, errors = upload_handler.process_uploads(uploaded_files)
            
            if errors:
                for error in errors:
                    st.warning(error)
            
            if not xml_files:
                st.error("Nenhum arquivo XML válido encontrado!")
                return
            
            st.session_state.xml_files = xml_files
            st.success(f"✅ {len(xml_files)} arquivo(s) XML carregado(s)")
            
            # 2. Parse XML → DataFrame
            progress_bar.progress(25, text="Convertendo XMLs...")
            parser = XMLParser()
            df = parser.parse_multiple_xmls(xml_files)
            
            if df.empty:
                st.error("Erro ao processar XMLs. Verifique o formato dos arquivos.")
                return
            
            # 3. Filtros
            progress_bar.progress(50, text="Aplicando filtros...")
            if enable_filters:
                filter_handler = DataFilter()
                
                # Filtra por data
                if start_date or end_date:
                    date_columns = [col for col in df.columns if 'data' in col.lower()]
                    if date_columns:
                        df = filter_handler.filter_by_date_range(
                            df, date_columns[0], start_date, end_date
                        )
                
                # Filtra por valor
                if min_value or max_value:
                    value_columns = [col for col in df.columns if 'valor' in col.lower()]
                    if value_columns:
                        df = filter_handler.filter_by_value_range(
                            df, value_columns[0], min_value if min_value > 0 else None,
                            max_value if max_value > 0 else None
                        )
                
                # Remove duplicatas
                if remove_duplicates:
                    df = filter_handler.remove_duplicates(df)
            
            # 4. Formatação
            progress_bar.progress(75, text="Formatando dados...")
            formatter = DataFormatter()
            df = formatter.format_dataframe(df)
            df = formatter.fill_missing_values(df, strategy='empty')
            
            # 5. Finalização
            progress_bar.progress(100, text="Concluído!")
            
            # Salva no estado
            st.session_state.df_processed = df
            st.session_state.processing_complete = True
            
            logger.info(f"Processamento concluído: {len(df)} registros")
            st.success(f"✅ Processamento concluído! {len(df)} registros prontos.")
            st.rerun()
    
    except Exception as e:
        st.error(f"❌ Erro durante o processamento: {str(e)}")
        logger.error(f"Erro no processamento: {e}")

def display_results(include_summary):
    """
    Exibe resultados e dashboard
    
    Args:
        include_summary: Se deve incluir aba de resumo no Excel
    """
    df = st.session_state.df_processed
    
    st.divider()
    st.header("2️⃣ Resultados")
    
    # Dashboard com métricas
    dashboard = DashboardBuilder()
    dashboard.display_metrics(df)
    
    st.divider()
    
    # Gráficos em abas
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Evolução", "🏆 Top Emitentes", "📊 Distribuição", "📋 Dados"])
    
    with tab1:
        fig_evolution = dashboard.create_value_chart(df)
        if fig_evolution:
            st.plotly_chart(fig_evolution, use_container_width=True)
        else:
            st.info("Gráfico de evolução não disponível (dados insuficientes)")
    
    with tab2:
        fig_top = dashboard.create_top_emitters_chart(df)
        if fig_top:
            st.plotly_chart(fig_top, use_container_width=True)
        else:
            st.info("Gráfico de emitentes não disponível (dados insuficientes)")
    
    with tab3:
        fig_dist = dashboard.create_distribution_chart(df)
        if fig_dist:
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            st.info("Gráfico de distribuição não disponível (dados insuficientes)")
    
    with tab4:
        dashboard.display_data_table(df, max_rows=200)
    
    st.divider()
    
    # Exportação
    st.header("3️⃣ Exportar para Excel")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        filename = st.text_input(
            "Nome do arquivo:",
            value=f"notas_fiscais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("📥 Baixar Excel", type="primary", use_container_width=True):
            export_excel(df, filename, include_summary)
    
    with col3:
        st.write("")
        st.write("")
        if st.button("🔄 Nova Conversão", use_container_width=True):
            reset_app()

def export_excel(df, filename, include_summary):
    """
    Exporta DataFrame para Excel
    
    Args:
        df: DataFrame a exportar
        filename: Nome do arquivo
        include_summary: Se deve incluir resumo
    """
    try:
        with st.spinner("Gerando Excel..."):
            exporter = ExcelExporter()
            
            if include_summary:
                excel_buffer = exporter.export_with_summary(df)
            else:
                excel_buffer = exporter.export_to_excel(df, filename)
            
            if excel_buffer:
                st.download_button(
                    label="📥 Clique para baixar",
                    data=excel_buffer,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                st.success("✅ Excel gerado com sucesso!")
            else:
                st.error("❌ Erro ao gerar Excel")
    
    except Exception as e:
        st.error(f"❌ Erro ao exportar: {str(e)}")
        logger.error(f"Erro na exportação: {e}")

def reset_app():
    """Reseta a aplicação para nova conversão"""
    st.session_state.df_processed = None
    st.session_state.xml_files = []
    st.session_state.processing_complete = False
    st.rerun()

# Ponto de entrada
if __name__ == "__main__":
    main()