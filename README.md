# 📊 DataOps Local

> Sistema completo de análise de dados para pequenas empresas - 100% local

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🎯 O que é?

**DataOps Local** é uma solução completa de gestão e análise de dados desenvolvida especialmente para pequenas empresas que precisam de controle financeiro e gerencial, mas não têm conhecimento técnico ou orçamento para ferramentas complexas.

### ✨ Características

- 🏠 **100% Local** - Seus dados ficam no seu computador
- 🔒 **Privado** - Total controle sobre suas informações
- 📊 **Visual** - Dashboards coloridos e intuitivos
- 📄 **Automático** - Relatórios PDF gerados automaticamente
- 🚀 **Fácil de usar** - Interface simples para não-técnicos

---

## 📦 O que está incluído?

```
DataOps-Local/
├── 1-coleta/              ← VOCÊ PREENCHE AQUI (Excel)
│   ├── Template_Receitas.xlsx
│   ├── Template_Despesas.xlsx
│   ├── Template_Profissionais.xlsx
│   └── Template_Servicos.xlsx
│
├── 2-processamento/       ← Sistema processa automaticamente
│   └── processar_dados.py
│
├── 3-visualizacao/        ← Dashboard interativo
│   └── dashboard.py
│
├── 4-relatorios/          ← Relatórios PDF gerados
│   └── gerar_relatorio.py
│
├── dados/                 ← Banco de dados (SQLite)
│   └── dataops.db
│
└── documentacao/          ← Guias de uso
    ├── INICIO_RAPIDO.md
    └── COMO_PREENCHER_PLANILHAS.md
```

---

## 🚀 Início Rápido

### 1️⃣ Instalação (apenas 1 vez)

