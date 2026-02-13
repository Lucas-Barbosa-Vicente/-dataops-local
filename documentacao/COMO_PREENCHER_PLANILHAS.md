# 📊 Guia Completo: Como Preencher as Planilhas

## 🎯 Visão Geral

As planilhas são a porta de entrada dos seus dados. Preencha-as corretamente e o sistema fará todo o resto!

---

## 📋 Template_Receitas.xlsx

### Quando usar?
Sempre que realizar um serviço e receber pagamento.

### Colunas e como preencher:

| Coluna | O que é? | Como preencher | Exemplo |
|--------|----------|----------------|---------|
| **Data** | Dia do serviço | Formato: DD/MM/AAAA | 15/02/2025 |
| **Tipo_Servico** | Qual serviço foi feito | Nome exato do serviço | Corte de Cabelo |
| **Profissional** | Quem fez o serviço | Nome completo | João Silva |
| **Cliente** | Nome do cliente | Pode ser "Cliente A" se preferir | Maria Santos |
| **Valor_Servico** | Quanto cobrou | Só números, use ponto para centavos | 50.00 |
| **Forma_Pagamento** | Como recebeu | Dinheiro / PIX / Débito / Crédito | PIX |
| **Observacoes** | Anotações extras | Qualquer comentário (opcional) | Cliente VIP |

### ⚠️ Atenção:
- Use sempre o **mesmo nome** para o profissional
- Use sempre o **mesmo nome** para cada tipo de serviço
- **NÃO** use vírgula nos valores, use ponto: ✅ 50.00 | ❌ 50,00

### Exemplo de preenchimento:

```
Data        | Tipo_Servico  | Profissional  | Cliente    | Valor_Servico | Forma_Pagamento | Observacoes
01/02/2025  | Corte Cabelo  | João Silva    | Cliente A  | 50.00         | Dinheiro        | 
02/02/2025  | Manicure      | Maria Santos  | Cliente B  | 35.00         | PIX             | Cliente frequente
03/02/2025  | Barba         | João Silva    | Cliente C  | 30.00         | Débito          |
```

---

## 💸 Template_Despesas.xlsx

### Quando usar?
Sempre que pagar alguma conta ou despesa do negócio.

### Colunas e como preencher:

| Coluna | O que é? | Como preencher | Exemplo |
|--------|----------|----------------|---------|
| **Data** | Dia do pagamento | Formato: DD/MM/AAAA | 05/02/2025 |
| **Categoria** | Tipo de despesa | Produtos / Aluguel / Energia / Salários / etc | Produtos |
| **Descricao** | O que foi comprado | Descrição curta | Shampoo profissional |
| **Valor** | Quanto pagou | Só números, use ponto | 120.00 |
| **Forma_Pagamento** | Como pagou | Dinheiro / PIX / Débito / Crédito / Boleto | Crédito |
| **Fornecedor** | De quem comprou | Nome do fornecedor | Distribuidora XYZ |
| **Observacoes** | Anotações | Qualquer comentário (opcional) | Promoção |

### 💡 Categorias sugeridas:
- **Produtos**: Materiais de trabalho (shampoo, tintas, etc)
- **Aluguel**: Valor do aluguel do estabelecimento
- **Energia**: Conta de luz
- **Água**: Conta de água
- **Salários**: Pagamento de funcionários
- **Marketing**: Anúncios, panfletos
- **Manutenção**: Reparos, limpeza
- **Impostos**: Taxas e impostos
- **Outros**: Demais despesas

### Exemplo de preenchimento:

```
Data        | Categoria  | Descricao           | Valor    | Forma_Pagamento | Fornecedor        | Observacoes
01/02/2025  | Produtos   | Shampoo 5L          | 120.00   | Crédito         | Distribuidora XYZ | 
05/02/2025  | Aluguel    | Aluguel fevereiro   | 1500.00  | Transferência   | Imobiliária ABC   |
10/02/2025  | Energia    | Conta de luz        | 250.00   | Boleto          | Cia Energia       |
```

---

## 👥 Template_Profissionais.xlsx

### Quando usar?
Ao cadastrar um novo funcionário ou atualizar informações.

### Colunas e como preencher:

| Coluna | O que é? | Como preencher | Exemplo |
|--------|----------|----------------|---------|
| **Nome_Profissional** | Nome completo | Use sempre o mesmo nome | João Silva |
| **Funcao** | Cargo | Cabeleireiro / Manicure / Barbeiro / etc | Cabeleireiro |
| **Tipo_Contrato** | Como é pago | Percentual ou Fixo | Percentual |
| **Percentual_Comissao** | % que leva | Número de 0 a 100 (só se Percentual) | 60 |
| **Salario_Fixo** | Salário mensal | Valor fixo (só se Fixo) | 2500 |
| **Status** | Está trabalhando? | Ativo ou Inativo | Ativo |
| **Data_Admissao** | Quando começou | Formato: DD/MM/AAAA | 01/01/2024 |

### 💡 Tipos de Contrato:

**Percentual:**
- Funcionário ganha % do que vende
- Exemplo: 60% de R$ 100 = R$ 60 para o profissional
- Preencha `Percentual_Comissao` e deixe `Salario_Fixo` em 0

