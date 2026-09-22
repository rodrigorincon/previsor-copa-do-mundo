from typing import List
from load_history import carrega_historico
from modelos.model_controller import ModelController

class ModelFactory:
  pesos: List[bool]
  use_monte_carlo: List[bool]
  elos: List[bool]
  k_list: List[int|None]

  def __init__(self, features):
    self.pesos = features['peso']
    self.use_monte_carlo = features['monte_carlo']
    self.elos = features['Elo']
    self.k_list = features['K']

  def set_pesos(self):
    dados_com_peso = carrega_historico(True)
    dados_sem_peso = carrega_historico(False)

    dados_list = [None, None]
    if(True in self.pesos):
      true_idx = self.pesos.index(True)
      dados_list[true_idx] = dados_com_peso
    if(False in self.pesos):
      false_idx = self.pesos.index(False)
      dados_list[false_idx] = dados_sem_peso

    return dados_list

  def initialize(self):
    dados_list = self.set_pesos()

    model_list = []
    for peso_idx, peso in enumerate(self.pesos):
      if(peso == None): continue

      for monte_carlo in self.use_monte_carlo:
        for elo in self.elos:
          dataset = dados_list[peso_idx]
          if(elo):
            for k in self.k_list:
              nome = "Com peso, " if peso else 'Sem peso, '
              nome += "Com Monte Carlo, " if monte_carlo else 'Com resultado mais provável, '
              nome += "com Elo"
              nome += f' e K = {k}' if k else ' e K padrão'
              model = ModelController(nome, dataset, monte_carlo, elo, k)
              model_list.append(model)
          else:
            nome = "Com peso, " if peso else 'Sem peso, '
            nome += "Com Monte Carlo, " if monte_carlo else 'Com resultado mais provável, '
            nome += 'sem Elo'
            model = ModelController(nome, dataset, monte_carlo, elo, None)
            model_list.append(model)
    return model_list