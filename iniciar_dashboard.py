#!/usr/bin/env python3
"""
DataOps Local - Inicializador Rápido
Autor: Sistema DataOps
Descrição: Script para iniciar o dashboard facilmente
"""

import subprocess
import sys
import os

def verificar_dados():
    """Verifica se há dados processados"""
    if not os.path.exists('dados/dataops.db'):
        print("⚠️  ATENÇÃO: Banco de dados não encontrado!")
        print("\n📝 Você precisa primeiro:")
        print("   1. Preencher as planilhas em '1-coleta/'")
        print("   2. Executar: python 2-processamento/processar_dados.py")
        print("\n💡 OU gere dados de exemplo:")
        print("   python gerar_exemplo.py")
        print()
        
        resposta = input("Deseja gerar dados de exemplo agora? (s/n): ")
        
        if resposta.lower() == 's':
            print("\n🎲 Gerando dados de exemplo...")
            try:
                subprocess.run([sys.executable, "gerar_exemplo.py"], input="s\n", text=True, check=True)
                print("\n📊 Processando dados...")
                subprocess.run([sys.executable, "2-processamento/processar_dados.py"], check=True)
            except subprocess.CalledProcessError:
                print("\n❌ Erro ao gerar dados. Tente manualmente.")
                return False
        else:
            print("\n❌ Dashboard não pode ser iniciado sem dados.")
            return False
    
    return True

def iniciar_dashboard():
    """Inicia o dashboard Streamlit"""
    print("\n🚀 Iniciando Dashboard DataOps Local...\n")
    print("="*60)
    print("  O dashboard abrirá automaticamente no navegador")
    print("  URL: http://localhost:8501")
    print("  Para parar: Pressione Ctrl+C")
    print("="*60 + "\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "3-visualizacao/dashboard.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard encerrado. Até logo!")
    except FileNotFoundError:
        print("\n❌ Streamlit não está instalado!")
        print("   Execute: pip install streamlit")

def main():
    print("\n📊 DATAOPS LOCAL - DASHBOARD")
    print("="*60 + "\n")
    
    # Verificar se há dados
    if not verificar_dados():
        sys.exit(1)
    
    # Iniciar dashboard
    iniciar_dashboard()

if __name__ == "__main__":
    main()
