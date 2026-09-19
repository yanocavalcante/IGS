# Relatório AIGen - IGS

Durante a implementação do presente trabalho, a utilização de *Large Language Models* (LLMs) se limitou ao desenvolvimento de *snippets* de código para funções auxiliares dos algoritmos utilizados pelo Sistema Gráfico Interativo (SGI), aperfeiçoamento da documentação principal do repositório, aprofundamento teórico a respeito do conteúdo estudado e a criação de testes para validação das funcionalidades implementadas. Todos os usos estão listados, a seguir.

## Snippets

Apontamentos para os pedaços de código do SGI que foram sintetizados a partir de IAs.

### ./src/core/clipper.py

Os métodos privados auxiliares da classe `Clipper`, `__find_intersections()`, `__point_inside_polygon()`, `__point_on_segment()` e `__segment_intersection()` foram criados com o auxílio de Inteligência Artificial.

## Diretrizes INE5420 - Computação Gráfica

Diretrizes redigidas pelo Prof. Dr. rer.nat. Aldo von Wangenheim para a documentação do uso de Inteligência Artificial Generativa (IAGen) na confecção do primeiro trabalho da disciplina INE5420 - Computação Gráfica.

1. Se foi usada para gerar uma função ou um snippet de código, a documentação deve estar no cabeçalho da função;
2. Se foi usada para desenvolver uma categoria ou conjunto de funções em uma classe, a documentação deve estar no cabeçalho da classe;
3. Se a interface de uma função foi gerada com **IAGen** e não é óbvia (porque a **IAGen** gerou um conjunto de funções e também a lógica de comunicação entre estas), a documentação deve conter um dicionário de dados explicitando a semântica de cada parâmetro;

A documentação da **IAGen**, deve incluir as seguintes informações:

- Finalidade do uso (gerar uma função, um trecho de função, um conjunto de funções)
- Grand Modelo de Linguagem utilizado.
- **URL** da implementação do modelo de linguagem.
- *Prompt(s)* empregado(s).
- Casos de teste: junto com o código deve ser entregue um conjunto de arquivos de dados em formato **.obj** contendo casos de teste suficientes para o teste dos requisitos explicitados no enunciado pelo professor. Na documentação deve constar o conjunto de requisitos que cada arquivo o conjunto de arquivos testes, de forma que a comprovação de funcionamento do código seja facilitada.
- Requisitos não-funcionais gerais.
