# Relatório AIGen - IGS

Durante a implementação do presente trabalho, a utilização de *Large Language Models* (LLMs) se limitou ao desenvolvimento de *snippets* de código para funções auxiliares dos algoritmos utilizados pelo Sistema Gráfico Interativo (SGI), aperfeiçoamento da documentação principal do repositório, aprofundamento teórico a respeito do conteúdo estudado e a criação de testes para validação das funcionalidades implementadas. Todos os usos estão listados, a seguir.

## Snippets

Apontamentos para os pedaços de código do SGI que foram sintetizados a partir de IAs.

### ./src/core/clipper.py

Os métodos privados auxiliares da classe `Clipper`, `__find_intersections()`, `__point_inside_polygon()`, `__point_on_segment()` e `__segment_intersection()` foram criados com o auxílio de Inteligência Artificial.

### ./src/models/bspline_curve.py

A classe `BSplineCurve` (modelo de curva B-Spline cúbica uniforme rasterizada por *Forward Differences*), incluindo o método `forward_differences()` e o método privado `__fwd_diff()`, foi implementada com o auxílio de Inteligência Artificial.

### ./src/view/dialogs/bspline_dialog.py

A classe `BSplineDialog`, incluindo o método privado `__parse()`, responsável pela entrada de pontos de controle no padrão `(x1,y1),(x2,y2),...`, foi implementada com o auxílio de Inteligência Artificial.

### ./src/core/projection.py

Os métodos `view_space()` (rotação do mundo para alinhar o VPN ao eixo Z, extraída do antigo `parallel()`) e `perspective_edge()` (projeção em perspectiva de uma aresta, Eq. 6.2 dos slides, com COP virtual atrás do plano de projeção e proteção de *near* para pontos atrás do COP), além do enum `ProjectionType`, foram criados com o auxílio de Inteligência Artificial.

### ./src/core/window.py

As propriedades e métodos `projection`, `cop_distance`, `field_of_view`, `toggle_projection()` e `move_cop()` (estado do COP e do modo de projeção) foram criados com o auxílio de Inteligência Artificial.

### ./src/core/obj_loader.py

A classe `ObjLoader` (leitura de modelos de arame em formato Wavefront `.obj`: `v`, `l` e `f`), incluindo os métodos `load()`, `parse()` e o privado `__resolve()`, foi implementada com o auxílio de Inteligência Artificial.

### ./src/controller/controller.py

Os métodos `toggle_projection()`, `move_cop()`, `load_obj()` e `__project_edges()` (e a adaptação de `get_drawable_objects()` para usá-lo) foram criados com o auxílio de Inteligência Artificial.

### ./src/view/interface.py

Os botões de projeção/COP e de carga de `.obj`, `__toggle_projection()`, `__cop_closer()`, `__cop_farther()`, `refresh_projection_controls()` e `__load_obj()` foram criados com o auxílio de Inteligência Artificial.

## Projeção em Perspectiva (INE5420 - Aula 6)

- **Finalidade do uso:** gerar um conjunto de funções e classes (projeção em perspectiva com Clipping 2D, controle do centro de projeção e carga de modelos `.obj`).
- **Grande Modelo de Linguagem utilizado:** Claude Sonnet 5.5 (Anthropic).
- **URL:** https://claude.ai
- **Prompt:** "Implemente projeção em perspectiva (vista em aula e no material) realizando Clipping 2D. Objetivos: compreender a transformação de perspectiva; compreender o uso de um centro de projeção virtual, atrás do Plano de Projeção. Requisitos: tomar uma cena composta por pelo menos 2 objetos 3D na forma de modelos de arame armazenados no Display File e mostrá-los em perspectiva; variar a posição do centro de projeção, permitindo distorções tipo \"grande angular\" e \"teleobjetiva\"; carregar pelo menos um modelo de arame de paralelepípedo em formato .obj de um arquivo para mostrar em perspectiva."
- **Dicionário de dados (`Projection.perspective_edge(start, end, window)`):** `start` e `end` são as extremidades da aresta no espaço da câmera (saída de `view_space()`, `numpy` com x, y, z); `window` fornece o centro da Window (VRP/CW, no plano de projeção) e `cop_distance` (d, distância do COP ao plano, medida sobre o VPN). Retorna 2 `Coordinate` no plano UV ou `[]` se a aresta estiver inteira atrás do COP.

### Casos de teste

Os modelos ficam em `./assets/models/` e são carregados pelo botão `Load .obj`.

| Arquivo | Conteúdo | Requisitos testados |
| --- | --- | --- |
| `parallelepiped_lines.obj` | Paralelepípedo 120x60x200 com arestas em `l` (polilinhas) | Carga de modelo de arame `.obj`; exibição em perspectiva; efeito de grande angular/teleobjetiva (maior profundidade em Z) |
| `parallelepiped_faces.obj` | Paralelepípedo 80x120x80 com arestas derivadas de `f` (inclui `v/vt/vn` e índices negativos) | Carga de `.obj` com faces; eliminação de arestas duplicadas (12 arestas); exibição em perspectiva |

A cena inicial (`Cube` e `Pyramid`, criados em `Controller.testing()`) cobre o requisito de pelo menos 2 objetos 3D no *Display File*. O botão `Projection` alterna entre perspectiva e paralela, e `COP -` / `COP +` aproximam/afastam o COP (grande angular / teleobjetiva).

### Requisitos não-funcionais

- O Clipping de X e Y é feito em 2D (Cohen-Sutherland) após a projeção; apenas pontos atrás do COP são cortados antes da divisão por profundidade (`Projection.NEAR`), para evitar divisão por zero.

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
