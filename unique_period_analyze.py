import streamlit as st # type: ignore
import matplotlib.pyplot as plt # type: ignore
from ai_generation import propor_solucao
from collections import Counter

ROOT_CAUSE_NAME = 'Root Cause'

def count_categories(categorias_contadas): 
  contagem = Counter(categorias_contadas)
  resultado_contagem = list(contagem.items())

  return resultado_contagem

def formatar_resultado(contagem_tuplas):
  # Criar uma lista de strings formatadas
  partes_formatadas = [f"{contagem} BUGs {valor}" for valor, contagem in contagem_tuplas]
  
  # Unir as partes formatadas em uma única string
  resultado_formatado = ', '.join(partes_formatadas)
  
  return resultado_formatado

async def analise_unico_periodo(actions_taken, df):
  # Upload do arquivo CSV
    
  # Análise de incidências
  categorias_contagem = df[ROOT_CAUSE_NAME].value_counts()
  categorias_bugs = df[ROOT_CAUSE_NAME].values 
  categorias_contadas = count_categories(categorias_bugs)
  # Seleciona a categoria com maior incidência
  # categoria_principal = categorias_contagem.idxmax()
  # Filtra bugs da categoria principal
  # df_categoria_principal = df[df[ROOT_CAUSE_NAME] == categoria_principal]
  
  # Propor solução para a categoria principal
  solucao_proposta = await propor_solucao(formatar_resultado(categorias_contadas), actions_taken, '')

  plt.style.use('dark_background')
  fig, ax = plt.subplots()
  ax.bar(categorias_contagem.index, categorias_contagem.values, color='skyblue')
  ax.set_xlabel('Categorias')
  ax.set_ylabel('Número de Bugs')
  ax.set_title('Incidência de Bugs por Categoria')
  
  # Salvar o gráfico como uma imagem temporária
  temp_img_path = "temp_plot.png"
  plt.savefig(temp_img_path)
  plt.close(fig)
  
  st.write(f"Número total de bugs: {len(df)}")
  # st.write(f"Categoria com maior incidência: {categoria_principal}")

  st.image(temp_img_path, use_column_width=True)
  st.write("Incidência de Bugs por Categoria")
  st.bar_chart(categorias_bugs)
  
  bugs_por_prioridade= df['Priority'].value_counts()
  st.write("Bugs por Prioridade")
  st.bar_chart(bugs_por_prioridade)
  
  quant_retornos = df['Qtde Retornos'].value_counts()
  st.write("Quantidade de retornos por BUGs")
  st.bar_chart(quant_retornos)

  st.write(f"Solução Proposta: {solucao_proposta}")
  # generate_report_files(categoria_principal, solucao_proposta, df_categoria_principal, temp_img_path)