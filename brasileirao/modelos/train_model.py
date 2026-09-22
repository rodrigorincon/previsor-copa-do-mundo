from typing import List, Tuple
import pandas as pd
import numpy as np
from penaltyblog.models import DixonColesGoalModel
from penaltyblog.ratings import Elo
from penaltyblog.models import create_dixon_coles_grid
import campeonato

MAX_GOLS = 7
class DixonColesPred:
  df: pd.DataFrame
  modelo: DixonColesGoalModel
  params: any
  rho: float
  vantagem_mandante: float
  elo: Elo = None
  times: List[pd.DataFrame]
  monte_carlo_num_sim: int

  def __init__(self, df, monte_carlo: bool, use_elo: bool, monte_carlo_num_sim: int = 50_000, k_elo: int|None= None):
    self.df = df
    self.monte_carlo = monte_carlo
    self.monte_carlo_num_sim = monte_carlo_num_sim
    if(use_elo): self.configure_elo(k_elo)

  def create_model(self)->None:
    # treina o modelo usando o peso com vários fatores que inventamos
    self.modelo = DixonColesGoalModel(
      self.df["gols_mandante"].to_numpy(copy=True),
      self.df["gols_visitante"].to_numpy(copy=True),
      self.df["time_mandante"].to_numpy(copy=True), # to_numpy porque a biblioteca do modelo trabalha com números, não com dataframe e o copy é para que ele possa fazer alterações internas nos dados sem afetar os originais
      self.df["time_visitante"].to_numpy(copy=True),
      weights=self.df["peso"].to_numpy(copy=True),
    ) # params: gols do time da casa, gols do visitante, nome do time da casa, nome do visitante. Peso é opcional

    self.modelo.fit() # define um valor de ataque e de defesa para cada time, uma constante de vantagem para o dono da casa
    self.params = self.modelo.get_params()
    self.rho = self.params['rho']
    self.vantagem_mandante = self.params['home_advantage']

  # aqui não tem a opção de mandar None como k_param. É preciso passar algum K
  def configure_elo(self, k_param: int):
    # por default todo mundo começa com 1500 e vai mudando a cada jogo do dataset
    # home_field_advantage é o quanto adicionamos de vantagem pro mandante da casa
    self.elo = Elo(k=k_param, home_field_advantage=75)

    # atualiza o ELO apos cada jogo
    diff_elo_jogos_neutros = []
    diff_gols_jogos_neutros = []
    for i in range(self.df.shape[0]):
      line = self.df.iloc[i]
      mandante_nome = line['time_mandante']
      visitante_nome = line['time_visitante']
      mandante_gols = line['gols_mandante']
      visitante_gols = line['gols_visitante']

      if(mandante_gols > visitante_gols):
        result = 0
      else:
        if(mandante_gols == visitante_gols):
          result = 1 
        else: 
          result = 2
      self.elo.update_ratings(mandante_nome, visitante_nome, result)

  def calc_expect_goals(self, time1_name, time2_name, local):
    atk_time1 = self.params[f'attack_{time1_name}']
    def_time1 = self.params[f'defence_{time1_name}']
    atk_time2 = self.params[f'attack_{time2_name}']
    def_time2 = self.params[f'defence_{time2_name}']

    expect_gols_time1 = np.exp( atk_time1 + def_time2)
    expect_gols_time2 = np.exp( atk_time2 + def_time1)

    if(self.elo):
      elo_time1 = self.elo.get_team_rating(time1_name)
      elo_time2 = self.elo.get_team_rating(time2_name)
      diff_abs = abs(elo_time1 - elo_time2)
      if(diff_abs < 0.5): diff_abs = 1 # para evitar log de valores muito baixos, que tendem ao -infinito (log(1) = 0, então zera o lado do elo)
      diff_time1_signal = 1 if elo_time1 >= elo_time2 else -1
      diff_time2_signal = 1 if elo_time2 >= elo_time1 else -1

      # Peso jogo: 80% dixon-coles e 20% ELO
      expect_gols_time1 = 0.8 * expect_gols_time1  + 0.2 * diff_time1_signal * np.log(diff_abs)
      expect_gols_time2 = 0.8 * expect_gols_time2  + 0.2 * diff_time2_signal * np.log(diff_abs)

    # como lambda representa os gols esperados, ñ pode ser negativo. Portanto vamos considerar o menor valor como 0.05 (proximo de 0, mas com alguma chance de fazer gol ainda)
    expect_gols_time1 = max(expect_gols_time1, 0.05)
    expect_gols_time2 = max(expect_gols_time2, 0.05)

    # soma expectativa adicional de gols para o mandante
    if(time1_name == local):
      expect_gols_time1 *= np.exp(self.vantagem_mandante)
    if(time2_name == local):
      expect_gols_time2 *= np.exp(self.vantagem_mandante)

    return expect_gols_time1, expect_gols_time2

  def predict(self)-> Tuple[List[Tuple[int,int]],List[Tuple[int,int]]]:
    real_scores = []
    pred_scores = []
    self.times = campeonato.tabela_zerada()
    for _, time1 in self.times.iterrows():
      for _, time2 in self.times.iterrows():
        if(time1['nome'] == time2['nome']): continue

        time1_name = time1['nome']
        time2_name = time2['nome']
        score_real = campeonato.match_score(time1_name, time2_name)
        if(not score_real): continue

        expect_goals_time1, expect_goals_time2 = self.calc_expect_goals(time1_name, time2_name, time1_name)
        # retorna o mesmo objeto do predict, portanto esse método faz a mesma função do predict 
        # para quando vc já tem a previsão de gols vindas de algum lugar (como um bolão ou bet) ou quando quer dar seus proprios pesos a chance de gols
        previsao = create_dixon_coles_grid(expect_goals_time1, expect_goals_time2, self.rho, max_goals=MAX_GOLS)
        matriz_placar = previsao.grid

        if(self.monte_carlo):
          gols_time1, gols_time2 = self.monte_carlo_score(matriz_placar)
        else:
          gols_time1, gols_time2 = self.most_common_score(matriz_placar)

        real_scores.append(score_real)
        pred_scores.append( (gols_time1, gols_time2) )
        self.fill_score_group_table(time1_name, time2_name, gols_time1, gols_time2)
    return real_scores, pred_scores

  def most_common_score(self, matriz_placar):
    return np.unravel_index(np.argmax(matriz_placar), matriz_placar.shape)

  def monte_carlo_score(self, matriz_placar):
    # transforma a matriz em um array com as probabilidades
    probabilidades = np.array(matriz_placar).reshape(-1)
    # Normalizar as probabilidades para garantir que somem exatamente 1.0 (exigência do numpy). Antes estava dando 0.9999999999
    probabilidades /= probabilidades.sum()

    # Sorteia os índices (placares) com base na probabilidade (É AQUI QUE A SIMULAÇÃO É EXECUTADA)
    indices_sorteados = np.random.choice(len(probabilidades), size=self.monte_carlo_num_sim, p=probabilidades)
    indice_mais_repetido = np.argmax(np.bincount(indices_sorteados))
    gols_time1 = indice_mais_repetido//(MAX_GOLS+1) # recupera qual era a linha da matriz (pega a divisao inteira por MAX_GOLS+1 pq o tamanho de cada linha é MAX_GOLS+1)
    gols_time2 = indice_mais_repetido % (MAX_GOLS+1) # recupera qual a coluna da matriz (o resto da divisão por MAX_GOLS+1 dá a coluna)
    return gols_time1, gols_time2

  def fill_score_group_table(self, time1_name, time2_name, gols_time1, gols_time2):
    line1 = self.times.loc[self.times['nome'] == time1_name]
    line2 = self.times.loc[self.times['nome'] == time2_name]

    line1['gols_feitos'] += gols_time1
    line1['saldo_gols'] += gols_time1 - gols_time2
    line1['pontos'] += 3 if gols_time1 > gols_time2 else (0 if gols_time1 < gols_time2 else 1)

    line2['gols_feitos'] += gols_time2
    line2['saldo_gols'] += gols_time2 - gols_time1
    line2['pontos'] += 3 if gols_time2 > gols_time1 else (0 if gols_time2 < gols_time1 else 1)

    self.times.loc[self.times['nome'] == time1_name] = line1
    self.times.loc[self.times['nome'] == time2_name] = line2
