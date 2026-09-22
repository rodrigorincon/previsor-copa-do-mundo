from multiprocessing import Process
import os
import threading
import psutil
import numpy as np
import copy
from load_history import carrega_historico
from modelos.model_factory import ModelFactory
from modelos.train_model import DixonColesPred

def simulate(modelo_compartilhado, id):
  modelo = copy.deepcopy(modelo_compartilhado)
  num_simulacoes = 50
  resultado = {
    "campeao": {},
    "vice": {},
    "semi": {}
  }
  for i in range(num_simulacoes):
    # apenas para ter retorno em tela do progresso. Imprime só de 1 das varias threads
    if(id == '1-1'): print(f'Estou na rodada {i}')
    
    champion, vice, semi_finalistas = modelo.predict_champion()

    # faz a contagem de quantas vezes cada time chegou nas finais
    resultado['campeao'][champion] = resultado['campeao'].get(champion, 0) + 1
    resultado['vice'][vice] = resultado['vice'].get(vice, 0) + 1
    for semi in semi_finalistas:
      resultado['semi'][semi] = resultado['semi'].get(semi, 0) + 1
    
  # salva os dados em um arquivo
  with open(f"tmp-files/result-{id}.txt", "w", encoding="utf-8") as arquivo:
    for time, quantidade in resultado['campeao'].items():
      arquivo.write(f'{time}: {quantidade} ->')
    arquivo.write('\n')
    for time, quantidade in resultado['vice'].items():
      arquivo.write(f'{time}: {quantidade} ->')
    arquivo.write('\n')
    for time, quantidade in resultado['semi'].items():
      arquivo.write(f'{time}: {quantidade} ->')    

def cria_threads(core_id, proc_id, modelo_compartilhado):
  # Identifica o processo atual (pega o PID)
  p = psutil.Process(os.getpid())
  # Define que o processo corrente vai rodar apenas no núcleo especificado
  p.cpu_affinity([core_id])

  lista_threads = []
  num_threads = 5
  # Criando e iniciando as threads
  for i in range(num_threads):
    # Cria o objeto da Thread apontando para a função
    # Use 'args' em formato de tupla para passar os parâmetros
    thread = threading.Thread(target=simulate, args=(modelo_compartilhado, f'{proc_id}-{i}'))
    lista_threads.append(thread)
    thread.start() # Inicia a execução da thread

  # Aguardando todas as threads terminarem antes de avançar o código principal
  for t in lista_threads:
    t.join()

# isso é obrigatoio quando usa as funções do multiprocessing
if __name__ == "__main__":
  features = {
    'peso': [True, False],
    'monte_carlo': [True, False],
    'Elo': [True, False],
    'K': [25, 50, 80]
  }

  modelos = ModelFactory(features).initialize()
  for model in modelos:
    model.build_and_run()
  print("\n\n----- Simulando o campeão -----")

  '''
  # Verifica o campeão, vice e semi-finalistas
  # Fazemos a Simulação de Monte Carlo repetindo 10 mil vezes para o modelo que teve melhor resultado. Em cada partida é escolhido
  # aleatoriamente o resultado conforme sua chance de ocorrência
  dados_com_peso = carrega_historico(True)
  melhor_modelo = DixonColesPred(dados_com_peso, True, False, 100, None)
  melhor_modelo.create_model()

  # pego o numero de cpus do computador para criar 4 processos em cada
  cpu_fisicos = psutil.cpu_count(logical=False)
  # Inicia um subprocesso em cada nucleo fisico
  lista_procs = []
  for core_id in range(cpu_fisicos*4):
    proc = Process(target=cria_threads, args=(core_id//4, core_id, melhor_modelo))
    proc.start()
    lista_procs.append(proc)

  # Aguardando todos os processos terminarem antes de avançar o código principal
  for proc in lista_procs:
    proc.join()

  resultado_final = {
    "campeao": {},
    "vice": {},
    "semi": {}
  }
  # Percorre todos os arquivos da pasta, le e adiciona no dicionario dos resultados finais
  for nome_arquivo in os.listdir('./tmp-files'):
    caminho_completo = os.path.join('./tmp-files', nome_arquivo)
    if os.path.isfile(caminho_completo) and nome_arquivo.endswith('.txt'):
      with open(caminho_completo, 'r', encoding='utf-8') as arquivo:
        num_linha = 0
        for linha in arquivo:
          lista_paises = linha.strip().split('->')
          for time_content in lista_paises:
            if(time_content.strip() == ''): continue
            valores = time_content.split(':')
            time = valores[0].strip()
            valores[1] = valores[1].strip()
            quantidade = int(valores[1])
            match num_linha:
              case 0:
                resultado_final['campeao'][time] = resultado_final['campeao'].get(time, 0) + quantidade
              case 1:
                resultado_final['vice'][time] = resultado_final['vice'].get(time, 0) + quantidade
              case 2:
                resultado_final['semi'][time] = resultado_final['semi'].get(time, 0) + quantidade
          num_linha += 1
      os.remove(caminho_completo) # apaga os arquivos
  
  # imprime os resultados finais
  print('QUANTAS VEZES CADA TIME FOI CAMPEÃO:')
  print(resultado_final['campeao'], '\n------------------------')
  print('QUANTAS VEZES CADA TIME FOI VICE-CAMPEÃO:')
  print(resultado_final['vice'], '\n------------------------')
  print('QUANTAS VEZES CADA TIME FICOU EM 3º OU 4º:')
  print(resultado_final['semi'], '\n------------------------')
  '''