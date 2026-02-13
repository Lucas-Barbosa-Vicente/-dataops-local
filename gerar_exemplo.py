"""
DataOps Local - Gerador de Dados de Exemplo
Autor: Sistema DataOps
Descrição: Gera dados fictícios para demonstração do sistema
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def gerar_dados_exemplo():
    """Gera dados de exemplo para demonstração"""
    
    print("🎲 Gerando dados de exemplo para demonstração...\n")
    
    # Configurações
    dias = 30
    data_final = datetime.now()
    data_inicial = data_final - timedelta(days=dias)
    
    # Dados base
    profissionais = [
        {'nome': 'João Silva', 'funcao': 'Cabeleireiro', 'comissao': 60},
        {'nome': 'Maria Santos', 'funcao': 'Manicure', 'comissao': 50},
        {'nome': 'Pedro Oliveira', 'funcao': 'Barbeiro', 'comissao': 55},
        {'nome': 'Ana Costa', 'funcao': 'Esteticista', 'comissao': 65}
    ]
    
    servicos = {
        'Corte Masculino': {'preco': 50, 'tempo': 30, 'categoria': 'Cabelo'},
        'Corte Feminino': {'preco': 80, 'tempo': 60, 'categoria': 'Cabelo'},
        'Barba': {'preco': 30, 'tempo': 20, 'categoria': 'Barba'},
        'Manicure': {'preco': 35, 'tempo': 45, 'categoria': 'Unhas'},
        'Pedicure': {'preco': 40, 'tempo': 60, 'categoria': 'Unhas'},
        'Luzes': {'preco': 150, 'tempo': 120, 'categoria': 'Cabelo'},
        'Hidratação': {'preco': 60, 'tempo': 45, 'categoria': 'Cabelo'},
        'Design Sobrancelha': {'preco': 25, 'tempo': 20, 'categoria': 'Estética'}
    }
    
    formas_pagamento = ['Dinheiro', 'PIX', 'Débito', 'Crédito']
    
    # Gerar Receitas
    print("📊 Gerando receitas...")
    receitas = []
    
    for dia in range(dias):
        data_atual = data_inicial + timedelta(days=dia)
        
        # Dia da semana (mais movimento em sábado)
        dia_semana = data_atual.weekday()
        
        # Quantidade de serviços por dia (mais em sábado)
        if dia_semana == 5:  # Sábado
            num_servicos = random.randint(15, 25)
        elif dia_semana == 6:  # Domingo - fechado
            num_servicos = 0
        else:
            num_servicos = random.randint(8, 15)
        
        for _ in range(num_servicos):
            servico = random.choice(list(servicos.keys()))
            profissional = random.choice(profissionais)
            
            # Variação de preço (±10%)
            preco_base = servicos[servico]['preco']
            preco_final = preco_base * random.uniform(0.9, 1.1)
            
            receitas.append({
                'Data': data_atual.strftime('%d/%m/%Y'),
                'Tipo_Servico': servico,
                'Profissional': profissional['nome'],
                'Cliente': f'Cliente {random.randint(1, 100):03d}',
                'Valor_Servico': round(preco_final, 2),
                'Forma_Pagamento': random.choice(formas_pagamento),
                'Observacoes': random.choice(['', '', '', 'VIP', 'Retorno'])
            })
    
    df_receitas = pd.DataFrame(receitas)
    print(f"   ✅ {len(receitas)} receitas geradas")
    
    # Gerar Despesas
    print("💸 Gerando despesas...")
    despesas = []
    
    # Despesas fixas mensais
    despesas_fixas = [
        {'categoria': 'Aluguel', 'descricao': 'Aluguel do salão', 'valor': 2500, 'fornecedor': 'Imobiliária Central'},
        {'categoria': 'Energia', 'descricao': 'Conta de luz', 'valor': random.randint(350, 450), 'fornecedor': 'Companhia de Energia'},
        {'categoria': 'Água', 'descricao': 'Conta de água', 'valor': random.randint(80, 120), 'fornecedor': 'Companhia de Água'},
        {'categoria': 'Internet', 'descricao': 'Internet/Telefone', 'valor': 150, 'fornecedor': 'Telecom XYZ'},
    ]
    
    for desp in despesas_fixas:
        despesas.append({
            'Data': (data_inicial + timedelta(days=5)).strftime('%d/%m/%Y'),
            'Categoria': desp['categoria'],
            'Descricao': desp['descricao'],
            'Valor': desp['valor'],
            'Forma_Pagamento': random.choice(['Boleto', 'Débito Automático']),
            'Fornecedor': desp['fornecedor'],
            'Observacoes': ''
        })
    
    # Despesas variáveis
    produtos = [
        'Shampoo profissional 5L',
        'Condicionador 5L',
        'Tintura cores variadas',
        'Óxidante',
        'Esmaltes sortidos',
        'Lâminas de barbear',
        'Toalhas',
        'Acetona',
        'Algodão',
        'Luvas descartáveis'
    ]
    
    for _ in range(15):
        despesas.append({
            'Data': (data_inicial + timedelta(days=random.randint(0, dias))).strftime('%d/%m/%Y'),
            'Categoria': 'Produtos',
            'Descricao': random.choice(produtos),
            'Valor': round(random.uniform(50, 300), 2),
            'Forma_Pagamento': random.choice(['Crédito', 'Débito', 'Dinheiro']),
            'Fornecedor': random.choice(['Distribuidora ABC', 'Fornecedor XYZ', 'Loja de Produtos']),
            'Observacoes': ''
        })
    
    # Outras despesas
    outras = [
        {'cat': 'Marketing', 'desc': 'Anúncios Facebook/Instagram', 'valor': 200},
        {'cat': 'Manutenção', 'desc': 'Conserto cadeira', 'valor': 150},
        {'cat': 'Impostos', 'desc': 'MEI - DAS', 'valor': 67},
    ]
    
    for outra in outras:
        despesas.append({
            'Data': (data_inicial + timedelta(days=random.randint(0, dias))).strftime('%d/%m/%Y'),
            'Categoria': outra['cat'],
            'Descricao': outra['desc'],
            'Valor': outra['valor'],
            'Forma_Pagamento': random.choice(formas_pagamento),
            'Fornecedor': 'Diversos',
            'Observacoes': ''
        })
    
    df_despesas = pd.DataFrame(despesas)
    print(f"   ✅ {len(despesas)} despesas geradas")
    
    # Gerar Profissionais
    print("👥 Gerando cadastro de profissionais...")
    df_profissionais = pd.DataFrame([
        {
            'Nome_Profissional': prof['nome'],
            'Funcao': prof['funcao'],
            'Tipo_Contrato': 'Percentual',
            'Percentual_Comissao': prof['comissao'],
            'Salario_Fixo': 0,
            'Status': 'Ativo',
            'Data_Admissao': (data_inicial - timedelta(days=random.randint(30, 365))).strftime('%d/%m/%Y')
        }
        for prof in profissionais
    ])
    print(f"   ✅ {len(profissionais)} profissionais cadastrados")
    
    # Gerar Serviços
    print("💼 Gerando catálogo de serviços...")
    df_servicos = pd.DataFrame([
        {
            'Nome_Servico': nome,
            'Preco_Base': info['preco'],
            'Tempo_Medio_Minutos': info['tempo'],
            'Categoria': info['categoria'],
            'Status': 'Ativo'
        }
        for nome, info in servicos.items()
    ])
    print(f"   ✅ {len(servicos)} serviços cadastrados")
    
    # Salvar arquivos
    print("\n💾 Salvando templates com dados de exemplo...")
    
    with pd.ExcelWriter('1-coleta/Template_Receitas.xlsx', engine='openpyxl') as writer:
        df_receitas.to_excel(writer, sheet_name='Receitas', index=False)
    print("   ✅ Template_Receitas.xlsx")
    
    with pd.ExcelWriter('1-coleta/Template_Despesas.xlsx', engine='openpyxl') as writer:
        df_despesas.to_excel(writer, sheet_name='Despesas', index=False)
    print("   ✅ Template_Despesas.xlsx")
    
    with pd.ExcelWriter('1-coleta/Template_Profissionais.xlsx', engine='openpyxl') as writer:
        df_profissionais.to_excel(writer, sheet_name='Profissionais', index=False)
    print("   ✅ Template_Profissionais.xlsx")
    
    with pd.ExcelWriter('1-coleta/Template_Servicos.xlsx', engine='openpyxl') as writer:
        df_servicos.to_excel(writer, sheet_name='Servicos', index=False)
    print("   ✅ Template_Servicos.xlsx")
    
    # Estatísticas
    print("\n📈 RESUMO DOS DADOS GERADOS:")
    print("="*50)
    total_receitas = df_receitas['Valor_Servico'].sum()
    total_despesas = df_despesas['Valor'].sum()
    print(f"💵 Total Receitas: R$ {total_receitas:,.2f}")
    print(f"📉 Total Despesas: R$ {total_despesas:,.2f}")
    print(f"💰 Saldo: R$ {total_receitas - total_despesas:,.2f}")
    print(f"📊 Quantidade de serviços: {len(receitas)}")
    print(f"🎯 Ticket médio: R$ {df_receitas['Valor_Servico'].mean():.2f}")
    print("="*50)
    
    print("\n✅ Dados de exemplo gerados com sucesso!")
    print("\n📝 PRÓXIMOS PASSOS:")
    print("   1. Execute: python 2-processamento/processar_dados.py")
    print("   2. Depois: streamlit run 3-visualizacao/dashboard.py")

if __name__ == "__main__":
    print("\n🎲 DATAOPS LOCAL - GERADOR DE DADOS DE EXEMPLO")
    print("="*50)
    print("\nEste script vai gerar dados fictícios de 30 dias para demonstração.")
    print("Os dados atuais serão SUBSTITUÍDOS.\n")
    
    resposta = input("Deseja continuar? (s/n): ")
    
    if resposta.lower() == 's':
        gerar_dados_exemplo()
    else:
        print("\n❌ Operação cancelada")
