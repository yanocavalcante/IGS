# Fluxo de Criação de Novos Objetos v0.2

1. Usuário clica no botão `Create New Object` da Interface Gráfica → `SGIInterface.create_object()` abre diálogo, monta `obj_dict` com `Coordinates` de mundo.
2. `SGIInterface` chama `controller.add_object(obj_dict)`.
3. `Controller` pede para DisplayFile.add(...) criar o `Line` com `id` novo e guardar na lista.
4. `Controller` chama `self.sgi.refresh_canvas()`.
5. Consequentemente, `Canvas.paintEvent` é engatilhado e o `Canvas`solicita ao `Controller` a lista de objetos de `Display File`.
6. Ao mesmo tempo, a interface reescreve a lista de objetos a serem expostos no menu.
7. Para cada objeto, `Viewport.transform_all(obj.coords, window)` converte mundo → tela usando a transformada de `Viewport`.
8. Os objetos se desenham, `obj.draw(painter, vp_coords)`, a partir de suas respectivas coordenadas e utilizando uma instância de `QPainter` passada pelo `Canvas`.