**Pré-requisito:** Ter Python instalado → [Download Python](https://www.python.org/downloads/)

```bash
# Clone ou baixe este projeto
cd DataOps-Local

# Instale as dependências
pip install -r requirements.txt
```

### 2️⃣ Uso Diário

**Passo 1:** Preencha as planilhas Excel na pasta `1-coleta/`

**Passo 2:** Processe os dados
```bash
python 2-processamento/processar_dados.py
```

**Passo 3:** Visualize os resultados
```bash
# Dashboard interativo
streamlit run 3-visualizacao/dashboard.py

# OU gere relatório PDF
python 4-relatorios/gerar_relatorio.py
```

---

## 📊 Funcionalidades

### 💰 Controle Financeiro
- ✅ Registro de todas as receitas
- ✅ Controle de despesas por categoria
- ✅ Cálculo automático de saldo
- ✅ Análise de formas de pagamento

### 👥 Gestão de Profissionais
- ✅ Desempenho individual de cada colaborador
- ✅ Cálculo automático de comissões
- ✅ Ranking de produtividade
- ✅ Análise de ticket médio por pessoa

### 💼 Análise de Serviços
- ✅ Serviços mais vendidos
- ✅ Rentabilidade por tipo de serviço
- ✅ Tempo médio de atendimento
- ✅ Análise de precificação

### 📈 Visualizações
- ✅ Gráficos de evolução temporal
- ✅ Comparativos por período
- ✅ Dashboards interativos
- ✅ Relatórios PDF profissionais

---

## 🎓 Documentação

| Documento | Descrição |
|-----------|-----------|
| [Início Rápido](documentacao/INICIO_RAPIDO.md) | Guia completo de instalação e primeiros passos |
| [Como Preencher Planilhas](documentacao/COMO_PREENCHER_PLANILHAS.md) | Tutorial detalhado de cada planilha |

---

## 🛠 Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| **Python** | Linguagem principal |
| **Pandas** | Processamento de dados |
| **SQLite** | Banco de dados local |
| **Streamlit** | Interface web do dashboard |
| **Plotly** | Gráficos interativos |
| **ReportLab** | Geração de PDFs |
| **OpenPyXL** | Leitura de arquivos Excel |

---

## 📋 Requisitos

- Python 3.8 ou superior
- Windows, Mac ou Linux
- 50MB de espaço em disco
- Navegador web (para dashboard)

---

## 🎯 Para quem é este projeto?

### ✅ Ideal para:
- 💇 Salões de beleza e barbearias
- 🍽️ Restaurantes e lanchonetes
- 🔧 Oficinas e prestadores de serviço
- 🏥 Clínicas e consultórios pequenos
- 🎨 Estúdios e ateliês
- 📚 Escolas de idiomas e cursos

### ❌ NÃO é ideal para:
- Grandes empresas com ERPs complexos
- Negócios que precisam de múltiplos usuários simultâneos
- Empresas com departamento de TI próprio

---

## 🔐 Privacidade e Segurança

- ✅ Todos os dados ficam no SEU computador
- ✅ Nenhuma informação é enviada para internet
- ✅ Você tem controle total dos seus dados
- ✅ Faça backup quando quiser
- ✅ Delete quando quiser

---

## 📸 Screenshots

### Dashboard Principal
```
┌─────────────────────────────────────────────────────┐
│  💰 Indicadores Financeiros                         │
├─────────────────────────────────────────────────────┤
│  💵 Receitas    📉 Despesas    💰 Saldo    🎯 Ticket│
│  R$ 10.500     R$ 7.200       R$ 3.300    R$ 75    │
└─────────────────────────────────────────────────────┘

┌──────────────────────┬──────────────────────────────┐
│ 📊 Receitas/Prof     │ 🥧 Distribuição Serviços     │
│                      │                              │
│  [Gráfico de Barras] │  [Gráfico Pizza]            │
└──────────────────────┴──────────────────────────────┘
```

### Relatório PDF
```
╔════════════════════════════════════════╗
║  RELATÓRIO GERENCIAL MENSAL            ║
╠════════════════════════════════════════╣
║  1. RESUMO FINANCEIRO                  ║
║  2. DESEMPENHO POR PROFISSIONAL        ║
║  3. SERVIÇOS MAIS REALIZADOS           ║
║  4. DESPESAS POR CATEGORIA             ║
╚════════════════════════════════════════╝
```

---

## 🆘 Suporte e Ajuda

### Problemas Comuns

**"Módulo não encontrado"**
```bash
pip install -r requirements.txt
```

**"Erro ao processar dados"**
- Verifique se as planilhas estão preenchidas corretamente
- Confira o formato das datas (DD/MM/AAAA)
- Use ponto nos valores, não vírgula

**"Dashboard não abre"**
```bash
streamlit run 3-visualizacao/dashboard.py --server.port 8502
```

---

## 🗺️ Roadmap

### Versão 1.0 (Atual)
- ✅ Sistema de coleta por Excel
- ✅ Processamento automatizado
- ✅ Dashboard interativo
- ✅ Relatórios em PDF

### Versão 2.0 (Futuro)
- 🔲 Múltiplas empresas no mesmo sistema
- 🔲 Exportação para Google Sheets
- 🔲 Backup automático em nuvem (opcional)
- 🔲 App mobile para registro rápido
- 🔲 Previsões com Machine Learning

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Reportar bugs
2. Sugerir novas funcionalidades
3. Melhorar a documentação
4. Enviar pull requests

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Sistema DataOps**  
Desenvolvido para democratizar análise de dados para pequenos negócios

---

## ⭐ Dê uma estrela!

Se este projeto te ajudou, considere dar uma ⭐ para ajudar outras pessoas a encontrá-lo!

---

## 🙏 Agradecimentos

Este projeto foi criado com o objetivo de ajudar pequenos empreendedores a terem acesso a ferramentas profissionais de análise de dados, sem custos e sem complexidade.

**Bons negócios! **

---

<div align="center">

**[📚 Documentação](documentacao/)** • **[🐛 Reportar Bug](issues)** • **[💡 Sugerir Funcionalidade](issues)**

</div>
