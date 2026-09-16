import pandas as pd
import numpy as np
from penaltyblog.models import DixonColesGoalModel
from penaltyblog.ratings import Elo
import seaborn as sns
import matplotlib.pyplot as plt
from penaltyblog.models import create_dixon_coles_grid
from load_history import carrega_historico
from train_model import DixonColesPred
import world_cup_groups as wpg

df = carrega_historico(True)
modelo = DixonColesPred(df)
modelo.create_model()
modelo.configure_elo()
MAX_GOLS = 7

all_groups = wpg.groups()
for group_idx, group in enumerate(all_groups):
  for rodada in range(3):
    jogos = wpg.group_match(group_idx, rodada)
    for jogo in jogos:
      time1_name = group.iloc[jogo[0]]['time']
      time2_name = group.iloc[jogo[1]]['time']
      expect_goals_time1, expect_goals_time2 = modelo.calc_expect_goals(time1_name, time2_name, jogo[2])

      # retorna o mesmo objeto do predict, portanto esse método faz a mesma função do predict 
      # para quando vc já tem a previsão de gols vindas de algum lugar (como um bolão ou bet) ou quando quer dar seus proprios pesos a chance de gols
      previsao = create_dixon_coles_grid(expect_goals_time1, expect_goals_time2, modelo.rho, max_goals=MAX_GOLS)
      matriz_placar = previsao.grid

      max_val = matriz_placar.max()
      gols_time1, gols_time2 = np.unravel_index(np.argmax(matriz_placar), matriz_placar.shape)

      print(f"Placar mais provável: {time1_name} {gols_time1} x {time2_name} {gols_time2}")