from typing import List, Tuple
import pandas as pd
import numpy as np
from penaltyblog.models import DixonColesGoalModel
from penaltyblog.ratings import Elo
from penaltyblog.models import create_dixon_coles_grid
import world_cup_groups as wpg

MAX_GOLS = 7
class DixonColesPred:
  df: pd.DataFrame
  modelo: DixonColesGoalModel
  params: any
  rho: float
  vantagem_mandante: float
  elo: Elo = None

  def __init__(self, df, use_elo: bool, k_elo: int|None= None):
    self.df = df
    if(use_elo): self.configure_elo(k_elo)

  def create_model(self)->None:
    # treina o modelo usando o peso com vários fatores que inventamos
    self.modelo = DixonColesGoalModel(
      self.df["home_score"].to_numpy(copy=True),
      self.df["away_score"].to_numpy(copy=True),
      self.df["home_team"].to_numpy(copy=True), # to_numpy porque a biblioteca do modelo trabalha com números, não com dataframe e o copy é para que ele possa fazer alterações internas nos dados sem afetar os originais
      self.df["away_team"].to_numpy(copy=True),
      weights=self.df["peso"].to_numpy(copy=True),
    ) # params: gols do time da casa, gols do visitante, nome do time da casa, nome do visitante. Peso é opcional

    self.modelo.fit() # define um valor de ataque e de defesa para cada time, uma constante de vantagem para o dono da casa
    self.params = self.modelo.get_params()
    self.rho = self.params['rho']
    self.vantagem_mandante = self.params['home_advantage']
    
  def set_k(self):
    k_values = self.df.tournament.apply(self.valor_k_competicao)
    return sum(k_values)/len(k_values)

  # calculando K como a média dos campeonatos na base de dados
  # segundo a biblioteca, um site importante aplica Elo diferentes para cada torneio (60 copa, 50 continental, 40 eliminatorias, 20 amistoso e 30 os demais)
  # aplicaremos esse valores pros torneios e tirar a média para ter o Elo final
  def valor_k_competicao(self, tournament):
    copa_mundo = 'FIFA World Cup'
    continentais = ['UEFA Euro', 'African Cup of Nations', 'Copa América', 'Gold Cup', 'AFC Asian Cup', 'Oceania Nations Cup']
    eliminatorias_copa = 'FIFA World Cup qualification'
    eliminatorias_continental = ['AFC Asian Cup qualification', 'UEFA Euro qualification', 'African Cup of Nations qualification', 'Gold Cup qualification', 
                                'Copa América qualification', 'CONCACAF Nations League qualification', 'Gold Cup qualification']
    if(tournament == copa_mundo): return 60
    if(tournament in continentais): return 50
    if(tournament == eliminatorias_copa): return 40
    if(tournament in eliminatorias_continental): return 40
    if(tournament == 'Friendly'): return 20
    return 30

  def configure_elo(self, k_param: int|None= None):
    k_final = k_param or self.set_k()
    # por default todo mundo começa com 1500 e vai mudando a cada jogo do dataset
    # home_field_advantage é o quanto adicionamos de vantagem pro mandante da casa
    self.elo = Elo(k=k_final, home_field_advantage=75)

    # atualiza o ELO apos cada jogo
    diff_elo_jogos_neutros = []
    diff_gols_jogos_neutros = []
    for i in range(self.df.shape[0]):
      line = self.df.iloc[i]
      mandante_nome = line['home_team']
      visitante_nome = line['away_team']
      mandante_gols = line['home_score']
      visitante_gols = line['away_score']

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
    all_groups = wpg.groups()
    for group_idx, group in enumerate(all_groups):
      for rodada in range(3):
        jogos = wpg.group_match(group_idx, rodada)
        for jogo in jogos:
          time1_name = group.iloc[jogo[0]]['time']
          time2_name = group.iloc[jogo[1]]['time']
          expect_goals_time1, expect_goals_time2 = self.calc_expect_goals(time1_name, time2_name, jogo[2])

          # retorna o mesmo objeto do predict, portanto esse método faz a mesma função do predict 
          # para quando vc já tem a previsão de gols vindas de algum lugar (como um bolão ou bet) ou quando quer dar seus proprios pesos a chance de gols
          previsao = create_dixon_coles_grid(expect_goals_time1, expect_goals_time2, self.rho, max_goals=MAX_GOLS)
          matriz_placar = previsao.grid

          gols_time1, gols_time2 = np.unravel_index(np.argmax(matriz_placar), matriz_placar.shape)
          real_scores.append(jogo[3])
          pred_scores.append( (gols_time1, gols_time2) )

    return real_scores, pred_scores