from load_history import carrega_historico
from modelos.model_builder import ModelBuilder
from modelos.train_model import DixonColesPred
from metrics import analise

dados_com_peso = carrega_historico(True)
dados_sem_peso = carrega_historico(False)

modelo_com_peso1 = ModelBuilder('Com peso, Elo e K padrão', dados_com_peso, True, None)
modelo_com_peso2 = ModelBuilder('Com peso, Elo e K=24', dados_com_peso, True, 24)
modelo_com_peso3 = ModelBuilder('Com peso, Elo e K=50', dados_com_peso, True, 50)
modelo_com_peso4 = ModelBuilder('Com peso, Elo e K=80', dados_com_peso, True, 80)
modelo_com_peso5 = ModelBuilder('Com peso e SEM Elo', dados_com_peso, False, None)

modelo_sem_peso1 = ModelBuilder('Sem peso, Elo e K padrão', dados_sem_peso, True, None)
modelo_sem_peso2 = ModelBuilder('Sem peso, Elo e K=24', dados_sem_peso, True, 24)
modelo_sem_peso3 = ModelBuilder('Sem peso, Elo e K=50', dados_sem_peso, True, 50)
modelo_sem_peso4 = ModelBuilder('Sem peso, Elo e K=80', dados_sem_peso, True, 80)
modelo_sem_peso5 = ModelBuilder('Sem peso e SEM Elo', dados_sem_peso, False, None)

modelos = [modelo_com_peso1, modelo_com_peso2, modelo_com_peso3, modelo_com_peso4, modelo_com_peso5, modelo_sem_peso1, modelo_sem_peso2, 
            modelo_sem_peso3, modelo_sem_peso4, modelo_sem_peso5]

for model in modelos:
  model.build_and_run()