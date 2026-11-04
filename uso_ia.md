# Documento de uso de IA — ES2 Ferretería El Martillo

## Parte 1: Registro de consultas

### Consulta 1 — Guía paso a paso de la migración
**Prompt:** "Necesito que este mismo código lo modifiques a las pautas de evaluación de la ES2. Explícame qué hiciste, cómo lo hiciste, en una guía paso a paso para hacer manualmente el cambio en los códigos."

**Resumen de respuesta:** La IA me entregó una guía dividida en 5 fases (una por etapa): qué archivos crear, qué borrar de la ES1, cómo quedarían los modelos, cómo se registra el admin y cómo se carga la fixture. Cada paso indicaba el archivo exacto y el comando a ejecutar.

**Qué usó o modificó antes de integrarla:** Usé la guía como plan de trabajo para ejecutar las 5 etapas. Le pedí ajustes antes de empezar: conservar login/registro/carrito de la ES1 (la ES3 los necesita), usar pipenv además de generar `requirements.txt`, y que los templates no cambiaran calculando `username` y `es_admin` desde `request.user` en una función auxiliar. También me indicó que borrara el admin propio de la ES1 (4 vistas, 4 URLs, 3 templates) porque Django Admin lo reemplazaba.

### Consulta 2 — Modelo de datos y migraciones
**Prompt:** "Crea el modelo Producto de la variante ferretería con nombre, categoría, precio e stock (y el campo imagen para las fotos de la ES1), con __str__. También un modelo ItemCarrito con usuario ( ForeignKey a User), producto ( ForeignKey a Producto) y cantidad, con unique_together."

**Resumen de respuesta:** Me generó los dos modelos con los tipos adecuados: `CharField` para nombre/categoría/imagen, `IntegerField` para precio/stock, `PositiveIntegerField` para cantidad, más las foreign keys y el `__str__` pedido en ambos.

**Qué usó o modificó antes de integrarla:** Agregué `Meta.ordering = ["id"]` al Producto para mantener el orden del catálogo de la ES1 y `related_name` a las foreign keys. Luego ejecuté `python manage.py makemigrations catalogo` y `python manage.py migrate`, verificando que las migraciones se aplicaran sin errores. Como el superusuario tenía que existir en cualquier clon nuevo, le pedí además una migración de datos (`0002_crear_superusuario`) que crea `admin/admin123` en cada `migrate`.

### Consulta 3 — Django Admin con list_display y búsqueda
**Prompt:** "Registra Producto e ItemCarrito en admin.py con list_display de 3 campos o más, search_fields y list_filter, para cumplir el criterio 2.1.2 de la pauta."

**Resumen de respuesta:** Me entregó las clases `ProductoAdmin` y `ItemCarritoAdmin` decoradas con `@admin.register`, con `list_display = ("nombre", "categoria", "precio", "stock")`, `search_fields = ("nombre", "categoria")` y `list_filter = ("categoria",)`.

**Qué usó o modificó antes de integrarla:** Probé todo desde `/admin`: la búsqueda con `?q=martillo`, el filtro por categoría y el CRUD completo (crear, editar y eliminar un producto de prueba), verificando cada vez que el cambio se reflejara en el catálogo del sitio.

### Consulta 4 — Autenticación con django.contrib.auth
**Prompt:** "Reemplaza mi autenticación en JSON (usuarios.json con SHA-256) por django.contrib.auth: login con authenticate() y login(), registro con User.objects.create_user() y logout con logout(). Mis validaciones de registro se mantienen, el rol admin pasa a ser user.is_staff, y los templates no deben cambiar."

**Resumen de respuesta:** Me reescribió las tres vistas (`vista_login`, `vista_registro`, `vista_logout`) usando la API de autenticación de Django. Para no tocar los templates, creó una función `_contexto_base(request)` que calcula `username`, `es_admin` y `cart_count` desde `request.user`, y las vistas usan `**_contexto_base(request)` en el contexto.

**Qué usó o modificó antes de integrarla:** Cambié las validaciones: `_usuario_existe()` pasó a `User.objects.filter(username=...).exists()`. Verifiqué que las contraseñas ahora se guardan con PBKDF2 de Django (ya no SHA-256) y probé el flujo completo: registro crea el usuario en la BD, login autentica, logout cierra la sesión, y el badge "Admin" del nav sale de `user.is_staff`.

### Consulta 5 — Poblamiento con IA y lectura desde la BD ⭐
**Prompt (poblamiento):**
> "Genera una fixture JSON de Django para el modelo catalogo.Producto con 40 productos de ferretería chilenos realistas. Campos: nombre, categoría, precio (int, 1000 a 150000), stock (int, 0 a 50). Formato: lista de objetos con model, pk y fields, lista para cargar con loaddata."

**Prompt (posterior):** "Ya con la fixture cargada, elimina PRODUCTOS_DEFAULT, la función _asegurar_productos y cualquier referencia a JSON en views.py, para que el template principal lea desde la BD con ORM sin datos en duro. También conecta los productos destacados del landing a la BD."

**Resumen de respuesta:** Del primer prompt: la lista completa de 40 productos con precios chilenos realistas en formato fixture. Del segundo: las líneas exactas a eliminar y el loop `{% for p in destacados %}` con `Producto.objects.order_by("-precio")[:4]`.

**Ajustes que hice antes de integrarla:**
1. **Formato:** ajusté la salida al formato exacto de fixture de Django — `{"model": "catalogo.producto", "pk": 1, "fields": {...}}` con el nombre del modelo en minúsculas y `pk` explícito, tal como lo exige `loaddata`.
2. **Volumen:** mi base de la ES1 tenía 41 productos (uno se había agregado desde el admin); la pauta pide 40, así que eliminé el sobrante.
3. **Stock:** mantuve exactamente 7 productos agotados (stock 0: IDs 4, 8, 13, 19, 27, 35, 40) para conservar el comportamiento de la ES1.
4. **Carga:** guardé el archivo en `catalogo/fixtures/productos.json` y lo cargué con `python manage.py loaddata productos.json`, verificando los 40 productos y los 7 agotados en `/admin`.
5. **Datos en duro:** eliminé 48 líneas de `views.py` y reemplacé los 4 productos hardcodeados del landing por el loop dinámico; verifiqué con grep que no quedara ninguna referencia a JSON.

---

## Parte 2: Explicación del proceso

Lo que más me gustó fue trabajar con el ORM. Antes de esto yo hacía todo leyendo archivos y metiendo datos a mano, así que entender que con `Producto.objects.all()` ya tenías todo el catálogo fue un alivio. Lo que más me complicó fue el carrito: la primera versión que me salió guardaba el precio en el momento de agregar el producto, y después probé cambiando un precio en el admin y el total quedaba mal. Tuve que pensarlo un rato y cambiarlo para que siempre lea el precio de la BD.

Con la fixture me pasó algo parecido: la IA me generó los 40 productos bien, pero cuando lo metí al formato que pide Django el `loaddata` me tiraba error hasta que acomodé el modelo en minúsculas y los `pk`. También tenía un producto de más de la ES1 y tuve que sacarlo para cumplir exactamente 40. Al final entendí algo que antes no me quedaba claro: las migraciones no son "el script que crea la tabla una vez", son parte del proyecto; por eso hice una que crea el superusuario, porque si alguien clona el repo y solo corre `migrate`, el admin ya está ahí esperando. Eso de que el proyecto se pueda levantar desde cero sin tocar nada fue lo que más me gustó de esta evaluación.
