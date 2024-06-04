from fpdf import FPDF
import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Análise de Bugs', 0, 1, 'C')
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def gerar_pdf(categoria_principal, descricao_categoria, solucao_proposta, df_categoria_principal):
    pdf = PDF()
    pdf.add_page()

    # Título
    pdf.chapter_title('Análise de Bugs')

    # Data
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.chapter_body(f'Data: {data_atual}')

    # Categoria Principal
    pdf.chapter_body(f'Categoria com maior incidência: {categoria_principal}')
    
    # IDs dos Bugs
    ids_bugs = ', '.join(df_categoria_principal['ID'].astype(str).tolist())
    pdf.chapter_body(f'IDs dos Bugs analisados: {ids_bugs}')

    # Descrição Combinada
    pdf.chapter_body(f'Descrição combinada: {descricao_categoria}')

    # Solução Proposta
    pdf.chapter_body(f'Solução Proposta: {solucao_proposta}')
    
    # Salvar PDF
    pdf.output('relatorio_analise_bugs.pdf')
    return 'relatorio_analise_bugs.pdf'