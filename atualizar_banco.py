import sqlite3
import os

# Verificar se o banco existe
if not os.path.exists('dados/dataops.db'):
    print("❌ Banco de dados não encontrado em dados/dataops.db")
    print("   Certifique-se de estar na pasta raiz do projeto")
    exit()

# Conectar ao banco
print("🔄 Conectando ao banco de dados...")
conn = sqlite3.connect('dados/dataops.db')
cursor = conn.cursor()

# Adicionar coluna tipo_despesa
try:
    cursor.execute("ALTER TABLE despesas ADD COLUMN tipo_despesa TEXT DEFAULT 'Manual'")
    print("✅ Coluna 'tipo_despesa' adicionada com sucesso")
except sqlite3.OperationalError as e:
    if "duplicate column" in str(e).lower():
        print("⚠️  Coluna 'tipo_despesa' já existe (tudo bem!)")
    else:
        print(f"❌ Erro ao adicionar coluna: {e}")

# Atualizar despesas existentes
cursor.execute("UPDATE despesas SET tipo_despesa = 'Manual' WHERE tipo_despesa IS NULL")
qtd_atualizadas = cursor.rowcount
if qtd_atualizadas > 0:
    print(f"✅ {qtd_atualizadas} despesas marcadas como 'Manual'")

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
print("✅ Tabela 'comissoes_calculadas' criada/verificada")

# Salvar mudanças
conn.commit()
conn.close()

print("\n🎉 Banco de dados atualizado com sucesso!")
print("\n📝 Próximos passos:")
print("   1. Substitua os arquivos processar_dados.py e dashboard.py")
print("   2. Execute: python 2-processamento/processar_dados.py")
print("   3. Execute: streamlit run 3-analytics/dashboard.py")