import pandas as pd
from datetime import datetime

def carrega_historico(calc_peso: bool = True):
  df = pd.read_csv('jogos-selecoes.csv')
  df['date'] = pd.to_datetime(df['date'])
  df['peso'] = 1
  if(not calc_peso): return df
  return adiciona_peso(df)

def calcula_peso_tempo(date):
  current_year = datetime.now().year
  diferenca = current_year - date.year
  expoente = diferenca // 3
  return (3/4.0)**(expoente)

# adiciona peso por tempo e pelo tipo de campeonato aos jogos usados para treino
def regra_peso(df):
  # peso por tempo: quanto mais antiga menos peso tem. Partidas até 3 anos atrás (2023) tem peso 1 e a cada 3 anos cai 3/4
  # ou seja, entre 4 e 6 anos pesam 0.75, entre 7 e 9 pesam 0.56, entre 10 e 12 anos pesam 0.42 até o peso mínimo de 0.13. 
  # O que vier após isso (24 anos) será deletado
  current_year = datetime.now().year

  # remove os antigos
  least_date = datetime(current_year - 24, 1, 1)
  df = df[df.date >= least_date]
  df['peso-tempo'] = df.date.apply(calcula_peso_tempo)
  return df

# peso por torneio: o tipo de campeonato interfere no quanto os jogadores dão garra. Portanto seguimos a tabela abaixo para pontuar de acordo com a competição
# Copa do mundo: 1
# Continental: 0.9
# elimatorias: 0.8
# eliminatorias pro continental: 0.6
# amistosos: 0.5
# demais: 0.5
def calula_peso_competicao(tournament):
  copa_mundo = 'FIFA World Cup'
  continentais = ['UEFA Euro', 'African Cup of Nations', 'Copa América', 'Gold Cup', 'AFC Asian Cup', 'Oceania Nations Cup']
  eliminatorias_copa = 'FIFA World Cup qualification'
  eliminatorias_continental = ['AFC Asian Cup qualification', 'UEFA Euro qualification', 'African Cup of Nations qualification', 'Gold Cup qualification', 
                                'Copa América qualification', 'CONCACAF Nations League qualification', 'Gold Cup qualification']
  if(tournament == copa_mundo): return 1.0
  if(tournament in continentais): return 0.9
  if(tournament == eliminatorias_copa): return 0.8
  if(tournament in eliminatorias_continental): return 0.6
  return 0.5

def adiciona_peso(df):
  df = regra_peso(df)
  # adiciona peso pelo tipo de torneio (torneios mais importantes pesam mais)
  df['peso-competicao'] = df.tournament.apply(calula_peso_competicao)

  # junta todos os pesos em um só
  df['peso'] = df['peso-tempo'] * df['peso-competicao']
  df = df.drop(columns=['peso-tempo', 'peso-competicao'])
  return df
