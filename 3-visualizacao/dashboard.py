"""
DataOps Local - Dashboard Interativo
Autor: Sistema DataOps
Descrição: Dashboard visual para análise de dados do negócio
Versão: 2.0 (Corrigida)

MELHORIAS NESTA VERSÃO:
- ✅ Comissões incluídas no cálculo de despesas
- ✅ Visualização separada de despesas manuais vs comissões
- ✅ Filtros aprimorados
- ✅ Análise detalhada por forma de pagamento
- ✅ Indicadores de margem e lucratividade
- ✅ Alertas visuais para despesas sem categoria
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3

# Função para formatar valores em Real brasileiro
def formatar_real(valor):
    """Formata valor para moeda brasileira (R$ 1.234,56)"""
    if pd.isna(valor) or valor is None:
        return "R$ 0,00"
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def formatar_real_compacto(valor):
    """Formata valor de forma compacta para métricas (77,2 mil)"""
    if pd.isna(valor) or valor is None:
        return "R$ 0"
    
    try:
        valor = float(valor)
        
        # Milhões
        if abs(valor) >= 1000000:
            return f"R$ {valor/1000000:.1f}M".replace(".", ",")
        # Milhares
        elif abs(valor) >= 1000:
            return f"R$ {valor/1000:.1f}k".replace(".", ",")
        # Centenas
        else:
            return f"R$ {valor:.0f}"
    except:
        return "R$ 0"

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
    df['data'] = pd.to_datetime(df['data'], format='mixed', errors='coerce')
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
            fornecedor,
            tipo_despesa,
            observacoes
        FROM despesas
        ORDER BY data DESC
    """
    df = pd.read_sql_query(query, conn)
    df['data'] = pd.to_datetime(df['data'], format='mixed', errors='coerce')
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
st.markdown("### - Com Análise de Comissões")
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

# Verificar se há dados
if len(df_receitas) == 0 and len(df_despesas) == 0:
    st.warning("⚠️ Nenhum dado encontrado no banco. Importe os dados primeiro!")
    st.stop()

# Filtro de período
periodo_opcoes = {
    "Últimos 7 dias": 7,
    "Últimos 30 dias": 30,
    "Últimos 90 dias": 90,
    "Último ano": 365,
    "Tudo": None
}
periodo_selecionado = st.sidebar.selectbox("📅 Período", list(periodo_opcoes.keys()), index=2)

# Aplicar filtro de período
if periodo_opcoes[periodo_selecionado]:
    data_limite = datetime.now() - timedelta(days=periodo_opcoes[periodo_selecionado])
    df_receitas_filtrado = df_receitas[df_receitas['data'] >= data_limite]
    df_despesas_filtrado = df_despesas[df_despesas['data'] >= data_limite]
else:
    df_receitas_filtrado = df_receitas
    df_despesas_filtrado = df_despesas

# Mostrar range de datas
if len(df_receitas_filtrado) > 0 or len(df_despesas_filtrado) > 0:
    datas_todas = pd.concat([df_receitas_filtrado['data'], df_despesas_filtrado['data']])
    data_min = datas_todas.min()
    data_max = datas_todas.max()
    st.sidebar.info(f"📆 {data_min.strftime('%d/%m/%Y')} até {data_max.strftime('%d/%m/%Y')}")

# Filtro de profissional
profissionais_lista = ['Todos'] + sorted(df_receitas['profissional'].unique().tolist())
profissional_selecionado = st.sidebar.selectbox("👤 Profissional", profissionais_lista)

if profissional_selecionado != 'Todos':
    df_receitas_filtrado = df_receitas_filtrado[df_receitas_filtrado['profissional'] == profissional_selecionado]

# Filtro de tipo de despesa (NOVO)
st.sidebar.markdown("---")
st.sidebar.subheader("💸 Tipos de Despesa")
tipos_despesa = df_despesas_filtrado['tipo_despesa'].unique().tolist() if 'tipo_despesa' in df_despesas_filtrado.columns else ['Manual']
mostrar_manuais = st.sidebar.checkbox("Despesas Manuais", value=True)
mostrar_comissoes = st.sidebar.checkbox("Comissões Calculadas", value=True)

# Aplicar filtro de tipo
filtro_tipos = []
if mostrar_manuais:
    filtro_tipos.append('Manual')
if mostrar_comissoes:
    filtro_tipos.append('Comissão Calculada')

if filtro_tipos:
    df_despesas_filtrado = df_despesas_filtrado[df_despesas_filtrado['tipo_despesa'].isin(filtro_tipos)]

