1. Usuário cria objeto ou clica pan/zoom
2. SGIInterface → controller.add_object() / pan() / zoom()
3. Controller atualiza DisplayFile (permanente) ou Window (recorte atual)
4. Controller chama sgi.refresh_canvas() → canvas.update()
5. Qt dispara paintEvent
6. Canvas pede controller.get_drawable_objects()
7. Controller, pra CADA objeto do DisplayFile (mesmo os fora da window):
      viewport.transform_all(obj.coords, window)
8. Canvas manda pro painter — Qt corta visualmente o que sobra da tela