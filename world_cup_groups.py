import pandas as pd

# saldo gols, gols marcados (o 1º é confronto direto mas podemos ignora-lo pois saldo bsempre ateu com confronto direto nessa copa)
def sort_group(grupo):
  return grupo.sort_values(['pontos', 'saldo_gols', 'gols_feitos'], ascending=False)

def groups():
  return [ groupA(), groupB(), groupC(), groupD(), groupE(), groupF(), groupG(), groupH(), groupI(), groupJ(), groupK(), groupL() ]

# retorna o indice do 1º time, o indice do 2º, o país aonde aconteceu e uma tupla com o placar final
# o placar final está na ordem dos índices
def group_match(grupo_idx, rodada):
  match grupo_idx:
    case 0:
      return groupA_matches(rodada)
    case 1:
      return groupB_matches(rodada)
    case 2:
      return groupC_matches(rodada)
    case 3:
      return groupD_matches(rodada)
    case 4:
      return groupE_matches(rodada)
    case 5:
      return groupF_matches(rodada)
    case 6:
      return groupG_matches(rodada)
    case 7:
      return groupH_matches(rodada)
    case 8:
      return groupI_matches(rodada)
    case 9:
      return groupJ_matches(rodada)
    case 10:
      return groupK_matches(rodada)
    case 11:
      return groupL_matches(rodada)

def groupA():
  return pd.DataFrame({
    'time': ['Mexico', 'South Africa', 'South Korea', 'Czech Republic'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupA_matches(rodada):
  match rodada:
    case 0:
      return [(0,1,'Mexico',(2,0)),(2,3,'Mexico',(2,1))]
    case 1:
      return [(3,1,'Mexico',(1,1)),(0,2,'Mexico',(1,0))]
    case 2:
      return [(1,2,'Mexico',(1,0)),(3,0,'Mexico',(0,3))]
    case _:
      return []

def groupB():
  return pd.DataFrame({
    'time': ['Canada', 'Switzerland', 'Bosnia and Herzegovina', 'Qatar'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupB_matches(rodada):
  match rodada:
    case 0:
      return [(0,2,'Canada',(1,1)),(1,3,'Canada',(1,1))]
    case 1:
      return [(1,2,'Canada',(4,1)),(0,3,'Canada',(6,0))]
    case 2:
      return [(1,0,'Canada',(2,1)),(2,3,'Canada',(3,1))]
    case _:
      return []

def groupC():
  return pd.DataFrame({
    'time': ['Brazil', 'Morocco', 'Scotland', 'Haiti'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupC_matches(rodada):
  match rodada:
    case 0:
      return [(0,1,'United States',(1,1)),(3,2,'United States',(0,1))]
    case 1:
      return [(2,1,'United States',(0,1)),(0,3,'United States',(3,0))]
    case 2:
      return [(1,3,'United States',(4,2)),(2,0,'United States',(0,3))]
    case _:
      return []

def groupD():
  return pd.DataFrame({
    'time': ['United States', 'Australia', 'Paraguay', 'Turkey'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupD_matches(rodada):
  match rodada:
    case 0:
      return [(0,2,'United States',(4,1)),(1,3,'United States',(2,0))]
    case 1:
      return [(0,1,'United States',(2,0)),(3,2,'United States',(0,1))]
    case 2:
      return [(3,0,'United States',(3,2)),(2,1,'United States',(0,0))]
    case _:
      return []

def groupE():
  return pd.DataFrame({
    'time': ['Germany', 'Ivory Coast', 'Ecuador', 'Curaçao'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupE_matches(rodada):
  match rodada:
    case 0:
      return [(0,3,'United States',(7,1)),(1,2,'United States',(1,0))]
    case 1:
      return [(0,1,'United States',(2,1)),(2,3,'United States',(0,0))]
    case 2:
      return [(3,1,'United States',(0,2)),(2,0,'United States',(2,1))]
    case _:
      return []

def groupF():
  return pd.DataFrame({
    'time': ['Netherlands', 'Japan', 'Sweden', 'Tunisia'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupF_matches(rodada):
  match rodada:
    case 0:
      return [(0,1,'United States',(2,2)),(2,3,'United States',(5,1))]
    case 1:
      return [(0,2,'United States',(5,1)),(3,1,'United States',(0,4))]
    case 2:
      return [(3,0,'United States',(1,3)),(1,2,'United States',(1,1))]
    case _:
      return []

def groupG():
  return pd.DataFrame({
    'time': ['Belgium', 'Egypt', 'Iran', 'New Zealand'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupG_matches(rodada):
  match rodada:
    case 0:
      return [(0,1,'United States',(1,1)),(2,3,'United States',(2,2))]
    case 1:
      return [(0,2,'United States',(0,0)),(3,1,'United States',(1,3))]
    case 2:
      return [(3,0,'United States',(1,5)),(1,2,'United States',(1,1))]
    case _:
      return []

def groupH():
  return pd.DataFrame({
    'time': ['Spain', 'Cape Verde', 'Uruguay', 'Saudi Arabia'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupH_matches(rodada):
  match rodada:
    case 0:
      return [(0,1,'United States',(0,0)),(2,3,'United States',(1,1))]
    case 1:
      return [(0,3,'United States',(4,0)),(1,2,'United States',(2,2))]
    case 2:
      return [(0,2,'United States',(1,0)),(1,3,'United States',(0,0))]
    case _:
      return []

def groupI():
  return pd.DataFrame({
    'time': ['France', 'Norway', 'Senegal', 'Iraq'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupI_matches(rodada):
  match rodada:
    case 0:
      return [(0,2,'United States',(3,1)),(3,1,'United States',(1,4))]
    case 1:
      return [(0,3,'United States',(3,0)),(1,2,'United States',(3,2))]
    case 2:
      return [(1,0,'United States',(1,4)),(2,3,'United States',(5,0))]
    case _:
      return []

def groupJ():
  return pd.DataFrame({
    'time': ['Argentina', 'Austria', 'Algeria', 'Jordan'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupJ_matches(rodada):
  match rodada:
    case 0:
      return [(0,2,'United States',(3,0)),(1,3,'United States',(3,1))]
    case 1:
      return [(0,1,'United States',(2,0)),(3,2,'United States',(1,2))]
    case 2:
      return [(2,1,'United States',(3,3)),(3,0,'United States',(1,3))]
    case _:
      return []

def groupK():
  return pd.DataFrame({
    'time': ['Colombia', 'Portugal', 'DR Congo', 'Uzbekistan'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupK_matches(rodada):
  match rodada:
    case 0:
      return [(3,0,'United States',(1,3)),(1,2,'United States',(1,1))]
    case 1:
      return [(1,3,'United States',(5,0)),(0,2,'United States',(1,0))]
    case 2:
      return [(0,1,'United States',(0,0)),(2,3,'United States',(3,1))]
    case _:
      return []

def groupL():
  return pd.DataFrame({
    'time': ['England', 'Croatia', 'Ghana', 'Panama'],
    'pontos': [0,0,0,0],
    'saldo_gols': [0,0,0,0],
    'gols_feitos': [0,0,0,0]
  })

def groupL_matches(rodada):
  match rodada:
    case 0:
      return [(0,1,'United States',(4,2)),(2,3,'United States',(1,0))]
    case 1:
      return [(0,2,'United States',(0,0)),(3,1,'United States',(0,1))]
    case 2:
      return [(3,0,'United States',(0,2)),(1,2,'United States',(2,1))]
    case _:
      return []