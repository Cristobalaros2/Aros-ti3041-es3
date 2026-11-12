# Documento de uso de IA — ES3 Ferretería El Martillo

## Parte 1: Registro de consultas

### Consulta 1 — Entorno del proyecto (Etapa 0)
**Prompt:** "Prepara la Evaluación Sumativa 3: crea el proyecto Django con la app catalogo usando pipenv y dejando también requirements.txt, un .gitignore que excluya db.sqlite3 y __pycache__, y el README con la tabla de las 5 etapas y sus entregables. Todo en el repo nuevo, con el primer commit etapa-0-entorno."

**Resumen de respuesta:** Proyecto Django con settings en `config`, app `catalogo`, Pipfile y requirements.txt actualizados, .gitignore con la basura de Python y SQLite, y README con la tabla de etapas.

**Qué usó o modificó antes de integrarla:** Instalé con pipenv y verifiqué que `runserver` arrancara sin errores. Como db.sqlite3 no se versiona, dejé la fixture `catalogo/fixtures/productos.json` para poder regenerar los 40 productos con `loaddata` en cualquier clon. Revisé con `git status` que no se colara nada (venv, .pyc, la BD) antes de cerrar el commit.

### Consulta 2 — CRUD web con confirmación (Etapa 1)
**Prompt:** "Etapa 1: CRUD de productos desde el sitio. Crea un ModelForm para Producto y las vistas de crear, editar y eliminar con plantilla, protegidas con un decorador staff_required que si el usuario no es staff lo redirija con un mensaje de error; antes de eliminar muestra una página de confirmación. Usa django.contrib.messages para los avisos de éxito y error, y enlaza todo desde el listado del catálogo. Commit etapa-1-crud."

**Resumen de respuesta:** Las tres vistas (`crear_producto`, `editar_producto`, `eliminar_producto`) con el decorador `staff_required`, el formulario compartido `producto_form.html`, la página `confirmar_eliminar.html` que solo borra en POST, y los mensajes success/error en cada acción.

**Qué usó o modificó antes de integrarla:** Probé tres escenarios: sin sesión me devuelve el mensaje "Inicia sesión con una cuenta de administrador…", con usuario normal "No tienes permisos…", y como admin puedo crear, editar y eliminar (siempre pasando por la confirmación). Verifiqué el token CSRF en los formularios y que los mensajes se mostraran en base.html.

### Consulta 3 — Reportes con ORM (Etapa 2)
**Prompt:** "Etapa 2: dos reportes que usen el ORM y no cálculos a mano: resumen general con values y annotate por categoría (cantidad de productos, precio promedio, stock total) más aggregate con los totales generales, y stock crítico con filter de los productos con stock menor o igual a 5 ordenados de menor a mayor. Cada reporte en su página: /reportes/resumen/ y /reportes/stock/. Commit etapa-2-reportes."

**Resumen de respuesta:** Las vistas `reporte_resumen` y `reporte_stock` con `Count`, `Avg`, `Sum`, `values().annotate()` y `filter(stock__lte=UMBRAL_STOCK_CRITICO)`, más las dos tablas en sus templates.

**Qué usó o modificó antes de integrarla:** Contrasté cada número contra la base: 40 productos, 6 categorías, 1.718 unidades en stock y 11 productos bajo el umbral de los cuales 7 están agotados. Revisé que los cálculos salieran todos del ORM y no de listas en Python.

### Consulta 4 — Formulario de consulta con validaciones (Etapa 3)
**Prompts:**
- "Crea el modelo ConsultaCliente con nombre, correo, mensaje, producto de interés (ForeignKey opcional a Producto) y fecha automática, más el ModelForm con estas validaciones: nombre obligatorio de mínimo 3 caracteres, solo letras, espacios y puntos (sin números); correo obligatorio que termine en @gmail.com; mensaje entre 10 y 500 caracteres. Con labels y help_texts en español, y el template con {% csrf_token %}."
- "Agrega la vista /consulta/ que al enviar por POST guarde la consulta en la BD y muestre una página de éxito; y que cada vez que alguien abre un producto lo registre en la sesión (clave 'visitados', máximo 3 y sin repetir) para mostrarle el historial en la página de detalle."

**Resumen de respuesta:** El modelo `ConsultaCliente`, el `ConsultaClienteForm` con `clean_nombre`, `clean_correo` y `clean_mensaje`, la vista `formulario_consulta` con `consulta.html` y `consulta_exitosa.html`, y la sesión con `ULTIMOS_VISITADOS = 3` que se actualiza en `detalle_producto` y entrega el `historial`.

