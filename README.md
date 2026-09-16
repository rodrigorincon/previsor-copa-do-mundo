# PREVISOR DA COPA DO MUNDO

Este projeto de IA busca criar diversos modelos de machine learning para prever o campeão da copa do mundo. O projeto foi desenvolvido durante a copa do mundo de 2026 porém pode ser aproveitado para outras edições.

## Base do Projeto

O projeto usa a biblioteca `Penaltyblog`, criada especialmente para machine learning para futebol. O modelo escolhido foi o Dixon-Coles, uma variação da distribuição de Poisson que aumenta ainda mais o peso para os valores mais baixos (especificamente os valores 0-0, 0-1, 1-0 e 1-1). O projeto é levemente inspirado no [Hashtag Programação](https://www.hashtagtreinamentos.com/previsao-da-copa-2026-com-python).

Para treinamento dos modelos é usado todos os jogos entre seleções dos últimos 21 anos, parando pouco antes da copa do mundo analisada.

## Os Modelos

Alguns modelos foram criados, todos com base no modelo Dixon-Coles fornecido pela biblioteca. Cada um varia um hiper-parâmetro ou desliga algumas configurações para podermos comparar os modelos e ver quais combinações dão os melhores resultados.

Os pontos que variam entre eles são:

- **Valor K**: hiper-parâmetro usado no cálculo do ranking Elo
- **Ranking Elo**: habilita ou desabilita o uso do eanking Elo no modelo
- **Peso dos jogos**: habilita ou desabilita o uso de pesos nos jogos usados na base de treino
- **Método de seleção do vencedor**: hiper-parâmetro que definir qual método usado para definir o vencedor de cada jogo
  - Placar mais provável
  - Vencedor mais provável
- **Simulação de Monte Carlo**: habilita ou desabilita o uso de simulações de Monte Carlo para definir o vencedor de cada jogo

Os modelos usados podem ser encontrados na pasta `modelos`, todos herdando da interface pai `DixonColesPred` em `train_model`.

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

### Definindo o vencedor

O vencedor pode ser definido das formas abaixo. Cada um deles é uma classe filho do modelo base.

1. **Placar mais provável**

Nesse caso o resultado com maior probabilidade será escolhido como resultado do modelo. Ele permite calcular os pontos, saldo de gols e gols feitos de cada seleção.

2. **Vencedor mais provável**

Nesse caso o time que soma maior probabilidade de vencer será escolhido como resultado do modelo. Ele difere do anterior pois o placar mais provável pode ser para o time A ou empate, mas a soma de todas as probabilidades em que o placar dá vitória para B ser maior que a soma das probabilidades de A. Apesar de improvável, pode acontecer.  Esse método não pode permite calcular os saldo de gols e gols feitos de cada seleção.

3. **Simulações de Monte Carlo**

Nesse caso 50 mil simulações de cada jogo são feitas, usando o mesmo modelo que define as probabilidades dos anteriores. A diferença está em não definir o vencedor apenas por ser o mais provável, mas sim repetindo milhares de vezes os jogos e com isso simular a aleatoriedade natural do esporte. Ao fim o placar mais repetido é escolhido como o que acontecerá.

## Se familiarizando com a biblioteca

Para quem nunca usou a biblioteca ou fez previsões esportivas, a pasta `exemplos-basicos` fornece alguns exemplos mais simples para facilitar o entendimento do que está acontecendo. Eles trazem um cenário infinitamente menor e mais simples, aonde podemos visualizar cada passo e entender o que está acontecendo. Ele também permite conhecer a biblioteca usada e suas funções. `Primeiro-exemplo` mostra a estrutura básica e como usar a biblioteca. `Exemplo-elo` adiciona o ranking Elo e `copa-1-jogo` adiciona os dados reais, porém faz a previsão apenas do primeiro jogo da copa.

## Dados de apostas

Um segundo projeto está presente na pasta `modelo-por-palpite`, aonde ao invés de usar dados históricos de partidas é usado apenas os palpites feitos pelas pessoas nos jogos da própria copa do mundo. Para tanto a base de treino é outra, usando os palpites feitos em uma casa de apostas. Também é usado os palpites feitos em um bolão privado e comparado os resultados com os modelos tradicionais e entre si (com milhares de pessoas palpitando o placar e com poucas dezenas).

Aqui não é mais usado a distribuição Dixon-Cole, mas sim a lei dos grandes números. A média, moda e mediana dos palpites serão usadas como placar escolhido pelo modelo. Portanto para esse tipo de avaliação o que foi discutido antes de peso e Elo não se aplica. O modelo usado é muito mais simples por se basear em um conceito muito mais direto e com poucos detalhes.

### Modelos Usados

- **Média**: retira a média dos gols para cada time independentemente em cada partida. Portanto no jogo AxB os palpites de gols feitos por A não interferem no cálculo da média de gols palpitados para o time B. A média é arredondada para cima a partir de $\ge 0.5$.
- **Mediana**: retira a mediana dos gols de cada time, seguindo a mesma suposição de independência da média.
- **Moda**: usa o palpite mais repetido para dada time.

Esses valores são calculado tanto da lista de palpites da casa de apostas usada de exemplo quanto do bolão com pouco mais de 30 pessoas participando. O que nos permite comparar a precisão de modelos com poucas e muitas pessoas palpitando.

### Métrcas dos modelos de palpite

Para avaliar é medido tanto métricas de regressão (para saber o tamanho do erro do palpite) quanto de classificação (para saber se acertou o vencedor). As métricas são as mesmas dos modelos usando histórico.

# Resultado dos modelos

- **MAE, RMSE e Pontuação de precisão** quase não mudaram entre os modelos treinados com o histórico. Todos erravam quantos gols cada time faria mais ou menos na mesma quantidade.
- **F1-Score e Acurácia** pouco mudaram ao variar K. Porém ao desligar os pesos tivemos uma melhora tímida e ao desligar o Elo as métricas subiram um pouco mais.
  - O pricipal motivo dos valores baixos é a dificuldade do modelo em prever empates, sendo a categoria com menor precisão e por uma larga vantagem. Mais especificamente o campo recall que fica próximo de 0 na maioria dos modelos. Isso ocorre porque o modelo quase nunca define um empate.
- **Placares exatos**: cai conforme aumenta K e alcança seus maiores valores ao desligar o Elo