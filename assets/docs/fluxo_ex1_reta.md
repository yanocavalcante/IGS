Fluxo de "criar uma reta e ver na tela"
1. Usuário clica Create New Object → SGIInterface.create_object() abre diálogo, monta obj_dict com Coordinates de mundo.
2. SGIInterface chama controller.add_object(obj_dict).
3. Controller pede para DisplayFile.add(...) criar o Line com id novo e guardar na lista.
4. Controller chama self.sgi.refresh_canvas().
5. Canvas.paintEvent roda: pede controller.get_drawable_objects().
6. Para cada objeto, Viewport.transform_all(obj.coords, window) converte mundo→tela usando a EQ. 1.1/1.2.
7. obj.draw(painter, vp_coords) desenha só com QPainter, sem saber nada de mundo/window.

Zoom/Pan: botão → controller.zoom(...)/pan(...) → altera Window → refresh_canvas() → mesmo pipeline do passo 5–7 roda de novo com a window nova, sem tocar no DisplayFile.