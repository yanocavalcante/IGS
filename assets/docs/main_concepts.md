Mundo (coordenadas do modelo)
      │  recorte (o que é visível)
      ▼
   Window   →  retângulo em coordenadas de MUNDO
      │  transformada de viewport (EQ. 1.1)
      ▼
   Viewport →  retângulo em coordenadas de TELA (onde a Window é mapeada)
      │  esses pixels precisam existir em algum lugar físico
      ▼
   Canvas   →  a SUPERFÍCIE FÍSICA de desenho — o "Display Rectangle"/
               "Graphics I/O Rectangle" da seção 1.4


Mais específico:

DisplayFile   →  guarda TODOS os objetos, sempre, em coords de MUNDO (não muda com pan/zoom)
     │
     │  Window recorta: "quero ver só esse pedaço do mundo agora"
     ▼
Window        →  retângulo em coords de mundo (muda quando você dá pan/zoom)
     │
     │  Viewport mapeia esse recorte pra coords de tela
     ▼
Viewport      →  fórmula EQ 1.1 (não guarda pixel nenhum, só calcula)
     │
     ▼
Canvas        →  só pinta o que caiu dentro da Window atual, no lugar que a Viewport calculou