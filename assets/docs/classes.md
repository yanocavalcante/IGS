┌─────────────────────────────────────────────────────────────────┐
│                          Controller                               │
│  (mediador — único que conhece todo mundo)                        │
│  - display_file: DisplayFile                                      │
│  - window: Window                                                 │
│  - viewport: Viewport                                             │
│  - sgi: SGIInterface                                               │
│  + add_object(obj_dict)                                            │
│  + pan(dx, dy) / zoom(factor)                                      │
│  + get_drawable_objects() -> list[(GraphicObject, list[Coordinate])]│
└───────┬───────────────┬───────────────┬───────────────┬──────────┘
        │ tem            │ tem            │ tem            │ tem
        ▼                ▼                ▼                ▼
┌───────────────┐ ┌─────────────┐ ┌──────────────┐ ┌────────────────┐
│  DisplayFile   │ │   Window    │ │   Viewport   │ │  SGIInterface   │
│ objetos, TODOS │ │ recorte do  │ │ mapeamento   │ │ (View / Qt)     │
│ (visíveis ou   │ │ mundo, pan  │ │ lógico p/    │ │ formulários,    │
│ não)           │ │ e zoom      │ │ tela (EQ 1.1)│ │ botões          │
└───────┬────────┘ └─────────────┘ └──────────────┘ └───────┬─────────┘
        │ contém                                             │ contém
        ▼                                                     ▼
┌───────────────────┐                                 ┌───────────────┐
│  GraphicObject(ABC)│                                 │    Canvas      │
│  name, id, type,   │                                 │  (QWidget —    │
│  coords: list[     │                                 │   dispositivo  │
│  Coordinate]        │                                │   físico)      │
│  + draw(painter,    │                                └───────────────┘
│    vp_coords)       │
└─────────┬───────────┘
    ┌──────┼──────┐
    ▼      ▼      ▼
 Point   Line  Wireframe


- Regra de dependência (para imports)
view/  ──▶  controller/  ──▶  models/  ──▶  core/

core/ (Coordinate, Window, Viewport): não importa nada do projeto.
models/ (GraphicObject e subtipos, DisplayFile): importa só core/ (usa Coordinate).
controller/: importa core/ e models/.
view/: importa controller/ (chama métodos) e models/ (tipagem/draw()), nunca o contrário.