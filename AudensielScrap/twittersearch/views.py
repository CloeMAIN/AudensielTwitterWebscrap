from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import random
from django.shortcuts import render
from .models import tweet_collection,req_collection


from datetime import datetime
from django.http import JsonResponse
from bson.json_util import dumps

from decouple import config
# Variables d'environnement pour stocker les identifiants Twitter
USER_ID = config('USER_ID')
USER_PASSWORD = config('USER_PASSWORD')

# Ensemble pour stocker les identifiants des tweets traités
processed_tweets = set()


def random_sleep():
    """
    Réalise une pause aléatoire entre 2 et 5 secondes. 

    parameters
    ----------
    None.

    Returns
    -------
    None.
    """
    time.sleep(random.uniform(2, 5))


class Commentaires: # Classe pour stocker les commentaires d'un tweet
    def __init__(self, commentaires=None, timelist=None):
        self.commentaires = commentaires if commentaires else [] # Liste des commentaires
        self.date_commentaire = timelist if timelist else [] # Liste des dates des commentaires


    def add_comment(self,comment, timelist): 
        """
        Ajouter un commentaire à la liste des commentaires
        """
        for comm, time in zip(comment, timelist):

            self.commentaires.append(comm)
            self.date_commentaire.append(time)
    def to_dict(self): 
        """
        Convertir l'objet en dictionnaire
        """
        #if not empty
        if self.commentaires:
            return [{"commentaire": c, "date_commentaire": d} for c, d in zip(self.commentaires, self.date_commentaire)]

        else:
            return [{"commentaire": "", "date_commentaire": ""}]

class DonneeCollectee: # Classe pour stocker les données d'un tweet
    
    def __init__(self, text_tweet, nombre_likes, nombre_reposts, nombre_replies, nombre_views, date_tweet, identifiant_tweet, req_id, comment_tweet=None):
        self.text_tweet = text_tweet
        self.date_tweet = date_tweet
        self.identifiant = int(identifiant_tweet)
        self.req_id = req_id
        if nombre_likes == "":
            self.nombre_likes = 0
        else:
            self.nombre_likes = self.convert_number(nombre_likes)

        if nombre_reposts == "":
            self.nombre_reposts = 0
        else:
            self.nombre_reposts = self.convert_number(nombre_reposts)

        if nombre_replies == "":
            self.nombre_replies = 0
        else:
            self.nombre_replies = self.convert_number(nombre_replies)

        if nombre_views == "":
            self.nombre_views = 0
        else:
            self.nombre_views = self.convert_number(nombre_views)

        self.comment_tweet = Commentaires() 

    # === PRIVATE METHODS === # 
    def convert_number(self, value): # Convertir les nombres en entiers
        if value[-1] == "K":
            return int(float(value[:-1]) * 1000)
        elif value[-1] == "M":
            return int(float(value[:-1]) * 1000000)
        else:
            return int(value)

    def add_comment(self,comment, timelist): # Ajouter un commentaire à la liste des commentaires
        self.comment_tweet.add_comment(comment, timelist) 
        # self.comment_tweet.append([comm, time] for comm, time in zip(comment, timelist))  

    # === PUBLIC METHODS === #
    def to_dict(self): # Convertir l'objet en dictionnaire
        return {
            "text_tweet": self.text_tweet,
            "nombre_likes": self.nombre_likes,
            "nombre_reposts": self.nombre_reposts,
            "nombre_replies": self.nombre_replies,
            "nombre_views": self.nombre_views,
            "date_tweet": self.date_tweet,
            "identifiant": self.identifiant,
            "comment_tweet": self.comment_tweet.to_dict(),
            "req_id": self.req_id
        }

