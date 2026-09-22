from modelos.model_factory import ModelFactory

features = {
  'peso': [True, False],
  'monte_carlo': [True, False],
  'Elo': [True, False],
  'K': [25, 50, 80]
}

modelos = ModelFactory(features).initialize()
for model in modelos:
  model.build_and_run()