# ============================================
# MÉTRICAS PRINCIPAIS
# ============================================
st.header("💰 Indicadores Financeiros")

# Usar 3 colunas em vez de 5 para dar mais espaço
col1, col2, col3 = st.columns(3)

total_receitas = df_receitas_filtrado['valor_servico'].sum()
total_despesas = df_despesas_filtrado['valor'].sum()
saldo = total_receitas - total_despesas
ticket_medio = df_receitas_filtrado['valor_servico'].mean() if len(df_receitas_filtrado) > 0 else 0
margem = (saldo / total_receitas * 100) if total_receitas > 0 else 0

with col1:
    st.metric(
        label="💵 Receitas Total", 
        value=formatar_real_compacto(total_receitas),
        help=f"Valor completo: {formatar_real(total_receitas)}"
    )

with col2:
    st.metric(
        label="📉 Despesas Total", 
        value=formatar_real_compacto(total_despesas),
        help=f"Valor completo: {formatar_real(total_despesas)}"
    )

with col3:
    margem_color = "🟢" if margem >= 20 else "🟡" if margem >= 10 else "🔴"
    st.metric(
        label=f"{margem_color} Saldo / Margem", 
        value=formatar_real_compacto(saldo),
        delta=f"{margem:.1f}% margem",
        help=f"Saldo completo: {formatar_real(saldo)}"
    )

# Segunda linha de métricas
st.markdown("")
col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        label="🎯 Ticket Médio", 
        value=formatar_real(ticket_medio)
    )

with col5:
    qtd_servicos = len(df_receitas_filtrado)
    st.metric(
        label="📊 Quantidade Serviços", 
        value=f"{qtd_servicos}"
    )

with col6:
    qtd_despesas = len(df_despesas_filtrado)
    st.metric(
        label="📝 Quantidade Despesas", 
        value=f"{qtd_despesas}"
    )

# Breakdown de despesas (NOVO)
st.markdown("---")
st.subheader("📊 Composição das Despesas")

col1, col2, col3 = st.columns(3)

despesas_manuais = df_despesas_filtrado[df_despesas_filtrado['tipo_despesa'] == 'Manual']['valor'].sum() if 'tipo_despesa' in df_despesas_filtrado.columns else total_despesas
despesas_comissoes = df_despesas_filtrado[df_despesas_filtrado['tipo_despesa'] == 'Comissão Calculada']['valor'].sum() if 'tipo_despesa' in df_despesas_filtrado.columns else 0
outras_despesas = total_despesas - despesas_manuais - despesas_comissoes

with col1:
    st.metric("🏢 Despesas Operacionais", formatar_real(despesas_manuais), 
              f"{despesas_manuais/total_despesas*100:.1f}% do total" if total_despesas > 0 else "0%")

with col2:
    st.metric("👥 Folha (Comissões)", formatar_real(despesas_comissoes),
              f"{despesas_comissoes/total_despesas*100:.1f}% do total" if total_despesas > 0 else "0%")

with col3:
    custo_aquisicao = (despesas_comissoes / total_receitas * 100) if total_receitas > 0 else 0
    st.metric("📈 CAC (Custo Aquisição)", f"{custo_aquisicao:.1f}%",
              help="Percentual da receita gasto com comissões")

st.markdown("---")

# ============================================
# ANÁLISE DE RECEITAS
# ============================================
st.header("📈 Análise de Receitas")

col1, col2 = st.columns(2)

with col1:
    # Receitas por profissional
    if len(df_receitas_filtrado) > 0:
        receitas_prof = df_receitas_filtrado.groupby('profissional')['valor_servico'].sum().reset_index()
        receitas_prof = receitas_prof.sort_values('valor_servico', ascending=False)
        
        fig_prof = px.bar(
            receitas_prof,
            x='profissional',
            y='valor_servico',
            title='Receitas por Profissional',
            labels={'valor_servico': 'Receita (R$)', 'profissional': 'Profissional'},
            color='valor_servico',
            color_continuous_scale='Blues',
            text='valor_servico'
        )
        fig_prof.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
        fig_prof.update_layout(showlegend=False)
        st.plotly_chart(fig_prof, use_container_width=True)
    else:
        st.info("Nenhuma receita no período selecionado")

with col2:
    # Receitas por tipo de serviço
    if len(df_receitas_filtrado) > 0:
        receitas_servico = df_receitas_filtrado.groupby('tipo_servico')['valor_servico'].sum().reset_index()
        receitas_servico = receitas_servico.sort_values('valor_servico', ascending=False)
        
        fig_servico = px.pie(
            receitas_servico,
            values='valor_servico',
            names='tipo_servico',
            title='Distribuição por Tipo de Serviço',
            hole=0.4
        )
        fig_servico.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_servico, use_container_width=True)
    else:
        st.info("Nenhuma receita no período selecionado")

