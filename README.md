# 📊 DataOps Local v2.0

<div align="center">

**Sistema completo de gestão financeira para pequenos negócios**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

[Funcionalidades](#-funcionalidades) •
[Instalação](#-instalação) •
[Como Usar](#-como-usar) •
[Tecnologias](#️-tecnologias)

</div>

---

## 🎯 Sobre o Projeto

O **DataOps Local** é um sistema de gestão financeira desenvolvido para automatizar e simplificar o controle de receitas, despesas e comissões em pequenos negócios. Com dashboard interativo e cálculos automáticos, você tem visão completa do seu negócio em tempo real.

### ✨ Destaques da v2.0

- 💰 **Cálculo automático de comissões** - Configure percentuais e o sistema calcula tudo
- 💵 **Formatação brasileira** - Valores em R$ 1.234,56
- 📊 **Dashboard interativo** - Métricas em tempo real com Streamlit
- 🔍 **Validação robusta** - Sistema de logs e verificação de dados
- 📈 **Análises avançadas** - Margem, CAC, fluxo de caixa

---

## 🚀 Funcionalidades

### 💰 Gestão Financeira
- ✅ Controle de receitas e despesas
- ✅ Cálculo automático de comissões por profissional
- ✅ Análise de margem de lucro
- ✅ Separação entre custos fixos e variáveis
- ✅ Múltiplas formas de pagamento (Boleto, PIX, Cartão, etc.)

### 📊 Dashboard Analítico
- ✅ Métricas financeiras em tempo real
- ✅ Gráfico de fluxo de caixa
- ✅ Análise por profissional
- ✅ Comparação: Despesas Manuais vs Comissões
- ✅ Filtros inteligentes (período, profissional, tipo)
- ✅ Visualização de formas de pagamento

### 🔧 Recursos Técnicos
- ✅ Sistema de logs completo
- ✅ Validação de dados antes da importação
- ✅ Suporte a múltiplos formatos de data
- ✅ Download de dados em CSV
- ✅ Alertas automáticos de performance
- ✅ Backup automático

---

## 🛠️ Tecnologias

- **Python 3.8+** - Linguagem principal
- **Pandas** - Manipulação de dados
- **Streamlit** - Dashboard interativo
- **Plotly** - Gráficos e visualizações
- **SQLite** - Banco de dados local
- **OpenPyXL** - Leitura de arquivos Excel

---

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/Lucas-Barbosa-Vicente/-dataops-local.git
cd -dataops-local
```

2. **Instale as dependências:**
```bash
pip install pandas streamlit plotly openpyxl
```

3. **Estrutura de pastas:**
```
DataOps-Local/
├── 1-coleta/          # Planilhas Excel
├── 2-processamento/   # Scripts de importação
├── 3-analytics/       # Dashboard
├── dados/             # Banco de dados (criado automaticamente)
└── logs/              # Logs de processamento
```

---

## 🎯 Como Usar

### 1️⃣ Preparar os Dados

Preencha as planilhas na pasta `1-coleta/`:

- **Template_Receitas.xlsx** - Serviços prestados
- **Template_Despesas.xlsx** - Gastos operacionais
- **Template_Profissionais.xlsx** - Dados dos profissionais
- **Template_Servicos.xlsx** - Catálogo de serviços

### 2️⃣ Processar os Dados
```bash
python 2-processamento/processar_dados.py
```

**O que acontece:**
- ✅ Importa todas as planilhas
- ✅ Valida os dados
- ✅ Calcula comissões automaticamente
- ✅ Gera relatório completo
- ✅ Salva logs em `logs/importacao.log`

### 3️⃣ Visualizar o Dashboard
```bash
streamlit py -3.10 -m streamlit run 3-visualizacao\dashboard.py

```

O dashboard abre automaticamente no navegador em `http://localhost:8501`

---

## 📊 Métricas Disponíveis

### Indicadores Principais
- 💵 **Receitas Totais**
- 📉 **Despesas Totais** (Operacionais + Comissões)
- 💰 **Saldo e Margem**
- 🎯 **Ticket Médio**

### Análises Detalhadas
- 👥 **Desempenho por Profissional**
  - Total de vendas
  - Comissão calculada
  - Margem de contribuição
  
- 💳 **Formas de Pagamento**
  - Receitas por método
  - Despesas por método
  
- 📈 **Fluxo de Caixa**
  - Entradas e saídas diárias
  - Saldo acumulado

---

---

## 🐛 Solução de Problemas

### Problema: "Erro ao converter data"
**Solução:** Verifique se as datas nas planilhas estão em formato DD/MM/YYYY

### Problema: "Comissões não aparecem"
**Solução:** Execute o processamento: `python 2-processamento/processar_dados.py`

### Problema: "Dashboard não carrega"
**Solução:** 
1. Verifique se o banco existe: `dados/dataops.db`
2. Execute o diagnóstico: `python diagnostico.py`

---

## 📚 Documentação Adicional

- [ANALISE_COMPLETA.md](ANALISE_COMPLETA.md) - Análise detalhada do projeto
- [GUIA_MIGRACAO.md](GUIA_MIGRACAO.md) - Como migrar da v1.0 para v2.0
- [logs/importacao.log](logs/) - Logs de cada processamento

---

## 🔄 Atualizações

### v2.0 - Fevereiro 2026
- ✨ Cálculo automático de comissões
- 🐛 Correção do bug de data (fevereiro)
- 💵 Formatação brasileira completa
- 📊 Novo layout de métricas
- 🔍 Sistema de validação robusto
- 📝 Logs detalhados

### v1.0 - Janeiro 2026
- 🎉 Lançamento inicial
- 📊 Dashboard básico
- 💾 Importação de dados

---

## 🤝 Contribuindo

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Lucas Barbosa Vicente**

- GitHub: [@Lucas-Barbosa-Vicente](https://github.com/Lucas-Barbosa-Vicente)
- LinkedIn: [Lucas Barbosa](https://www.linkedin.com/in/lucas-barbosa-966930251/)

---

## ⭐ Mostre seu apoio

Se este projeto te ajudou, dê uma ⭐️!

---

<div align="center">


</div>