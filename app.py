"""
Aplicação Principal - Conversor XML para XLSX
Escritório de Contabilidade - Versão Corrigida
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        font-size: 16px;
        font-weight: 600;
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
    if 'show_debug' not in st.session_state:
        st.session_state.show_debug = False

def main():
    """Função principal da aplicação"""
    
    # Inicializa estado
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📊 Conversor XML → XLSX</h1>', unsafe_allow_html=True)
    st.markdown("**Sistema profissional para conversão de Notas Fiscais Eletrônicas**")
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ Sobre o Sistema")
        st.info("""
        **Formatos aceitos:**
        - Arquivos XML individuais
        - Arquivos ZIP com múltiplos XMLs
        
        **Tamanho máximo:** 200 MB por arquivo
        """)
        
        st.divider()
        
        st.subheader("📖 Como usar")
        st.markdown("""
        1. Faça upload dos arquivos XML
        2. Escolha as colunas desejadas
        3. Configure o processamento
        4. Clique em "Processar"
        5. Baixe o Excel formatado
        """)
        
        st.divider()
        
        # Opção de debug
        st.session_state.show_debug = st.checkbox(
            "🐛 Modo Debug", 
            value=st.session_state.show_debug,
            help="Mostra informações detalhadas sobre o processamento"
        )
    
    # ABAS PRINCIPAIS
    tab_conversion, tab_dashboard = st.tabs(["📤 Conversão", "📊 Dashboard"])
    
    # ============= ABA 1: CONVERSÃO =============
    with tab_conversion:
        show_conversion_tab()
    
    # ============= ABA 2: DASHBOARD =============
    with tab_dashboard:
        show_dashboard_tab()

def show_conversion_tab():
    """Exibe a aba de conversão"""
    
    st.header("Upload e Configuração")
    
    # Upload de arquivos
    uploaded_files = st.file_uploader(
        "Arraste seus arquivos XML ou ZIP aqui",
        type=['xml', 'zip'],
        accept_multiple_files=True,
        help="Você pode enviar múltiplos arquivos de uma vez"
    )
    
    if not uploaded_files:
        st.info("👆 Faça upload dos arquivos XML para começar")
        return
    
    # Valida arquivos
    is_valid, errors = validate_uploaded_files(uploaded_files)
    
    if not is_valid:
        for error in errors:
            st.error(error)
        return
    
    st.success(f"✅ {len(uploaded_files)} arquivo(s) carregado(s)")
    
    st.divider()
    
    # Configurações com DROPDOWNS
    col_settings, col_columns = st.columns([1, 2])
    
    with col_settings:
        st.subheader("⚙️ Opções de Processamento")
        
        # Dropdown para remoção de duplicatas
        remove_duplicates = st.selectbox(
            "🗑️ Remover duplicatas?",
            options=["Não", "Sim"],
            index=0,
            help="Remove registros idênticos do resultado"
        )
        remove_duplicates = (remove_duplicates == "Sim")
        
        # Dropdown para aba de resumo
        include_summary = st.selectbox(
            "📊 Incluir aba de resumo?",
            options=["Sim", "Não"],
            index=0,
            help="Adiciona uma aba com estatísticas no Excel"
        )
        include_summary = (include_summary == "Sim")
        
        # Dropdown para formatação de datas
        format_dates = st.selectbox(
            "📅 Formatar datas?",
            options=["Sim", "Não"],
            index=0,
            help="Converte datas para formato brasileiro"
        )
        format_dates = (format_dates == "Sim")
        
        # Dropdown para formatação de valores
        format_currency = st.selectbox(
            "💰 Formatar valores monetários?",
            options=["Sim", "Não"],
            index=0,
            help="Formata valores como moeda brasileira"
        )
        format_currency = (format_currency == "Sim")
    
    with col_columns:
        st.subheader("📋 Selecione as Colunas para Exportar")
        st.caption("Marque apenas os campos que você precisa no Excel")
        
        # Colunas disponíveis
        available_fields = list(config.DEFAULT_XML_FIELDS.keys())
        
        # Opção de selecionar/desselecionar tudo
        col_all1, col_all2 = st.columns(2)
        with col_all1:
            select_all = st.button("✅ Selecionar Tudo", use_container_width=True)
        with col_all2:
            deselect_all = st.button("❌ Desmarcar Tudo", use_container_width=True)
        
        # Inicializa seleção no session_state
        if 'selected_fields' not in st.session_state:
            st.session_state.selected_fields = available_fields.copy()
        
        # Atualiza seleção baseado nos botões
        if select_all:
            st.session_state.selected_fields = available_fields.copy()
        if deselect_all:
            st.session_state.selected_fields = []
        
        # Organiza em 3 colunas
        cols = st.columns(3)
        selected_columns = []
        
        for idx, field in enumerate(available_fields):
            col_idx = idx % 3
            with cols[col_idx]:
                is_selected = field in st.session_state.selected_fields
                if st.checkbox(field, value=is_selected, key=f"col_{field}"):
                    selected_columns.append(field)
        
        # Atualiza session_state
        st.session_state.selected_fields = selected_columns
        
        if not selected_columns:
            st.warning("⚠️ Selecione pelo menos uma coluna para continuar")
    
    st.divider()
    
    # Botão de processamento
    col_btn1, col_btn2 = st.columns([3, 1])
    
    with col_btn1:
        if selected_columns:
            if st.button("🚀 Processar Arquivos", type="primary", use_container_width=True):
                process_files(
                    uploaded_files, 
                    selected_columns, 
                    remove_duplicates,
                    format_dates, 
                    format_currency, 
                    include_summary
                )
        else:
            st.button("🚀 Processar Arquivos", disabled=True, use_container_width=True)
    
    with col_btn2:
        st.caption("👈 Configure e processe")
    
    st.divider()
    
    # ÁREA DE DOWNLOAD DO EXCEL (aparece após processamento)
    if st.session_state.processing_complete and st.session_state.df_processed is not None:
        st.success("✅ Processamento concluído! Arquivo pronto para download.")
        
        st.subheader("💾 Baixar Resultado")
        
        col_file, col_down = st.columns([2, 1])
        
        with col_file:
            filename = st.text_input(
                "Nome do arquivo Excel:",
                value=f"notas_fiscais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                key="export_filename"
            )
        
        with col_down:
            st.write("")
            st.write("")
            # Remove colunas de metadados
            df_export = st.session_state.df_processed.copy()
            df_export = df_export[[col for col in df_export.columns if not col.startswith('_')]]
            
            # Gera Excel
            exporter = ExcelExporter()
            include_sum = st.session_state.get('include_summary', True)
            
            if include_sum:
                excel_buffer = exporter.export_with_summary(df_export)
            else:
                excel_buffer = exporter.export_to_excel(df_export, filename)
            
            if excel_buffer:
                st.download_button(
                    label="📥 Baixar Excel",
                    data=excel_buffer,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )

def show_dashboard_tab():
    """Exibe a aba de dashboard"""
    
    if not st.session_state.processing_complete or st.session_state.df_processed is None:
        st.info("📊 Faça o processamento na aba **Conversão** para visualizar o dashboard")
        return
    
    df = st.session_state.df_processed
    
    # Filtra colunas de metadados
    display_df = df[[col for col in df.columns if not col.startswith('_')]].copy()
    
    st.header("📊 Dashboard de Análise")
    
    # Métricas principais
    st.subheader("Estatísticas Gerais")
    dashboard = DashboardBuilder()
    dashboard.display_metrics(display_df)
    
    st.divider()
    
    # Preview da tabela
    st.subheader("📋 Preview dos Dados")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Registros", len(display_df))
    with col2:
        st.metric("Colunas", len(display_df.columns))
    with col3:
        memory_mb = display_df.memory_usage(deep=True).sum() / (1024**2)
        st.metric("Tamanho", f"{memory_mb:.2f} MB")
    
    # Controle de visualização
    show_all = st.checkbox("Mostrar todas as linhas", value=False)
    max_rows = len(display_df) if show_all else min(100, len(display_df))
    
    st.dataframe(
        display_df.head(max_rows),
        use_container_width=True,
        height=400
    )
    
    if not show_all and len(display_df) > 100:
        st.caption(f"Mostrando 100 de {len(display_df)} linhas. Marque a opção acima para ver tudo.")
    
    st.divider()
    
    # Gráficos
    if len(display_df) > 1:
        st.subheader("📈 Visualizações")
        
        graph_tab1, graph_tab2, graph_tab3 = st.tabs([
            "📈 Evolução Temporal", 
            "🏆 Top Emitentes", 
            "📊 Distribuição"
        ])
        
        with graph_tab1:
            fig = dashboard.create_value_chart(display_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Para ver este gráfico, inclua colunas de **Data** e **Valor** na conversão.")
        
        with graph_tab2:
            fig = dashboard.create_top_emitters_chart(display_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Para ver este gráfico, inclua a coluna **Nome Emitente** na conversão.")
        
        with graph_tab3:
            fig = dashboard.create_distribution_chart(display_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Para ver este gráfico, inclua colunas de **Valor** na conversão.")

def process_files(uploaded_files, selected_columns, remove_duplicates, 
                 format_dates, format_currency, include_summary):
    """Processa os arquivos enviados"""
    
    try:
        progress_container = st.container()
        
        with progress_container:
            with st.spinner("⏳ Processando arquivos..."):
                progress_bar = st.progress(0, text="Iniciando...")
                
                # 1. Upload e extração
                progress_bar.progress(10, text="📦 Extraindo arquivos...")
                upload_handler = UploadHandler()
                xml_files, errors = upload_handler.process_uploads(uploaded_files)
                
                if errors:
                    for error in errors:
                        st.warning(error)
                
                if not xml_files:
                    st.error("❌ Nenhum arquivo XML válido encontrado!")
                    return
                
                st.session_state.xml_files = xml_files
                
                # 2. Parse XML
                progress_bar.progress(30, text="🔄 Convertendo XMLs...")
                parser = XMLParser()
                df = parser.parse_multiple_xmls(xml_files)
                
                if df.empty:
                    st.error("❌ Erro ao processar XMLs. Verifique o formato dos arquivos.")
                    
                    # Modo debug
                    if st.session_state.show_debug:
                        st.warning("🐛 **Modo Debug Ativado**")
                        st.write("Tentando analisar o primeiro XML...")
                        
                        if xml_files:
                            sample_fields = parser.get_available_fields(xml_files[0][1])
                            st.write("**Campos disponíveis no XML:**")
                            st.code("\n".join(sample_fields[:50]))
                    
                    return
                
                # 3. Substituir valores None por strings vazias ou zeros
                progress_bar.progress(45, text="🧹 Limpando dados...")
                for col in df.columns:
                    df[col] = df[col].replace(['None', 'none', None], '')
                
                # 4. Filtrar colunas
                progress_bar.progress(50, text="🔍 Filtrando colunas...")
                available_cols = [col for col in selected_columns if col in df.columns]
                
                if not available_cols:
                    st.error(f"❌ Nenhuma das colunas selecionadas foi encontrada!")
                    
                    if st.session_state.show_debug:
                        st.write("**Colunas esperadas:**", selected_columns)
                        st.write("**Colunas encontradas:**", list(df.columns))
                    
                    return
                
                # Mantém colunas selecionadas + metadados
                metadata_cols = [col for col in df.columns if col.startswith('_')]
                df = df[available_cols + metadata_cols]
                
                # 5. Remover duplicatas
                if remove_duplicates:
                    progress_bar.progress(60, text="🗑️ Removendo duplicatas...")
                    filter_handler = DataFilter()
                    original_len = len(df)
                    df = filter_handler.remove_duplicates(df)
                    removed = original_len - len(df)
                    if removed > 0:
                        st.info(f"🗑️ Removidas {removed} linha(s) duplicada(s)")
                
                # 6. Formatar dados
                progress_bar.progress(75, text="✨ Formatando dados...")
                
                formatter = DataFormatter()
                
                if format_dates or format_currency:
                    df = formatter.format_dataframe(df)
                
                # Preenche valores faltantes
                df = formatter.fill_missing_values(df, strategy='empty')
                
                # 7. Validação final - remove None restantes
                progress_bar.progress(90, text="✅ Finalizando...")
                df = df.fillna('')
                
                # Garante que colunas de valor são numéricas
                for col in df.columns:
                    if any(keyword in col.lower() for keyword in ['valor', 'total', 'preco', 'custo']):
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
                # 8. Finalizar
                progress_bar.progress(100, text="✅ Concluído!")
                
                st.session_state.df_processed = df
                st.session_state.processing_complete = True
                st.session_state.include_summary = include_summary
                
                logger.info(f"Processamento OK: {len(df)} registros, {len(available_cols)} colunas")
                
                st.success(f"""
                ✅ **Processamento Concluído com Sucesso!**
                
                📊 **Estatísticas:**
                - {len(df)} registros processados
                - {len(available_cols)} coluna(s) extraída(s)
                - {len(xml_files)} arquivo(s) XML processado(s)
                
                💡 **Próximos passos:**
                - Role para baixo para **baixar o Excel**
                - Ou acesse a aba **Dashboard** para visualizar gráficos
                """)
                
                # Debug info
                if st.session_state.show_debug:
                    with st.expander("🐛 Informações de Debug"):
                        st.write("**Colunas extraídas:**", available_cols)
                        st.write("**Tipos de dados:**")
                        st.write(df.dtypes)
                        st.write("**Amostra dos dados (primeiras 3 linhas):**")
                        st.dataframe(df.head(3))
                        st.write("**Valores únicos por coluna:**")
                        for col in df.columns[:5]:
                            st.write(f"- {col}: {df[col].nunique()} valores únicos")
    
    except Exception as e:
        st.error(f"❌ Erro durante o processamento: {str(e)}")
        logger.error(f"Erro no processamento: {e}")
        
        if st.session_state.show_debug:
            st.exception(e)

# Ponto de entrada da aplicação
if __name__ == "__main__":
    main()