import pandas as pd
import streamlit as st
import asyncio
import google.generativeai as genai
import os
from pdf_generator import gerar_pdf


genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title('Análise de Bugs e Propostas de Soluções com Gemini')

async def main() -> None:
  # Upload do arquivo CSV
  uploaded_file = st.file_uploader("Carregar Relatório de Bugs", type=["csv"])

  if uploaded_file is not None:
      df = pd.read_csv(uploaded_file)
      
      # Limpeza de dados
      df.dropna(inplace=True)
      
      # Análise de incidências
      categorias_contagem = df['Root Cause'].value_counts()
      categorias_bugs = df['Root Cause'].values 

      # Seleciona a categoria com maior incidência
      categoria_principal = categorias_contagem.idxmax()
      
      # Filtra bugs da categoria principal
      df_categoria_principal = df[df['Root Cause'] == categoria_principal]
      
      # Combina descrições para criar um texto representativo da categoria
      descricao_categoria = ' '.join(df_categoria_principal['Title'].tolist())
      
      async def propor_solucao(categoria):
          prompt = f"Considerando um ambiente de desenvolvimento ágil com múltiplos desenvolvedores, trabalhando em um projeto utilizando Angular para o frontend e Java no backend. Considerando a seguinte lista de categorias de BUGs, identifique os possíveis problemas de nossa equipe e também proponha soluções para reduzir a incidência de bugs nessas categorias '{', '.join(categoria.tolist())}'."
          response = model.generate_content(prompt)
          return response.text
      
      # Propor solução para a categoria principal
      solucao_proposta = await propor_solucao(categorias_bugs)
      
      # Exibição das análises e proposta de solução
      st.write("Incidência de Bugs por Categoria")
      st.bar_chart(categorias_bugs)
      
      st.write(f"Categoria com maior incidência: {categoria_principal}")
      st.write(f"Descrição combinada: {descricao_categoria}")
      st.write(f"Solução Proposta: {solucao_proposta}")

      if st.button('Gerar Relatório em PDF'):
        pdf_path = gerar_pdf(categoria_principal, descricao_categoria, solucao_proposta, df_categoria_principal)
        st.success(f'Relatório salvo em {pdf_path}')
        with open(pdf_path, 'rb') as f:
            st.download_button('Download PDF', f, file_name='relatorio_analise_bugs.pdf')

asyncio.run(main())