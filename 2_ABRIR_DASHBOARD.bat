@echo off
REM DataOps Local - Abrir Dashboard (Windows)

echo.
echo ========================================
echo   DATAOPS LOCAL - DASHBOARD
echo ========================================
echo.
echo O dashboard abrira no navegador...
echo Para fechar: Pressione Ctrl+C nesta janela
echo.

py -3.10 -m streamlit run 3-visualizacao\dashboard.py
start http://localhost:8501

pause