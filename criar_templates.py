import pandas as pd
from datetime import datetime, timedelta
import random

# Template de Receitas
receitas_template = pd.DataFrame({
    'Data': ['01/02/2025', '02/02/2025', '03/02/2025'],
    'Tipo_Servico': ['Corte de Cabelo', 'Manicure', 'Corte de Cabelo'],
    'Profissional': ['João Silva', 'Maria Santos', 'João Silva'],
    'Cliente': ['Cliente A', 'Cliente B', 'Cliente C'],
    'Valor_Servico': [50.00, 35.00, 50.00],
    'Forma_Pagamento': ['Dinheiro', 'PIX', 'Cartão Débito'],
    'Observacoes': ['', 'Cliente frequente', '']
})

# Template de Despesas
despesas_template = pd.DataFrame({
    'Data': ['01/02/2025', '05/02/2025', '10/02/2025'],
    'Categoria': ['Produtos', 'Aluguel', 'Energia'],
    'Descricao': ['Shampoo profissional', 'Aluguel do salão', 'Conta de luz'],
    'Valor': [120.00, 1500.00, 250.00],
    'Forma_Pagamento': ['Cartão Crédito', 'Transferência', 'Boleto'],
    'Fornecedor': ['Distribuidora XYZ', 'Imobiliária ABC', 'Companhia Energia'],
    'Observacoes': ['', '', '']
})

# Template de Profissionais
profissionais_template = pd.DataFrame({
    'Nome_Profissional': ['João Silva', 'Maria Santos', 'Pedro Oliveira'],
    'Funcao': ['Cabeleireiro', 'Manicure', 'Barbeiro'],
    'Tipo_Contrato': ['Percentual', 'Percentual', 'Fixo'],
    'Percentual_Comissao': [60, 50, 0],
    'Salario_Fixo': [0, 0, 2500],
    'Status': ['Ativo', 'Ativo', 'Ativo'],
    'Data_Admissao': ['01/01/2024', '01/03/2024', '01/06/2024']
})

# Template de Serviços
servicos_template = pd.DataFrame({
    'Nome_Servico': ['Corte de Cabelo Masculino', 'Corte de Cabelo Feminino', 'Manicure', 'Pedicure', 'Barba'],
    'Preco_Base': [50.00, 80.00, 35.00, 40.00, 30.00],
    'Tempo_Medio_Minutos': [30, 60, 45, 60, 20],
    'Categoria': ['Cabelo', 'Cabelo', 'Unhas', 'Unhas', 'Barba'],
    'Status': ['Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo']
})

# Salvar templates
with pd.ExcelWriter('/home/claude/DataOps-Local/1-coleta/Template_Receitas.xlsx', engine='openpyxl') as writer:
    receitas_template.to_excel(writer, sheet_name='Receitas', index=False)

with pd.ExcelWriter('/home/claude/DataOps-Local/1-coleta/Template_Despesas.xlsx', engine='openpyxl') as writer:
    despesas_template.to_excel(writer, sheet_name='Despesas', index=False)

with pd.ExcelWriter('/home/claude/DataOps-Local/1-coleta/Template_Profissionais.xlsx', engine='openpyxl') as writer:
    profissionais_template.to_excel(writer, sheet_name='Profissionais', index=False)

with pd.ExcelWriter('/home/claude/DataOps-Local/1-coleta/Template_Servicos.xlsx', engine='openpyxl') as writer:
    servicos_template.to_excel(writer, sheet_name='Servicos', index=False)

print("✅ Templates Excel criados com sucesso!")
print("Localização: DataOps-Local/1-coleta/")
