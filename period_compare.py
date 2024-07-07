import streamlit as st # type: ignore
import matplotlib.pyplot as plt # type: ignore
from ai_generation import content_generation
from markdown_generator import gerar_markdown_comparacao

# Função para gerar gráficos de comparação
def gerar_graficos_comparacao(metricas1, metricas2):
  fig, axes = plt.subplots(2, 2, figsize=(15, 10))

  # Comparação do número total de bugs
  axes[0, 0].bar(["Período 1", "Período 2"], [metricas1["total_bugs"], metricas2["total_bugs"]])
  axes[0, 0].set_title("Número Total de Bugs")

  # Comparação de bugs por categoria
  categorias = list(set(metricas1["bugs_por_categoria"].index).union(set(metricas2["bugs_por_categoria"].index)))
  valores1 = [metricas1["bugs_por_categoria"].get(categoria, 0) for categoria in categorias]
  valores2 = [metricas2["bugs_por_categoria"].get(categoria, 0) for categoria in categorias]
  axes[0, 1].bar(categorias, valores1, alpha=0.5, label='Período 1')
  axes[0, 1].bar(categorias, valores2, alpha=0.5, label='Período 2')
  axes[0, 1].set_title("Bugs por Categoria")
  axes[0, 1].legend()

  # Comparação de bugs por prioridade
  prioridades = list(set(metricas1["bugs_por_prioridade"].index).union(set(metricas2["bugs_por_prioridade"].index)))
  valores1 = [metricas1["bugs_por_prioridade"].get(prioridade, 0) for prioridade in prioridades]
  valores2 = [metricas2["bugs_por_prioridade"].get(prioridade, 0) for prioridade in prioridades]
  axes[1, 0].bar(prioridades, valores1, alpha=0.5, label='Período 1')
  axes[1, 0].bar(prioridades, valores2, alpha=0.5, label='Período 2')
  axes[1, 0].set_title("Bugs por Prioridade")
  axes[1, 0].legend()

  plt.tight_layout()
  return fig

async def solicitar_analise_comparativa(metricas1, metricas2):
  prompt = f"""
  Compare as seguintes métricas de bugs entre dois períodos:

  Período 1:
  - Número total de bugs: {metricas1['total_bugs']}
  - Bugs por categoria: {metricas1['bugs_por_categoria'].to_dict()}
  - Bugs por prioridade: {metricas1['bugs_por_prioridade'].to_dict()}

  Período 2:
  - Número total de bugs: {metricas2['total_bugs']}
  - Bugs por categoria: {metricas2['bugs_por_categoria'].to_dict()}
  - Bugs por prioridade: {metricas2['bugs_por_prioridade'].to_dict()}

  Analise as diferenças e sugira possíveis melhorias.
  """
  response = await content_generation(prompt)
  return response.text

async def analise_dois_periodos(metricas1, metricas2):
  fig = gerar_graficos_comparacao(metricas1, metricas2)
  temp_img_path = "temp_comparacao_plot.png"
  fig.savefig(temp_img_path)

  # Fechar a figura para liberar memória
  plt.close(fig)

  # Exibir o gráfico no Streamlit
  st.image(temp_img_path, use_column_width=True)

  # Exibição das análises e comparação
  st.write("Número total de bugs:")
  st.write(f"Período 1: {metricas1['total_bugs']}, Período 2: {metricas2['total_bugs']}")
  st.write("Tempo médio de resolução (dias):")

  # Solicitar análise comparativa à IA
  analise_comparativa = await solicitar_analise_comparativa(metricas1, metricas2)
  st.write("Análise Comparativa da IA:")
  st.write(analise_comparativa)

  if st.button('Gerar Relatório em Markdown'):
    markdown_path = gerar_markdown_comparacao(metricas1, metricas2, temp_img_path, analise_comparativa)
    st.success(f'Relatório salvo em {markdown_path}')
    with open(markdown_path, 'rb') as f:
      st.download_button('Download Markdown', f, file_name='relatorio_comparacao_bugs.md')