import pandas as pd # type: ignore
import streamlit as st # type: ignore
import asyncio
from pdf_generator import gerar_pdf
from markdown_generator import gerar_markdown
from ai_generation import propor_solucao
from unique_period_analyze import analise_unico_periodo
from period_compare import analise_dois_periodos

ROOT_CAUSE_NAME = 'Root Cause'

st.title('Análise de Bugs e Propostas de Soluções com Gemini')

def processar_csv(uploaded_file):
  df = pd.read_csv(uploaded_file)
  df.dropna(inplace=True)
  return df

def processar_planilha(uploaded_file):
  xls = pd.ExcelFile(uploaded_file)
  available_sheets = xls.sheet_names
  print(available_sheets)

  tab_selected = st.text_input('Qual aba da planilha deseja analisar?') # 'INCIDENTES FUNCIONAIS WFM - N2'

  if len(tab_selected):
    df = pd.read_excel(xls, sheet_name=tab_selected)
  
    return df
  else:
    return pd.read_excel(xls, sheet_name='INCIDENTES FUNCIONAIS WFM - N2')
    

def generate_report_files(categoria_principal, solucao_proposta, df_categoria_principal, temp_img_path):
  if st.button('Gerar Relatório em PDF'):
    pdf_path = gerar_pdf(categoria_principal, solucao_proposta, df_categoria_principal, temp_img_path)
    st.success(f'Relatório salvo em {pdf_path}')
    with open(pdf_path, 'rb') as f:
        st.download_button('Download PDF', f, file_name='relatorio_analise_bugs.pdf')

  if st.button('Gerar Relatório em Markdown'):
    markdown_path = gerar_markdown(categoria_principal, solucao_proposta, df_categoria_principal, temp_img_path)
    st.success(f'Relatório salvo em {markdown_path}')
    with open(markdown_path, 'rb') as f:
        st.download_button('Download Markdown', f, file_name='relatorio_analise_bugs.md')

def calcular_metricas(df):
  metricas = {
    "total_bugs": len(df),
    "bugs_por_categoria": df[ROOT_CAUSE_NAME].value_counts(),
    "bugs_por_prioridade": df['Priority'].value_counts()
  }
  return metricas

async def main() -> None:

  modo_analise = st.radio(
    "Selecione o modo de análise",
    ("Análise de um único período", "Comparação entre dois períodos", "Encontrar causas e soluções")
  )

  actions_taken = st.text_input("Há alguma ação que você já executa no time para resolução de bugs? (Adicione separado por vírgula)")

  if modo_analise == "Análise de um único período":
    uploaded_file = st.file_uploader("Carregar Relatório de Bugs", type=["csv"])

    if uploaded_file is not None:
      df = pd.read_csv(uploaded_file)
    
      df.dropna(inplace=True)
      await analise_unico_periodo(actions_taken, df)
  elif modo_analise == "Comparação entre dois períodos":
    uploaded_file1 = st.file_uploader("Carregar Relatório de Bugs - Período 1", type=["csv"])
    uploaded_file2 = st.file_uploader("Carregar Relatório de Bugs - Período 2", type=["csv"])

    if uploaded_file1 is not None and uploaded_file2 is not None:
      df1 = processar_csv(uploaded_file1)
      df2 = processar_csv(uploaded_file2)

      metricas1 = calcular_metricas(df1)
      metricas2 = calcular_metricas(df2)

      await analise_dois_periodos(metricas1, metricas2)
  elif modo_analise == "Encontrar causas e soluções":
    file = st.file_uploader("Carregar Relatório", type=["csv", "xlsx"])

    if file is not None:
      if file.name.endswith('.csv'):
        df = processar_csv(file)
      else:
        df = processar_planilha(file)

        descricoes = df['Descrição'].values 
        
        solucao_proposta = await propor_solucao('', actions_taken, descricoes)
        st.write("Análise realizada pela IA:")
        st.write(solucao_proposta)

asyncio.run(main())