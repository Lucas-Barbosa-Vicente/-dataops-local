"""
Script de Diagnóstico - DataOps Local
Verifica integridade dos dados e identifica possíveis problemas
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

class DiagnosticoDataOps:
    def __init__(self, db_path='dados/dataops.db'):
        self.db_path = db_path
        self.conn = None
        self.problemas = []
        
    def conectar(self):
        """Conecta ao banco de dados"""
        if not os.path.exists(self.db_path):
            print(f"❌ ERRO: Banco de dados não encontrado em {self.db_path}")
            print("   Execute primeiro: python 2-processamento/processar_dados.py")
            return False
        
        self.conn = sqlite3.connect(self.db_path)
        print(f"✅ Conectado ao banco: {self.db_path}\n")
        return True
    
    def adicionar_problema(self, tipo, descricao, solucao):
        """Adiciona um problema encontrado"""
        self.problemas.append({
            'tipo': tipo,
            'descricao': descricao,
            'solucao': solucao
        })
    
    def verificar_tabelas(self):
        """Verifica se todas as tabelas existem"""
        print("="*70)
        print("1️⃣  VERIFICANDO ESTRUTURA DO BANCO")
        print("="*70)
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = [row[0] for row in cursor.fetchall()]
        
        tabelas_esperadas = ['receitas', 'despesas', 'profissionais', 'servicos']
        
        print("Tabelas encontradas:")
        for tabela in tabelas:
            print(f"  ✅ {tabela}")
        
        print("\nTabelas faltando:")
        faltando = [t for t in tabelas_esperadas if t not in tabelas]
        if faltando:
            for tabela in faltando:
                print(f"  ❌ {tabela}")
                self.adicionar_problema(
                    "CRITICO",
                    f"Tabela '{tabela}' não existe",
                    "Execute o script de processamento para criar as tabelas"
                )
        else:
            print("  ✅ Todas as tabelas esperadas existem")
        
        print()
    
    def verificar_despesas_sem_forma_pagamento(self):
        """Verifica despesas sem forma de pagamento"""
        print("="*70)
        print("2️⃣  VERIFICANDO DESPESAS SEM FORMA DE PAGAMENTO")
        print("="*70)
        
        query = """
            SELECT COUNT(*) as total,
                   SUM(valor) as valor_total
            FROM despesas 
            WHERE forma_pagamento IS NULL OR forma_pagamento = ''
        """
        df = pd.read_sql_query(query, self.conn)
        
        total = df['total'].iloc[0]
        valor = df['valor_total'].iloc[0] or 0
        
        if total > 0:
            print(f"⚠️  {total} despesas SEM forma de pagamento definida")
            print(f"   Valor total: R$ {valor:,.2f}")
            
            # Mostrar exemplos
            query_exemplos = """
                SELECT data, categoria, descricao, valor
                FROM despesas
                WHERE forma_pagamento IS NULL OR forma_pagamento = ''
                LIMIT 5
            """
            exemplos = pd.read_sql_query(query_exemplos, self.conn)
            print("\n   Exemplos:")
            for _, row in exemplos.iterrows():
                print(f"   - {row['data']} | {row['categoria']} | {row['descricao']} | R$ {row['valor']:,.2f}")
            
            self.adicionar_problema(
                "MEDIO",
                f"{total} despesas sem forma de pagamento",
                "Atualize a planilha de despesas com a forma de pagamento e reimporte"
            )
        else:
            print("✅ Todas as despesas possuem forma de pagamento")
        
        print()
    
    def verificar_despesas_por_forma_pagamento(self):
        """Analisa despesas por forma de pagamento"""
        print("="*70)
        print("3️⃣  ANÁLISE POR FORMA DE PAGAMENTO")
        print("="*70)
        
        query = """
            SELECT 
                COALESCE(forma_pagamento, 'NÃO DEFINIDO') as forma,
                COUNT(*) as quantidade,
                SUM(valor) as total
            FROM despesas
            GROUP BY forma_pagamento
            ORDER BY total DESC
        """
        df = pd.read_sql_query(query, self.conn)
        
        if len(df) > 0:
            print("Despesas por forma de pagamento:\n")
            print(f"{'Forma':<20} {'Qtd':>8} {'Total (R$)':>15}")
            print("-" * 45)
            for _, row in df.iterrows():
                print(f"{row['forma']:<20} {row['quantidade']:>8} {row['total']:>15,.2f}")
            
            # Verificar se boleto existe
            if 'Boleto' not in df['forma'].values and 'boleto' not in df['forma'].values.str.lower():
                print("\n⚠️  ATENÇÃO: Nenhuma despesa com forma de pagamento 'Boleto'")
                print("   Se você tem despesas de boleto, verifique:")
                print("   1. O nome da forma de pagamento na planilha")
                print("   2. Se os dados foram importados corretamente")
                self.adicionar_problema(
                    "INFO",
                    "Nenhuma despesa de boleto encontrada",
                    "Verifique se as despesas de boleto foram importadas e se a forma de pagamento está correta"
                )
        else:
            print("❌ Nenhuma despesa encontrada no banco")
            self.adicionar_problema(
                "CRITICO",
                "Banco de dados vazio",
                "Execute o processamento para importar os dados"
            )
        
        print()
    
    def verificar_datas_invalidas(self):
        """Verifica se há problemas com datas"""
        print("="*70)
        print("4️⃣  VERIFICANDO DATAS")
        print("="*70)
        
        # Verificar receitas
        query = "SELECT MIN(data) as min_data, MAX(data) as max_data FROM receitas"
        df = pd.read_sql_query(query, self.conn)
        
        if df['min_data'].iloc[0]:
            print(f"📅 Receitas:")
            print(f"   Primeira: {df['min_data'].iloc[0]}")
            print(f"   Última:   {df['max_data'].iloc[0]}")
        else:
            print("❌ Nenhuma receita encontrada")
        
        # Verificar despesas
        query = "SELECT MIN(data) as min_data, MAX(data) as max_data FROM despesas"
        df = pd.read_sql_query(query, self.conn)
        
        if df['min_data'].iloc[0]:
            print(f"\n📅 Despesas:")
            print(f"   Primeira: {df['min_data'].iloc[0]}")
            print(f"   Última:   {df['max_data'].iloc[0]}")
        else:
            print("❌ Nenhuma despesa encontrada")
        
        # Verificar datas futuras
        hoje = datetime.now().strftime('%Y-%m-%d')
        query = f"SELECT COUNT(*) as futuras FROM despesas WHERE data > '{hoje}'"
        df = pd.read_sql_query(query, self.conn)
        
        if df['futuras'].iloc[0] > 0:
            print(f"\n⚠️  {df['futuras'].iloc[0]} despesas com data FUTURA")
            self.adicionar_problema(
                "ALERTA",
                f"{df['futuras'].iloc[0]} despesas com data futura",
                "Verifique se as datas estão corretas"
            )
        
        print()
    
    def verificar_comissoes(self):
        """Verifica cálculo e registro de comissões"""
        print("="*70)
        print("5️⃣  VERIFICANDO COMISSÕES")
        print("="*70)
        
        # Verificar se existe o campo tipo_despesa
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA table_info(despesas)")
        colunas = [row[1] for row in cursor.fetchall()]
        
        if 'tipo_despesa' not in colunas:
            print("⚠️  Campo 'tipo_despesa' NÃO existe na tabela despesas")
            print("   Isso significa que está usando a versão antiga do sistema")
            self.adicionar_problema(
                "CRITICO",
                "Tabela de despesas sem campo tipo_despesa",
                "Atualize para a nova versão do sistema (v2.0)"
            )
        else:
            # Verificar comissões calculadas
            query = """
                SELECT COUNT(*) as qtd, SUM(valor) as total
                FROM despesas
                WHERE tipo_despesa = 'Comissão Calculada'
            """
            df = pd.read_sql_query(query, self.conn)
            
            qtd = df['qtd'].iloc[0]
            total = df['total'].iloc[0] or 0
            
            if qtd > 0:
                print(f"✅ {qtd} comissões calculadas encontradas")
                print(f"   Total: R$ {total:,.2f}")
                
                # Detalhamento
                query_det = """
                    SELECT descricao, valor, data
                    FROM despesas
                    WHERE tipo_despesa = 'Comissão Calculada'
                    ORDER BY data DESC
                """
                det = pd.read_sql_query(query_det, self.conn)
                print("\n   Detalhamento:")
                for _, row in det.iterrows():
                    print(f"   - {row['data']} | {row['descricao']} | R$ {row['valor']:,.2f}")
            else:
                print("⚠️  Nenhuma comissão calculada encontrada")
                print("   Execute o processamento para calcular comissões")
                self.adicionar_problema(
                    "INFO",
                    "Nenhuma comissão calculada",
                    "Execute: python 2-processamento/processar_dados.py"
                )
        
        print()
    
    def verificar_profissionais(self):
        """Verifica dados de profissionais"""
        print("="*70)
        print("6️⃣  VERIFICANDO PROFISSIONAIS")
        print("="*70)
        
        query = """
            SELECT 
                nome_profissional,
                tipo_contrato,
                percentual_comissao,
                salario_fixo,
                status
            FROM profissionais
        """
        df = pd.read_sql_query(query, self.conn)
        
        if len(df) > 0:
            print(f"Total de profissionais: {len(df)}\n")
            
            for _, row in df.iterrows():
                print(f"👤 {row['nome_profissional']}")
                print(f"   Contrato: {row['tipo_contrato']}")
                print(f"   Comissão: {row['percentual_comissao']}%")
                print(f"   Fixo: R$ {row['salario_fixo'] or 0:,.2f}")
                print(f"   Status: {row['status']}")
                print()
                
                # Verificar se tem comissão mas não tem percentual
                if row['tipo_contrato'] == 'Percentual' and (not row['percentual_comissao'] or row['percentual_comissao'] == 0):
                    self.adicionar_problema(
                        "ALERTA",
                        f"Profissional {row['nome_profissional']} tem contrato 'Percentual' mas percentual é zero",
                        "Atualize o percentual de comissão na planilha de profissionais"
                    )
        else:
            print("❌ Nenhum profissional encontrado")
            self.adicionar_problema(
                "CRITICO",
                "Nenhum profissional cadastrado",
                "Importe a planilha de profissionais"
            )
        
        print()
    
    def verificar_valores_zerados(self):
        """Verifica valores zerados ou negativos"""
        print("="*70)
        print("7️⃣  VERIFICANDO VALORES INVÁLIDOS")
        print("="*70)
        
        # Receitas zeradas
        query = "SELECT COUNT(*) as qtd FROM receitas WHERE valor_servico <= 0"
        df = pd.read_sql_query(query, self.conn)
        if df['qtd'].iloc[0] > 0:
            print(f"⚠️  {df['qtd'].iloc[0]} receitas com valor ZERO ou NEGATIVO")
            self.adicionar_problema(
                "ALERTA",
                f"{df['qtd'].iloc[0]} receitas com valor inválido",
                "Verifique os valores na planilha de receitas"
            )
        else:
            print("✅ Todas as receitas têm valores válidos")
        
        # Despesas zeradas
        query = "SELECT COUNT(*) as qtd FROM despesas WHERE valor <= 0"
        df = pd.read_sql_query(query, self.conn)
        if df['qtd'].iloc[0] > 0:
            print(f"⚠️  {df['qtd'].iloc[0]} despesas com valor ZERO ou NEGATIVO")
            self.adicionar_problema(
                "ALERTA",
                f"{df['qtd'].iloc[0]} despesas com valor inválido",
                "Verifique os valores na planilha de despesas"
            )
        else:
            print("✅ Todas as despesas têm valores válidos")
        
        print()
    
    def gerar_relatorio_problemas(self):
        """Gera relatório final com todos os problemas"""
        print("\n")
        print("="*70)
        print("📋 RESUMO DOS PROBLEMAS ENCONTRADOS")
        print("="*70)
        
        if not self.problemas:
            print("\n🎉 PARABÉNS! Nenhum problema encontrado!")
            print("   Seu sistema está funcionando corretamente.\n")
            return
        
        # Agrupar por tipo
        criticos = [p for p in self.problemas if p['tipo'] == 'CRITICO']
        medios = [p for p in self.problemas if p['tipo'] == 'MEDIO']
        alertas = [p for p in self.problemas if p['tipo'] == 'ALERTA']
        infos = [p for p in self.problemas if p['tipo'] == 'INFO']
        
        if criticos:
            print(f"\n🔴 PROBLEMAS CRÍTICOS ({len(criticos)}):")
            for i, p in enumerate(criticos, 1):
                print(f"\n{i}. {p['descricao']}")
                print(f"   💡 Solução: {p['solucao']}")
        
        if medios:
            print(f"\n🟡 PROBLEMAS MÉDIOS ({len(medios)}):")
            for i, p in enumerate(medios, 1):
                print(f"\n{i}. {p['descricao']}")
                print(f"   💡 Solução: {p['solucao']}")
        
        if alertas:
            print(f"\n🟠 ALERTAS ({len(alertas)}):")
            for i, p in enumerate(alertas, 1):
                print(f"\n{i}. {p['descricao']}")
                print(f"   💡 Solução: {p['solucao']}")
        
        if infos:
            print(f"\n🔵 INFORMAÇÕES ({len(infos)}):")
            for i, p in enumerate(infos, 1):
                print(f"\n{i}. {p['descricao']}")
                print(f"   💡 Solução: {p['solucao']}")
        
        print("\n" + "="*70)
        print(f"Total de problemas: {len(self.problemas)}")
        print("="*70 + "\n")
    
    def executar_diagnostico_completo(self):
        """Executa todos os diagnósticos"""
        print("\n🔍 DIAGNÓSTICO COMPLETO DO SISTEMA DATAOPS LOCAL")
        print("=" * 70)
        print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 70 + "\n")
        
        if not self.conectar():
            return
        
        self.verificar_tabelas()
        self.verificar_despesas_sem_forma_pagamento()
        self.verificar_despesas_por_forma_pagamento()
        self.verificar_datas_invalidas()
        self.verificar_comissoes()
        self.verificar_profissionais()
        self.verificar_valores_zerados()
        
        self.gerar_relatorio_problemas()
        
        self.conn.close()
        
        print("✅ Diagnóstico concluído!\n")

if __name__ == "__main__":
    diagnostico = DiagnosticoDataOps()
    diagnostico.executar_diagnostico_completo()
