import edge_tts
import asyncio
import pygame
import os

VOZ = "pt-BR-FranciscaNeural"

async def gerar_audio(texto):
  comunicacao = edge_tts.Communicate(texto, VOZ, rate="+10%")
  await comunicacao.save("fala_temp.mp3")

def tocar_audio():
  pygame.mixer.init()
  pygame.mixer.music.load("fala_temp.mp3")
  pygame.mixer.music.play()

  while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(15)

  pygame.mixer.music.unload()
  pygame.mixer.quit()
  
def falar(texto):
  if os.path.exists("fala_temp.mp3"):
    try:
      os.remove("fala_temp.mp3")
    except:
      pass
    
  asyncio.run(gerar_audio(texto))
  tocar_audio()