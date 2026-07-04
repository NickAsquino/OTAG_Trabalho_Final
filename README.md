# AMAR-É-LINDO — Exergame de Amarelinha

## Descrição
MVP (Minimum Viable Product) de um exergame baseado na brincadeira tradicional de amarelinha.
O jogador deve memorizar uma sequência de casas iluminadas e reproduzi-la na ordem correta. O jogo agora conta com diferentes dificuldades e suporte para dois jogadores em modo competitivo.

## Estrutura do Projeto
O projeto foi modularizado para melhor organização e manutenção do código:
```
AmarELindo/
├── main.py                ← Ponto de entrada (inicializa o jogo)
├── game.py                ← Lógica central, máquina de estados e renderização
├── constants.py           ← Configurações, cores e definições de categorias
├── board.py               ← Lógica de construção do grid da amarelinha
├── README.md              ← Este arquivo
└── assets/
    ├── images/            ← Imagens (logo, backgrounds, sprites)
    ├── sounds/            ← Efeitos sonoros (.wav)
    └── fonts/             ← Fontes personalizadas (.ttf)
```

## Como Executar
```bash
pip install pygame
python main.py
```

## Detalhes
- **Modo Competitivo Intergeracional:**
  - Dois jogadores participam no mesmo equipamento em sessões independentes.
  - O vencedor é decidido pela pontuação acumulada.
  - Critérios de desempate automáticos: Maior sequência correta > Menor tempo total > Menor número de dicas utilizadas.
  - Tela de classificação final comparando os status de ambos os jogadores.
- **Categorias de Dificuldade com Limite de Rodadas:**
  - **Iniciante:** Fases mais lentas, máximo de 5 rodadas.
  - **Intermediário:** Fases moderadas, máximo de 7 rodadas.
  - **Avançado:** Fases rápidas e longas, máximo de 10 rodadas.

## Controles
| Ação               | Controle                                     |
|--------------------|----------------------------------------------|
| Iniciar jogo / Navegar | Clique do mouse                            |
| Validar casas      | Clique do mouse **OU** Teclas `1` a `9` (NumPad/Teclado) |
| Reiniciar          | Tecla `R`                                    |
| Voltar / Sair      | Tecla `ESC`                                  |

## Sons (opcionais)
Coloque arquivos `.wav` na pasta `assets/sounds/`:
- `acerto.wav` — Toca ao acertar uma casa
- `erro.wav` — Toca ao errar
- `dica.wav` — Toca quando a dica é ativada
- `bonus.wav` — Toca ao completar a sequência
- `inicio.wav` — Toca ao iniciar uma rodada

## Regras
- **Acerto:** +10 pontos por casa correta.
- **Sequência completa:** +20 pontos de bônus.
- **Dica:** Ativada ao ficar alguns segundos sem clicar, mostra o próximo passo. Custa pontos (desconto na rodada).
- **Erro:** Pontuação da rodada zerada, perde 1 vida. O jogador possui 3 vidas por partida.
- **Condição de Vitória:** Completar o número máximo de rodadas da categoria.
- **Game Over:** Perder as 3 vidas.

## Integração Futura com Câmera
Os pontos de integração para visão computacional continuam demarcados. O método principal é `processar_entrada_jogador(pos)` e, agora, também existe o método direto `_processar_jogada_casa(casa)`, o qual pode receber diretamente o número da casa (1 a 9) processado pela câmera.
