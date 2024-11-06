# My HTML to JSON Blocks Library

**Descripción:**
Esta librería convierte contenido HTML en una estructura de bloques JSON, útil para sistemas que requieren transformar contenido web en formatos procesables. Es altamente personalizable, permitiendo a los usuarios definir su propio método de conversión para imágenes mediante el uso de un sistema de clases abstractas.

**Características principales:**
- Convierte etiquetas HTML comunes como párrafos, encabezados, listas, y enlaces en bloques JSON estructurados.
- Ofrece una clase abstracta para que los usuarios personalicen la transformación de imágenes (`ImageTransformer`).
- Diseño modular que permite extender y adaptar la funcionalidad base.
- Ideal para integrar en sistemas de gestión de contenido o aplicaciones que procesen contenido web.

**Estructura de bloques JSON:**
- **Encabezados:** Convertidos a bloques con niveles de título (`h1`-`h6`).
- **Párrafos:** Procesa contenido inline como texto, negritas, cursivas y enlaces.
- **Listas:** Soporte tanto para listas ordenadas como desordenadas.
- **Imágenes:** Proporciona un bloque de imagen con metadatos detallados, personalizable mediante el método abstracto `ImageTransformer`.

**Cómo usar:**
1. Clona el repositorio:
   ```bash
   git clone https://github.com/yourusername/html-to-json-blocks.git
   cd html-to-json-blocks
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Instala la librería:
   ```bash
   pip install .
   ```

4. Crea una instancia del convertidor:
   ```python
   from html_to_json_blocks.core import HtmlToJsonConverter
   from html_to_json_blocks.transformers.image_transformer import ImageTransformer

   class CustomImageTransformer(ImageTransformer):
       def transform_image(self, img_node, images_info):
           # Tu lógica personalizada para transformar imágenes
           pass

   converter = HtmlToJsonConverter(image_transformer=CustomImageTransformer())
   ```

5. Usa el convertidor para transformar HTML en bloques JSON:
   ```python
   from bs4 import BeautifulSoup

   html_content = "<p>Ejemplo de contenido HTML</p>"
   soup = BeautifulSoup(html_content, 'html.parser')
   images_info = []  # Información de imágenes si es necesario
   json_blocks = converter.convert(soup, images_info)
   print(json_blocks)
   ```

**Pruebas:**
Las pruebas unitarias están incluidas en el directorio `tests`. Para ejecutarlas, utiliza:

```bash
pytest
```

**Contribuciones:**
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request si deseas mejorar la funcionalidad o corregir errores.