# Evolução temporal
if len(df_receitas_filtrado) > 0:
    st.subheader("📊 Evolução das Receitas")
    
    # Agrupar por dia
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

# ============================================
# ANÁLISE DE DESPESAS
# ============================================
st.header("📉 Análise de Despesas")

col1, col2 = st.columns(2)

with col1:
    # Despesas por categoria
    if len(df_despesas_filtrado) > 0:
        despesas_cat = df_despesas_filtrado.groupby('categoria')['valor'].sum().reset_index()
        despesas_cat = despesas_cat.sort_values('valor', ascending=False)
        
        fig_desp = px.bar(
            despesas_cat,
            x='categoria',
            y='valor',
            title='Despesas por Categoria',
            labels={'valor': 'Despesa (R$)', 'categoria': 'Categoria'},
            color='valor',
            color_continuous_scale='Reds',
            text='valor'
        )
        fig_desp.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
        fig_desp.update_layout(showlegend=False)
        st.plotly_chart(fig_desp, use_container_width=True)
    else:
        st.info("Nenhuma despesa no período selecionado")

with col2:
    # Distribuição de despesas
    if len(df_despesas_filtrado) > 0:
        fig_desp_pie = px.pie(
            despesas_cat,
            values='valor',
            names='categoria',
            title='Distribuição de Despesas',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig_desp_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_desp_pie, use_container_width=True)
    else:
        st.info("Nenhuma despesa no período selecionado")

# Análise de despesas por tipo (NOVO)
if 'tipo_despesa' in df_despesas_filtrado.columns and len(df_despesas_filtrado) > 0:
    st.subheader("🔍 Despesas: Manual vs Comissões")
    
    col1, col2 = st.columns(2)
    
    with col1:
        despesas_tipo = df_despesas_filtrado.groupby('tipo_despesa')['valor'].sum().reset_index()
        
        fig_tipo = px.bar(
            despesas_tipo,
            x='tipo_despesa',
            y='valor',
            title='Comparação: Despesas Manuais vs Comissões',
            labels={'valor': 'Valor (R$)', 'tipo_despesa': 'Tipo'},
            color='tipo_despesa',
            color_discrete_map={
                'Manual': '#ff7f0e',
                'Comissão Calculada': '#2ca02c'
            },
            text='valor'
        )
        fig_tipo.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
        st.plotly_chart(fig_tipo, use_container_width=True)
    
    with col2:
        # Mostrar detalhes
        st.markdown("**📋 Resumo por Tipo:**")
        for _, row in despesas_tipo.iterrows():
            percentual = (row['valor'] / total_despesas * 100) if total_despesas > 0 else 0
            st.metric(
                row['tipo_despesa'],
                formatar_real(row['valor']),
                f"{percentual:.1f}% do total"
            )

st.markdown("---")

# ============================================
# DESEMPENHO POR PROFISSIONAL
# ============================================
st.header("👥 Desempenho por Profissional")

