import pandas as pd
from metrics import analise
from modelos import calc_score

def transforma_tuplas(df):
  return list(df.itertuples(index=False, name=None))

# le os arquivos e retira os palpites para cada jogo
bolao1 = pd.read_excel('dados/bolao-grupo-brasil.xlsx', sheet_name=None)
sheet_br_marrocos =  transforma_tuplas(bolao1['br-marrocos'].iloc[1:])
sheet_br_haiti =  transforma_tuplas(bolao1['br-haiti'].iloc[1:])
sheet_br_escocia =  transforma_tuplas(bolao1['br-escocia'].iloc[1:])
sheet_haiti_escocia =  transforma_tuplas(bolao1['haiti-escocia'].iloc[1:])
sheet_escocia_marrocos =  transforma_tuplas(bolao1['escocia-marrocos'].iloc[1:])
sheet_marrocos_haiti =  transforma_tuplas(bolao1['marrocos-haiti'].iloc[1:])

bolao2 = pd.read_excel('dados/bolao-completo.xlsx', sheet_name=None)
b2_br_marrocos = transforma_tuplas(bolao2['pt1'].iloc[1:, 10:12])
b2_br_haiti = transforma_tuplas(bolao2['pt3'].iloc[1:, 12:14])
b2_br_escocia = transforma_tuplas(bolao2['pt5'].iloc[1:, 8:10])
b2_haiti_escocia = transforma_tuplas(bolao2['pt1'].iloc[1:, 12:14])
b2_escocia_marrocos = transforma_tuplas(bolao2['pt3'].iloc[1:, 10:12])
b2_marrocos_haiti = transforma_tuplas(bolao2['pt5'].iloc[1:, 10:12])

bolao3 = pd.read_excel('dados/comparacao-bolao-pequeno-e-grande.xlsx', sheet_name=0)
b3_br_escocia = transforma_tuplas(bolao3.iloc[1:, 0:2])
b3_br_marrocos = transforma_tuplas(bolao3.iloc[1:, 8:10])
b3_br_haiti = transforma_tuplas(bolao3.iloc[1:, 12:14])

# junta todos os palpites de todos os bolões
palpites_br_marrocos = sheet_br_marrocos + b2_br_marrocos + b3_br_marrocos
palpites_br_haiti = sheet_br_haiti + b2_br_haiti + b3_br_haiti
palpites_br_escocia = sheet_br_escocia + b2_br_escocia + b3_br_escocia
palpites_haiti_marrocos = sheet_marrocos_haiti + b2_marrocos_haiti
palpites_haiti_escocia = sheet_haiti_escocia + b2_haiti_escocia
palpites_marrocos_escocia = sheet_escocia_marrocos + b2_escocia_marrocos

jogos = [ palpites_br_marrocos, palpites_br_haiti, palpites_br_escocia, palpites_haiti_marrocos, palpites_haiti_escocia, 
         palpites_marrocos_escocia]

# placar real de cada jogo, na mesma ordem que os palpites foram listados
real_scores = [(1,1),(3,0),(0,3),(4,2),(0,1),(0,1)]
previsoes = []
for placares in jogos:
  palpites_time1 = [placar[0] for placar in placares]
  palpites_time2 = [placar[1] for placar in placares]
  result = calc_score(palpites_time1, palpites_time2, False)
  previsoes.append(result)

print('------------ MEDIA')
analise(real_scores, [prev['media'] for prev in previsoes])
print('------------ MEDIANA')
analise(real_scores, [prev['mediana'] for prev in previsoes])
print('------------ MODA')
analise(real_scores, [prev['moda'] for prev in previsoes])
