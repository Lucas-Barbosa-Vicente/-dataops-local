"""
Script de Migração Simplificado - DataOps Local v1.0 -> v2.0
Para usar quando você baixou apenas os arquivos individuais (não a pasta completa)

INSTRUÇÕES:
1. Baixe os arquivos do chat:
   - processar_dados.py (v2.0)
   - dashboard.py (v2.0)
   - diagnostico.py

2. Coloque este script na pasta raiz do seu projeto

3. Execute: python migrar_simplificado.py

4. O script vai pedir onde estão os arquivos baixados
"""

import os
import shutil
import sqlite3
from datetime import datetime
import sys

class MigradorSimplificado:
    def __init__(self):
        self.pasta_backup = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.sucesso = []
        self.erros = []
        
    def log(self, msg, tipo="INFO"):
        simbolos = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        print(f"{simbolos.get(tipo, 'ℹ️')} {msg}")
        
    def criar_backup(self):
        """Cria backup dos arquivos atuais"""
        print("\n" + "="*70)
        print("💾 CRIANDO BACKUP")
        print("="*70)
        
        try:
            os.makedirs(self.pasta_backup, exist_ok=True)
            
            # Backup dos arquivos Python
            if os.path.exists('2-processamento/processar_dados.py'):
                shutil.copy2('2-processamento/processar_dados.py', 
                           f'{self.pasta_backup}/processar_dados.py')
                self.log("Backup: processar_dados.py", "SUCCESS")
            
            if os.path.exists('3-analytics/dashboard.py'):
                shutil.copy2('3-analytics/dashboard.py', 
                           f'{self.pasta_backup}/dashboard.py')
                self.log("Backup: dashboard.py", "SUCCESS")
            
            # Backup do banco
            if os.path.exists('dados/dataops.db'):
                shutil.copy2('dados/dataops.db', 
                           f'{self.pasta_backup}/dataops.db')
                self.log("Backup: banco de dados", "SUCCESS")
            
            print(f"\n✅ Backup completo salvo em: {self.pasta_backup}")
            return True
            
        except Exception as e:
            self.log(f"Erro ao criar backup: {e}", "ERROR")
            return False
    
    def atualizar_banco(self):
        """Adiciona nova coluna ao banco"""
        print("\n" + "="*70)
        print("🔄 ATUALIZANDO BANCO DE DADOS")
        print("="*70)
        
        if not os.path.exists('dados/dataops.db'):
            self.log("Banco não existe ainda. Será criado no primeiro processamento.", "INFO")
            return True
        
        try:
            conn = sqlite3.connect('dados/dataops.db')
            cursor = conn.cursor()
            
            # Verificar se coluna existe
            cursor.execute("PRAGMA table_info(despesas)")
            colunas = [row[1] for row in cursor.fetchall()]
            
            if 'tipo_despesa' in colunas:
                self.log("Coluna 'tipo_despesa' já existe", "SUCCESS")
            else:
                # Adicionar coluna
                cursor.execute("ALTER TABLE despesas ADD COLUMN tipo_despesa TEXT DEFAULT 'Manual'")
                conn.commit()
                self.log("Coluna 'tipo_despesa' adicionada", "SUCCESS")
                
                # Atualizar registros existentes
                cursor.execute("UPDATE despesas SET tipo_despesa = 'Manual' WHERE tipo_despesa IS NULL")
                conn.commit()
                
                cursor.execute("SELECT COUNT(*) FROM despesas")
                qtd = cursor.fetchone()[0]
                self.log(f"{qtd} despesas marcadas como 'Manual'", "SUCCESS")
            
            # Criar tabela de comissões
            cursor.execute("""
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
            """)
            conn.commit()
            self.log("Tabela 'comissoes_calculadas' criada", "SUCCESS")
            
            conn.close()
            return True
            
        except Exception as e:
            self.log(f"Erro ao atualizar banco: {e}", "ERROR")
            return False
    
    def solicitar_arquivos(self):
        """Solicita ao usuário onde estão os arquivos baixados"""
        print("\n" + "="*70)
        print("📁 LOCALIZAÇÃO DOS ARQUIVOS v2.0")
        print("="*70)
        print("\nVocê precisa ter baixado 3 arquivos do chat:")
        print("  1. processar_dados.py (versão 2.0)")
        print("  2. dashboard.py (versão 2.0)")
        print("  3. diagnostico.py (novo)")
        
        arquivos = {}
        
        # Solicitar cada arquivo
        print("\n" + "-"*70)
        print("Digite o caminho COMPLETO de cada arquivo:")
        print("(Exemplo: C:\\Users\\SeuNome\\Downloads\\processar_dados.py)")
        print("-"*70 + "\n")
        
        # processar_dados.py
        while True:
            print("1️⃣  processar_dados.py v2.0")
            caminho = input("   Caminho: ").strip().strip('"').strip("'")
            
            if os.path.exists(caminho):
                arquivos['processar_dados.py'] = caminho
                self.log(f"Arquivo encontrado: {caminho}", "SUCCESS")
                break
            else:
                self.log(f"Arquivo não encontrado: {caminho}", "ERROR")
                print("   Tente novamente ou digite 'pular' para pular este arquivo.")
                if input("   > ").lower() == 'pular':
                    break
        
        # dashboard.py
        print()
        while True:
            print("2️⃣  dashboard.py v2.0")
            caminho = input("   Caminho: ").strip().strip('"').strip("'")
            
            if os.path.exists(caminho):
                arquivos['dashboard.py'] = caminho
                self.log(f"Arquivo encontrado: {caminho}", "SUCCESS")
                break
            else:
                self.log(f"Arquivo não encontrado: {caminho}", "ERROR")
                print("   Tente novamente ou digite 'pular' para pular este arquivo.")
                if input("   > ").lower() == 'pular':
                    break
        
        # diagnostico.py (opcional)
        print()
        while True:
            print("3️⃣  diagnostico.py (opcional)")
            caminho = input("   Caminho (ou 'pular'): ").strip().strip('"').strip("'")
            
            if caminho.lower() == 'pular':
                self.log("Diagnóstico pulado (opcional)", "INFO")
                break
            elif os.path.exists(caminho):
                arquivos['diagnostico.py'] = caminho
                self.log(f"Arquivo encontrado: {caminho}", "SUCCESS")
                break
            else:
                self.log(f"Arquivo não encontrado: {caminho}", "ERROR")
        
        return arquivos
    
    def instalar_arquivos(self, arquivos):
        """Instala os novos arquivos"""
        print("\n" + "="*70)
        print("📥 INSTALANDO ARQUIVOS v2.0")
        print("="*70)
        
        try:
            if 'processar_dados.py' in arquivos:
                shutil.copy2(arquivos['processar_dados.py'], 
                           '2-processamento/processar_dados.py')
                self.log("processar_dados.py v2.0 instalado", "SUCCESS")
            
            if 'dashboard.py' in arquivos:
                shutil.copy2(arquivos['dashboard.py'], 
                           '3-analytics/dashboard.py')
                self.log("dashboard.py v2.0 instalado", "SUCCESS")
            
            if 'diagnostico.py' in arquivos:
                shutil.copy2(arquivos['diagnostico.py'], 'diagnostico.py')
                self.log("diagnostico.py instalado", "SUCCESS")
            
            return True
            
        except Exception as e:
            self.log(f"Erro ao instalar arquivos: {e}", "ERROR")
            return False
    
    def gerar_relatorio(self):
        """Gera relatório final"""
        print("\n" + "="*70)
        print("📋 MIGRAÇÃO CONCLUÍDA")
        print("="*70)
        
        print(f"\n💾 Backup salvo em: {self.pasta_backup}")
        
        print("\n📝 PRÓXIMOS PASSOS:")
        print("   1. Execute: python 2-processamento/processar_dados.py")
        print("   2. Execute: streamlit run 3-analytics/dashboard.py")
        print("   3. Verifique se tudo está funcionando")
        
        if os.path.exists('diagnostico.py'):
            print("   4. Se necessário, execute: python diagnostico.py")
        
        print(f"\n⚠️  Se houver problemas, restaure o backup:")
        print(f"   cp {self.pasta_backup}/* para as pastas originais")
        
        print("\n" + "="*70 + "\n")
    
    def migrar(self):
        """Executa migração"""
        print("\n" + "="*70)
        print("🚀 MIGRAÇÃO SIMPLIFICADA - DATAOPS v1.0 -> v2.0")
        print("="*70)
        print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*70)
        
        # Verificar estrutura básica
        if not os.path.exists('2-processamento') or not os.path.exists('3-analytics'):
            self.log("Estrutura de pastas incorreta!", "ERROR")
            self.log("Execute este script na pasta raiz do projeto", "ERROR")
            return False
        
        # Criar backup
        if not self.criar_backup():
            return False
        
        # Atualizar banco
        if not self.atualizar_banco():
            self.log("Erro ao atualizar banco, mas continuando...", "WARNING")
        
        # Solicitar arquivos
        arquivos = self.solicitar_arquivos()
        
        if not arquivos:
            self.log("Nenhum arquivo para instalar", "ERROR")
            return False
        
        # Instalar arquivos
        if not self.instalar_arquivos(arquivos):
            return False
        
        # Relatório
        self.gerar_relatorio()
        
        return True