if len(df_receitas_filtrado) > 0:
    # Calcular métricas por profissional
    analise_prof = df_receitas_filtrado.groupby('profissional').agg({
        'valor_servico': ['sum', 'count', 'mean']
    }).round(2)
    
    analise_prof.columns = ['Total Vendas (R$)', 'Qtd Serviços', 'Ticket Médio (R$)']
    analise_prof = analise_prof.reset_index()
    
    # Adicionar informações de comissão
    analise_prof = analise_prof.merge(
        df_profissionais[['nome_profissional', 'percentual_comissao', 'salario_fixo', 'tipo_contrato']],
        left_on='profissional',
        right_on='nome_profissional',
        how='left'
    )
    
    # Calcular comissão
    analise_prof['Comissão (R$)'] = analise_prof.apply(
        lambda x: x['Total Vendas (R$)'] * (x['percentual_comissao'] / 100) if x['tipo_contrato'] == 'Percentual' and pd.notna(x['percentual_comissao']) else 0,
        axis=1
    ).round(2)
    
    # Adicionar salário fixo
    analise_prof['Salário Fixo (R$)'] = analise_prof['salario_fixo'].fillna(0)
    
    # Total a pagar
    analise_prof['Total a Pagar (R$)'] = (analise_prof['Salário Fixo (R$)'] + analise_prof['Comissão (R$)']).round(2)
    
    # Margem de contribuição
    analise_prof['Margem (R$)'] = (analise_prof['Total Vendas (R$)'] - analise_prof['Total a Pagar (R$)']).round(2)
    analise_prof['Margem (%)'] = (analise_prof['Margem (R$)'] / analise_prof['Total Vendas (R$)'] * 100).round(1)
    
    # Formatar colunas de moeda para exibição
    analise_prof_display = analise_prof.copy()
    colunas_moeda = ['Total Vendas (R$)', 'Ticket Médio (R$)', 'Salário Fixo (R$)', 
                     'Comissão (R$)', 'Total a Pagar (R$)', 'Margem (R$)']
    
    for col in colunas_moeda:
        if col in analise_prof_display.columns:
            analise_prof_display[col] = analise_prof_display[col].apply(formatar_real)
    
    # Exibir tabela
    st.dataframe(
        analise_prof_display[[
            'profissional', 
            'Qtd Serviços', 
            'Total Vendas (R$)', 
            'Ticket Médio (R$)',
            'Salário Fixo (R$)',
            'Comissão (R$)',
            'Total a Pagar (R$)',
            'Margem (R$)',
            'Margem (%)'
        ]].sort_values('Qtd Serviços', ascending=False),
        hide_index=True,
        use_container_width=True
    )
    
    # Alertas
    total_folha = analise_prof['Total a Pagar (R$)'].sum()
    percentual_folha = (total_folha / total_receitas * 100) if total_receitas > 0 else 0
    
    if percentual_folha > 50:
        st.warning(f"⚠️ A folha de pagamento representa {percentual_folha:.1f}% da receita. Considere revisar.")
    elif percentual_folha > 30:
        st.info(f"💡 A folha de pagamento representa {percentual_folha:.1f}% da receita.")
    else:
        st.success(f"✅ A folha de pagamento representa {percentual_folha:.1f}% da receita. Está saudável!")

else:
    st.info("Nenhuma receita no período para análise de profissionais")

st.markdown("---")

# ============================================
# FORMAS DE PAGAMENTO
# ============================================
st.header("💳 Análise de Formas de Pagamento")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Receitas")
    if len(df_receitas_filtrado) > 0 and 'forma_pagamento' in df_receitas_filtrado.columns:
        pagto_receitas = df_receitas_filtrado.groupby('forma_pagamento')['valor_servico'].agg(['sum', 'count']).reset_index()
        pagto_receitas.columns = ['Forma', 'Total', 'Quantidade']
        
        fig_pagto_rec = px.pie(
            pagto_receitas,
            values='Total',
            names='Forma',
            title='Recebimentos por Forma',
            color_discrete_sequence=px.colors.sequential.Greens,
            hover_data=['Quantidade']
        )
        fig_pagto_rec.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pagto_rec, use_container_width=True)
        
        # Tabela detalhada com formatação
        pagto_receitas_display = pagto_receitas.copy()
        pagto_receitas_display['Total'] = pagto_receitas_display['Total'].apply(formatar_real)
        st.dataframe(
            pagto_receitas_display.sort_values('Quantidade', ascending=False),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Sem dados de forma de pagamento em receitas")

with col2:
    st.subheader("Despesas")
    if len(df_despesas_filtrado) > 0 and 'forma_pagamento' in df_despesas_filtrado.columns:
        # Filtrar apenas despesas com forma de pagamento preenchida
        despesas_com_pagto = df_despesas_filtrado[df_despesas_filtrado['forma_pagamento'].notna()]
        
        if len(despesas_com_pagto) > 0:
            pagto_despesas = despesas_com_pagto.groupby('forma_pagamento')['valor'].agg(['sum', 'count']).reset_index()
            pagto_despesas.columns = ['Forma', 'Total', 'Quantidade']
            
            fig_pagto_desp = px.pie(
                pagto_despesas,
                values='Total',
                names='Forma',
                title='Pagamentos por Forma',
                color_discrete_sequence=px.colors.sequential.Oranges,
                hover_data=['Quantidade']
            )
            fig_pagto_desp.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pagto_desp, use_container_width=True)
            
            # Tabela detalhada com formatação
            pagto_despesas_display = pagto_despesas.copy()
            pagto_despesas_display['Total'] = pagto_despesas_display['Total'].apply(formatar_real)
            st.dataframe(
                pagto_despesas_display.sort_values('Quantidade', ascending=False),
                hide_index=True,
                use_container_width=True
            )
            
            # Alerta para despesas sem forma de pagamento
            sem_forma = len(df_despesas_filtrado) - len(despesas_com_pagto)
            if sem_forma > 0:
                st.warning(f"⚠️ {sem_forma} despesas sem forma de pagamento definida")
        else:
            st.warning("⚠️ Nenhuma despesa possui forma de pagamento registrada")
    else:
        st.info("Sem dados de forma de pagamento em despesas")

