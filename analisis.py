"""
Adaptado de: https://www.freecodecamp.org/news/how-to-make-your-own-sentiment-analyzer-using-python-and-googles-natural-language-api-9e91e1c493e/
"""

import tweepy
import os
import json
from datetime import datetime, timedelta
import re
from nltk.tokenize import WordPunctTokenizer
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


# Accedemos a las claves de acceso a nuestra App de Twitter:
with open('Keys.json') as f:
    data = json.load(f)

ACC_TOKEN = data["Access_token"]
ACC_SECRET = data["Access_token secret"]
CONS_KEY = data["API_key"]
CONS_SECRET = data["API_secret key"]


def authentication(cons_key, cons_secret, acc_token, acc_secret):
    """
    Función para obtener acceso a una app de Twitter dadas las
    claves.

    Args:
        cons_key: Consumer Key.
        cons_secret: Consumer API Secret.
        acc_token: Access Token.
        acc_secret: Access Token Secret.

    Returns:
        api con el acceso garantizado.
    """

    auth = tweepy.OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(acc_token, acc_secret)
    api = tweepy.API(auth)

    return api


def search_tweets(keyword, total_tweets):
    """
    Función para buscar tweets en español dados un keyword y una cantidad total de tweets. En
    este caso se limitan también a buscar en un periodo no mayor a 24 horas.

    Args:
        keyword: Palabra a buscar en Twitter.
        total_tweets: Cantidad total de tweets a buscar.

    Returns:
        search result: Iterable con toda la información de los tweets encontrados.
    """

    today_datetime = datetime.today().now()
    yesterday_datetime = today_datetime - timedelta(days=1)
    yesterday_date = yesterday_datetime.strftime('%Y-%m-%d')
    api = authentication(CONS_KEY, CONS_SECRET, ACC_TOKEN, ACC_SECRET)
    search_result = tweepy.Cursor(api.search,
                                  q=keyword,
                                  since=yesterday_date,
                                  result_type='recent',
                                  lang='es').items(total_tweets)

    return search_result


def clean_tweets(tweet):
    """
    Función para limpiar los tweets de elementos innecesarios al momento de realizar
    análisis de sentimiento.

    Nota:   La API de Google es bastante flexible a la hora de realizar análisis de
            sentimiento. No estoy seguro de que todas estas "limpiezas" sean del todo
            necesarias.

    Args:
        tweet: Tweet (o texto) a limpiar.

    Returns:
        clean_tweet: Tweet ya limpio para proceder a realizar análisis de sentimiento.
    """

    # Removemos el usuario en el tweet
    user_removed = re.sub(r'@[A-Za-z0-9]+', '', tweet.decode('utf-8'))

    # Removemos cualquier link presente en el tweet
    link_removed = re.sub('https?://[A-Za-z0-9./]+', '', user_removed)

    # llevamos todo a minúsculas
    lower_case_tweet = link_removed.lower()

    # Instanciamos un tokenizador y, de aucerdo a sus reglas, creamos la lista de tokens
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)

    # Unimos los tokens para crear un único string a ser enviado
    clean_tweet = (' '.join(words)).strip()

    return clean_tweet


def get_sentiment_score(tweet):
    """
    Función que utiliza la API NLP de Google para realizar análisis de sentimiento
    sobre un texto.

    Args:
        tweet: Tweet (o texto) a realizar análisis de sentimiento.

    Returns:
        sentiment_score: Puntaje de sentimiento cuyo rango va desde -1.0 (negativo) hasta
        1.0 (positivo).

    Nota:
        El análisis de sentimiento de Google también arroja un valor de magnitud ("magnitude").
        Este valor es usado para determinar la "fuerza" general del sentimiento calculado. Para
        mayor detalle consultar:
            https://cloud.google.com/natural-language/docs/basics#interpreting_sentiment_analysis_values
    """

    client = language.LanguageServiceClient()
    document = types\
        .Document(content=tweet, type=enums.Document.Type.PLAIN_TEXT)
    sentiment_score = client\
        .analyze_sentiment(document=document)\
        .document_sentiment\
        .score

    return sentiment_score


def analyze_tweets(keyword, total_tweets):
    """
    Función general para realizar el análisis de tweets, engloba las funciones anteriores.

    Args:
        keyword: Palabra a buscar en Twitter.
        total_tweets: Cantidad total de tweets a buscar.

    Returns:
        final_score: Promedio del score de sentimiento entre los tweets analizados.
    """

    score = 0
    tweets = search_tweets(keyword, total_tweets)
    lista_tweets = []
    for tweet in tweets:
        cleaned_tweet = clean_tweets(tweet.text.encode('utf-8'))
        sentiment_score = get_sentiment_score(cleaned_tweet)
        score += sentiment_score
        no_link_tweet = re.sub('https?://[A-Za-z0-9./]+', '', tweet.text)
        lista_tweets.append((no_link_tweet, sentiment_score))
    final_score = round((score / float(total_tweets)), 2)

    return final_score, lista_tweets


# Casos Ejemplo:

# 1.- Probando comentarios específicos:
""" bad_comment = get_sentiment_score('¡Esta lavadora no sirve para nada!')
good_comment = get_sentiment_score('Esta lavadora es buenisima')
neutral_comment = get_sentiment_score('Lavadora mas o menos')

print('bad_comment_score:', bad_comment)
print('good_comment_score:', good_comment)
print('neutral_comment_score:', neutral_comment) """