**Qué usó o modificó antes de integrarla:** Le armé un script de pruebas con 19 casos hasta que pasaran todos: nombre con números rechazado, nombre de menos de 3 caracteres, nombre solo con puntos, correo sin @gmail.com, correo con espacios al medio, mensaje de 9 y de 501 caracteres, y los casos válidos con tildes y ñ. Ajusté los mensajes de error para que explicaran cada regla, verifiqué que el token CSRF estuviera en el template y que el historial mostrara exactamente 3 productos sin importar cuántas veces repitiera uno. Commit etapa-3-clientes.

### Consulta 5 — Primer landing animado (OpenCode)
**Prompts:**
- "Hazme el landing page de la ferretería con animaciones: preloader al entrar, hero con título animado, secciones de categorías y productos destacados, contadores que muestren datos reales del ORM y barra de progreso al hacer scroll."
- "podrias dejar ese sello de calidad mas cerca del boton de crear cuenta, para que asi no este por encima de la imagen, como tambien la etiqueta pequeña del precios bajos"
- "haz que cada uno este un poco mas abajo y mas separado el uno del otro, que no queden tan juntos que si no el sello no se ve completo"

**Resumen de respuesta:** Un landing con preloader, hero a dos columnas con collage 3D que sigue el cursor, contadores armados con los `aggregate` de la vista (40 productos, 6 categorías, 1.718 unidades), carrusel infinito de productos, banda con marquee, categorías en cuadrícula bento y un sello circular giratorio con texto en SVG.

**Qué usó o modificó antes de integrarla:** Moví el sello y el chip "Precios bajos" a un contenedor junto al botón "Crear cuenta" y luego los bajé y separé en una segunda ronda hasta que el sello se viera completo sin tapar las imágenes. Verifiqué que los contadores usaran los datos del ORM y no números fijos, que todo respondiera en móvil y que hubiera respaldo para `prefers-reduced-motion`. Lo integré en el commit entrega-final; más adelante lo reemplacé por completo con el diseño de la consulta 6.

### Consulta 6 — Rediseño del landing (OpenCode)
**Prompt:** "quiero que en base a este diseño https://godly.design/website/lightspark/ cambies el landing page al diseño que te mande, con las imagenes que ya tienes acerca de herramientas, materiales de construccion y todo eso"

**Resumen de respuesta:** La IA descargó las capturas del sitio de referencia para analizar el diseño (fondo claro, grilla de imágenes redondeadas alrededor del título, líneas finas con marcas "+", botones tipo píldora, CTA y footer oscuros). Agregó bloques nuevos en `base.html` (`body_class`, `main_class`, `footer_content`) para poder cambiar solo el landing, actualizó la vista `landing_page` para enviar las categorías y la cantidad de productos con stock crítico, y reescribió `landing.html` con las secciones nuevas usando las imágenes de `static/images` y los datos del ORM.

**Qué usó o modificó antes de integrarla:** La sesión quedó incompleta: nunca se creó el archivo de estilos `landing.css` y la grilla del hero tenía un error de posiciones que hacía que una imagen quedara encima del título. Por eso no la integré tal cual y la continué en la consulta 7.

### Consulta 7 — Terminar el landing (Claude Code)
**Prompt:** "hola, te voy a pasar las cosas que me habia cambiado una ia de opencode en cuanto al landing page de mi pagina, necesito que lo termines" (y le pegué la conversación completa con OpenCode).

**Resumen de respuesta:** Creó `landing.css` con el estilo de la referencia, movió las posiciones de las imágenes del hero al CSS y levantó el servidor para revisar la página en el navegador, en escritorio y en celular. Al revisarla detectó que la franja de categorías salía repetida (unas 40 en vez de 6): el `ordering` del `Meta` de `Producto` hacía que `distinct()` no agrupara solo por categoría. Lo corrigió en la vista ordenando explícitamente por `categoria` antes del `distinct()`.

**Qué usó o modificó antes de integrarla:** Revisé el resultado en el navegador y pedí cambios en las consultas siguientes.

### Consulta 8 — Ajustes visuales del hero, header y footer
**Prompts:**
- "estas imagenes no las difumines tanto, lo otro es que acomodes las letras y los botones para que no queden por encima de las imagenes y de la segunda imagen borra ese texto en grande del 'el martillo'"
- "ahora quita el emoji de martillo y coloca solo 'El martillo' y al medio de la pagina junto con el slogan"
- "puedes hacer que las letras queden como mas en negro, como esta la de la segunda imagen"

**Resumen de respuesta:** Bajó el difuminado de las imágenes (de `blur(12px)` a `blur(3px)`). Para que el texto no se montara sobre las imágenes, hizo que el hero completo fuera una grilla CSS donde el texto ocupa su propia celda central y la fila del medio crece según su alto. Eliminó la palabra gigante "el martillo" del footer, dejó el header como "El Martillo" centrado con el slogan y cambió los links del menú a color negro con más grosor.

