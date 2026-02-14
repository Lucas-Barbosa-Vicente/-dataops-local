"""
DataOps Local - Dashboard Interativo
Autor: Sistema DataOps
Descrição: Dashboard visual para análise de dados do negócio
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3

# Configuração da página
st.set_page_config(
    page_title="DataOps Local - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para conectar ao banco
@st.cache_resource
def get_database_connection():
    return sqlite3.connect('dados/dataops.db', check_same_thread=False)

# Função para carregar dados
@st.cache_data(ttl=60)
def carregar_receitas():
    conn = get_database_connection()
    query = """
        SELECT 
            data,
            tipo_servico,
            profissional,
            cliente,
            valor_servico,
            forma_pagamento
        FROM receitas
        ORDER BY data DESC
    """
    df = pd.read_sql_query(query, conn)
    df['data'] = pd.to_datetime(df['data'])
    return df

@st.cache_data(ttl=60)
def carregar_despesas():
    conn = get_database_connection()
    query = """
        SELECT 
            data,
            categoria,
            descricao,
            valor,
            forma_pagamento,
            fornecedor
        FROM despesas
        ORDER BY data DESC
    """
    df = pd.read_sql_query(query, conn)
    df['data'] = pd.to_datetime(df['data'])
    return df

@st.cache_data(ttl=60)
def carregar_profissionais():
    conn = get_database_connection()
    query = "SELECT * FROM profissionais WHERE status = 'Ativo'"
    return pd.read_sql_query(query, conn)

@st.cache_data(ttl=60)
def carregar_servicos():
    conn = get_database_connection()
    query = "SELECT * FROM servicos WHERE status = 'Ativo'"
    return pd.read_sql_query(query, conn)

# Título principal
st.title("📊 DataOps Local - Dashboard Gerencial")
st.markdown("---")

# Sidebar - Filtros
st.sidebar.header("🔍 Filtros")

# Carregar dados
try:
    df_receitas = carregar_receitas()
    df_despesas = carregar_despesas()
    df_profissionais = carregar_profissionais()
    df_servicos = carregar_servicos()
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.info("💡 Execute primeiro o script de processamento: python 2-processamento/processar_dados.py")
    st.stop()

# Filtro de período
periodo_opcoes = {
    "Últimos 7 dias": 7,
    "Últimos 30 dias": 30,
    "Últimos 90 dias": 90,
    "Tudo": None
}
periodo_selecionado = st.sidebar.selectbox("📅 Período", list(periodo_opcoes.keys()))

# Aplicar filtro de período
if periodo_opcoes[periodo_selecionado]:
    data_limite = datetime.now() - timedelta(days=periodo_opcoes[periodo_selecionado])
    df_receitas_filtrado = df_receitas[df_receitas['data'] >= data_limite]
    df_despesas_filtrado = df_despesas[df_despesas['data'] >= data_limite]
else:
    df_receitas_filtrado = df_receitas
    df_despesas_filtrado = df_despesas

# Filtro de profissional
profissionais_lista = ['Todos'] + sorted(df_receitas['profissional'].unique().tolist())
profissional_selecionado = st.sidebar.selectbox("👤 Profissional", profissionais_lista)

if profissional_selecionado != 'Todos':
    df_receitas_filtrado = df_receitas_filtrado[df_receitas_filtrado['profissional'] == profissional_selecionado]

# Métricas principais
st.header("💰 Indicadores Financeiros")

col1, col2, col3, col4 = st.columns(4)

total_receitas = df_receitas_filtrado['valor_servico'].sum()
total_despesas = df_despesas_filtrado['valor'].sum()
saldo = total_receitas - total_despesas
ticket_medio = df_receitas_filtrado['valor_servico'].mean() if len(df_receitas_filtrado) > 0 else 0

with col1:
    st.metric("💵 Receitas", f"R$ {total_receitas:,.2f}")

with col2:
    st.metric("📉 Despesas", f"R$ {total_despesas:,.2f}")

with col3:
    delta_color = "normal" if saldo >= 0 else "inverse"
    st.metric("💰 Saldo", f"R$ {saldo:,.2f}", delta=f"{saldo:,.2f}")

with col4:
    st.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.markdown("---")

# Análise de Receitas
st.header("📈 Análise de Receitas")

col1, col2 = st.columns(2)

with col1:
    # Receitas por profissional
    receitas_prof = df_receitas_filtrado.groupby('profissional')['valor_servico'].sum().reset_index()
    receitas_prof = receitas_prof.sort_values('valor_servico', ascending=False)
    
    fig_prof = px.bar(
        receitas_prof,
        x='profissional',
        y='valor_servico',
        title='Receitas por Profissional',
        labels={'valor_servico': 'Receita (R$)', 'profissional': 'Profissional'},
        color='valor_servico',
        color_continuous_scale='Blues'
    )
    fig_prof.update_layout(showlegend=False)
    st.plotly_chart(fig_prof, use_container_width=True)

with col2:
    # Receitas por tipo de serviço
    receitas_servico = df_receitas_filtrado.groupby('tipo_servico')['valor_servico'].sum().reset_index()
    receitas_servico = receitas_servico.sort_values('valor_servico', ascending=False)
    
    fig_servico = px.pie(
        receitas_servico,
        values='valor_servico',
        names='tipo_servico',
        title='Distribuição por Tipo de Serviço',
        hole=0.4
    )
    st.plotly_chart(fig_servico, use_container_width=True)

# Evolução temporal
st.subheader("📊 Evolução das Receitas")
receitas_diarias = df_receitas_filtrado.groupby(df_receitas_filtrado['data'].dt.date)['valor_servico'].sum().reset_index()
receitas_diarias.columns = ['data', 'valor']

fig_evolucao = px.line(
    receitas_diarias,
    x='data',
    y='valor',
    title='Receitas Diárias',
    labels={'valor': 'Receita (R$)', 'data': 'Data'},
    markers=True
)
fig_evolucao.update_traces(line_color='#1f77b4', line_width=3)
st.plotly_chart(fig_evolucao, use_container_width=True)

st.markdown("---")

# Análise de Despesas
st.header("📉 Análise de Despesas")

col1, col2 = st.columns(2)

with col1:
    # Despesas por categoria
    despesas_cat = df_despesas_filtrado.groupby('categoria')['valor'].sum().reset_index()
    despesas_cat = despesas_cat.sort_values('valor', ascending=False)
    
    fig_desp = px.bar(
        despesas_cat,
        x='categoria',
        y='valor',
        title='Despesas por Categoria',
        labels={'valor': 'Despesa (R$)', 'categoria': 'Categoria'},
        color='valor',
        color_continuous_scale='Reds'
    )
    fig_desp.update_layout(showlegend=False)
    st.plotly_chart(fig_desp, use_container_width=True)

with col2:
    # Distribuição de despesas
    fig_desp_pie = px.pie(
        despesas_cat,
        values='valor',
        names='categoria',
        title='Distribuição de Despesas',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    st.plotly_chart(fig_desp_pie, use_container_width=True)

st.markdown("---")

# Análise por Profissional
st.header("👥 Desempenho por Profissional")

# Calcular métricas por profissional
analise_prof = df_receitas_filtrado.groupby('profissional').agg({
    'valor_servico': ['sum', 'count', 'mean']
}).round(2)

analise_prof.columns = ['Total (R$)', 'Qtd Serviços', 'Ticket Médio (R$)']
analise_prof = analise_prof.reset_index()

# Adicionar informações de comissão
analise_prof = analise_prof.merge(
    df_profissionais[['nome_profissional', 'percentual_comissao', 'tipo_contrato']],
    left_on='profissional',
    right_on='nome_profissional',
    how='left'
)

# Calcular comissão
analise_prof['Comissão (R$)'] = analise_prof.apply(
    lambda x: x['Total (R$)'] * (x['percentual_comissao'] / 100) if x['tipo_contrato'] == 'Percentual' else 0,
    axis=1
).round(2)

# Exibir tabela
st.dataframe(
    analise_prof[['profissional', 'Qtd Serviços', 'Total (R$)', 'Ticket Médio (R$)', 'Comissão (R$)']],
    hide_index=True,
    use_container_width=True
)

st.markdown("---")

# Análise de Formas de Pagamento
st.header("💳 Formas de Pagamento")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Receitas")
    pagto_receitas = df_receitas_filtrado.groupby('forma_pagamento')['valor_servico'].sum().reset_index()
    
    fig_pagto_rec = px.pie(
        pagto_receitas,
        values='valor_servico',
        names='forma_pagamento',
        title='Recebimentos',
        color_discrete_sequence=px.colors.sequential.Greens
    )
    st.plotly_chart(fig_pagto_rec, use_container_width=True)

with col2:
    st.subheader("Despesas")
    pagto_despesas = df_despesas_filtrado.groupby('forma_pagamento')['valor'].sum().reset_index()
    
    fig_pagto_desp = px.pie(
        pagto_despesas,
        values='valor',
        names='forma_pagamento',
        title='Pagamentos',
        color_discrete_sequence=px.colors.sequential.Oranges
    )
    st.plotly_chart(fig_pagto_desp, use_container_width=True)

st.markdown("---")

# Tabelas detalhadas
st.header("📋 Registros Detalhados")

tab1, tab2 = st.tabs(["Receitas", "Despesas"])

with tab1:
    st.dataframe(
        df_receitas_filtrado.sort_values('data', ascending=False),
        hide_index=True,
        use_container_width=True
    )

with tab2:
    st.dataframe(
        df_despesas_filtrado.sort_values('data', ascending=False),
        hide_index=True,
        use_container_width=True
    )

# Footer
st.markdown("---")
st.caption("📊 DataOps Local v1.0 | Última atualização: " + datetime.now().strftime("%d/%m/%Y %H:%M"))

# Botão de atualização
if st.sidebar.button("🔄 Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()
