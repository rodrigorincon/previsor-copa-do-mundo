from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.metrics import accuracy_score, f1_score, classification_report

def analise(real, predicted):
  exact_scores = count_exact_score(real, predicted)
  mae, rmse = mean_metrics(real, predicted)
  acc, f1, report = classification_metrics(real, predicted)

  print(f'Placares exatos: {exact_scores} ({(100 * exact_scores/len(real)):.2f}%)')
  print(f'MAE = {mae:.4f}. RMSE = {rmse:.4f}')

  print(f'F1-score: {f1:.2f}')
  print(f'Acurácia: {acc:.2f}')
  print(report)


def count_exact_score(real, predicted):
  counter = 0
  for i in range(len(real)):
    real_score = real[i]
    pred_score = predicted[i]
    if(real_score[0] == pred_score[0] and real_score[1] == pred_score[1]):
      counter += 1
  return counter

def mean_metrics(real, predicted):
  real_goals_team1 = [score[0] for score in real]
  real_goals_team2 = [score[1] for score in real]
  pred_goals_team1 = [score[0] for score in predicted]
  pred_goals_team2 = [score[1] for score in predicted]

  real_goals = real_goals_team1 + real_goals_team2
  pred_goals = pred_goals_team1 + pred_goals_team2
  
  mae = mean_absolute_error(real_goals, pred_goals)
  rmse = root_mean_squared_error(real_goals, pred_goals)
  return mae, rmse

def classification_metrics(real_score_list, predicted_score_list):
  real = [convert_to_category(real_score) for real_score in real_score_list]
  pred = [convert_to_category(predicted_score) for predicted_score in predicted_score_list]

  acc = accuracy_score(real, pred)
  f1 = f1_score(real, pred, average='macro', zero_division=0)
  report = classification_report(real, pred, target_names=['Vitória', 'Derrota', 'Empates'])
  return acc, f1, report

# 0 = team1 wins, 1 = team2 wins, 2 = tie
def convert_to_category(score):
  if(score[0] > score[1]):
    return 0
  elif(score[0] < score[1]):
    return 1
  else:
    return 2
