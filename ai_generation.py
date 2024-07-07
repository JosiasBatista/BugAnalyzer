import google.generativeai as genai # type: ignore
import streamlit as st # type: ignore
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
print(os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

async def propor_solucao(categoria, actions_taken, descricoes):
  if len(descricoes) > 0:
    prompt = "Possuo uma massa de dados de Incidentes de BUGs em produção nos quais preciso realizar uma análise. Sendo os sistemas da área de telefônica identifique dentre as seguintes descrições quais são os principais problemas com maior incidência buscando identificar sua causa raiz e após isso me proponha soluções que podemos aplicar para diminuir a quantidade de problemas. Por favor, indique os problemas identificados e as soluções de acordo com a maior quantidade de incidência ou criticidade: Descrições " + '\n\n'.join(descricoes)
  else:
    prompt = f"Considerando um ambiente de desenvolvimento ágil com múltiplos desenvolvedores, trabalhando em um projeto utilizando Angular para o frontend e Java no backend. Considerando a seguinte lista de categorias de BUGs, identifique os possíveis problemas de nossa equipe e também proponha soluções para reduzir a incidência de bugs nessas categorias '{categoria}'."
  if (len(actions_taken) > 0):
    prompt += f"\n Considerando que as seguintes ações já são executadas pelo time: {actions_taken}. Me informe de forma prática as ações que devem ser tomadas para melhorar"
  
  # st.write(f"Prompt passado para propor soluções: {prompt}")
  response = await content_generation(prompt)
  return response.text

async def content_generation(prompt):
  return model.generate_content(prompt)