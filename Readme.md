GUSTAVO AUAD PICCOLI - 00275858 - Turma: A
JÚLIA DEL PINO RITTMANN - 00262512 - Turma: A 
NÍKOLAS PADÃO SCHUSTER - 00323741 - Turma: A

Função de Avaliação:
--------------------

A função de avaliação leva em conta vários aspectos (talvez até mais do que deveria). Os aspectos são: número de peças do agente, número de peças  do agente no centro, número de movimentos legais do oponente, número de movimentos legais do agente, número de corners do agente, número de corners do oponente, riscos do agente entregar um corner, número de peças do agente no "outer square", penalidade de sequência longas de peças do agente na fronteira de risco (explicarei logo mais), número de peças do agente que foram colocadas em X-tiles (explicarei logo mais).

A fronteira de risco é marcada em X a seguir: 
                                     """. . . . . . . .
                                      . X X X X X X .
                                      . X . . . . X .
                                      . X . . . . X .
                                      . X . . . . x .
                                      . X . . . . X .
                                      . X X X X X X .
                                      . . . . . . . ."""
Os X-tiles são marcados pelos X a seguir:
                                      ```. . . . . . . .
                                      . X . . . . X .
                                      . . . . . . . .
                                      . . . . . . . .
                                      . . . . . . . .
                                      . . . . . . . .
                                      . X . . . . X .
                                      . . . . . . . .```
Esses dois aspectos são sobre riscos não imediatos, os X-tiles são tiles altamente vulneráveis para liberar um corner para o oponente, enquanto que a fronteira de risco libera muitas jogadas para o oponente. A fronteira de risco tem risco 0 quando o outer square é pouco esparso/muito povoado.
Sobre os weights colocados em cada váriavel dessa heurística de avaliação, eles foram feitos através de apenas através do conhecimento empírico (alguns testes), então não são os valores ótimos. Para weight de número de peças do agente, utilizei uma função sigmoide modificada, e para peças centrais do agente utilizei uma sigmoide modificada inversa (que vai de y = 1 para y = 0). Essa função sigmoide recebe como input o número total de peças no tabuleiro. Ela é útil pois no ínicio do jogo (quando há poucas peças) o número de peças que o agente tem não é um parâmetro de grande importância. No caso de peças centrais é o inverso, no ínicio do jogo as peças centrais são de grande importância.

Estratégia de Parada e Melhorias:
---------------------------------

A estratégia de parada foi feita com uma profundidade fixa = 4. Após essa parada é feito um Quiescence search com profundidade máxima = 2, que considera como estados voláteis os estados em que o jogador só tem um movimento legal (movimento forçado) e quando tem movimentos na região dos corners.
Região dos corners marcadas por X: 
                                      ```X X . . . . X X
                                      X X . . . . X X
                                      . . . . . . . .
                                      . . . . . . . .
                                      . . . . . . . .
                                      . . . . . . . .
                                      X X . . . . X X
                                      X X . . . . X X```
                                      

Dificuldades:
-------------

Maior dificuldade foi a função de avaliação, sendo escolher quais parâmetros do estado a serem avaliados, tanto como os pesos usados.
Outra dificuldade foi uma pequena bobagem cometida, que só perecebemos mais para o final. Foi um erro cometido no próprio algoritmo MinMax e apesar de mesmo com o erro o agente estar ganhando consistentemente do randomplayer, ele fazia jogadas duvidosas. Com esse erro muitas mudanças de parâmetros e pesos na função de avaliação não tinham o resultado esperado e passamos muito procurando o problema.


Bibliografias:
--------------

https://matthieu-zimmer.net/~matthieu/courses/python/othello.pdf

https://www.ultraboardgames.com/othello/tips.php

http://home.datacomm.ch/t_wolf/tw/misc/reversi/html/index.html

https://barberalec.github.io/pdf/An_Analysis_of_Othello_AI_Strategies.pdf  

https://en.wikipedia.org/wiki/Quiescence_search

https://www.chessprogramming.org/Quiescence_Search