st.markdown("---")

# ============================================
# FLUXO DE CAIXA
# ============================================
st.header("💰 Fluxo de Caixa")

if len(df_receitas_filtrado) > 0 or len(df_despesas_filtrado) > 0:
    # Preparar dados de receitas
    receitas_fluxo = df_receitas_filtrado.groupby(df_receitas_filtrado['data'].dt.date)['valor_servico'].sum().reset_index()
    receitas_fluxo.columns = ['data', 'receitas']
    
    # Preparar dados de despesas
    despesas_fluxo = df_despesas_filtrado.groupby(df_despesas_filtrado['data'].dt.date)['valor'].sum().reset_index()
    despesas_fluxo.columns = ['data', 'despesas']
    
    # Merge
    fluxo = pd.merge(receitas_fluxo, despesas_fluxo, on='data', how='outer').fillna(0)
    fluxo['saldo_dia'] = fluxo['receitas'] - fluxo['despesas']
    fluxo['saldo_acumulado'] = fluxo['saldo_dia'].cumsum()
    fluxo = fluxo.sort_values('data')
    
    # Gráfico
    fig_fluxo = go.Figure()
    
    fig_fluxo.add_trace(go.Scatter(
        x=fluxo['data'],
        y=fluxo['receitas'],
        name='Receitas',
        line=dict(color='green', width=2),
        fill='tozeroy'
    ))
    
    fig_fluxo.add_trace(go.Scatter(
        x=fluxo['data'],
        y=fluxo['despesas'],
        name='Despesas',
        line=dict(color='red', width=2),
        fill='tozeroy'
    ))
    
    fig_fluxo.add_trace(go.Scatter(
        x=fluxo['data'],
        y=fluxo['saldo_acumulado'],
        name='Saldo Acumulado',
        line=dict(color='blue', width=3, dash='dash'),
        yaxis='y2'
    ))
    
    fig_fluxo.update_layout(
        title='Fluxo de Caixa Diário',
        xaxis_title='Data',
        yaxis_title='Valor (R$)',
        yaxis2=dict(
            title='Saldo Acumulado (R$)',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_fluxo, use_container_width=True)
else:
    st.info("Sem dados para exibir fluxo de caixa")

st.markdown("---")

# ============================================
# TABELAS DETALHADAS
# ============================================
st.header("📋 Registros Detalhados")

tab1, tab2 = st.tabs(["Receitas", "Despesas"])

with tab1:
    if len(df_receitas_filtrado) > 0:
        # Formatar valores antes de exibir
        df_receitas_display = df_receitas_filtrado.copy()
        df_receitas_display['valor_servico'] = df_receitas_display['valor_servico'].apply(formatar_real)
        
        st.dataframe(
            df_receitas_display.sort_values('data', ascending=False),
            hide_index=True,
            use_container_width=True
        )
        
        # Botão de download
        csv_receitas = df_receitas_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Receitas (CSV)",
            data=csv_receitas,
            file_name=f'receitas_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    else:
        st.info("Nenhuma receita no período selecionado")

with tab2:
    if len(df_despesas_filtrado) > 0:
        # Formatar valores antes de exibir
        df_despesas_display = df_despesas_filtrado.copy()
        df_despesas_display['valor'] = df_despesas_display['valor'].apply(formatar_real)
        
        st.dataframe(
            df_despesas_display.sort_values('data', ascending=False),
            hide_index=True,
            use_container_width=True
        )
        
        # Botão de download
        csv_despesas = df_despesas_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Despesas (CSV)",
            data=csv_despesas,
            file_name=f'despesas_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    else:
        st.info("Nenhuma despesa no período selecionado")

# Footer
st.markdown("---")
st.caption("📊 DataOps Local v2.0 | Última atualização: " + datetime.now().strftime("%d/%m/%Y %H:%M"))

# Botão de atualização
if st.sidebar.button("🔄 Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()

# Informações do sistema na sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ Informações do Sistema")
st.sidebar.info(f"""
**Total de Registros:**
- Receitas: {len(df_receitas)}
- Despesas: {len(df_despesas)}
- Profissionais: {len(df_profissionais)}
- Serviços: {len(df_servicos)}

**Período Filtrado:**
- Receitas: {len(df_receitas_filtrado)}
- Despesas: {len(df_despesas_filtrado)}
""")