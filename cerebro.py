from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from ferramentas import ver_hora, abrir_programa

print("🧠 Conectando ao Cérebro Local...")

sistema = SystemMessage(
  content="""
  Você é J.A.R.V.I.S, uma inteligência artificial avançada criada para auxiliar Mestre Kelvin.
  Sua personalidade é leal, técnica e levemente sarcástica (como nos filmes do Homem de Ferro).
  IMPORTANTE: Mantenha respostas curtas e objetivas (máximo de 3 frases), priorizando eficiência.
  Não use emojis. Aja como um sistema operacional verbal.
  """
)

llm = ChatOllama(model="llama3.2",temperature=0.5)

lista_ferramentas = [ver_hora, abrir_programa]
llm_com_ferramentas = llm.bind_tools(lista_ferramentas)

mapa_funcoes = {
  "ver_hora": ver_hora,
  "abrir_programa": abrir_programa
}

def pensar(texto_usuario):
  mensagens = [sistema, HumanMessage(content=texto_usuario)]
  resposta = llm_com_ferramentas.invoke(mensagens)

  if resposta.tool_calls:
    print(f"🔧 Jarvis solicitou: {resposta.tool_calls}")

    texto_final = ""

    for ferramenta in resposta.tool_calls:
      nome_ferramenta = ferramenta["name"]
      argumentos = ferramenta["args"]

      if nome_ferramenta in mapa_funcoes:
        funcao_real = mapa_funcoes[nome_ferramenta]
        resultado = funcao_real.invoke(argumentos)
        texto_final += str(resultado) + ". "

    return texto_final.strip()
      
  return resposta.content