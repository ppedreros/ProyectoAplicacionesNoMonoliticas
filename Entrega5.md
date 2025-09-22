# Entrega 5

## Cambios en el Diagrama de Mapas de Contexto TO-BE

El diagrama de mapas de contexto TO-BE presentado en la primera entrega no tuvo cambios para esta entrega. Se mantiene la misma estructura y relaciones entre los sistemas y actores identificados inicialmente.

![Diagrama de Mapas de Contexto TO-BE](/images/Context_TOBE.jpg)
[Diagrama de Mapas de Contexto TO-BE URL](https://miro.com/app/board/uXjVJEzOfyw=/?share_link_id=299680112257)

## Refinamiento de los Diagramas de Puntos de Vista

### Diagrama Contexto C&C

Sin cambios

![Diagrama Contexto C&C](/images/Contexto_C&C.png)

### Diagrama Funcional de Tipo Módulo

Se realizó un refinamiento en el diagrama funcional de tipo módulo, agregando un nuevo módulo denominado **"Saga"**. Este módulo fue incorporado para soportar la implementación del patrón Saga, facilitando la gestión de transacciones distribuidas y la coordinación entre los diferentes módulos del sistema.

![Diagrama Funcional Tipo Mòdulo](/images/Modulo.png)

### Diagrama Funcional de Tipo C&C (Componentes y Conectores)

El diagrama funcional de tipo C&C fue refinado para mostrar la implementación de un **bus de eventos**. Este bus de eventos permite la comunicación asíncrona entre los componentes del sistema, mejorando la escalabilidad y desacoplamiento de los módulos.

![Diagrama Funcional C&C](/images/C&C.png)

## Resumen de Cambios

- **Mapa de contexto TO-BE:** Sin cambios respecto a la primera entrega.
- **Diagrama Contexto C&C:** No tuvo cambios.
- **Diagrama funcional de tipo módulo:** Se añadió el módulo "Saga".
- **Diagrama funcional de tipo C&C:** Se incorporó la implementación de un bus de eventos.

Estos refinamientos responden a la evolución de la arquitectura y a la necesidad de soportar patrones de diseño que mejoran la robustez y flexibilidad del sistema.
