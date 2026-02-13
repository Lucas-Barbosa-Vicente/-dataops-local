#!/usr/bin/env python3
"""
DataOps Local - Script de Instalação Automatizada
Autor: Sistema DataOps
Descrição: Instala e configura o sistema automaticamente
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(step_number, text):
    """Imprime passo da instalação"""
    print(f"\n{'='*60}")
    print(f"  PASSO {step_number}: {text}")
    print(f"{'='*60}\n")

def check_python_version():
    """Verifica versão do Python"""
    print("🔍 Verificando versão do Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERRO: Python 3.8 ou superior é necessário!")
        print(f"   Versão atual: Python {version.major}.{version.minor}")
        print("   Baixe em: https://www.python.org/downloads/")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def install_dependencies():
    """Instala dependências do requirements.txt"""
    print("📦 Instalando dependências...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências!")
        print("   Tente manualmente: pip install -r requirements.txt")
        return False

def verify_structure():
    """Verifica estrutura de pastas"""
    print("📁 Verificando estrutura de pastas...")
    
    required_folders = [
        '1-coleta',
        '2-processamento',
        '3-visualizacao',
        '4-relatorios',
        'dados',
        'documentacao'
    ]
    
    all_exist = True
    for folder in required_folders:
        if not os.path.exists(folder):
            print(f"⚠️  Pasta não encontrada: {folder}")
            os.makedirs(folder, exist_ok=True)
            print(f"   ✅ Pasta criada: {folder}")
        else:
            print(f"✅ {folder}")
    
    return True

def verify_templates():
    """Verifica se os templates Excel existem"""
    print("📊 Verificando templates Excel...")
    
    templates = [
        '1-coleta/Template_Receitas.xlsx',
        '1-coleta/Template_Despesas.xlsx',
        '1-coleta/Template_Profissionais.xlsx',
        '1-coleta/Template_Servicos.xlsx'
    ]
    
    all_exist = True
    for template in templates:
        if os.path.exists(template):
            print(f"✅ {template}")
        else:
            print(f"⚠️  Não encontrado: {template}")
            all_exist = False
    
    if not all_exist:
        print("\n💡 Execute: python criar_templates.py")
    
    return all_exist

def create_database():
    """Cria/verifica banco de dados"""
    print("🗄️  Criando banco de dados...")
    
    try:
        subprocess.check_call([
            sys.executable, "2-processamento/processar_dados.py"
        ])
        print("✅ Banco de dados criado e populado!")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Aviso: Execute o processamento depois dos templates")
        return True  # Não é crítico neste momento

def test_dashboard():
    """Testa se o dashboard pode ser iniciado"""
    print("🧪 Testando componentes do dashboard...")
    
    try:
        # Apenas importar, não executar
        import streamlit
        import plotly
        import pandas
        print("✅ Todos os componentes do dashboard OK!")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar componentes: {e}")
        return False

def print_next_steps():
    """Imprime próximos passos após instalação"""
    print_header("INSTALAÇÃO CONCLUÍDA! 🎉")
    
    print("📋 PRÓXIMOS PASSOS:\n")
    
    print("1️⃣  PREENCHER DADOS")
    print("   └─ Vá até a pasta '1-coleta'")
    print("   └─ Abra e preencha os templates Excel\n")
    
    print("2️⃣  PROCESSAR DADOS")
    print("   └─ Execute: python 2-processamento/processar_dados.py\n")
    
    print("3️⃣  VISUALIZAR RESULTADOS")
    print("   └─ Dashboard: streamlit run 3-visualizacao/dashboard.py")
    print("   └─ Relatório: python 4-relatorios/gerar_relatorio.py\n")
    
    print("📚 DOCUMENTAÇÃO:")
    print("   └─ documentacao/INICIO_RAPIDO.md")
    print("   └─ documentacao/COMO_PREENCHER_PLANILHAS.md\n")
    
    print("💡 DICA: Leia primeiro o INICIO_RAPIDO.md!")
    
    print("\n" + "="*60)
    print("  Bons negócios! 🚀")
    print("="*60 + "\n")

def main():
    """Função principal de instalação"""
    print_header("🚀 DATAOPS LOCAL - INSTALAÇÃO AUTOMATIZADA")
    
    print("Este script vai:")
    print("  ✓ Verificar requisitos")
    print("  ✓ Instalar dependências")
    print("  ✓ Configurar estrutura")
    print("  ✓ Preparar o sistema\n")
    
    input("Pressione ENTER para continuar...")
    
    # Passo 1: Verificar Python
    print_step(1, "Verificando Python")
    if not check_python_version():
        sys.exit(1)
    
    # Passo 2: Instalar dependências
    print_step(2, "Instalando Dependências")
    if not install_dependencies():
        print("\n⚠️  Algumas dependências falharam, mas você pode continuar")
        print("   Tente instalar manualmente depois: pip install -r requirements.txt")
    
    # Passo 3: Verificar estrutura
    print_step(3, "Verificando Estrutura")
    verify_structure()
    
    # Passo 4: Verificar templates
    print_step(4, "Verificando Templates")
    if not verify_templates():
        print("\n💡 Criando templates Excel...")
        try:
            subprocess.check_call([sys.executable, "criar_templates.py"])
            print("✅ Templates criados!")
        except:
            print("⚠️  Execute manualmente: python criar_templates.py")
    
    # Passo 5: Testar componentes
    print_step(5, "Testando Componentes")
    test_dashboard()
    
    # Passo 6: Criar banco (opcional)
    print_step(6, "Preparando Banco de Dados")
    create_database()
    
    # Finalizar
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro durante instalação: {e}")
        print("   Entre em contato com o suporte")
        sys.exit(1)
