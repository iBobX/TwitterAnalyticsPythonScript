#----------------------------------------------------------------------------
# Librerías
#----------------------------------------------------------------------------
from twython import Twython
from wordcloud import WordCloud, STOPWORDS
from pandas import DataFrame
import os
import re
import nltk
from nltk.corpus import stopwords
import sys
import json

#----------------------------------------------------------------------------
# Variables Globales
#----------------------------------------------------------------------------
usingCommandLine = False

#----------------------------------------------------------------------------
# Funciones
#----------------------------------------------------------------------------

# Creacion de WordCloud
# La salida es en el directorio actual
def generateWordCloud(words, width, height, bg_color, words_count, output_file_name):
    stopwords = set(STOPWORDS)
    text = ' '.join(words)
    wc = WordCloud(width=width,
                   height=height,
                   background_color=bg_color,
                   max_words=words_count,
                   stopwords=stopwords,
                   random_state=1,
                   collocations=False).generate(text)
    # Si se usa línea de comandos, se requiere todo el path de salida
    if usingCommandLine is True:
        wc.to_file(output_file_name)
    # De lo contrario se pone en el directorio actual/images
    else:
        wc.to_file(os.path.join(os.getcwd(), output_file_name))


# Funcion que toma todo el texto, lo limpia
# de menciones, hastags, emoticones, URL's, símbolos,
# y palabras comunes no importantes para el cometido
# retorna un list con todas las palabras
def cleanAndTokenizeText(list_TwitsText):
    # patter para eliminar emoticons
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    # cargo todo el texto en un solo string
    clean_text = ' '.join(list_TwitsText)
    # eliminar menciones
    clean_text = re.sub(r'@([a-zA-Z0-9\\_\\.]+)', '', clean_text)
    # eliminar urls
    clean_text = re.sub(r'https:([a-zA-Z0-9\\_\\.\\/]+)', '', clean_text)
    # eliminar hashtags
    clean_text = re.sub('#([a-zA-Z0-9\\_\\.]+)', '', clean_text)
    # eliminar números
    clean_text = re.sub(r'[0-9]+', '', clean_text)
    # eliminar emojis
    clean_text = emoji_pattern.sub('', clean_text)
    # eliminar otros símbolos
    clean_text = re.sub(r'[^\w\ \_]', '', clean_text)
    # tokenizar palabras nuevamente
    terms_all = clean_text.split()
    # filtro/exluyo palabras no requeridas
    filtered_words = [
        word
        for word in terms_all
        if word not in stopwords.words('english')
        and
        word not in stopwords.words('spanish')
        and
        len(word) > 3  # prevenir la, el, acá, y cosas por el estilo
    ]
    # retorno las palabras
    return filtered_words


#----------------------------------------------------------------------------
# Inicialización de Twitter
# Debes crear una aplicacion en https://apps.twitter.com para obtener
# el APP_KEY y el APP_SECRET
#----------------------------------------------------------------------------
# Authorizo Twython
APP_KEY = ''
APP_SECRET = ''
twythonInst = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twythonInst.obtain_access_token()
twitterClient = Twython(APP_KEY, access_token=ACCESS_TOKEN)

#----------------------------------------------------------------------------
# Bajo últimos 100 tweets excluyendo los retweets
#------------------------------------------------------------------------------

# Para permitir usar en línea de comandos, y pasarle lo que se desea buscar
# si se paso los keywords via línea de commandos
try:
    query = sys.argv[1]
    usingCommandLine = True
except:  # si no, cargar predeterminado
    query = "@Uruguay OR #Uruguay"

# Buscar...
queryResult = twitterClient.search(q=query + ' -filter:retweets',
                              count=100)

# Si no se encontraron twits, salir
if len(queryResult['statuses']) == 0:
    print("No twits found for the specified search keywords")
    sys.exit(1)

#----------------------------------------------------------------------------
# Proceso los nombres de los archivos de salida en la línea de comandos
#----------------------------------------------------------------------------

if usingCommandLine == True:
    try:  # intento cargar los nombres
        # nombre de archivo para screen names (usuarios mas activos)
        mostactiveusers_file_name = sys.argv[2]
        # nombre de archivo para palabras mas usadas
        mostusedwords_file_name = sys.argv[3]
        # nombre de archivo para nube de hashtags
        hashtags_file_name = sys.argv[4]
    except:  # si alguno de los nombres no fue pasado error y salir
        print("\n\nPlease specify desired output images filenames. Ex: \"tda_mentions\" \"tda_words\"")
        sys.exit(1)
else:  # en caso de no ser línea de commandos, asumir nombres
    mostactiveusers_file_name = 'tda_mostactive.png'
    mostusedwords_file_name = 'tda_words.png'
    hashtags_file_name = 'tda_hashtags.png'


#----------------------------------------------------------------------------
# Descargar stopwords ...
#----------------------------------------------------------------------------
nltk.download("stopwords", quiet=True)



