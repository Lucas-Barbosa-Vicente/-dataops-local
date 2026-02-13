# 🔧 Guia de Solução de Problemas

## 📋 Índice
1. [Problemas de Instalação](#problemas-de-instalação)
2. [Problemas com Planilhas](#problemas-com-planilhas)
3. [Problemas de Processamento](#problemas-de-processamento)
4. [Problemas com Dashboard](#problemas-com-dashboard)
5. [Problemas com Relatórios](#problemas-com-relatórios)
6. [Perguntas Frequentes](#perguntas-frequentes)

---

## 🔴 Problemas de Instalação

### ❌ "Python não é reconhecido como comando"

**Causa:** Python não foi adicionado ao PATH do sistema

**Solução Windows:**
1. Desinstale o Python
2. Reinstale marcando a opção: ☑️ "Add Python to PATH"
3. Reinicie o computador

**Solução Mac/Linux:**
```bash
# Use python3 em vez de python
python3 --version
```

---

### ❌ "pip: comando não encontrado"

**Solução Windows:**
```bash
python -m pip install -r requirements.txt
```

**Solução Mac/Linux:**
```bash
python3 -m pip install -r requirements.txt
```

---

### ❌ "Erro ao instalar dependências"

**Causa:** Pode ser problema de conexão ou permissões

**Solução:**
```bash
# Tente instalar uma por vez
pip install pandas
pip install openpyxl
pip install streamlit
pip install plotly
pip install reportlab
pip install sqlalchemy
```

---

## 📊 Problemas com Planilhas

### ❌ "Erro ao abrir planilha no Excel"

**Causa:** Arquivo corrompido ou versão incompatível

**Solução:**
1. Delete a planilha problemática
2. Execute `python criar_templates.py`
3. Copie seus dados manualmente

---

### ❌ "Colunas não reconhecidas"

**Causa:** Colunas renomeadas ou deletadas

**Sintomas:**
```
KeyError: 'Data'
KeyError: 'Valor_Servico'
```

**Solução:**
1. Abra o template original (não modificado)
2. Compare as colunas
3. Renomeie para os nomes corretos:
   - Data
   - Tipo_Servico
   - Profissional
   - Valor_Servico
   - etc.

---

### ❌ "Dados não aparecem após preencher"

**Checklist:**
- [ ] Salvou a planilha Excel?
- [ ] Executou o processamento?
- [ ] Está na planilha correta (Receitas, não Sheet1)?
- [ ] Usou formato de data DD/MM/AAAA?
- [ ] Valores com ponto, não vírgula?

---

## ⚙️ Problemas de Processamento

### ❌ "FileNotFoundError: Template_Receitas.xlsx"

**Causa:** Arquivo não existe ou está em pasta errada

**Solução:**
```bash
# Verifique se está na pasta correta
cd DataOps-Local

# Verifique se os arquivos existem
ls 1-coleta/
# ou no Windows:
dir 1-coleta\
```

---

### ❌ "ValueError: time data does not match format"

**Causa:** Formato de data incorreto

**Exemplo Errado:**
```
2025/02/15    ❌
15-02-2025    ❌
15.02.2025    ❌
```

**Exemplo Correto:**
```
15/02/2025    ✅
```

**Solução:**
1. Abra a planilha Excel
2. Selecione a coluna Data
3. Use buscar/substituir:
   - Buscar: `/` ou `-` ou `.`
   - Substituir: `/`
4. Certifique-se do formato DD/MM/AAAA

---

### ❌ "ValueError: could not convert string to float"

**Causa:** Valores com vírgula ou texto em campo numérico

**Exemplo Errado:**
```
150,00    ❌
R$ 150    ❌
150 reais ❌
```

**Exemplo Correto:**
```
150.00    ✅
150       ✅
```

**Solução:**
1. Selecione coluna de valores
2. Buscar/substituir vírgula por ponto
3. Remova texto (R$, reais, etc)

---

### ❌ "IntegrityError: UNIQUE constraint failed"

**Causa:** Tentativa de inserir profissional/serviço duplicado

**Solução:**
1. Abra Template_Profissionais.xlsx ou Template_Servicos.xlsx
2. Verifique duplicatas
3. Mantenha apenas um registro por nome
4. Salve e processe novamente

---

## 📱 Problemas com Dashboard

### ❌ "ModuleNotFoundError: No module named 'streamlit'"

**Solução:**
```bash
pip install streamlit
```

---

### ❌ "Dashboard não abre no navegador"

**Solução Manual:**
1. Após executar o comando
2. Procure no terminal: `Local URL: http://localhost:8501`
3. Copie e cole este endereço no navegador

---

### ❌ "Dados não aparecem no dashboard"

**Checklist:**
- [ ] Processou os dados primeiro?
- [ ] Arquivo `dados/dataops.db` existe?
- [ ] Clicou no botão "Atualizar Dados"?

**Solução:**
```bash
# Re-processar dados
python 2-processamento/processar_dados.py

# Reiniciar dashboard
streamlit run 3-visualizacao/dashboard.py
```

---

### ❌ "Gráficos aparecem vazios"

**Causa:** Filtros muito restritivos ou sem dados no período

**Solução:**
1. Altere o filtro de período para "Tudo"
2. Altere filtro de profissional para "Todos"
3. Verifique se há dados nas planilhas

---

### ❌ "Erro: port 8501 is already in use"

**Causa:** Já existe um dashboard rodando

**Solução:**
```bash
# Feche o terminal anterior ou
streamlit run 3-visualizacao/dashboard.py --server.port 8502
```

---

## 📄 Problemas com Relatórios

### ❌ "Relatório PDF em branco"

**Causa:** Sem dados no período (últimos 30 dias)

**Solução:**
1. Verifique se há receitas/despesas nos últimos 30 dias
2. Ou adicione dados de exemplo:
```bash
python gerar_exemplo.py
python 2-processamento/processar_dados.py
python 4-relatorios/gerar_relatorio.py
```

---

### ❌ "Erro ao abrir PDF"

**Causa:** Arquivo corrompido ou em uso

**Solução:**
1. Feche o PDF se estiver aberto
2. Delete o arquivo PDF
3. Gere novamente

---

### ❌ "ModuleNotFoundError: No module named 'reportlab'"

**Solução:**
```bash
pip install reportlab
```

---

## ❓ Perguntas Frequentes

### P: Posso usar no Mac/Linux?
**R:** Sim! Use `python3` em vez de `python` nos comandos.

---

### P: Preciso de internet?
**R:** Não! Após a instalação, funciona 100% offline.

---

### P: Os dados são enviados para nuvem?
**R:** NÃO! Tudo fica no seu computador.

---

### P: Posso usar em várias empresas?
**R:** Sim! Crie uma pasta separada para cada empresa:
```
DataOps-Salao1/
DataOps-Salao2/
DataOps-Restaurante/
```

---

### P: Como faço backup?
**R:** Copie toda a pasta `DataOps-Local` para:
- Pen drive
- Google Drive
- Dropbox
- Qualquer local seguro

---

### P: Posso personalizar os relatórios?
**R:** Sim! Os scripts Python estão abertos para customização.

---

### P: Como atualizo o sistema?
**R:** Baixe a versão nova e copie sua pasta `dados/` e `1-coleta/`

---

### P: Posso adicionar mais profissionais?
**R:** Sim! Apenas adicione novas linhas em Template_Profissionais.xlsx

---

### P: Como adiciono novos serviços?
**R:** Adicione em Template_Servicos.xlsx e use o nome exato em Receitas

---

### P: O que significa "processamento de dados"?
**R:** É pegar os dados do Excel e organizar no banco de dados

---

### P: Preciso processar toda vez?
**R:** Apenas quando adicionar novos dados nas planilhas

---

### P: Posso deletar dados antigos?
**R:** Sim, mas faça backup primeiro!
1. Delete o arquivo `dados/dataops.db`
2. Processe novamente

---

### P: Como exporto para Excel?
**R:** No dashboard, cada tabela tem opção de download

---

## 🆘 Ainda com problemas?

### Opções:
1. **Re-instale do zero**
   - Delete a pasta
   - Baixe novamente
   - Execute `instalar.py`

2. **Use dados de exemplo**
   ```bash
   python gerar_exemplo.py
   ```

3. **Verifique logs**
   - Leia as mensagens de erro
   - Copie a mensagem e busque neste guia

4. **Entre em contato**
   - Descreva o problema
   - Envie print da tela
   - Mencione seu sistema (Windows/Mac/Linux)

---

## 📞 Informações de Suporte

**Antes de pedir ajuda, tenha em mãos:**
- Sistema operacional (Windows 10, Mac OS, etc)
- Versão do Python (`python --version`)
- Mensagem de erro completa
- Prints da tela

---

**Boa sorte! 🚀**
