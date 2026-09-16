# PREVISOR DA COPA DO MUNDO

Este projeto de IA busca criar diversos modelos de machine learning para prever o campeão da copa do mundo. O projeto foi desenvolvido durante a copa do mundo de 2026 porém pode ser aproveitado para outras edições.

## Base do Projeto

O projeto usa a biblioteca `Penaltyblog`, criada especialmente para machine learning para futebol. O modelo escolhido foi o Dixon-Coles, uma variação da distribuição de Poisson que aumenta ainda mais o peso para os valores mais baixos (0-0, 0-1, 1-0 e 1-1). O projeto é levemente inspirado no [Hashtag Programação](https://www.hashtagtreinamentos.com/previsao-da-copa-2026-com-python).

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

Os modelos usados podem ser encontrados na pasta `modelos`, todos herdando da interface pai `Predictor`.

## Estrutura

### Dados de treino e teste

Os dados de treino são todo o histórico de jogos até antes da copa do mundo de 2026 e os dados de teste são os jogos dessa copa.

### Módulos de apoio

Para facilitar a legibilidade do código e permitir o reuso dentre os diferentes modelos, sua lógica foi dividida em alguns arquivos. Cada arquivo na pasta raiz é responsável por uma parte específica do projeto. `Load_history` carrega os dados de teste e faz o processamento inicial dos mesmos, `world_cup_groups` define os times e grupos, etc.

> Comece pelo arquivo `run.py` que é onde o sistema começa.

### Comparação dos modelos

### Peso dos jogos

Cada partida presente nos dados de teste pode ou não ter um peso assocido (a depender dos hiper-parâmetros). Esse peso é definido por duas características: a antiguidade e o campeonato.

A antiguidade é quão antigo o jogo é. Quanto mais recente for o jogo mais relevante ele é e jogos antigos tem pouco peso no aprendizado. A cada 3 anos o peso cai pela metade. Outro fator é em qual campeonato o jogo aconteceu. Campeonatos mais importantes, aonde os jogadores entram com mais ímpeto no campo, tem maior peso. Copa do mundo tem o maior peso de todos, campeonatos continentais tem um peso um pouco menor e amistosos terão o menor de todos.

### Ranking Elo

Nos modelos em que essa função está ligada, o ranking Elo age como mais um peso nas decisões, porém agora apenas na previsão. Todas as seleções começam com ranking 1500 e é atualizada com base nos dados de treino. Assim, após terminar de atualizar o ranking com os dados de treino, cada país chega com um ranking diferente na copa.

> Disclaimer: o ranking Elo usado no projeto NÃO É o mesmo presente no ranking da FIFA.

Importante ressaltar que o ranking Elo é atualizado usando dados de treino, porém ele não afeta o treinamento do modelo. Habilitá-lo não afeta os resultados do treino e só impactará na previsão dos novos resultados.

### Definindo o vencedor

O vencedor pode ser definido das seguintes formas:

1. **Placar mais provável**

Nesse caso o resultado com maior probabilidade será escolhido como resultado do modelo. Ele permite calcular os pontos, saldo de gols e gols feitos de cada seleção.

2. **Vencedor mais provável**

Nesse caso o time que soma maior probabilidade de vencer será escolhido como resultado do modelo. Ele difere do anterior pois o placar mais provável pode ser para o time A ou empate, mas a soma de todas as probabilidades em que o placar dá vitória para B ser maior que a soma das probabilidades de A. Apesar de improvável, pode acontecer.  Esse método não pode permite calcular os saldo de gols e gols feitos de cada seleção.

3. **Simulações de Monte Carlo**

Nesse caso 50 mil simulações de cada jogo são feitas, usando o mesmo modelo que define as probabilidades dos anteriores. A diferença está em não definir o vencedor apenas por ser o mais provável, mas sim repetindo milhares de vezes os jogos e com isso simular a aleatoriedade natural do esporte. Ao fim o placar mais repetido é escolhido como o que acontecerá.

## Área de testes

Para quem nunca usou a biblioteca ou fez previsões esportivas, a pasta `exemplos-basicos` fornece alguns exemplos mais simples para facilitar o entendimento do que está acontecendo. Eles trazem um cenário infinitamente menor e mais simples, aonde podemos visualizar cada passo e entender o que está acontecendo. Ele também permite conhecer a biblioteca usada e suas funções. `Primeiro-exemplo` mostra a estrutura básica e como usar a biblioteca. `Exemplo-elo` adiciona o ranking Elo e `copa-1-jogo` adiciona os dados reais, porém faz a previsão apenas do primeiro jogo da copa.

## Dados de apostas

Um segundo projeto está presente na pasta `modelo-por-palpite`, aonde ao invés de usar dados históricos de partidas é usado apenas os palpites feitos pelas pessoas nos jogos da própria copa do mundo. Para tanto a base de treino é outra, usando os palpites feitos em uma casa de apostas. Também é usado os palpites feitos em um bolão privado e comparado os resultados com os modelos tradicionais e entre si (com milhares de pessoas palpitando o placar e com poucas dezenas).

Aqui não é mais usado a distribuição Dixon-Cole, mas sim a lei dos grandes números. A média dos palpites será usada como placar escolhido pelo modelo.

# Resultado dos modelos