#!/bin/bash
# DataOps Local - Gerar Relatorio PDF (Linux/Mac)

echo ""
echo "========================================"
echo "  DATAOPS LOCAL - GERAR RELATORIO PDF"
echo "========================================"
echo ""

python3 4-relatorios/gerar_relatorio.py

echo ""
echo "O relatorio foi salvo na pasta '4-relatorios'"
echo ""
read -p "Pressione ENTER para continuar..."
