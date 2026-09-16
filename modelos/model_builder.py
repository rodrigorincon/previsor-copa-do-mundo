import pandas as pd
from metrics import analise
from modelos.train_model import DixonColesPred


class ModelBuilder:
  modelo: DixonColesPred
  usa_elo: bool
  k: int|None
  df: pd.Dataframe
  nome: str

  def __init__(self, nome: str, df: pd.DataFrame, usa_elo: bool, k: int|None):
    self.nome = nome
    self.df = df
    self.usa_elo = usa_elo
    self.k = k

  def build(self):
    self.modelo = DixonColesPred(self.df, self.usa_elo, self.k)
    self.modelo.create_model()
    if(not self.k): self.nome += f" ({self.get_k():.0f})"

  def build_and_run(self):
    self.build()
    real, predict = self.modelo.predict()
    print('\n------', self.nome ,'------')
    analise(real, predict)

  def get_k(self):
    if(self.k): return self.k 
    if(self.modelo.elo): return self.modelo.elo.k
    return 0