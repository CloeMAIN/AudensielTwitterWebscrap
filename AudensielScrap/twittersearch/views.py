from django.http import HttpResponse, JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import random
import re
from django.shortcuts import render
#from .models import tweet_collection
from .models import DonneeCollectee
#add library for creating unique id
from datetime import datetime
from django.http import JsonResponse

<<<<<<< Updated upstream
=======
from decouple import config
# Variables d'environnement pour stocker les identifiants Twitter
USER_ID = config('USER_ID')
USER_PASSWORD = config('USER_PASSWORD')
>>>>>>> Stashed changes

# Classe pour stocker les données collectées afin de pouvoir les enregistrer dans la base de données MongoDB


def convert_number(number):
    if number:
        
        if number.endswith('K'):
            return int(float(number[:-1]) * 1000)
        elif number.endswith('M'):
            return int(float(number[:-1]) * 1000000)
        else:
            return int(number)
    else:
        return 0
    

# Fonction pour effectuer le login
def login(bot):
    # Navigation page login
    bot.get('https://twitter.com/i/flow/login')

    # Attends que la section où écrire le mail soit présente
    username_input = WebDriverWait(bot, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'r-1yadl64'))
    )
    username_input.send_keys('@UserNumber59901')

    # Attends qu'on puisse appuyer sur le bouton suivant
    button = bot.find_element(By.CSS_SELECTOR, 'div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox div.css-175oi2r.r-16y2uox.r-1jgb5lz.r-13qz1uu div:nth-child(6)')

    # Appuie sur le bouton
    button.click()

    # Attends que la section où écrire le mdp soit présente et y écrire le mdp
    password_input = WebDriverWait(bot, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-175oi2r input[type="password"]')))
    password_input.send_keys('aMkiuzi77/P')
    password_input.send_keys(Keys.RETURN)

    # Attendre un court délai pour le chargement après le login
    time.sleep(random.uniform(2, 5))

def random_sleep():
    time.sleep(random.uniform(2, 5))
    
<<<<<<< Updated upstream
# Fonction pour effectuer un scroll
def perform_scroll(bot):
    # Définissez la hauteur totale de la page
=======
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

        self.comment_tweet = comment_tweet if comment_tweet is not None else []

    def convert_number(self, value): # Convertir les nombres en entiers
        if value[-1] == "K":
            return int(float(value[:-1]) * 1000)
        elif value[-1] == "M":
            return int(float(value[:-1]) * 1000000)
        else:
            return int(value)

    def add_comment(self,comment): # Ajouter un commentaire à la liste des commentaires
        self.comment_tweet.append(comment)  

    def to_dict(self): # Convertir l'objet en dictionnaire
        return {
            "text_tweet": self.text_tweet,
            "nombre_likes": self.nombre_likes,
            "nombre_reposts": self.nombre_reposts,
            "nombre_replies": self.nombre_replies,
            "nombre_views": self.nombre_views,
            "date_tweet": self.date_tweet,
            "identifiant": self.identifiant,
            "comment_tweet": self.comment_tweet,
            "req_id": self.req_id
        }

def login(bot): # Fonction pour se connecter à Twitter
    bot.get('https://twitter.com/i/flow/login')

    username_input = WebDriverWait(bot, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'r-1yadl64'))
    )
    username_input.send_keys(USER_ID)

    button = bot.find_element(By.CSS_SELECTOR, 'div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox div.css-175oi2r.r-16y2uox.r-1jgb5lz.r-13qz1uu div:nth-child(6)')
    button.click() # Click the login button

    password_input = WebDriverWait(bot, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-175oi2r input[type="password"]')))
    password_input.send_keys(USER_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    random_sleep()
    


def save_tweets(tweets): # Fonction pour enregistrer les tweets dans la base de données
    element = tweets.to_dict()

    if tweet_collection.find_one({"identifiant": element["identifiant"]}): # Vérifier si l'élément existe déjà
        print("L'élément existe déjà")
        tweet_collection.update_one({"identifiant": element["identifiant"]},
                                     {"$set": {"nombre_views": element["nombre_views"],
                                               "nombre_likes": element["nombre_likes"],
                                               "nombre_reposts": element["nombre_reposts"],
                                               "nombre_replies": element["nombre_replies"]
                                               }
                                      }, upsert=False)

    else:
        print("L'élément n'existe pas")
        tweet_collection.insert_one(element)


def perform_scroll(bot): # Fonction pour faire défiler la page
>>>>>>> Stashed changes
    page_height = bot.execute_script("return document.body.scrollHeight")

    # Faites défiler petit à petit la page jusqu'à la fin et ajoutez une pause aléatoire
    bot.execute_script(f"window.scrollTo(0, {page_height/2});")
    random_sleep()
    bot.execute_script(f"window.scrollTo({page_height/2}, {page_height});")

    # Attendre un court délai pour le chargement après le scroll
    random_sleep()


#Fonction pour enregistrer les tweets dans la base de données MongoDB
def save_tweets(donnee):
    existing_tweet = DonneeCollectee.objects(identifiant=donnee.identifiant).first()
    if existing_tweet:
        # Si l'élément existe, mettre à jour les valeurs des champs
        existing_tweet.update(set__nombre_views=donnee.nombre_views)
    else:
        donnee.save()
        

def get_comment_tweet(bot, utilisateur, identifiant, search_url, scroll_position_before_click):
    tweet_url = f'https://twitter.com/{utilisateur}/status/{identifiant}'  
    bot.get(tweet_url)

     # Attendre que la page se charge 
    time.sleep(5)
        
    # Extraire les commentaires de la page du tweet individuel
               
    # ajouter à liste de commentaires

    # Revenir à la page de recherche au niveau du scroll où on était
    bot.get(search_url)
    random_sleep()
    bot.execute_script(f"window.scrollTo(0, {scroll_position_before_click});")
    random_sleep()

# Fonction principale

"""
ATTENTION
Voir si c'est possible de changer la fonction get_tweets en asynchrone
Frontend ne reçoit de réponse que quand la fonction a fini d'éxecuter
"""
def get_tweets(request, mot_cle, until_date, since_date):
    #Génère un id unique par rapport à la requête faite
    req_id = datetime.now().strftime("%Y%m%d%H%M")
    # On vide la base de données avant de commencer la collecte
    # tweet_collection.delete_many({})

    proxies = open("./twittersearch/proxies.txt").read().splitlines()

    options = webdriver.ChromeOptions()
<<<<<<< Updated upstream
    
    #options.add_argument("--headless")  Pour lancer en arrière plan
=======

    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems


>>>>>>> Stashed changes
    options.add_argument("--enable-javascript")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.3")
    
    # Ajouter des options pour éviter la détection automatisée
    options.add_argument("--disable-blink-features=AutomationControlled")
<<<<<<< Updated upstream
    
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False) 
    
    # Création du navigateur Chrome
    bot = webdriver.Chrome(options=options)
=======
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    bot = webdriver.Chrome(options)
>>>>>>> Stashed changes

    # Initializing a list with two Useragents 
    useragentarray = [ 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
    ]
<<<<<<< Updated upstream

    bot.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    
    
    # Effectuer le login
    login(bot)
=======
    # Wait until the page is fully loaded
    print("Ouverture webdriver")
    WebDriverWait(bot, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print("body appeared completly")
    bot.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
>>>>>>> Stashed changes

    # Navigation page de recherche
    search_url = f'https://twitter.com/search?q={mot_cle}%20until%3A{until_date}%20since%3A{since_date}&src=typed_query&f=live'
    bot.get(search_url)

    # Attendre que la page se charge
    time.sleep(10)

    # Définir le nombre maximum de défilements
    max_scrolls = 3 
    scroll_count = 0
    nombre_tweets = 0
    tweets = []

    while scroll_count< max_scrolls:
        
         # Randomly selecting a user agent
        useragent = random.choice(useragentarray)
    
        bot.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragent})
        
        # change proxy tous les 5 scrolls 
        if scroll_count % 5 == 0:
            options.add_argument("--proxy-server=%s" % proxies[scroll_count % 5])
        perform_scroll(bot)

        # Ajouter une pause aléatoire
        random_sleep()

        if scroll_count % 10 == 0:
            time.sleep(10)

        # Extraire le contenu de la page avec BeautifulSoup
        soup = BeautifulSoup(bot.page_source, 'html.parser')

        # Trouver les tweets grâce au data-testid spécifique
        tweet_elements = soup.find_all(attrs={'data-testid': 'tweet'})

        response_text = ""

        for tweet_element in tweet_elements:
            tweet_div_text = tweet_element.find(attrs={'data-testid': 'tweetText'})
            if tweet_div_text is not None:
                tweet_text = tweet_div_text.get_text(strip=True) 
            else:
                continue

            #On récupère les détails du tweet
            details = tweet_element.find_all(attrs={'data-testid': 'app-text-transition-container'})
            replies = details[0].get_text(strip=True)
            reposts = details[1].get_text(strip=True)
            likes = details[2].get_text(strip=True)
            views = details[3].get_text(strip=True)

            #On récupère la date du tweet
            user_info = tweet_element.find(attrs={'data-testid' : 'User-Name'})
            user_info2 = user_info.find_all('a', href=True)
            user_info = user_info.find('time')
            date = user_info['datetime'][0:10]

            #On récupère l'identifiant du tweet
            user_info2 = user_info2[2]['href']
            url_segments = user_info2.split("/")
            identifiant = url_segments[3]
            utilisateur = url_segments[1]

            # print(identifiant)

            if mot_cle in tweet_text:
                scroll_position_before_click = bot.execute_script("return window.scrollY;")
                donnee = DonneeCollectee(
                    text_tweet=tweet_text,
                    nombre_likes=convert_number(likes),
                    nombre_reposts=convert_number(reposts),
                    nombre_replies=convert_number(replies),
                    nombre_views=convert_number(views),
                    date_tweet=date,
                    identifiant=identifiant,
                    req_id=req_id
                )
                get_comment_tweet(bot, utilisateur, identifiant, search_url, scroll_position_before_click)
                save_tweets(donnee)
                nombre_tweets += 1
                response_text += ("\n" + str(identifiant))

        print(f"Scroll count: {scroll_count}")
        scroll_count += 1

    print(f"Nombre de tweets : {nombre_tweets}")

    # Fermer le navigateur
    bot.quit()

    with open('twitter.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    
    # Retourner le texte de réponse en tant qu'objet HttpResponse
    return HttpResponse(response_text, content_type='text/plain')



def get_dbreq_tweet(request, req_id):
    # Récupère les tweets avec le req_id correspondant de la base de données
    tweets = DonneeCollectee.objects(req_id=req_id)

    # Convertir les tweets en un format qui peut être renvoyé en réponse
    tweets_data = [tweet.to_mongo().to_dict() for tweet in tweets]

    # Renvoyer les données des tweets en tant que réponse JSON
    return JsonResponse(tweets_data, safe=False)
