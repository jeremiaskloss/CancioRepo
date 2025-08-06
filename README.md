# CifraClub CLI

Interfaz de línea de comandos para buscar canciones en [CifraClub](https://www.cifraclub.com.br/) y ver la letra con acordes sin abrir el navegador. También incluye una interfaz web mínima en HTML.

## Uso

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Interfaz de línea de comandos:
   ```bash
   python cli.py
   ```
3. Interfaz web:
   ```bash
   python app.py
   ```
   Luego abrir [http://127.0.0.1:5000](http://127.0.0.1:5000) en el navegador.
4. Ingresá el nombre de la canción, elegí un resultado y se mostrará la letra con los acordes.

La herramienta realiza scraping del sitio, por lo que el formato puede variar según la página.
