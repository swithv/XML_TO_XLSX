"""
Módulo responsável pela construção do dashboard interativo
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from typing import Dict, Any
import config
from utils.logger import logger
from utils.helpers import format_currency

class DashboardBuilder:
    """Constrói visualizações e métricas do dashboard"""
    
    def __init__(self):
        self.config = config.DASHBOARD_CONFIG
    
    def display_metrics(self, df: pd.DataFrame):
        """
        Exibe métricas principais em cards
        
        Args:
            df: DataFrame com os dados
        """
        if df.empty:
            st.warning("Nenhum dado disponível para exibir métricas")
            return
        
        # Identifica colunas de valor e data
        value_columns = self._get_monetary_columns(df)
        date_columns = self._get_date_columns(df)
        
        # Cria colunas para os cards
        cols = st.columns(4)
        
        # Métrica 1: Total de registros
        with cols[0]:
            st.metric(
                label="📊 Total de Notas",
                value=f"{len(df):,}".replace(",", ".")
            )
        
        # Métrica 2: Valor total (primeira coluna monetária encontrada)
        if value_columns:
            total_value = df[value_columns[0]].sum()
            with cols[1]:
                st.metric(
                    label=f"💰 {value_columns[0]}",
                    value=format_currency(total_value)
                )
        
        # Métrica 3: Valor médio
        if value_columns:
            avg_value = df[value_columns[0]].mean()
            with cols[2]:
                st.metric(
                    label="📈 Valor Médio",
                    value=format_currency(avg_value)
                )
        
        # Métrica 4: Período (se houver data)
        if date_columns:
            date_col = date_columns[0]
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            min_date = df[date_col].min()
            max_date = df[date_col].max()
            
            with cols[3]:
                st.metric(
                    label="📅 Período",
                    value=f"{min_date.strftime('%d/%m/%Y') if pd.notna(min_date) else 'N/A'}"
                )
                if pd.notna(max_date):
                    st.caption(f"até {max_date.strftime('%d/%m/%Y')}")
    
    def create_value_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de valores ao longo do tempo
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Figura do Plotly
        """
        value_columns = self._get_monetary_columns(df)
        date_columns = self._get_date_columns(df)
        
        if not value_columns or not date_columns:
            return None
        
        try:
            # Prepara dados
            plot_df = df.copy()
            date_col = date_columns[0]
            value_col = value_columns[0]
            
            # Converte data
            plot_df[date_col] = pd.to_datetime(plot_df[date_col], errors='coerce')
            plot_df = plot_df.dropna(subset=[date_col])
            
            # Agrupa por data
            daily_data = plot_df.groupby(plot_df[date_col].dt.date)[value_col].sum().reset_index()
            daily_data.columns = ['Data', 'Valor']
            
            # Cria gráfico
            fig = px.line(
                daily_data,
                x='Data',
                y='Valor',
                title=f'Evolução de {value_col}',
                labels={'Data': 'Data', 'Valor': 'Valor (R$)'},
                template=self.config['chart_template']
            )
            
            fig.update_traces(line_color='#4472C4', line_width=3)
            fig.update_layout(
                height=self.config['chart_height'],
                hovermode='x unified'
            )
            
            return fig
        
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de valores: {e}")
            return None
    
    def create_top_emitters_chart(self, df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Cria gráfico dos principais emitentes
        
        Args:
            df: DataFrame com os dados
            top_n: Número de emitentes a mostrar
            
        Returns:
            Figura do Plotly
        """
        # Busca coluna de emitente
        emitter_col = None
        for col in df.columns:
            if 'emitente' in col.lower() or 'nome' in col.lower():
                emitter_col = col
                break
        
        if not emitter_col:
            return None
        
        value_columns = self._get_monetary_columns(df)
        if not value_columns:
            # Se não há valor, conta quantidade
            top_emitters = df[emitter_col].value_counts().head(top_n)
            
            fig = px.bar(
                x=top_emitters.values,
                y=top_emitters.index,
                orientation='h',
                title=f'Top {top_n} Emitentes (por quantidade)',
                labels={'x': 'Quantidade', 'y': 'Emitente'},
                template=self.config['chart_template']
            )
        else:
            # Agrupa por emitente e soma valores
            value_col = value_columns[0]
            top_emitters = df.groupby(emitter_col)[value_col].sum().sort_values(ascending=False).head(top_n)
            
            fig = px.bar(
                x=top_emitters.values,
                y=top_emitters.index,
                orientation='h',
                title=f'Top {top_n} Emitentes (por valor)',
                labels={'x': 'Valor (R$)', 'y': 'Emitente'},
                template=self.config['chart_template']
            )
        
        fig.update_traces(marker_color='#4472C4')
        fig.update_layout(height=self.config['chart_height'])
        
        return fig
    
    def create_distribution_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de distribuição de valores
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Figura do Plotly
        """
        value_columns = self._get_monetary_columns(df)
        
        if not value_columns:
            return None
        
        try:
            value_col = value_columns[0]
            
            fig = px.histogram(
                df,
                x=value_col,
                nbins=30,
                title=f'Distribuição de {value_col}',
                labels={value_col: 'Valor (R$)', 'count': 'Frequência'},
                template=self.config['chart_template']
            )
            
            fig.update_traces(marker_color='#4472C4')
            fig.update_layout(height=self.config['chart_height'])
            
            return fig
        
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de distribuição: {e}")
            return None
    
    def display_data_table(self, df: pd.DataFrame, max_rows: int = 100):
        """
        Exibe tabela de dados com paginação
        
        Args:
            df: DataFrame a exibir
            max_rows: Número máximo de linhas a mostrar
        """
        if df.empty:
            st.info("Nenhum dado para exibir")
            return
        
        st.subheader("📋 Visualização dos Dados")
        
        # Mostra informações da tabela
        st.caption(f"Exibindo {min(len(df), max_rows)} de {len(df)} registros")
        
        # Exibe tabela
        display_df = df.head(max_rows)
        st.dataframe(display_df, use_container_width=True, height=400)
    
    def create_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Cria estatísticas resumidas do DataFrame
        
        Args:
            df: DataFrame
            
        Returns:
            Dicionário com estatísticas
        """
        stats = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        
        # Estatísticas de valores
        value_columns = self._get_monetary_columns(df)
        if value_columns:
            for col in value_columns:
                stats[f'{col}_total'] = df[col].sum()
                stats[f'{col}_mean'] = df[col].mean()
                stats[f'{col}_min'] = df[col].min()
                stats[f'{col}_max'] = df[col].max()
        
        return stats
    
    def _get_monetary_columns(self, df: pd.DataFrame) -> list:
        """Retorna lista de colunas monetárias"""
        monetary_keywords = ['valor', 'total', 'preco', 'preço', 'custo']
        columns = []
        
        for col in df.columns:
            if any(keyword in col.lower() for keyword in monetary_keywords):
                if pd.api.types.is_numeric_dtype(df[col]):
                    columns.append(col)
        
        return columns
    
    def _get_date_columns(self, df: pd.DataFrame) -> list:
        """Retorna lista de colunas de data"""
        date_columns = []
        
        for col in df.columns:
            if 'data' in col.lower() or pd.api.types.is_datetime64_any_dtype(df[col]):
                date_columns.append(col)
        
        return date_columns