**Fixo:**
- Funcionário ganha salário mensal fixo
- Preencha `Salario_Fixo` e deixe `Percentual_Comissao` em 0

### Exemplo de preenchimento:

```
Nome_Profissional | Funcao       | Tipo_Contrato | Percentual_Comissao | Salario_Fixo | Status | Data_Admissao
João Silva        | Cabeleireiro | Percentual    | 60                  | 0            | Ativo  | 01/01/2024
Maria Santos      | Manicure     | Percentual    | 50                  | 0            | Ativo  | 01/03/2024
Pedro Oliveira    | Barbeiro     | Fixo          | 0                   | 2500         | Ativo  | 01/06/2024
```

---

## 💼 Template_Servicos.xlsx

### Quando usar?
Ao definir ou atualizar a lista de serviços oferecidos.

### Colunas e como preencher:

| Coluna | O que é? | Como preencher | Exemplo |
|--------|----------|----------------|---------|
| **Nome_Servico** | Nome do serviço | Use sempre o mesmo nome | Corte de Cabelo Masculino |
| **Preco_Base** | Preço padrão | Valor cobrado normalmente | 50.00 |
| **Tempo_Medio_Minutos** | Duração | Quantos minutos leva | 30 |
| **Categoria** | Tipo de serviço | Cabelo / Unhas / Barba / etc | Cabelo |
| **Status** | Está oferecendo? | Ativo ou Inativo | Ativo |

### Exemplo de preenchimento:

```
Nome_Servico              | Preco_Base | Tempo_Medio_Minutos | Categoria | Status
Corte de Cabelo Masculino | 50.00      | 30                  | Cabelo    | Ativo
Corte de Cabelo Feminino  | 80.00      | 60                  | Cabelo    | Ativo
Manicure                  | 35.00      | 45                  | Unhas     | Ativo
Pedicure                  | 40.00      | 60                  | Unhas     | Ativo
Barba                     | 30.00      | 20                  | Barba     | Ativo
```

---

## ⚠️ REGRAS IMPORTANTES

### ✅ O que FAZER:

1. **Mantenha os nomes consistentes**
   - Se João é "João Silva", sempre use "João Silva"
   - ❌ Não misture: João Silva, Joao Silva, J. Silva

2. **Use sempre o formato de data correto**
   - ✅ 15/02/2025
   - ❌ 15-02-2025 ou 2025/02/15

3. **Valores com ponto, não vírgula**
   - ✅ 150.00
   - ❌ 150,00

4. **Adicione novas linhas abaixo**
   - Não sobrescreva os dados antigos
   - Cada linha = um novo registro

### ❌ O que NÃO fazer:

1. **NÃO renomeie as colunas**
   - O sistema precisa dos nomes exatos

2. **NÃO delete colunas**
   - Mesmo que não use, mantenha

3. **NÃO use fórmulas do Excel**
   - Apenas valores simples

4. **NÃO delete as planilhas exemplo**
   - Use-as como referência

---

## 🔄 Fluxo de Trabalho Ideal

```
🌅 MANHÃ
├─ Abra Template_Receitas.xlsx
└─ Deixe aberto para ir preenchendo

💼 DURANTE O DIA
├─ A cada serviço → Preencha uma linha em Receitas
└─ A cada despesa → Preencha uma linha em Despesas

🌙 FIM DO DIA
├─ Revise os dados do dia
├─ Salve as planilhas
└─ (Opcional) Processe e veja o dashboard

📊 SEMANAL
├─ Processe os dados
└─ Analise o dashboard

📈 MENSAL
└─ Gere relatório PDF completo
```

---

## 🆘 Problemas Comuns

### "Erro ao processar receitas"
➡️ Verifique se todas as datas estão no formato DD/MM/AAAA  
➡️ Confira se os valores usam ponto, não vírgula

### "Profissional não encontrado"
➡️ Certifique-se que o nome está igual em todas as planilhas  
➡️ Cadastre o profissional em Template_Profissionais.xlsx

### "Valores estranhos no relatório"
➡️ Verifique se não há espaços extras nos nomes  
➡️ Confira se os valores estão corretos (sem vírgula)

---

## 💾 Backup dos Dados

### Sempre faça backup!

1. **Semanalmente:** Copie a pasta `1-coleta` para um pen drive
2. **Mensalmente:** Copie toda a pasta `DataOps-Local`
3. **Use nuvem:** Salve também no Google Drive ou Dropbox

---

## 🎓 Dicas Profissionais

### 📝 Para Receitas:
- Anote em tempo real para não esquecer
- Use códigos para clientes sensíveis (Cliente A, B, C)
- Marque clientes VIP nas observações

### 💰 Para Despesas:
- Guarde os comprovantes por categoria
- Anote despesas pequenas também
- Separe despesas pessoais das do negócio

### 👥 Para Profissionais:
- Atualize quando mudar comissão
- Marque como "Inativo" quem saiu
- Mantenha histórico completo

---

**Agora você está pronto para usar o sistema! 🚀**

Qualquer dúvida, consulte o arquivo INICIO_RAPIDO.md ou entre em contato com o suporte.