**Qué usó o modificó antes de integrarla:** Mandé capturas de pantalla de lo que no me gustaba y revisé cada cambio en distintos tamaños de pantalla antes de pedir el siguiente.

### Consulta 9 — Aplicar el diseño al resto del sitio
**Prompt:** "ya mira, sucede de que el resto de la pagina y las ventanas estan asi como en la primera imagen, no se si puedes retocar con los mismos colores y mejorar un poco cada pestaña"

**Resumen de respuesta:** Separó en un archivo nuevo, `tema.css`, los estilos del header, el nav y el footer junto con los de las páginas internas: catálogo, detalle, reportes, formularios, carrito y compra. Lo cargó en `base.html` para todas las páginas y dejó `landing.css` solo con las secciones del inicio. Movió el footer oscuro de 4 columnas a `base.html` y quitó un color azul que estaba escrito directo en `reporte_stock.html`. No modificó `style.css`: el tema nuevo se carga después y lo sobrescribe.

**Qué usó o modificó antes de integrarla:** Revisé que las páginas públicas cargaran y se vieran bien. Las páginas que requieren sesión (carrito, compra exitosa y crear o editar productos) las tengo que revisar iniciando sesión.

### Consulta 10 — Limpieza de comentarios
**Prompt:** "puedes borrar todos los comentarios de los archivos en visual studio que colocaste"

**Resumen de respuesta:** Eliminó los comentarios agregados durante el rediseño en `tema.css`, `landing.css`, `landing.html` y `views.py`, sin tocar los comentarios que ya existían en el proyecto, y verificó que todas las páginas siguieran cargando.

**Qué usó o modificó antes de integrarla:** Lo integré tal cual.

### Consulta 11 — Actualizar este registro
**Prompt:** "puedes modificar el anexo de ia acorde a lo que hicimos ahora, modificalo entero si quieres"

**Resumen de respuesta:** Agregó a la Parte 1 las consultas 6 a 11 del rediseño. No escribió la Parte 2, porque la pauta exige que la redacte yo.

**Qué usó o modificó antes de integrarla:** Revisé que cada consulta correspondiera a lo que pedí. La Parte 2 la actualicé con mis propias palabras.

### Consulta 12 — Dejar este anexo solo de la ES3 (OpenCode)
**Prompt:** "puedes hacer el anexo de ia que sea solamente de esta evaluacion y con prompts coherentes acorde a lo que te pedi del formulario?"

**Resumen de respuesta:** Reestructuró el documento completo: sacó las consultas de la ES2, agregó las de las etapas 0 a 3 (incluida la del formulario con sus validaciones y las del primer landing animado), dejó el registro cubriendo solo esta evaluación y reescribió la Parte 2 como borrador enfocado en la ES3.

**Qué usó o modificó antes de integrarla:** Revisé que los prompts correspondieran a lo que realmente le pedí en cada etapa y ajusté la Parte 2 con mis palabras antes de entregarla.

---

## Parte 2: Explicación del proceso

Para esta evaluación lo que más me gustó fue el formulario de consulta con sus validaciones. Antes habría hecho los chequeos con un montón de if repartidos en la vista o con JavaScript en el navegador, y ver que con `clean_nombre`, `clean_correo` y `clean_mensaje` quedaba todo en un solo lugar, con mensajes en español y sin tocar el template, cambió cómo voy a hacer los formularios de ahora en adelante. Los 19 casos de prueba que le armé me hicieron encontrar huecos que no había pensado, como el correo con un espacio al medio o un nombre que solo tenía puntos.

Lo que más me complicó fueron dos cosas del backend. La primera, la sesión de los últimos productos visitados: al principio, si abría el mismo producto dos veces se repetía en el historial, y tuve que dejarlo sin repetir y cortado en 3. La segunda, una franja de categorías en el landing que mostraba 40 categorías en vez de 6: pasé rato mirando el template hasta que vi que el problema era del ORM — el `ordering` del modelo hacía que el `distinct()` agrupara por id y no por categoría, y la solución fue ordenar explícitamente por categoría antes de agrupar.

También me costó partir de una referencia de diseño ajena y adaptarla a mi proyecto sin romper el resto del sitio. Usar bloques en `base.html` (como los del footer y las clases de body y main) para cambiar solo el landing me salvó: las páginas internas siguieron iguales mientras el inicio se veía distinto. Al final, esta evaluación me dejó claro que el ORM y los formularios de Django hacen el trabajo pesado; a mí me queda pensar bien los datos, las reglas y cómo se ve todo al final.
