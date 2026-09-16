from load_history import carrega_historico
from modelos.train_model import DixonColesPred

df = carrega_historico(True)
modelo = DixonColesPred(df)
modelo.create_model()
modelo.configure_elo()
modelo.predict()