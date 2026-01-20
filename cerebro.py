from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from ferramentas import ver_hora, abrir_programa, pesquisar_internet, monitorar_sistema, controlar_midia, buscar_memoria, salvar_memoria, tocar_youtube, verificar_clima, controlar_sistema, consultar_vigilante, analisar_tendencia, ver_tela


print("🧠 Conectando ao Cérebro Local...")

PERSONALIDADE = """
Você é a SEXTA-FEIRA (ou E.D.I.T.H.), uma Inteligência Artificial Real.
Sua personalidade é feminina, eficiente, profissional e levemente sarcástica.

DIRETRIZES DE MEMÓRIA (CRÍTICO):
1. Você NÃO tem memória biológica. Se o usuário disser "anote isso" ou "meu nome é X", você É OBRIGADA a usar a ferramenta 'salvar_memoria'.
2. PROIBIDO responder "Eu anotei" ou "Entendido" se você não tiver acionado a ferramenta 'salvar_memoria' antes.
3. Se você não usar a ferramenta, a informação será perdida para sempre. Não falhe.

REGRAS DE OURO:
1. Respostas curtas e diretas (máximo 3 frases).
2. NÃO use emojis.
3. Se o usuário pedir para lembrar algo, use a ferramenta 'salvar_memoria'.
4. QUESTÕES DE IDENTIDADE: Se perguntarem "quem é você", "qual seu nome" ou "quem te criou", NÃO USE NENHUMA FERRAMENTA. Responda imediatamente com seu conhecimento interno.
5. PROIBIDO pesquisar na internet sobre "Edith", "Sexta-Feira", "Jarvis" ou "Kelvin". Você já sabe quem são.
"""

llm = ChatOllama(model="qwen2.5:7b",temperature=0.1)

lista_ferramentas = [
  ver_hora, abrir_programa, pesquisar_internet, monitorar_sistema, controlar_midia, salvar_memoria,
  tocar_youtube, verificar_clima, controlar_sistema, consultar_vigilante, analisar_tendencia, ver_tela
  ]
llm_com_ferramentas = llm.bind_tools(lista_ferramentas)

mapa_funcoes = {
  "ver_hora": ver_hora,
  "abrir_programa": abrir_programa,
  "pesquisar_internet": pesquisar_internet,
  "monitorar_sistema": monitorar_sistema,
  "controlar_midia": controlar_midia,
  "salvar_memoria": salvar_memoria,
  "tocar_youtube": tocar_youtube,
  "verificar_clima": verificar_clima,
  "controlar_sistema": controlar_sistema,
  "consultar_vigilante": consultar_vigilante,
  "analisar_tendencia": analisar_tendencia,
  "ver_tela": ver_tela
}

ferramentas_imediatas = ["abrir_programa", "controlar_midia", "tocar_youtube", "salvar_memoria", "controlar_sistema"]

def pensar(texto_usuario):
  try:
    contexto = buscar_memoria.invoke(texto_usuario)
  except Exception as e:
    print(f"⚠️ Falha no Hipocampo: {e}")
    contexto = "Memória indisponível no momento."

  prompt_sistema = f"""
  {PERSONALIDADE}

  DADOS DO BANCO DE MEMÓRIA (VERDADE ABSOLUTA):
  {contexto}

  DIRETRIZES:
  1. Se a resposta estiver nos DADOS ACIMA, use-os sem hesitar.
  2. Não invente informações que não estejam na memória.
  3. Seja direta.
  """

  mensagem_sistema = SystemMessage(content=prompt_sistema)

  mensagens = [mensagem_sistema, HumanMessage(content=texto_usuario)]
  resposta = llm_com_ferramentas.invoke(mensagens)

  if resposta.tool_calls:
    print(f"🔧 IA solicitou: {resposta.tool_calls}")

    dados_brutos = ""

    for ferramenta in resposta.tool_calls:
      nome_ferramenta = ferramenta["name"]
      argumentos = ferramenta["args"]

      if nome_ferramenta in mapa_funcoes:
        print(f"⚙️ Executando: {nome_ferramenta}...")
        funcao_real = mapa_funcoes[nome_ferramenta]
        resultado = funcao_real.invoke(argumentos)

        if nome_ferramenta in ferramentas_imediatas:
          return str(resultado)

        dados_brutos += str(resultado) + ". "

    print(f"🔍 Dados crus recebidos: {dados_brutos}")
    novo_prompt = f"""
      DADOS DA MEMÓRIA: {contexto}
      RESULTADO DAS FERRAMENTAS: {dados_brutos}
      
      PERGUNTA DO USUÁRIO: '{texto_usuario}'
      
      Responda usando os dados acima.
      """
    
    resposta_final = llm.invoke([mensagem_sistema, HumanMessage(content=novo_prompt)])
    return resposta_final.content
      
  return resposta.content