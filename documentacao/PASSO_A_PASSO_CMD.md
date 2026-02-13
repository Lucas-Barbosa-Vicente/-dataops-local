# 🚀 PASSO A PASSO COMPLETO - CMD do Windows

## ✅ INSTRUÇÕES FINAIS

### 1️⃣ Abrir o CMD na pasta correta

**Opção A (Mais Fácil):**
1. Abra a pasta `C:\Users\Lucas\Desktop\DataOps-Local` no Windows Explorer
2. Clique na barra de endereço (onde mostra o caminho)
3. Digite: `cmd` e aperte Enter
4. O CMD abre já na pasta certa! ✅

**Opção B:**
1. Aperte `Windows + R`
2. Digite: `cmd`
3. Digite: `cd C:\Users\Lucas\Desktop\DataOps-Local`

---

### 2️⃣ Instalar Dependências (APENAS 1 VEZ)

Cole este comando e aguarde terminar (1-2 minutos):

```bash
py -3.10 -m pip install --user plotly streamlit pandas openpyxl reportlab sqlalchemy python-dateutil
```

Aguarde aparecer: `Successfully installed...`

---

### 3️⃣ Gerar Dados de Exemplo

```bash
py -3.10 gerar_exemplo.py
```

Quando perguntar "Deseja continuar? (s/n):", digite `s` e Enter

---

### 4️⃣ Processar os Dados

```bash
py -3.10 2-processamento\processar_dados.py
```

Você verá um resumo com:
- Total de receitas
- Total de despesas
- Saldo
- Etc.

---

### 5️⃣ Abrir o Dashboard

```bash
py -3.10 -m streamlit run 3-visualizacao\dashboard.py
```

**Aguarde 10-30 segundos**

O navegador abrirá automaticamente! 🎉

**NÃO FECHE a janela do CMD** enquanto estiver usando o dashboard!

---

## 📊 O que você verá no Dashboard:

- 💰 Indicadores financeiros
- 📈 Gráficos de receitas
- 👥 Desempenho por profissional
- 📉 Análise de despesas
- E muito mais!

---

## 🔄 USO DIÁRIO (depois da instalação):

### Quando adicionar novos dados nas planilhas Excel:

**1. Processar:**
```bash
py -3.10 2-processamento\processar_dados.py
```

**2. Ver Dashboard:**
```bash
py -3.10 -m streamlit run 3-visualizacao\dashboard.py
```

**3. Gerar Relatório PDF:**
```bash
py -3.10 4-relatorios\gerar_relatorio.py
```

O PDF fica salvo em `4-relatorios/`

---

## 💡 ATALHOS - Criar arquivos .bat

Você pode criar atalhos para não precisar digitar comandos!

### Criar arquivo: `PROCESSAR.bat`

1. Clique com botão direito na pasta do projeto
2. Novo → Arquivo de texto
3. Renomeie para `PROCESSAR.bat`
4. Edite com Bloco de Notas e cole:

```batch
@echo off
echo.
echo ========================================
echo   PROCESSANDO DADOS
echo ========================================
echo.
py -3.10 2-processamento\processar_dados.py
echo.
pause
```

### Criar arquivo: `DASHBOARD.bat`

```batch
@echo off
echo.
echo ========================================
echo   ABRINDO DASHBOARD
echo ========================================
echo.
echo O dashboard vai abrir no navegador...
echo Aguarde 10-30 segundos
echo.
echo Para fechar: Pressione Ctrl+C aqui
echo.
py -3.10 -m streamlit run 3-visualizacao\dashboard.py
```

### Criar arquivo: `RELATORIO.bat`

```batch
@echo off
echo.
echo ========================================
echo   GERANDO RELATORIO PDF
echo ========================================
echo.
py -3.10 4-relatorios\gerar_relatorio.py
echo.
echo O relatorio foi salvo em 4-relatorios/
echo.
pause
```

Depois é só dar **duplo clique** neles! 🖱️

---

## 📝 FLUXO COMPLETO DE TRABALHO:

```
1. Preencher planilhas Excel (pasta 1-coleta/)
   ↓
2. PROCESSAR.bat (ou comando processar)
   ↓
3. DASHBOARD.bat (ou comando dashboard)
   ↓
4. Analisar dados no navegador
   ↓
5. RELATORIO.bat (gera PDF)
```

---

## ❌ PROBLEMAS COMUNS:

### "Módulo não encontrado"
➡️ Não instalou as dependências. Rode o passo 2️⃣ novamente

### "Arquivo não encontrado"
➡️ Está na pasta errada. Certifique-se que está em `DataOps-Local/`

Digite `dir` no CMD e veja se aparecem os arquivos:
- requirements.txt
- README.md
- gerar_exemplo.py
- etc.

### Dashboard não abre
➡️ Aguarde 30 segundos. Se não abrir, copie o link que aparece no CMD e cole no navegador:
```
Local URL: http://localhost:8501
```

