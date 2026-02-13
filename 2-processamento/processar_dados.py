"""
DataOps Local - Script de Processamento de Dados
Autor: Sistema DataOps
Descrição: Processa dados das planilhas Excel e carrega no banco SQLite
"""

import pandas as pd
import sqlite3
from datetime import datetime
import os
import sys

class DataProcessor:
    def __init__(self, db_path='dados/dataops.db'):
        self.db_path = db_path
        self.conn = None
        
    def conectar_banco(self):
        """Conecta ao banco de dados SQLite"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            print("✅ Conexão com banco de dados estabelecida")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco: {e}")
            return False
    
    def criar_tabelas(self):
        """Cria as tabelas necessárias no banco"""
        try:
            cursor = self.conn.cursor()
            
            # Tabela de Receitas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS receitas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data DATE NOT NULL,
                    tipo_servico TEXT NOT NULL,
                    profissional TEXT NOT NULL,
                    cliente TEXT,
                    valor_servico REAL NOT NULL,
                    forma_pagamento TEXT,
                    observacoes TEXT,
                    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de Despesas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS despesas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data DATE NOT NULL,
                    categoria TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    valor REAL NOT NULL,
                    forma_pagamento TEXT,
                    fornecedor TEXT,
                    observacoes TEXT,
                    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de Profissionais
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS profissionais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_profissional TEXT UNIQUE NOT NULL,
                    funcao TEXT,
                    tipo_contrato TEXT,
                    percentual_comissao REAL,
                    salario_fixo REAL,
                    status TEXT,
                    data_admissao DATE,
                    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de Serviços
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS servicos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_servico TEXT UNIQUE NOT NULL,
                    preco_base REAL NOT NULL,
                    tempo_medio_minutos INTEGER,
                    categoria TEXT,
                    status TEXT,
                    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            print("✅ Tabelas criadas/verificadas com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return False
    
    def processar_receitas(self, arquivo_excel):
        """Processa e importa dados de receitas"""
        try:
            df = pd.read_excel(arquivo_excel, sheet_name='Receitas')
            
            # Converter data para formato adequado
            df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
            
            # Renomear colunas para match com banco
            df.columns = df.columns.str.lower()
            
            # Importar para o banco
            df.to_sql('receitas', self.conn, if_exists='append', index=False)
            
            print(f"✅ {len(df)} receitas importadas")
            return len(df)
            
        except Exception as e:
            print(f"❌ Erro ao processar receitas: {e}")
            return 0
    
    def processar_despesas(self, arquivo_excel):
        """Processa e importa dados de despesas"""
        try:
            df = pd.read_excel(arquivo_excel, sheet_name='Despesas')
            
            # Converter data para formato adequado
            df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
            
            # Renomear colunas para match com banco
            df.columns = df.columns.str.lower()
            
            # Importar para o banco
            df.to_sql('despesas', self.conn, if_exists='append', index=False)
            
            print(f"✅ {len(df)} despesas importadas")
            return len(df)
            
        except Exception as e:
            print(f"❌ Erro ao processar despesas: {e}")
            return 0
    
    def processar_profissionais(self, arquivo_excel):
        """Processa e importa dados de profissionais"""
        try:
            df = pd.read_excel(arquivo_excel, sheet_name='Profissionais')
            
            # Converter data
            df['Data_Admissao'] = pd.to_datetime(df['Data_Admissao'], format='%d/%m/%Y')
            
            # Renomear colunas
            df.columns = df.columns.str.lower()
            
            # Importar para o banco (substituindo dados antigos)
            df.to_sql('profissionais', self.conn, if_exists='replace', index=False)
            
            print(f"✅ {len(df)} profissionais importados")
            return len(df)
            
        except Exception as e:
            print(f"❌ Erro ao processar profissionais: {e}")
            return 0
    
    def processar_servicos(self, arquivo_excel):
        """Processa e importa dados de serviços"""
        try:
            df = pd.read_excel(arquivo_excel, sheet_name='Servicos')
            
            # Renomear colunas
            df.columns = df.columns.str.lower()
            
            # Importar para o banco (substituindo dados antigos)
            df.to_sql('servicos', self.conn, if_exists='replace', index=False)
            
            print(f"✅ {len(df)} serviços importados")
            return len(df)
            
        except Exception as e:
            print(f"❌ Erro ao processar serviços: {e}")
            return 0
    
    def gerar_relatorio_importacao(self):
        """Gera resumo dos dados importados"""
        try:
            cursor = self.conn.cursor()
            
            print("\n" + "="*50)
            print("RESUMO DOS DADOS IMPORTADOS")
            print("="*50)
            
            # Total de receitas
            cursor.execute("SELECT COUNT(*), SUM(valor_servico) FROM receitas")
            qtd_receitas, total_receitas = cursor.fetchone()
            print(f"📊 Receitas: {qtd_receitas} registros | Total: R$ {total_receitas:,.2f}")
            
            # Total de despesas
            cursor.execute("SELECT COUNT(*), SUM(valor) FROM despesas")
            qtd_despesas, total_despesas = cursor.fetchone()
            print(f"📊 Despesas: {qtd_despesas} registros | Total: R$ {total_despesas:,.2f}")
            
            # Profissionais ativos
            cursor.execute("SELECT COUNT(*) FROM profissionais WHERE status = 'Ativo'")
            qtd_prof = cursor.fetchone()[0]
            print(f"👥 Profissionais Ativos: {qtd_prof}")
            
            # Serviços ativos
            cursor.execute("SELECT COUNT(*) FROM servicos WHERE status = 'Ativo'")
            qtd_serv = cursor.fetchone()[0]
            print(f"💼 Serviços Disponíveis: {qtd_serv}")
            
            # Saldo
            saldo = (total_receitas or 0) - (total_despesas or 0)
            print(f"\n💰 Saldo: R$ {saldo:,.2f}")
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório: {e}")
    
    def fechar_conexao(self):
        """Fecha conexão com banco"""
        if self.conn:
            self.conn.close()
            print("✅ Conexão com banco fechada")

def main():
    """Função principal de processamento"""
    print("\n🚀 DATAOPS LOCAL - PROCESSAMENTO DE DADOS")
    print("="*50 + "\n")
    
    # Inicializar processador
    processor = DataProcessor()
    
    # Conectar ao banco
    if not processor.conectar_banco():
        sys.exit(1)
    
    # Criar tabelas
    if not processor.criar_tabelas():
        sys.exit(1)
    
    # Processar arquivos
    print("\n📂 Processando arquivos Excel...\n")
    
    base_path = '1-coleta/'
    
    # Processar cada tipo de arquivo
    processor.processar_profissionais(f'{base_path}Template_Profissionais.xlsx')
    processor.processar_servicos(f'{base_path}Template_Servicos.xlsx')
    processor.processar_receitas(f'{base_path}Template_Receitas.xlsx')
    processor.processar_despesas(f'{base_path}Template_Despesas.xlsx')
    
    # Gerar relatório
    processor.gerar_relatorio_importacao()
    
    # Fechar conexão
    processor.fechar_conexao()
    
    print("✅ Processamento concluído com sucesso!")

if __name__ == "__main__":
    main()
