# TwitterAnalyticsPythonScript
Twitter text mining de menciones y palabras mas usadas.

Por ahora solo genera tres nubes de palabras (wordcloud) con los usuarios mas activos, de las palabras, y hashtags mas relevantes.

## Ejemplo de resultados para "@Uruguay OR #Uruguay"

### Usuarios más activos (screen_names) 

![alt text](tda_mostactive.png "Usuarios mas activos")


### Palabras mas relevantes

![alt text](tda_words.png "Palabras mas relevantes")


### Hashtags mas relevantes
![alt text](tda_hashtags.png "Hashtags mas relevantes")


## Usándolo en línea de comandos

Este script se puede usar en línea de comandos.

La sintaxis sería algo así:

python3 visualizaciones.py "que buscar" "/camino/nombre_imagen_users.png"  "/camino/nombre_imagen_words.png"  "/camino/nombre_imagen_hashtags.png"

Esto devolverá una cadena JSON la cual contiene el camino a las imágenes generadas, la extracción de los links a las imágenes compartidas en las publicaciones, los links a las url's compartidas, y los links directos a los tuits:

```json
{
  "images": {
    "users": "/camino/nombre_imagen_users.png",
    "words": "/camino/nombre_imagen_words.png",
    "hashtags": "/camino/nombre_imagen_hashtags.png"
  },
  "media": {
    "links": {
      "images": [
        "http://pbs.twimg.com/media/...jpg",
        "http://pbs.twimg.com/media/...jpg",
        "http://pbs.twimg.com/media/...jpg",
        ...
      ],
      "tweet": [
        "https://twitter.com/statuses/####",
        "https://twitter.com/statuses/####",
        "https://twitter.com/statuses/####",
        ...
      ],
      "urls": [
        "https://shared_url_1...",
        "https://shared_url_2...",
        "https://shared_url_3...",
        ...
      ]
    }
  }
}
```


Nota: Un agradecimiento a [@d4tagirl](https://github.com/d4tagirl/DuraznoConfMentions) por haber compartido su script en R que me sirvió como inspiración para este. ¡Una genia! ¡gracias!