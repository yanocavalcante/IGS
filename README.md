# Interactive Graphic System

Sistema Gráfico Interativo para Computação Gráfica baseado em `Python` e `PyQt`.

## Componentes

Os principais componentes do sistema são: `Viewport`, `Window` e `Display File`. Os objetos gráficos são representados sobre o `Canvas`.

`Window`: Retângulo que representa o recorte do mundo 2D representado no `Display File` que será mostrado na tela.

`Viewport`: Área do vídeo onde será, de fato, desenhado o que se deseja mostrar, através de um sistema de coordenadas parcialmente invertido, onde o eixo Y aponta para baixo.

`Display File`: Estrutura responsável por armazenar os objetos gráficos que compõem a cena.

## Objetos

O sistema permite a criação de uma grande variedade de objetos gráficos, incluindo: Pontos, Linhas e Polígonos.

## Execução

*Obs: os passos a seguir consideram a utilização de um sistema operacional baseado em `Linux`.*

Para executar o programa é recomendado o uso de um ambiente virtual para isolar as dependências necessárias para sua execução do resto do sistema do usuário. Para isso, execute o seguinte comando:

```bash
python3 -m venv {venv_name}
```

Sendo `venv_name` o nome do ambiente virtual de sua escolha. Para ativá-lo e desativá-lo, respectivamente:

```bash
source {venv_name}/bin/activate

deactivate
```

Com o ambiente virtual criado e ativado, agora é preciso instalar os pacotes e bibliotecas que o programa utiliza para funcionar normalmente. Para isso, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

Por fim, com os pacotes instalados, basta executar o arquivo principal presente na pasta `src/`:

```bash
cd src/
python3 main.py
```

## Fluxos

### Criação de Novos Objetos

![Diagrama de Fluxo da Criação de Novos Objetos](assets/sgi_obj_creation_flux_v1.png)

## Autores

Rita Louro Barbosa e Yano H. de Melo R. Cavalcante.

INE5420 - Computação Gráfica, Prof. Dr. rer.nat. Aldo von Wangenheim.
