import pandas as pd
from metrics import analise
from modelos import calc_score

# EXECUTA PARA O PRIMEIRO BOLÃO, QUE SÓ TEM ALGUNS JOGOS
previsoes_bolao1 = []
real_scores = []
bolao2 = pd.read_excel('dados/bolao-grupo-brasil.xlsx', sheet_name=None)
for sheet_name, df in bolao2.items():
  result = calc_score(df.iloc[1:, 0], df.iloc[1:, 1])
  previsoes_bolao1.append(result)
  real_scores.append((df.iloc[0, 0], df.iloc[0, 1]))

print('------------ BOLAO COM APENAS O GRUPO DO BRASIL')
print(' MEDIA')
analise(real_scores, [prev['media'] for prev in previsoes_bolao1])
print('MEDIANA')
analise(real_scores, [prev['mediana'] for prev in previsoes_bolao1])
print('MODA')
analise(real_scores, [prev['moda'] for prev in previsoes_bolao1])
print('MONTE CARLO')
analise(real_scores, [prev['monte-carlo'] for prev in previsoes_bolao1])

#######################

# EXECUTA PARA O SEGUNDO BOLÃO, QUE TEM TODOS OS JOGOS
previsoes_bolao1 = []
real_scores = []
bolao2 = pd.read_excel('dados/bolao-completo.xlsx', sheet_name=None)
for sheet_name, df in bolao2.items():
  for col_idx in range(df.shape[1]//2):
    result = calc_score(df.iloc[1:, 2*col_idx], df.iloc[1:, 2*col_idx+1])
    previsoes_bolao1.append(result)
    real_scores.append((df.iloc[0, 2*col_idx], df.iloc[0, 2*col_idx+1]))

print('\n\n------------ BOLAO COM TODOS OS JOGOS')
print('MEDIA')
analise(real_scores, [prev['media'] for prev in previsoes_bolao1])
print('MEDIANA')
analise(real_scores, [prev['mediana'] for prev in previsoes_bolao1])
print('MODA')
analise(real_scores, [prev['moda'] for prev in previsoes_bolao1])
print('MONTE CARLO')
analise(real_scores, [prev['monte-carlo'] for prev in previsoes_bolao1])

#######################

# EXECUTA PARA UM TERCEIRO BOLÃO COM MUITO MENOS PARTICIPANTES E COMPARA O DESEMPENHO SÓ NOS JOGOS QUE ESSE BOLÃO PEQUENO TEM
# para facilitar o excel ja tem os palpites do bolão pequeno (só nos jogos do brasil) e os mesmos jogos do maior bolão
prev_bolao_peq = []
prev_bolao_gran = []
real_scores = []
bolao3 = pd.read_excel('dados/comparacao-bolao-pequeno-e-grande.xlsx', sheet_name=0)
for col_idx in range(bolao3.shape[1]//4):
  result_peq = calc_score(bolao3.iloc[1:, 4*col_idx], bolao3.iloc[1:, 4*col_idx+1])
  prev_bolao_peq.append(result_peq)
  result_gran = calc_score(bolao3.iloc[1:, 4*col_idx+2], bolao3.iloc[1:, 4*col_idx+3])
  prev_bolao_gran.append(result_gran)
  real_scores.append((bolao3.iloc[0, 4*col_idx], bolao3.iloc[0, 4*col_idx+1]))

print('\n\n------------ BOLAO COM POUCOS PALPITES')
print('MEDIA DO GRUPO PEQUENO')
analise(real_scores, [prev['media'] for prev in prev_bolao_peq])
print('MEDIANA DO GRUPO PEQUENO')
analise(real_scores, [prev['mediana'] for prev in prev_bolao_peq])
print('MODA DO GRUPO PEQUENO')
analise(real_scores, [prev['moda'] for prev in prev_bolao_peq])
print('MONTE CARLO DO GRUPO PEQUENO')
analise(real_scores, [prev['monte-carlo'] for prev in prev_bolao_peq])

print('\n\n------------ BOLAO COM MUITOS PALPITES')
print('MEDIA DO GRUPO GRANDE')
analise(real_scores, [prev['media'] for prev in prev_bolao_gran])
print('MEDIANA DO GRUPO GRANDE')
analise(real_scores, [prev['mediana'] for prev in prev_bolao_gran])
print('MODA DO GRUPO GRANDE')
analise(real_scores, [prev['moda'] for prev in prev_bolao_gran])
print('MONTE CARLO DO GRUPO GRANDE')
analise(real_scores, [prev['monte-carlo'] for prev in prev_bolao_gran])