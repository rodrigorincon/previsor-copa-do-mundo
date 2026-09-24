import numpy as np
from scipy import stats

def calc_score(time1, time2, is_df_prm=True):
  time1 = remove_nan_df(time1) if is_df_prm else remove_nan_list(time1)
  time2 = remove_nan_df(time2) if is_df_prm else remove_nan_list(time2)
  
  media_val1 = np.mean(time1).round() # 1.5 vira 2 mas 2.5 tbm vira 2
  media_val2 = np.mean(time2).round()  
  mediana_val1 = np.median(time1)
  mediana_val2 = np.median(time2)
  moda_val1 = stats.mode(time1).mode
  moda_val2 = stats.mode(time2).mode
  return {
    'media': [media_val1, media_val2], 
    'mediana': [mediana_val1, mediana_val2], 
    'moda': [moda_val1, moda_val2], 
    'num_palpites': len(time1)
  }

def remove_nan_df(lista):
  return lista[~np.isnan(lista)]

def remove_nan_list(lista):
  return [x for x in lista if not np.isnan(x) and x is not None]