### Janela fecha rápido
➡️ Use os arquivos .bat com `pause` no final

### "py não é reconhecido"
➡️ Use `python` em vez de `py -3.10`:
```bash
python -m streamlit run 3-visualizacao\dashboard.py
```

---

## 📁 ONDE ESTÃO OS ARQUIVOS:

- **Planilhas para preencher:** `1-coleta/`
- **Relatórios PDF gerados:** `4-relatorios/`
- **Banco de dados:** `dados/dataops.db`
- **Documentação:** `documentacao/`

---

## 🎯 RESUMO DOS COMANDOS:

```bash
# Instalar (só 1 vez)
py -3.10 -m pip install --user plotly streamlit pandas openpyxl reportlab sqlalchemy python-dateutil

# Gerar exemplo
py -3.10 gerar_exemplo.py

# Processar dados
py -3.10 2-processamento\processar_dados.py

# Dashboard
py -3.10 -m streamlit run 3-visualizacao\dashboard.py

# Relatório PDF
py -3.10 4-relatorios\gerar_relatorio.py
```

---

## 🔧 COMANDOS ÚTEIS:

### Verificar versão do Python:
```bash
py -3.10 --version
```

### Listar pacotes instalados:
```bash
py -3.10 -m pip list
```

### Ver conteúdo da pasta atual:
```bash
dir
```

### Navegar entre pastas:
```bash
cd nome-da-pasta      # Entrar em pasta
cd ..                 # Voltar uma pasta
```

### Limpar tela do CMD:
```bash
cls
```

---

## 📚 PRÓXIMOS PASSOS:

### 1. Entenda as Planilhas

Abra os arquivos Excel em `1-coleta/` e veja os exemplos:
- `Template_Receitas.xlsx` - Como registrar serviços
- `Template_Despesas.xlsx` - Como registrar despesas
- `Template_Profissionais.xlsx` - Cadastro de funcionários
- `Template_Servicos.xlsx` - Lista de serviços oferecidos

### 2. Customize para seu Negócio

- Edite `Template_Profissionais.xlsx` com seus funcionários reais
- Edite `Template_Servicos.xlsx` com seus serviços e preços
- Comece a registrar receitas e despesas reais

### 3. Use Diariamente

- **Manhã:** Abra `Template_Receitas.xlsx`
- **Durante o dia:** Registre cada serviço realizado
- **Fim do dia:** Processe os dados e veja o dashboard
- **Fim do mês:** Gere o relatório PDF

### 4. Faça Backup

Copie a pasta `DataOps-Local` completa para:
- Pen drive
- Google Drive
- OneDrive
- Qualquer local seguro

---

## 🎓 APRENDA MAIS:

Leia os documentos na pasta `documentacao/`:

1. **INICIO_RAPIDO.md** - Tutorial completo
2. **COMO_PREENCHER_PLANILHAS.md** - Guia detalhado das planilhas
3. **SOLUCAO_PROBLEMAS.md** - Troubleshooting completo

---

## 💡 DICAS PROFISSIONAIS:

### Para Salão/Barbearia:
- Registre cada atendimento em tempo real
- Anote cliente VIP nas observações
- Acompanhe comissão dos profissionais semanalmente

### Para Restaurante:
- Registre vendas por turno (almoço/jantar)
- Separe despesas por categoria (ingredientes, gás, etc)
- Analise dias/horários de pico

### Para Prestadores de Serviço:
- Use "Cliente" para identificar projetos
- Anote tempo gasto nas observações
- Calcule rentabilidade por tipo de serviço

---

## ✅ CHECKLIST FINAL:

- [ ] CMD aberto na pasta correta (`DataOps-Local`)
- [ ] Dependências instaladas (passo 2️⃣)
- [ ] Dados de exemplo gerados (passo 3️⃣)
- [ ] Dados processados (passo 4️⃣)
- [ ] Dashboard funcionando (passo 5️⃣)
- [ ] Atalhos .bat criados (opcional)
- [ ] Documentação lida
- [ ] Backup configurado

---

##  PRONTO!

Agora você tem um sistema profissional de análise de dados rodando no seu computador!

**Características:**
- ✅ 100% gratuito
- ✅ 100% local (seus dados não saem do computador)
- ✅ Fácil de usar
- ✅ Dashboards profissionais
- ✅ Relatórios automáticos

---

##  SUPORTE:

Se tiver dúvidas:
1. Consulte `documentacao/SOLUCAO_PROBLEMAS.md`
2. Releia este guia
3. Verifique se seguiu todos os passos na ordem

---

**Desenvolvido para democratizar análise de dados para pequenos negócios! 🚀**

**Versão:** 1.0.0  
**Licença:** MIT (Software Livre)  
**Última atualização:** 12/02/2025
