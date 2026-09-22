import pandas as pd
from datetime import date

def carrega_historico(calc_peso: bool = True):
  df = pd.read_csv('brasileirao-2005-2025.csv')
  df['peso'] = 1
  if(not calc_peso): return df
  return adiciona_peso(df)

def calcula_peso_tempo(ano):
  current_year = date.today().year
  diferenca = current_year - int(ano)
  expoente = diferenca // 2
  return (1/2.0)**(expoente)

def adiciona_peso(df):
  # a cada 2 anos o peso decai em 0,75. Cai mais rapido que na copa do mundo devido as mudanças rápidas do time e técnicos
  df['peso'] = df.ano_campeonato.apply(calcula_peso_tempo)
  return df
