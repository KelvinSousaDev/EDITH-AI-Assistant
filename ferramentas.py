import datetime
import subprocess
from langchain_core.tools import tool
from ddgs import DDGS
import psutil

@tool
def ver_hora():
  """
    Retorna o horário atual do sistema. Use isso quando o usuário perguntar as horas ou a data de hoje.
  """
  hora_atual = datetime.datetime.now()
  hora_formatada = hora_atual.strftime("%H:%M do dia %d/%m/%Y")
  return hora_formatada

@tool
def abrir_programa(nome_programa: str):
  """
    Abre um programa no computador.
    O argumento 'nome_programa' deve ser um destes: 'chrome', 'bloco de notas', 'calculadora', 'spotify'.
  """
  
  programas = {
    "chrome": "start chrome",
    "bloco de notas": "notepad",
    "calculadora": "calc",
    "spotify": "start spotify" # Funciona se estiver instalado na loja/caminho
    }
  
  chave = nome_programa.lower().strip()

  if chave in programas:
    subprocess.Popen(programas[chave], shell=True)
    return f"Abrindo {chave} para o senhor."
  else:
    return f"Desculpe, não sei como abrir '{nome_programa}' ainda."

@tool
def pesquisar_internet(pergunta: str):
  """
      Pesquisa informações na internet.
      Use isso para buscar fatos atuais, notícias, clima ou dados que você não sabe.
  """

  with DDGS() as ddgs:
    resultados = ddgs.text(pergunta, max_results=3)
    resposta = ""
    for resultado in resultados:
      titulo = resultado["title"]
      resumo = resultado["body"]
      frase = f"{titulo} - {resumo} \n"
      resposta += frase
    
    return resposta
  
@tool
def monitorar_sistema():
  """
    Verifica o uso atual do sistema (CPU, Memória RAM e Bateria).
    Use isso quando o usuário perguntar: 'Como está o PC?', 'Uso de CPU', 'Memória' ou 'Bateria'.
  """

  uso_cpu = psutil.cpu_percent(interval=1)
  uso_ram = psutil.virtual_memory().percent

  resposta = f"CPU em {uso_cpu}%. Memória RAM em {uso_ram}%."

  bateria = psutil.sensors_battery()
  if bateria:
    resposta += f"Bateria em {bateria.percent}%"
  else:
    resposta += " Ligado na tomada (Sem bateria)."
  return resposta