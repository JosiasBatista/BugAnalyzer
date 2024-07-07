from datetime import datetime
from PIL import Image

def gerar_markdown(categoria_principal, solucao_proposta, df_categoria_principal, temp_img_path):
    markdown_path = 'relatorio_analise_bugs.md'
    with open(markdown_path, 'w', encoding='utf-8') as f:
        # Título
        f.write('# Análise de Bugs\n\n')
        
        # Data
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'**Data:** {data_atual}\n\n')

        # Categoria Principal
        f.write(f'**Categoria com maior incidência:** {categoria_principal}\n\n')
        
        # IDs dos Bugs
        ids_bugs = ', '.join(df_categoria_principal['ID'].astype(str).tolist())
        f.write(f'**IDs dos Bugs analisados:** {ids_bugs}\n\n')

        # Inserir a imagem do gráfico
        f.write(f'![Incidência de Bugs por Categoria]({temp_img_path})\n')

        # Solução Proposta
        f.write(f'**Solução Proposta:**\n\n{solucao_proposta}\n\n')
        
    
    return markdown_path

def gerar_markdown_comparacao(metricas1, metricas2, grafico_comparacao_path, analise_comparativa):
    import datetime

    data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    markdown_content = f"""
# Relatório de Comparação de Bugs

**Data**: {data_atual}

## Métricas do Período 1:
- Número total de bugs: {metricas1['total_bugs']}
- Tempo médio de resolução: {metricas1['tempo_medio_resolucao']:.2f} dias

## Métricas do Período 2:
- Número total de bugs: {metricas2['total_bugs']}
- Tempo médio de resolução: {metricas2['tempo_medio_resolucao']:.2f} dias

## Comparação entre Períodos:
- Redução/Aumento no número de bugs: {metricas2['total_bugs'] - metricas1['total_bugs']}
- Redução/Aumento no tempo médio de resolução: {metricas2['tempo_medio_resolucao'] - metricas1['tempo_medio_resolucao']:.2f} dias

## Análise Comparativa:
{analise_comparativa}

![Gráfico de Comparação]({grafico_comparacao_path})
    """

    markdown_path = 'relatorio_comparacao_bugs.md'
    with open(markdown_path, 'w') as file:
        file.write(markdown_content)
    
    return markdown_path