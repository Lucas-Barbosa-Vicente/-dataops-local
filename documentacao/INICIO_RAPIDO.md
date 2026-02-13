# 🚀 DataOps Local - Guia de Início Rápido

## 📌 O que é o DataOps Local?

O DataOps Local é um sistema completo de gestão de dados para pequenas empresas (restaurantes, salões, barbearias, prestadores de serviço). Ele permite:

✅ **Controlar suas finanças** - Registre receitas e despesas facilmente  
✅ **Analisar desempenho** - Veja qual profissional está vendendo mais  
✅ **Identificar serviços rentáveis** - Descubra quais serviços dão mais lucro  
✅ **Visualizar dados** - Dashboards coloridos e fáceis de entender  
✅ **Gerar relatórios automáticos** - PDFs prontos para apresentar

---

## 🎯 Como Funciona?

O sistema funciona em 3 passos simples:

```
1️⃣ VOCÊ PREENCHE → Planilhas Excel simples
2️⃣ SISTEMA PROCESSA → Organiza tudo automaticamente
3️⃣ VOCÊ VISUALIZA → Gráficos, tabelas e relatórios prontos
```

---

## 📦 Instalação (Apenas 1 vez)

### Windows

1. **Instale o Python** (se ainda não tiver)
   - Baixe em: https://www.python.org/downloads/
   - Durante a instalação, marque: ☑️ "Add Python to PATH"

2. **Abra o Prompt de Comando**
   - Aperte tecla `Windows` + `R`
   - Digite: `cmd`
   - Aperte Enter

3. **Instale as ferramentas necessárias**
   ```
   cd caminho\para\DataOps-Local
   pip install -r requirements.txt
   ```

### Mac / Linux

1. **Abra o Terminal**

2. **Instale as ferramentas**
   ```bash
   cd caminho/para/DataOps-Local
   pip3 install -r requirements.txt
   ```

---

## 📝 Uso Diário

### Passo 1: Preencher as Planilhas

Vá até a pasta `1-coleta` e abra as planilhas no Excel:

**📊 Template_Receitas.xlsx**
- Preencha cada vez que fizer um serviço
- Exemplo: "João fez um corte no Cliente A por R$ 50,00"

**📉 Template_Despesas.xlsx**
- Preencha quando tiver uma despesa
- Exemplo: "Paguei R$ 1.500 de aluguel"

**👥 Template_Profissionais.xlsx**
- Cadastre seus funcionários
- Define se ganham percentual ou salário fixo

**💼 Template_Servicos.xlsx**
- Liste todos os serviços que você oferece
- Defina os preços

> 💡 **DICA:** Não delete as colunas! Apenas adicione novas linhas.

---

### Passo 2: Processar os Dados

Depois de preencher as planilhas, rode o processamento:

**Windows:**
```
python 2-processamento\processar_dados.py
```

**Mac/Linux:**
```bash
python3 2-processamento/processar_dados.py
```

✅ Você verá uma mensagem de sucesso e um resumo dos dados!

---

### Passo 3: Ver os Resultados

#### Opção A: Dashboard Interativo (Recomendado)

**Windows:**
```
streamlit run 3-visualizacao\dashboard.py

ou 

py -3.10 -m streamlit run 3-visualizacao\dashboard.py

```

**Mac/Linux:**
```bash
streamlit run 3-visualizacao/dashboard.py
```

🌐 Abrirá automaticamente no seu navegador!

#### Opção B: Relatório em PDF

**Windows:**
```
python 4-relatorios\gerar_relatorio.py
```

**Mac/Linux:**
```bash
python3 4-relatorios/gerar_relatorio.py
```

📄 O PDF estará na pasta `4-relatorios`

---

## 📅 Rotina Recomendada

### 🌅 **Diariamente**
- Preencha receitas conforme os serviços são realizados
- Anote despesas do dia

### 📊 **Semanalmente**
- Processe os dados (Passo 2)
- Veja o dashboard para acompanhar evolução

### 📈 **Mensalmente**
- Gere o relatório em PDF
- Analise os resultados
- Tome decisões baseadas nos dados

---

## 🆘 Problemas Comuns

### "Erro: arquivo não encontrado"
➡️ Certifique-se de estar na pasta correta do projeto

### "Erro: módulo não instalado"
➡️ Execute novamente: `pip install -r requirements.txt`

### "Dados não aparecem no dashboard"
➡️ Execute primeiro o processamento (Passo 2)

### "Coluna não encontrada"
➡️ Não delete ou renomeie as colunas das planilhas

---

## 📞 Precisa de Ajuda?

- 📧 Entre em contato com o suporte
- 📚 Veja os outros guias na pasta `documentacao`

---

## 🎉 Pronto!

Agora você tem um sistema profissional de análise de dados rodando localmente, sem internet necessária, e com total controle dos seus dados!

**Bons negócios! 🚀**
