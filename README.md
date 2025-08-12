# CifraClub CLI

Interfaz de línea de comandos para buscar canciones y mostrar sus acordes desde [CifraClub](https://www.cifraclub.com.br) sin necesidad de abrir el navegador.

## Uso

```bash
pip install -r requirements.txt
python cifraclub_cli.py "nombre de la canción"
```

El programa listará los primeros resultados; al elegir uno mostrará los acordes en la terminal.

> **Nota:** El sitio puede bloquear solicitudes automatizadas; en ese caso la herramienta mostrará un error al conectar.