def login(bot): # Fonction pour se connecter à Twitter
    bot.get('https://twitter.com/i/flow/login')

    USER_ID_input = WebDriverWait(bot, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'r-1yadl64'))
    )
    USER_ID_input.send_keys(USER_ID)

    button = bot.find_element(By.CSS_SELECTOR, 'div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox div.css-175oi2r.r-16y2uox.r-1jgb5lz.r-13qz1uu div:nth-child(6)')
    button.click() # Click the login button

    password_input = WebDriverWait(bot, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-175oi2r input[type="password"]')))
    password_input.send_keys(USER_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    random_sleep()
    


def save_tweets(tweets):
    """
    Enregistre les tweets dans la base de données. Si le tweet existe déjà, 
    les commentaires sont ajoutés à la liste des commentaires existants et 
    on met à jour les statistiques du tweet.
    tweetcollection est la collection de la base de données MongoDB où les tweets sont stockés.

    """
    element = tweets.to_dict()
    print(element)

    if tweet_collection.find_one({"identifiant": element["identifiant"]}): # Vérifier si l'élément existe déjà
        print("L'élément existe déjà")
        tweet_collection.update_one({"identifiant": element["identifiant"]},
                                     {"$set": {"nombre_views": element["nombre_views"],
                                               "nombre_likes": element["nombre_likes"],
                                               "nombre_reposts": element["nombre_reposts"],
                                               "nombre_replies": element["nombre_replies"]},
                                      "$addToSet": {"comment_tweet": {"$each": element["comment_tweet"]}} # Ajouter les nouveaux commentaires à la liste des commentaires existants
                                      },
                                      upsert=False
                                    )

    else: 
        print("L'élément n'existe pas")
        tweet_collection.insert_one(element)


def perform_scroll(bot): # Fonction pour faire défiler la page
    page_height = bot.execute_script("return document.body.scrollHeight")
    bot.execute_script(f"window.scrollTo(0, {page_height/2});")
    random_sleep()
    bot.execute_script(f"window.scrollTo({page_height/2}, {page_height});")
    random_sleep()



def get_comment_tweet(bot, utilisateur, identifiant, search_url, tweet_text): # Fonction récupérer les commentaires d'un tweet
    """
    Récupère les commentaires d'un tweet à partir de son identifiant

    Parameters
    ----------
    bot : webdriver
        Le navigateur web
    utilisateur : str
        Le nom de l'utilisateur
    identifiant : str
        L'identifiant du tweet
    search_url : str
        L'URL de la page de recherche
    tweet_text : str
        Le texte du tweet pour éviter de le scraper de nouveau
    
    Returns
    -------
    list, list
        La liste des commentaires, la liste des dates de commentaires 
    
    """

    tweet_url = f'https://twitter.com/{utilisateur}/status/{identifiant}'
    bot.get(tweet_url)

    time.sleep(5)

    scroll_position_before_click = bot.execute_script("return window.scrollY;") # On enregistre la position du scroll avant de cliquer sur le bouton "Afficher les commentaires"
    
    WebDriverWait(bot, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"] [data-testid="tweetText"]')))
    
    comments, timelist = extract_comments(bot, 10, tweet_text) # On extrait les commentaires
    # print(f"Comments for tweet {identifiant}: {comments}")

    bot.get(search_url) # On retourne à la page de recherche
    random_sleep()
    bot.execute_script(f"window.scrollTo(0, {scroll_position_before_click});")
    random_sleep()
    return comments, timelist

def extract_comments(bot, num_comments, tweet_text): # Fonction pour extraire les commentaires
    """
    Extrait les commentaires d'un tweet et parse les informations. Il est important de noter
    que le webdriver doit déjà être sur la page du tweet pour que cette fonction fonctionne. 

    Parameters
    ----------
    bot : webdriver
        Le navigateur web
    num_comments : int
        Le nombre de commentaires à extraire
    tweet_text : str
        Le texte du tweet pour éviter de le scraper de nouveau 
    
    Returns
    -------
    list
        La liste des commentaires 
    
    """
    comments = set()  # On utilise un ensemble pour stocker les commentaires uniques
    time_set = set()
    # Défilement de la page pour charger les commentaires supplémentaires
    for _ in range(num_comments // 5):  # 5 commentaires sont chargés à la fois
        
        page_height = bot.execute_script("return document.body.scrollHeight")
        bot.execute_script(f"window.scrollTo(0, {page_height/2});")
        soup = BeautifulSoup(bot.page_source, 'html.parser')
        # save soup to file with random name for debugging
        # with open(f'data/twitterComment{random.random()}.html', 'w', encoding='utf-8') as f:
        #     # url for debugging
        #     f.write(bot.current_url)
        #     f.write(soup.prettify())
        commententaires = soup.find_all(attrs={'data-testid': 'tweet'})
        time_elements = soup.find_all('time')

        for comment, time in zip(commententaires, time_elements):
            comment_text = comment.find(attrs={'data-testid': 'tweetText'})
            time = time['datetime'][0:10]
            if comment_text is not None and comment_text.get_text(strip=True) != tweet_text: # On vérifie que le commentaire n'est pas le même que le tweet
                comment_text = comment_text.get_text(strip=True)
                comments.add(comment_text)  # Ajouter le commentaire à l'ensemble
                time_set.add(time)
            else:
                continue
        random_sleep()

    return list(comments), list(time_set)  # On retourne la liste des commentaires


def scrap_tweets(tweet_elements, bot, search_url, mot_cle, nombre_tweets, nb_tweets, req_id, response_text, liste_tweets, utilisateurs): # Fonction pour récupérer les tweets et leurs informations
    """
    Récupère les tweets et leurs informations à partir des tweet elements

    Parameters
    ----------
    tweet_elements : list
        La liste des éléments de tweet récupérés avec BeautifulSoup
    bot : webdriver
        Le navigateur web
    search_url : str
        L'URL de la page de recherche
    mot_cle : str
        Le mot clé de la recherche
    nombre_tweets : int
        Le nombre de tweets récupérés
    nb_tweets : int
        Le nombre de tweets à récupérer
    req_id : str
        L'identifiant de la requête
    response_text : str
        Le texte de la réponse
    liste_tweets : list
        La liste des tweets
    utilisateurs : list
        La liste des utilisateurs
    
    Returns
    -------
    int, str, list(DonneeCollectee), list(str)
        Le nombre de tweets, le texte de la réponse, la liste des tweets, la liste des utilisateurs
    """
    
    for tweet_element in  tweet_elements:
        #Extraction du texte du tweet
        tweet_div_text = tweet_element.find(attrs={'data-testid': 'tweetText'})
        if tweet_div_text is not None:
            tweet_text = tweet_div_text.get_text(strip= False)
        else:
            continue

        #Extraction du nombre de likes, reposts, replies et vues du tweet
        details = tweet_element.find_all(attrs={'data-testid': 'app-text-transition-container'})
        replies = details[0].get_text(strip=True)
        reposts = details[1].get_text(strip=True)
        likes = details[2].get_text(strip=True)

        #S'assurer qu'il y a 4 éléments dans détails avant d'accéder à details[3] (parfois, le nombre de vus n'est pas inclus dans la liste
        views = details[3].get_text(strip=True) if len(details) >= 4 else ""

        #Extraction de la date d'émission du Tweet
        user_info = tweet_element.find(attrs={'data-testid': 'User-Name'})
        user_info2 = user_info.find_all('a', href=True)
        user_info = user_info.find('time')
        date = user_info['datetime'][0:10]

        #Extrait l'identifiant du tweet et l'utilisateur pour pouvoir récupérer les commentaires dans la suite le nom de l'utilisateur n'est pas conservé
        user_info2 = user_info2[2]['href']
        url_segments = user_info2.split("/")
        identifiant = url_segments[3]
        utilisateur = url_segments[1]

        if (mot_cle in tweet_text) and(nombre_tweets <= nb_tweets) and (identifiant not in processed_tweets):
            if not tweet_collection.find_one({"identifiant": identifiant}):
                    tweets_instance = DonneeCollectee(tweet_text, likes, reposts, replies, views, date, identifiant, req_id, [])
                    # Ajouter l'instance de tweet à la liste de tweets
                    liste_tweets.append(tweets_instance)
                    utilisateurs.append(utilisateur)
                    nombre_tweets += 1
                    response_text += f"\n{identifiant}"
                    processed_tweets.add(identifiant)  # Ajouter l'identifiant du tweet traité à l'ensemble
                    #print (f"Nombre de tweets : {nombre_tweets}")

    return nombre_tweets, response_text, liste_tweets, utilisateurs



def get_tweets(request, mot_cle, until_date, since_date, nb_tweets): # Fonction pour récupérer les tweets
    #Génère un identifiant unique basé sur la date et le temps pour retrouvé les tweets scraper par une requête en particulier
    req_id = datetime.now().strftime("%Y%m%d%H%M")

    # Enregistre la requête dans la base de données
    req_doc = {
        "req_id": req_id,
        "mot_cle": mot_cle,
        "date_fin": until_date,
        "date_debut": since_date,
        "nb_tweets": nb_tweets,
        "last_date_pulled": ""
    }

    req_collection.insert_one(req_doc)
    global processed_tweets  # Utiliser l'ensemble global
    proxies = open("./twittersearch/proxies.txt").read().splitlines() # Lire les proxies à partir du fichier proxies.txt pour ne pas être bloqué par Twitter
    # Initialiser le navigateur
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  #Pour lancer en arrière plan
    options.add_argument("--enable-javascript")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.3")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    bot = webdriver.Chrome(options=options)

    useragentarray = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    ]

    bot.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    login(bot) # Se connecter à Twitter

    # Recherche du mot clé
    search_url = f'https://twitter.com/search?q={mot_cle}%20until%3A{until_date}%20since%3A{since_date}&src=typed_query&f=live'
    bot.get(search_url)

    # Attendre que la page se charge
    time.sleep(5)

    max_scrolls = 20
    scroll_count = 0
    nombre_tweets = 0
    liste_tweets = []
    utilisateurs = []

    while nombre_tweets <= nb_tweets :
        
        soup = BeautifulSoup(bot.page_source, 'html.parser')
        tweet_elements = soup.find_all(attrs={'data-testid': 'tweet'}) # On récupère les tweets

        response_text = ""

        #Appel de la fonction qui permet de récupérer les tweets et toutes leurs informations. 
        nombre_tweets, response_text, liste_tweets, utilisateurs = scrap_tweets(tweet_elements, bot, search_url, mot_cle, nombre_tweets, nb_tweets, req_id, response_text, liste_tweets, utilisateurs)
                
        useragent = random.choice(useragentarray)
        bot.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragent}) # Changer l'user agent pour éviter d'être bloqué par Twitter

        if scroll_count % 5 == 0:
            options.add_argument("--proxy-server=%s" % proxies[scroll_count % 5])
        perform_scroll(bot)

        random_sleep()

        if scroll_count % 10 == 0:
            random_sleep()
            
        # print(f"Scroll count: {scroll_count}")
        scroll_count += 1  

    print(f"Nombre de tweets : {nombre_tweets}")
    
    # Récupérer les commentaires de chaque tweet et sauvegarder le tweet dans la base de données
    for tweet_instance, utilisateur in zip(liste_tweets, utilisateurs):
        comments, timelist = get_comment_tweet(bot, utilisateur, tweet_instance.identifiant, search_url, tweet_instance.text_tweet)
        tweet_instance.add_comment(comments, timelist)
        save_tweets(tweet_instance)

    

    print(f"Nombre de tweets : {nombre_tweets}")

    bot.quit()

    with open('twitter.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    return HttpResponse(response_text, content_type='text/plain')



from bson import json_util 
import json

def get_all_tweet(request): # Fonction pour récupérer tous les tweets
    tweets = tweet_collection.find()
    tweet_data = [json.loads(json_util.dumps(tweet)) for tweet in tweets]
    return JsonResponse(tweet_data, safe=False)

def get_tweet_by_reqid(request, req_id): # Fonction pour récupérer les tweets d'une requête
    tweets = tweet_collection.find({"req_id": req_id})
    tweet_data = [json.loads(json_util.dumps(tweet)) for tweet in tweets]
    return JsonResponse(tweet_data, safe=False)

def get_all_req(request): # Fonction pour récupérer toutes les requêtes
    reqs = req_collection.find()
    req_data = [json.loads(json_util.dumps(req)) for req in reqs]
    return JsonResponse(req_data, safe=False)