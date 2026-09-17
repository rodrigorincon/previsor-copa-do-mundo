from modelos.model_factory import ModelFactory

features = {
  'peso': [True, False],
  'Elo': [True, False],
  'K': [None, 24, 50, 80]
}

modelos = ModelFactory(features).initialize()
for model in modelos:
  model.build_and_run()