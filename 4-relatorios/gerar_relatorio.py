"""
DataOps Local - Gerador de Relatórios PDF
Autor: Sistema DataOps
Descrição: Gera relatórios automáticos em PDF
"""

import sqlite3
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime, timedelta
import sys

class RelatorioGerador:
    def __init__(self, db_path='dados/dataops.db'):
        self.db_path = db_path
        self.conn = None
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()
    
    def _configurar_estilos(self):
        """Configura estilos customizados"""
        self.styles.add(ParagraphStyle(
            name='TituloCustom',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubtituloCustom',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def conectar_banco(self):
        """Conecta ao banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco: {e}")
            return False
    
    def obter_metricas_periodo(self, dias=30):
        """Obtém métricas do período"""
        data_inicio = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
        
        # Receitas
        query_receitas = f"""
            SELECT 
                COUNT(*) as qtd,
                SUM(valor_servico) as total,
                AVG(valor_servico) as media
            FROM receitas
            WHERE data >= '{data_inicio}'
        """
        df_rec = pd.read_sql_query(query_receitas, self.conn)
        
        # Despesas
        query_despesas = f"""
            SELECT 
                COUNT(*) as qtd,
                SUM(valor) as total
            FROM despesas
            WHERE data >= '{data_inicio}'
        """
        df_desp = pd.read_sql_query(query_despesas, self.conn)
        
        return {
            'receitas': {
                'qtd': int(df_rec['qtd'].iloc[0]) if df_rec['qtd'].iloc[0] else 0,
                'total': float(df_rec['total'].iloc[0]) if df_rec['total'].iloc[0] else 0.0,
                'media': float(df_rec['media'].iloc[0]) if df_rec['media'].iloc[0] else 0.0
            },
            'despesas': {
                'qtd': int(df_desp['qtd'].iloc[0]) if df_desp['qtd'].iloc[0] else 0,
                'total': float(df_desp['total'].iloc[0]) if df_desp['total'].iloc[0] else 0.0
            }
        }
    
    def obter_top_profissionais(self, dias=30, limite=5):
        """Obtém ranking de profissionais"""
        data_inicio = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
        
        query = f"""
            SELECT 
                profissional,
                COUNT(*) as qtd_servicos,
                SUM(valor_servico) as total_receita,
                AVG(valor_servico) as ticket_medio
            FROM receitas
            WHERE data >= '{data_inicio}'
            GROUP BY profissional
            ORDER BY total_receita DESC
            LIMIT {limite}
        """
        return pd.read_sql_query(query, self.conn)
    
    def obter_servicos_mais_vendidos(self, dias=30, limite=5):
        """Obtém serviços mais realizados"""
        data_inicio = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
        
        query = f"""
            SELECT 
                tipo_servico,
                COUNT(*) as quantidade,
                SUM(valor_servico) as receita_total
            FROM receitas
            WHERE data >= '{data_inicio}'
            GROUP BY tipo_servico
            ORDER BY quantidade DESC
            LIMIT {limite}
        """
        return pd.read_sql_query(query, self.conn)
    
    def obter_despesas_por_categoria(self, dias=30):
        """Obtém despesas agrupadas por categoria"""
        data_inicio = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
        
        query = f"""
            SELECT 
                categoria,
                COUNT(*) as qtd,
                SUM(valor) as total
            FROM despesas
            WHERE data >= '{data_inicio}'
            GROUP BY categoria
            ORDER BY total DESC
        """
        return pd.read_sql_query(query, self.conn)
    
    def gerar_relatorio_mensal(self, nome_arquivo=None):
        """Gera relatório mensal completo"""
        if not nome_arquivo:
            nome_arquivo = f"4-relatorios/Relatorio_Mensal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Criar documento PDF
        doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
        elementos = []
        
        # Título
        titulo = Paragraph("RELATÓRIO GERENCIAL MENSAL", self.styles['TituloCustom'])
        elementos.append(titulo)
        
        # Período
        periodo_texto = f"Período: {(datetime.now() - timedelta(days=30)).strftime('%d/%m/%Y')} a {datetime.now().strftime('%d/%m/%Y')}"
        elementos.append(Paragraph(periodo_texto, self.styles['Normal']))
        elementos.append(Spacer(1, 0.5*cm))
        
        # Obter dados
        metricas = self.obter_metricas_periodo(30)
        
        # Resumo Financeiro
        elementos.append(Paragraph("1. RESUMO FINANCEIRO", self.styles['SubtituloCustom']))
        
        dados_financeiro = [
            ['Indicador', 'Valor'],
            ['Total de Receitas', f"R$ {metricas['receitas']['total']:,.2f}"],
            ['Quantidade de Serviços', f"{metricas['receitas']['qtd']}"],
            ['Ticket Médio', f"R$ {metricas['receitas']['media']:,.2f}"],
            ['Total de Despesas', f"R$ {metricas['despesas']['total']:,.2f}"],
            ['Saldo do Período', f"R$ {metricas['receitas']['total'] - metricas['despesas']['total']:,.2f}"]
        ]
        
        tabela_financeiro = Table(dados_financeiro, colWidths=[10*cm, 6*cm])
        tabela_financeiro.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elementos.append(tabela_financeiro)
        elementos.append(Spacer(1, 1*cm))
        
        # Top Profissionais
        elementos.append(Paragraph("2. DESEMPENHO POR PROFISSIONAL", self.styles['SubtituloCustom']))
        
        df_prof = self.obter_top_profissionais(30)
        
        dados_prof = [['Profissional', 'Qtd Serviços', 'Receita Total', 'Ticket Médio']]
        for _, row in df_prof.iterrows():
            dados_prof.append([
                row['profissional'],
                str(int(row['qtd_servicos'])),
                f"R$ {row['total_receita']:,.2f}",
                f"R$ {row['ticket_medio']:,.2f}"
            ])
        
        tabela_prof = Table(dados_prof, colWidths=[6*cm, 3*cm, 4*cm, 3*cm])
        tabela_prof.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elementos.append(tabela_prof)
        elementos.append(Spacer(1, 1*cm))
        
        # Serviços Mais Vendidos
        elementos.append(Paragraph("3. SERVIÇOS MAIS REALIZADOS", self.styles['SubtituloCustom']))
        
        df_servicos = self.obter_servicos_mais_vendidos(30)
        
        dados_servicos = [['Serviço', 'Quantidade', 'Receita Total']]
        for _, row in df_servicos.iterrows():
            dados_servicos.append([
                row['tipo_servico'],
                str(int(row['quantidade'])),
                f"R$ {row['receita_total']:,.2f}"
            ])
        
        tabela_servicos = Table(dados_servicos, colWidths=[9*cm, 3*cm, 4*cm])
        tabela_servicos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elementos.append(tabela_servicos)
        elementos.append(Spacer(1, 1*cm))
        
        # Despesas por Categoria
        elementos.append(Paragraph("4. DESPESAS POR CATEGORIA", self.styles['SubtituloCustom']))
        
        df_despesas = self.obter_despesas_por_categoria(30)
        
        dados_despesas = [['Categoria', 'Quantidade', 'Total']]
        for _, row in df_despesas.iterrows():
            dados_despesas.append([
                row['categoria'],
                str(int(row['qtd'])),
                f"R$ {row['total']:,.2f}"
            ])
        
        tabela_despesas = Table(dados_despesas, colWidths=[9*cm, 3*cm, 4*cm])
        tabela_despesas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f39c12')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffe6cc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elementos.append(tabela_despesas)
        
        # Rodapé
        elementos.append(Spacer(1, 2*cm))
        rodape = Paragraph(
            f"Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            self.styles['Normal']
        )
        elementos.append(rodape)
        
        # Gerar PDF
        doc.build(elementos)
        
        return nome_arquivo
    
    def fechar_conexao(self):
        """Fecha conexão com banco"""
        if self.conn:
            self.conn.close()

def main():
    """Função principal"""
    print("\n📄 DATAOPS LOCAL - GERADOR DE RELATÓRIOS")
    print("="*50 + "\n")
    
    # Inicializar gerador
    gerador = RelatorioGerador()
    
    # Conectar ao banco
    if not gerador.conectar_banco():
        print("❌ Erro: Execute primeiro o processamento de dados!")
        sys.exit(1)
    
    # Gerar relatório
    print("📊 Gerando relatório mensal...")
    
    try:
        arquivo_gerado = gerador.gerar_relatorio_mensal()
        print(f"✅ Relatório gerado com sucesso!")
        print(f"📁 Localização: {arquivo_gerado}")
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
    finally:
        gerador.fechar_conexao()

if __name__ == "__main__":
    main()
