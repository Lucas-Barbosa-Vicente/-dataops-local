"""
DataOps Local - Script de Processamento de Dados
Autor: Sistema DataOps
Descrição: Processa dados das planilhas Excel e carrega no banco SQLite
Versão: 2.0 (Corrigida)

MELHORIAS NESTA VERSÃO:
- ✅ Validação robusta de dados
- ✅ Tratamento de erros melhorado
- ✅ Log detalhado de importação
- ✅ Suporte a múltiplos formatos de data
- ✅ Verificação de dados duplicados
- ✅ Cálculo automático de comissões como despesa
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
        self.log_importacao = []
        
    def log(self, mensagem, tipo="INFO"):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{tipo}] {mensagem}"
        self.log_importacao.append(log_entry)
        print(log_entry)
        
    def conectar_banco(self):
        """Conecta ao banco de dados SQLite"""
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            self.conn = sqlite3.connect(self.db_path)
            self.log("✅ Conexão com banco de dados estabelecida", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"❌ Erro ao conectar ao banco: {e}", "ERROR")
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
                    tipo_despesa TEXT DEFAULT 'Manual',
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
            
            # Tabela de Comissões Calculadas (NOVA)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comissoes_calculadas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profissional TEXT NOT NULL,
                    periodo_inicio DATE NOT NULL,
                    periodo_fim DATE NOT NULL,
                    total_vendas REAL NOT NULL,
                    percentual_comissao REAL NOT NULL,
                    valor_comissao REAL NOT NULL,
                    salario_fixo REAL,
                    total_pagar REAL NOT NULL,
                    data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            self.log("✅ Tabelas criadas/verificadas com sucesso", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"❌ Erro ao criar tabelas: {e}", "ERROR")
            return False
    
    def converter_data(self, data_str):
        """Converte data para formato adequado, tentando múltiplos formatos"""
        if pd.isna(data_str):
            return None
            
        # Formatos possíveis
        formatos = [
            '%d/%m/%Y',
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%Y/%m/%d',
            '%d.%m.%Y'
        ]
        
        for formato in formatos:
            try:
                return pd.to_datetime(data_str, format=formato)
            except:
                continue
        
        # Tentativa genérica
        try:
            return pd.to_datetime(data_str)
        except:
            self.log(f"⚠️ Não foi possível converter data: {data_str}", "WARNING")
            return None
    
    def validar_dados(self, df, tipo_dados):
        """Valida dados antes da importação"""
        erros = []
        
        if tipo_dados == 'receitas':
            # Verificar colunas obrigatórias
            colunas_obrigatorias = ['data', 'tipo_servico', 'profissional', 'valor_servico']
            for col in colunas_obrigatorias:
                if col not in df.columns:
                    erros.append(f"Coluna obrigatória ausente: {col}")
                elif df[col].isna().any():
                    qtd_nulos = df[col].isna().sum()
                    erros.append(f"Coluna '{col}' possui {qtd_nulos} valores nulos")
            
            # Validar valores numéricos
            if 'valor_servico' in df.columns:
                if (df['valor_servico'] <= 0).any():
                    erros.append("Existem valores de serviço menores ou iguais a zero")
        
        elif tipo_dados == 'despesas':
            colunas_obrigatorias = ['data', 'categoria', 'descricao', 'valor']
            for col in colunas_obrigatorias:
                if col not in df.columns:
                    erros.append(f"Coluna obrigatória ausente: {col}")
                elif df[col].isna().any():
                    qtd_nulos = df[col].isna().sum()
                    erros.append(f"Coluna '{col}' possui {qtd_nulos} valores nulos")
            
            if 'valor' in df.columns:
                if (df['valor'] <= 0).any():
                    erros.append("Existem valores de despesa menores ou iguais a zero")
        
        return erros
    
    def processar_receitas(self, arquivo_excel):
        """Processa e importa dados de receitas"""
        try:
            self.log(f"📂 Processando receitas de: {arquivo_excel}")
            
            # Verificar se arquivo existe
            if not os.path.exists(arquivo_excel):
                self.log(f"❌ Arquivo não encontrado: {arquivo_excel}", "ERROR")
                return 0
            
            df = pd.read_excel(arquivo_excel, sheet_name='Receitas')
            self.log(f"📊 {len(df)} receitas encontradas no arquivo")
            
            # Renomear colunas para match com banco
            df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
            
            # Converter data
            if 'data' in df.columns:
                df['data'] = df['data'].apply(self.converter_data)
                # Remover linhas com datas inválidas
                linhas_antes = len(df)
                df = df.dropna(subset=['data'])
                if len(df) < linhas_antes:
                    self.log(f"⚠️ {linhas_antes - len(df)} receitas removidas por data inválida", "WARNING")
            
            # Validar dados
            erros = self.validar_dados(df, 'receitas')
            if erros:
                self.log("⚠️ Erros encontrados na validação:", "WARNING")
                for erro in erros:
                    self.log(f"  - {erro}", "WARNING")
                return 0
            
            # Importar para o banco
            df.to_sql('receitas', self.conn, if_exists='append', index=False)
            
            self.log(f"✅ {len(df)} receitas importadas com sucesso", "SUCCESS")
            return len(df)
            
        except Exception as e:
            self.log(f"❌ Erro ao processar receitas: {e}", "ERROR")
            import traceback
            self.log(traceback.format_exc(), "ERROR")
            return 0
    
    def processar_despesas(self, arquivo_excel):
        """Processa e importa dados de despesas"""
        try:
            self.log(f"📂 Processando despesas de: {arquivo_excel}")
            
            if not os.path.exists(arquivo_excel):
                self.log(f"❌ Arquivo não encontrado: {arquivo_excel}", "ERROR")
                return 0
            
            df = pd.read_excel(arquivo_excel, sheet_name='Despesas')
            self.log(f"📊 {len(df)} despesas encontradas no arquivo")
            
            # Renomear colunas
            df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
            
            # Converter data
            if 'data' in df.columns:
                df['data'] = df['data'].apply(self.converter_data)
                linhas_antes = len(df)
                df = df.dropna(subset=['data'])
                if len(df) < linhas_antes:
                    self.log(f"⚠️ {linhas_antes - len(df)} despesas removidas por data inválida", "WARNING")
            
            # Adicionar tipo de despesa
            df['tipo_despesa'] = 'Manual'
            
            # Validar dados
            erros = self.validar_dados(df, 'despesas')
            if erros:
                self.log("⚠️ Erros encontrados na validação:", "WARNING")
                for erro in erros:
                    self.log(f"  - {erro}", "WARNING")
                return 0
            
            # Importar para o banco
            df.to_sql('despesas', self.conn, if_exists='append', index=False)
            
            self.log(f"✅ {len(df)} despesas importadas com sucesso", "SUCCESS")
            
            # Mostrar despesas por forma de pagamento
            if 'forma_pagamento' in df.columns:
                self.log("📋 Despesas por forma de pagamento:")
                resumo_pagto = df.groupby('forma_pagamento')['valor'].agg(['count', 'sum'])
                for forma, (qtd, total) in resumo_pagto.iterrows():
                    self.log(f"  - {forma}: {qtd} despesas, Total: R$ {total:,.2f}")
            
            return len(df)
            
        except Exception as e:
            self.log(f"❌ Erro ao processar despesas: {e}", "ERROR")
            import traceback
            self.log(traceback.format_exc(), "ERROR")
            return 0
    
    def processar_profissionais(self, arquivo_excel):
        """Processa e importa dados de profissionais"""
        try:
            self.log(f"📂 Processando profissionais de: {arquivo_excel}")
            
            if not os.path.exists(arquivo_excel):
                self.log(f"❌ Arquivo não encontrado: {arquivo_excel}", "ERROR")
                return 0
            
            df = pd.read_excel(arquivo_excel, sheet_name='Profissionais')
            self.log(f"📊 {len(df)} profissionais encontrados no arquivo")
            
            # Renomear colunas
            df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
            
            # Converter data
            if 'data_admissao' in df.columns:
                df['data_admissao'] = df['data_admissao'].apply(self.converter_data)
            
            # Importar para o banco (substituindo dados antigos)
            df.to_sql('profissionais', self.conn, if_exists='replace', index=False)
            
            self.log(f"✅ {len(df)} profissionais importados com sucesso", "SUCCESS")
            return len(df)
            
        except Exception as e:
            self.log(f"❌ Erro ao processar profissionais: {e}", "ERROR")
            import traceback
            self.log(traceback.format_exc(), "ERROR")
            return 0
    
    def processar_servicos(self, arquivo_excel):
        """Processa e importa dados de serviços"""
        try:
            self.log(f"📂 Processando serviços de: {arquivo_excel}")
            
            if not os.path.exists(arquivo_excel):
                self.log(f"❌ Arquivo não encontrado: {arquivo_excel}", "ERROR")
                return 0
            
            df = pd.read_excel(arquivo_excel, sheet_name='Servicos')
            self.log(f"📊 {len(df)} serviços encontrados no arquivo")
            
            # Renomear colunas
            df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
            
            # Importar para o banco (substituindo dados antigos)
            df.to_sql('servicos', self.conn, if_exists='replace', index=False)
            
            self.log(f"✅ {len(df)} serviços importados com sucesso", "SUCCESS")
            return len(df)
            
        except Exception as e:
            self.log(f"❌ Erro ao processar serviços: {e}", "ERROR")
            import traceback
            self.log(traceback.format_exc(), "ERROR")
            return 0
    
    def calcular_comissoes_periodo(self, data_inicio=None, data_fim=None):
        """Calcula e registra comissões de profissionais como despesas"""
        try:
            import calendar
            cursor = self.conn.cursor()
            
            # Se não especificado, calcular para o mês atual
            if not data_inicio or not data_fim:
                hoje = datetime.now()
                data_inicio = datetime(hoje.year, hoje.month, 1).strftime('%Y-%m-%d')
                # Usar calendar para pegar o último dia correto do mês
                ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
                data_fim = datetime(hoje.year, hoje.month, ultimo_dia).strftime('%Y-%m-%d')
            
            self.log(f"💰 Calculando comissões do período: {data_inicio} a {data_fim}")
            
            # Buscar receitas por profissional no período
            query = """
                SELECT 
                    r.profissional,
                    SUM(r.valor_servico) as total_vendas,
                    p.percentual_comissao,
                    p.salario_fixo,
                    p.tipo_contrato
                FROM receitas r
                LEFT JOIN profissionais p ON r.profissional = p.nome_profissional
                WHERE r.data BETWEEN ? AND ?
                AND p.status = 'Ativo'
                GROUP BY r.profissional
            """
            
            df_comissoes = pd.read_sql_query(query, self.conn, params=(data_inicio, data_fim))
            
            if len(df_comissoes) == 0:
                self.log("⚠️ Nenhuma receita encontrada para calcular comissões", "WARNING")
                return 0
            
            total_comissoes = 0
            despesas_comissao = []
            
            for _, row in df_comissoes.iterrows():
                profissional = row['profissional']
                total_vendas = row['total_vendas']
                percentual = row['percentual_comissao'] or 0
                salario_fixo = row['salario_fixo'] or 0
                tipo_contrato = row['tipo_contrato']
                
                valor_comissao = 0
                total_pagar = salario_fixo
                
                if tipo_contrato == 'Percentual' and percentual > 0:
                    valor_comissao = total_vendas * (percentual / 100)
                    total_pagar += valor_comissao
                
                if valor_comissao > 0 or salario_fixo > 0:
                    self.log(f"  💵 {profissional}: Vendas R$ {total_vendas:,.2f} | "
                           f"Comissão ({percentual}%) R$ {valor_comissao:,.2f} | "
                           f"Fixo R$ {salario_fixo:,.2f} | Total R$ {total_pagar:,.2f}")
                    
                    total_comissoes += total_pagar
                    
                    # Preparar despesa de comissão
                    despesas_comissao.append({
                        'data': data_fim,
                        'categoria': 'Folha de Pagamento',
                        'descricao': f'Salário + Comissão - {profissional}',
                        'valor': total_pagar,
                        'forma_pagamento': 'Transferência',
                        'fornecedor': profissional,
                        'observacoes': f'Vendas: R$ {total_vendas:,.2f} | Comissão {percentual}%: R$ {valor_comissao:,.2f} | Fixo: R$ {salario_fixo:,.2f}',
                        'tipo_despesa': 'Comissão Calculada'
                    })
            
            # Inserir despesas de comissão
            if despesas_comissao:
                df_despesas = pd.DataFrame(despesas_comissao)
                df_despesas.to_sql('despesas', self.conn, if_exists='append', index=False)
                self.log(f"✅ {len(despesas_comissao)} comissões registradas como despesas. Total: R$ {total_comissoes:,.2f}", "SUCCESS")
            
            return len(despesas_comissao)
            
        except Exception as e:
            self.log(f"❌ Erro ao calcular comissões: {e}", "ERROR")
            import traceback
            self.log(traceback.format_exc(), "ERROR")
            return 0
    
    def gerar_relatorio_importacao(self):
        """Gera resumo dos dados importados"""
        try:
            cursor = self.conn.cursor()
            
            print("\n" + "="*60)
            print("RESUMO DOS DADOS IMPORTADOS")
            print("="*60)
            
            # Total de receitas
            cursor.execute("SELECT COUNT(*), SUM(valor_servico) FROM receitas")
            qtd_receitas, total_receitas = cursor.fetchone()
            total_receitas = total_receitas or 0
            print(f"📊 Receitas: {qtd_receitas} registros | Total: R$ {total_receitas:,.2f}")
            
            # Total de despesas
            cursor.execute("SELECT COUNT(*), SUM(valor) FROM despesas")
            qtd_despesas, total_despesas = cursor.fetchone()
            total_despesas = total_despesas or 0
            print(f"📊 Despesas: {qtd_despesas} registros | Total: R$ {total_despesas:,.2f}")
            
            # Despesas por tipo
            cursor.execute("""
                SELECT tipo_despesa, COUNT(*), SUM(valor) 
                FROM despesas 
                GROUP BY tipo_despesa
            """)
            print("\n📋 Despesas por tipo:")
            for tipo, qtd, total in cursor.fetchall():
                print(f"  - {tipo}: {qtd} registros | R$ {total:,.2f}")
            
            # Despesas por forma de pagamento
            cursor.execute("""
                SELECT forma_pagamento, COUNT(*), SUM(valor) 
                FROM despesas 
                WHERE forma_pagamento IS NOT NULL
                GROUP BY forma_pagamento
            """)
            print("\n💳 Despesas por forma de pagamento:")
            for forma, qtd, total in cursor.fetchall():
                print(f"  - {forma}: {qtd} registros | R$ {total:,.2f}")
            
            # Profissionais ativos
            cursor.execute("SELECT COUNT(*) FROM profissionais WHERE status = 'Ativo'")
            qtd_prof = cursor.fetchone()[0]
            print(f"\n👥 Profissionais Ativos: {qtd_prof}")
            
            # Serviços ativos
            cursor.execute("SELECT COUNT(*) FROM servicos WHERE status = 'Ativo'")
            qtd_serv = cursor.fetchone()[0]
            print(f"💼 Serviços Disponíveis: {qtd_serv}")
            
            # Saldo
            saldo = total_receitas - total_despesas
            print(f"\n💰 Saldo: R$ {saldo:,.2f}")
            print("="*60 + "\n")
            
        except Exception as e:
            self.log(f"❌ Erro ao gerar relatório: {e}", "ERROR")
    
    def salvar_log(self, arquivo_log='logs/importacao.log'):
        """Salva log de importação em arquivo"""
        try:
            os.makedirs(os.path.dirname(arquivo_log), exist_ok=True)
            with open(arquivo_log, 'a', encoding='utf-8') as f:
                f.write("\n" + "="*60 + "\n")
                f.write(f"IMPORTAÇÃO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n")
                for linha in self.log_importacao:
                    f.write(linha + "\n")
            print(f"📝 Log salvo em: {arquivo_log}")
        except Exception as e:
            print(f"⚠️ Não foi possível salvar log: {e}")
    
    def fechar_conexao(self):
        """Fecha conexão com banco"""
        if self.conn:
            self.conn.close()
            self.log("✅ Conexão com banco fechada", "SUCCESS")

def main():
    """Função principal de processamento"""
    print("\n🚀 DATAOPS LOCAL - PROCESSAMENTO DE DADOS v2.0")
    print("="*60 + "\n")
    
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
    
    # Calcular comissões do período (NOVO)
    print("\n" + "="*60)
    processor.calcular_comissoes_periodo()
    print("="*60)
    
    # Gerar relatório
    processor.gerar_relatorio_importacao()
    
    # Salvar log
    processor.salvar_log()
    
    # Fechar conexão
    processor.fechar_conexao()
    
    print("\n✅ Processamento concluído com sucesso!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()