#----------------------------------------------------------------------------
# Conversion a DataFrame para mejor manipulacion
# Extracción de URL's, HashTags, screen_names, y demás info
#----------------------------------------------------------------------------
#creo dataframe vacío con las columnas a usar
df_tweets = DataFrame(columns=['ids','texts','screen_names','names','locations','descriptions','langs','hashtags','urls','images','link_to_tweet'])
#creao una lista vacía que contendrá los hashtags
lst_hashtags = []
#creo una lista vacía que contendrá las URL's 
lst_urls = []
#creo una lista vacía que contendrá las imagenes/media y URL a tuit
lst_images = []
#creo una lista vacía que contendrá links directo to tuits
lst_links_to_tuits = []
#recorro todos los statuses
for status in queryResult['statuses']:
    #lista hashtag vacía
    hashtags=[]
    #si hay alguna hashtag
    if 'hashtags' in status['entities'] and len(status['entities']['hashtags']) > 0:
        #recorro todos los hashtags y obtengo el texto en minúsculas
        hashtags = [hashtag['text'].lower() for hashtag in status['entities']['hashtags']]
        #lo agrego a la lista de hashtags global
        lst_hashtags.extend(hashtags)
    #lista urls vacía
    urls=[]
    #si hay alguna URL
    if 'urls' in status['entities'] and len(status['entities']['urls']) > 0:
        #recorro todas las urls, extraigo la url expandida y la agrego a urls
        urls = [url['expanded_url'] for url in status['entities']['urls']]
        #agrego las urls encontradas a la lista
        lst_urls.extend(urls)
    #genero link to tuit
    link_to_tweet = 'https://twitter.com/statuses/'+status['id_str']
    #agrego link to tuit a la lista
    lst_links_to_tuits.append(link_to_tweet)
    #lista urls imágenes vacía
    images=[]
    #si hay alguna URL
    if 'media' in status['entities'] and len(status['entities']['media']) > 0:
        #recorro todas las urls, extraigo la url expandida y la agrego a urls
        images = [image['media_url'] for image in status['entities']['media']]
        #agrego las urls encontradas a la lista y el link al su tuit
        lst_images.append({"images":images,"url":link_to_tweet})

    #agrego nueva fila de datos al dataframe
    df_tweets = df_tweets.append({
            'ids': status['id'],
            'texts': status['text'],
            'screen_names': status['user']['screen_name'],
            'names': status['user']['name'],
            'locations': status['user']['location'],
            'descriptions': status['user']['description'],
            'langs': status['user']['lang'],
            'hashtags':hashtags,
            'urls':urls,
            'images':images,
            'link_to_tweet':link_to_tweet
            },ignore_index=True)


#----------------------------------------------------------------------------
# Extracción de Screen Names
#----------------------------------------------------------------------------


# Hago una nube de palabras de los usuarios que mas tuitearon sobre el tema
# y con un máximo de 60 screen names
generateWordCloud(words=df_tweets['screen_names'],
                  width=800,
                  height=400,
                  bg_color='black',
                  words_count=60,
                  output_file_name=mostactiveusers_file_name)

#----------------------------------------------------------------------------
# Extracción de Palabras Mas Usadas
#----------------------------------------------------------------------------

# Veo qué palabras son las más usadas en los tueets que mencionan los keywords,
# sacando los emoticones, las menciones, las urls, y los hastags
tweets_words = cleanAndTokenizeText(df_tweets['texts'])

# Hago una nube de palabras con las palabras mas usadas
# y con un máximo de 60 palabras mostradas
generateWordCloud(words=tweets_words,
                  width=800,
                  height=400,
                  bg_color='black',
                  words_count=60,
                  output_file_name=mostusedwords_file_name)


#----------------------------------------------------------------------------
# Extracción de HashTags mas usados
#----------------------------------------------------------------------------


# Hago una nube de palabras con los hashtags mas usados
# y con un máximo de 60 palabras mostradas
generateWordCloud(words=lst_hashtags,
                  width=800,
                  height=400,
                  bg_color='black',
                  words_count=60,
                  output_file_name=hashtags_file_name)


# Si estamos en línea de comandos, devolver los caminos a los archivos generados
if usingCommandLine == True:
    #creo objeto con estructura para JSON
    results = {
            'images':
                {
                 'users':mostactiveusers_file_name,
                 'words': mostusedwords_file_name,
                 'hashtags':hashtags_file_name
                 },
            'media':
                {
                 'tweet_images':lst_images,
                 'shared_urls':lst_urls
                }
            }
    #convierto objeto a string json y lo retorno
    print(json.dumps(results))
else:
    print(os.path.join(os.getcwd(), mostactiveusers_file_name))
    print(os.path.join(os.getcwd(), mostusedwords_file_name))
    print(os.path.join(os.getcwd(), hashtags_file_name))
    print("Done!")
