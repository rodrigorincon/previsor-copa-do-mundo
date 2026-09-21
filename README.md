# PREVISOR DA COPA DO MUNDO

Este projeto de IA busca criar diversos modelos de machine learning para prever o campeão da copa do mundo. O projeto foi desenvolvido durante a copa do mundo de 2026 porém pode ser aproveitado para outras edições.

## Base do Projeto

O projeto usa a biblioteca `Penaltyblog`, criada especialmente para machine learning para futebol. O modelo escolhido foi o Dixon-Coles, uma variação da distribuição de Poisson que aumenta ainda mais o peso para os valores mais baixos (especificamente os valores 0-0, 0-1, 1-0 e 1-1). O projeto é levemente inspirado no [Hashtag Programação](https://www.hashtagtreinamentos.com/previsao-da-copa-2026-com-python).

Para treinamento dos modelos é usado todos os jogos entre seleções dos últimos 24 anos, parando pouco antes da copa do mundo analisada.

## O Modelo

O modelo criado usa como base o modelo Dixon-Coles fornecido pela biblioteca. Nosso modelo pode ser encontrado na pasta `modelos` no arquivo `train_model`. Ele possui os seguintes hiper-parâmetros que permitem customizar e comparar os modelos e ver quais combinações dão os melhores resultados.

Os hiper-parâmetros são:

- **Valor K**: hiper-parâmetro usado no cálculo do ranking Elo
- **Ranking Elo**: habilita ou desabilita o uso do eanking Elo no modelo
- **Peso dos jogos**: habilita ou desabilita o uso de pesos nos jogos usados na base de treino
- **Monte Carlo**: habilita ou desabilita a Simulação de Monte Carlo como método de calcular o placar da partida
  - Se for `True` é executado a Simulação de Monte Carlo em todos os jogos, rodando 50 mil vezes e escolhido o placar mais repetido.
  - Se for `False` é escolhido o placar com maior probabilidade segundo a distribuição de Dixon-Coles.

Para inicializar diversos modelos com ligeiras diferenças temos a classe `ModelController` que cria um modelo com as configurações desejadas, o nomeia para o identificar, o executa e faz sua análise. O controlador encapsula o modelo ao criá-lo e dar uma função única para executá-los e analisar seu desempenho. A classe `ModelFactory` é uma fábrita de controladores, permitindo criar dezenas de modelos ao mesmo tempo, fazendo todas as combinações dos hiper-parâmetros desejados.

## Estrutura

### Dados de treino e teste

Os dados de treino são todo o histórico de jogos até antes da copa do mundo de 2026 e os dados de teste são os jogos dessa copa.

### Módulos de apoio

Para facilitar a legibilidade do código e permitir o reuso dentre os diferentes modelos, sua lógica foi dividida em alguns arquivos. Cada arquivo na pasta raiz é responsável por uma parte específica do projeto. `Load_history` carrega os dados de teste e faz o processamento inicial dos mesmos, `world_cup_groups` define os times e grupos, `metrics` calcula as métricas para cada modelo, etc.

> Comece pelo arquivo `run.py` que é onde o sistema começa.

### Métricas

Para comparar os modelos é usado tanto métricas de regressão (para comparar o tamanho do erro nos placares) quanto de classificação (se acertou o vencedor). As métricas usadas para comparar estão no arquivo `metrics`.

1. Métricas de regressão

Foca em dizer o quanto erramos o placar e medir o tamanho desses erros.

- **MAE e RMSE**: medem o quanto nossas previsões de gol erraram. Nos dão a noção se erramos o placar por poucos gol ou não. Foram escolhidas por funcionarem bem no contexto de muitos placares com 0 gols (MAPE por exeplo quebra com resultados zero).
- **Pontuação de precisão**: calcula o total de gols errados de nossa previção. Subtrai os gols previstos por cada time em cada partida pelo que realmente fizeram.
- **Placares exatos**: calcula quantos jogos acertamos o placar exato.

2. Métricas de classificação

Foca em dizer se acertamos o vencedor (ou empate) sem se importar com o placar. Temos 3 categorias (vitória, empate e derrota) e como a proporção entre esses grupos é diferente, usamos a **média macro** para medir essas métricas. A título de informação, na fase de grupos quase metade dos jogos foi vitória do time 1 e aproximadamente 25% de vitória do time 2 e 25% de empate.

Essa discrepância nas proporções das categorias levou ao uso da média macro como forma de comparar o acerto da categoria. Isso evita que acertar muito a categoria mais comum (vitória do time 1) ofuscasse o erro nas duas outras categorias.

- **F1-Score**: é a principal métrica por ser ideal quando as categorias são desproporcionais. Mede o grau de acerto em cada categoria sem deixar a categoria principal eclipsar as demais.
- **Acurácia**: métrica de apoio para nos dar quantos porcento dos jogos acertamos o vencedor. Ela só faz sentido se o F1-Score for alto.

### Peso dos jogos

Cada partida presente nos dados de teste pode ou não ter um peso assocido (a depender dos hiper-parâmetros). Esse peso é definido por duas características: a antiguidade e o campeonato.

A antiguidade é quão antigo o jogo é. Quanto mais recente for o jogo mais relevante ele é e jogos antigos tem pouco peso no aprendizado. A cada 3 anos o peso cai pela metade. Outro fator é em qual campeonato o jogo aconteceu. Campeonatos mais importantes, aonde os jogadores entram com mais ímpeto no campo, tem maior peso. Copa do mundo tem o maior peso de todos, campeonatos continentais tem um peso um pouco menor e amistosos terão o menor de todos.

### Ranking Elo

Nos modelos em que essa função está ligada, o ranking Elo age como mais um peso nas decisões, porém agora apenas na previsão. Todas as seleções começam com ranking 1500 e é atualizada com base nos dados de treino. Assim, após terminar de atualizar o ranking com os dados de treino, cada país chega com um ranking diferente na copa.

> Disclaimer: o ranking Elo usado no projeto NÃO É o mesmo presente no ranking da FIFA.

Importante ressaltar que o ranking Elo é atualizado usando dados de treino, porém ele não afeta o treinamento do modelo. Habilitá-lo não afeta os resultados do treino e só impactará na previsão dos novos resultados.

### Fase de grupos e eliminatória

Testamos as métricas dos modelos e suas precisões unicamente com base na fase de grupos, pois como os times classificados pelo modelo podem (e de fato acontecia em agluns) diferir dos reais, a comparação da fase eliminatória perdia o sentido. A fase eliminatória foi rodada apenas com o melhor modelo encontrado para testar sua precisão de dar o campeão do torneio, vice e semi-finalistas, sem intuito de testar as métricas anteriores.

Para testar a fase eliminatória rodo a Simulação de Monte Carlo 10 mil vezes, verificando em quantas delas acertamos o campeão. Fazemos o mesmo para o segundo lugar e para os semi-finalistas. Essas simulações são divididas em diversos processos que rodam cada um diversas threads com memória compartilhada para agilizar o processamento.

Na fase de grupos é rodada a versão com Monte-Carlo para que não fique 100% iguais em todas as 10 mil versões. A fase eliminatória sempre executa a simulação de Monte-Carlo em cada jogo pelo mesmo motivo. Essas simulações testam cada jogo 100 vezes, dando chance para a aleatoriedade que marca competições do tipo agirem mas com as probabilidades agindo a favor dos times com mais chances.

## Se familiarizando com a biblioteca

Para quem nunca usou a biblioteca ou fez previsões esportivas, a pasta `exemplos-basicos` fornece alguns exemplos mais simples para facilitar o entendimento do que está acontecendo. Eles trazem um cenário infinitamente menor e mais simples, aonde podemos visualizar cada passo e entender o que está acontecendo. Ele também permite conhecer a biblioteca usada e suas funções. `Primeiro-exemplo` mostra a estrutura básica e como usar a biblioteca. `Exemplo-elo` adiciona o ranking Elo e `copa-1-jogo` adiciona os dados reais, porém faz a previsão apenas do primeiro jogo da copa.

# Resultado dos modelos

## Fase de grupos

- **MAE, RMSE e Pontuação de precisão** quase não mudaram entre os modelos treinados com o histórico. Todos erravam quantos gols cada time faria mais ou menos na mesma quantidade.
- **F1-Score e Acurácia** pouco mudaram ao variar K. Porém ao desligar os pesos tivemos uma melhora tímida e ao desligar o Elo as métricas subiram um pouco mais.
  - O pricipal motivo dos valores baixos é a dificuldade do modelo em prever empates, sendo a categoria com menor precisão e por uma larga vantagem. Mais especificamente o campo recall que fica próximo de 0 na maioria dos modelos. Isso ocorre porque o modelo quase nunca define um empate.
- **Placares exatos**: cai conforme aumenta K e alcança seus maiores valores ao desligar o Elo

Com isso foi visto que dentre os modelos de DixonColes **o melhor modelo encontrado foi o com pesos nos dados históricos e sem ranking Elo**. Usar o método de **Monte Carlo não alterou significativamente as métricas**. O MAE, RMSE e pontuação de precisão tiveram mudanças mínimas enquanto os demais em nada mudaram. Também foi visto que Monte Carlo escolhia o resultado mais provável em certa de 99% das partidas. No modelo com melhor resultado (com peso e sem ranking Elo) a simulação de Monte Carlo deu exatamente 100% de mesmos resultados que o método tradicional. Portanto seguimos com a opção sem ela por ser mais rápida e ter mesmo poder preditivo.

## Fase eliminatória

**A previsão do campeão da copa do mundo 2026 foi a Espanha**. A Espanha foi campeã em 43,3% das simulações, seguido de perto pelo Brasil, com 41,8%. A Argentina, vice campeã, foi o terceiro país a mais ganhar simulações, em 9,1%. França e Inglaterra, os 3º e 4º lugares, foram os próximos, com 2,8% e 2,6%.

A lista completa dos países que ganharam alguma simulação está abaixo, juntamente com as estatísticas para segundo lugar e para quem ficou em 3º ou 4º lugar. 

Seguindo as maiores probabilidades de cada grupo e eliminando os já selecionados, o podium da simulação ficou

- 1º lugar: Espanha (43,3%)
- 2º lugar: Brasil (10,7%)
- 3º lugar: Argentina (57,6%)
- 4º lugar: França (52%)

|País      | Campeão     | Vice | Terceiro ou Quarto|
|:--       | :--         | :--  | :--               |
|Espanha   | 4229 (42,3%)|3763  | 1230 |
|Brasil    | 4124 (41,2%)|2263  | 1917 |
|Argentina | 1016 (10,1%)|1606  | 5643 |
|Inglaterra| 315 (3,1%)  |725   | 963 |
|França    | 296 (3%)    |1199  | 5264 |
|Portugal  | 11 (0,11%)  |114   | 983 |
|Holanda   | 5 (<0,1%)   |145   | 1929 |
|Alemanha  | 2 (<0,1%)   |72    |953  |
|Belgica   | 1 (<0,1%)   |46    |324  |
|Colômbia  | 1 (<0,1%)   |59    |603  |
|Uruguai   | 0           |5     |105  |
|Marrocos  | 0           | 5    |64 |
|Suíça | 0 | 0 | 10 |
|Equador | 0 | 0 | 5 |
|Croácia | 0 | 0 | 4  |
|Senegal | 0 | 0 | 2 |
|Noruega | 0 | 0 | 1 |

## Correções feitas

A partir dessa análise a fórmula do peso dos jogos foi alterado para decair de forma mais gradual, tornando jogos antigos mais valiosos. Foram testados vários valores de queda do peso e de quantos anos avaliar até chegar nos valores atuais. Isso melhorou todas as métricas, superando os modelos com peso desabilitado.

O número de simulações feitas em cada partida também foi alterada. Foi testado diversos valores até encontrar o número que equilibre aleatoriedade com poda de possibilidades muito pequenas. Quando se executava só 1 vez times com baixíssimas chances (como Austia ou Paraguai) chegavam até a final e conforme aumenta mais os times com maior chance predominam.

# Dados de apostas

Um segundo projeto está presente na pasta `modelo-por-palpite`, aonde ao invés de usar dados históricos de partidas é usado apenas os palpites feitos pelas pessoas nos jogos da própria copa do mundo. Para tanto a base de treino é outra, usando os palpites feitos em um bolão privado e comparado os resultados com os modelos tradicionais.

Aqui não é mais usado a distribuição Dixon-Cole, mas sim a lei dos grandes números. A média, moda e mediana dos palpites serão usadas como placar escolhido pelo modelo. Portanto para esse tipo de avaliação o que foi discutido antes de peso e Elo não se aplica. O modelo usado é muito mais simples por se basear em um conceito muito mais direto e com poucos detalhes.

## Modelos Usados

- **Média**: retira a média dos gols para cada time independentemente em cada partida. Portanto no jogo AxB os palpites de gols feitos por A não interferem no cálculo da média de gols palpitados para o time B. A média é arredondada para cima a partir de $\ge 0.5$.
- **Mediana**: retira a mediana dos gols de cada time, seguindo a mesma suposição de independência da média.
- **Moda**: usa o palpite mais repetido para dada time.

Esses valores são calculado tanto da lista de palpites do bolão com pouco mais de 30 pessoas participando. Para ter um comparativo do efeito do número de pessoas um segundo modelo será treinado usando uma amostra desse bolão, sorteando 5 palpites do bolão para cada jogo. Assim poderemos comparar a precisão de modelos com poucas e muitas pessoas palpitando.

## Métrcas dos modelos de palpite

Para avaliar é medido tanto métricas de regressão (para saber o tamanho do erro do palpite) quanto de classificação (para saber se acertou o vencedor). As métricas são as mesmas dos modelos usando histórico.

## Resultados dos modelos de palpite