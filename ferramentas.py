import datetime
import subprocess
from langchain_core.tools import tool

@tool
def ver_hora():
  """Retorna o horário atual do sistema. Use isso quando o usuário perguntar as horas ou a data de hoje."""
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