def main():
    print("\n" + "="*70)
    print("BEM-VINDO À MIGRAÇÃO SIMPLIFICADA")
    print("="*70)
    print("\nEste script vai:")
    print("  ✅ Fazer backup dos arquivos atuais")
    print("  ✅ Atualizar o banco de dados")
    print("  ✅ Instalar os novos arquivos v2.0")
    print("\nVocê precisará informar onde estão os arquivos baixados.")
    print("="*70)
    
    print("\n⚠️  IMPORTANTE:")
    print("Você já baixou os arquivos v2.0 do chat?")
    print("  - processar_dados.py")
    print("  - dashboard.py")
    print("  - diagnostico.py (opcional)")
    print("\nDigite 's' para continuar ou 'n' para cancelar: ", end="")
    
    resposta = input().lower()
    
    if resposta != 's':
        print("\n❌ Migração cancelada.")
        print("\nBAIXE PRIMEIRO os arquivos do chat:")
        print("  1. Clique em cada arquivo que enviei")
        print("  2. Baixe para seu computador")
        print("  3. Execute este script novamente")
        return
    
    migrador = MigradorSimplificado()
    sucesso = migrador.migrar()
    
    if sucesso:
        print("\n🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
    else:
        print("\n⚠️  Migração concluída com problemas. Verifique as mensagens acima.")

if __name__ == "__main__":
    main()
