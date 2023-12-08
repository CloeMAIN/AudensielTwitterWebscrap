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
import re
from django.shortcuts import render
from .models import tweet_collection


# Classe pour stocker les données collectées afin de pouvoir les enregistrer dans la base de données MongoDB
class DonneeCollectee:
    def __init__(self, text_tweet, nombre_likes, nombre_reposts, nombre_replies, nombre_views, date_tweet, identifiant_tweet):
        self.text_tweet = text_tweet
        self.date_tweet = date_tweet
        self.identifiant = int(identifiant_tweet)
        if (nombre_likes == ""):
            self.nombre_likes = 0
        else:
            if (nombre_likes[-1] == "K"): # Si le nombre de likes est exprimé en milliers
                self.nombre_likes = int(float(nombre_likes[:-1]) * 1000)
            elif (nombre_likes[-1] == "M"): # Si le nombre de likes est exprimé en millions
                self.nombre_likes = int(float(nombre_likes[:-1]) * 1000000)
            else:
                self.nombre_likes = int(nombre_likes)
        
        if (nombre_reposts == ""):
            self.nombre_reposts = 0
        else:
            if (nombre_reposts[-1] == "K"):
                self.nombre_reposts = int(float(nombre_reposts[:-1]) * 1000)
            elif (nombre_reposts[-1] == "M"):
                self.nombre_reposts = int(float(nombre_reposts[:-1]) * 1000000)
            else:
                self.nombre_reposts = int(nombre_reposts)
        
        if (nombre_replies == ""):
            self.nombre_replies = 0
        else:
            if (nombre_replies[-1] == "K"):
                self.nombre_replies = int(float(nombre_replies[:-1]) * 1000)
            elif (nombre_replies[-1] == "M"):
                self.nombre_replies = int(float(nombre_replies[:-1]) * 1000000)
            else:
                self.nombre_replies = int(nombre_replies)
        
        if (nombre_views == ""):
            self.nombre_views = 0
        else:
            if (nombre_views[-1] == "K"):
                self.nombre_views = int(float(nombre_views[:-1]) * 1000)
            elif (nombre_views[-1] == "M"):
                self.nombre_views = int(float(nombre_views[:-1]) * 1000000)
            else:
                self.nombre_views = int(nombre_views)

        

    def to_dict(self):
        return {
            "text_tweet": self.text_tweet,
            "nombre_likes": self.nombre_likes,
            "nombre_reposts": self.nombre_reposts,
            "nombre_replies": self.nombre_replies,
            "nombre_views": self.nombre_views,
            "date_tweet": self.date_tweet,
            "identifiant": self.identifiant
        }

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
    
# Fonction pour effectuer un scroll
def perform_scroll(bot):
    # Définissez la hauteur totale de la page
    page_height = bot.execute_script("return document.body.scrollHeight")

    # Faites défiler petit à petit la page jusqu'à la fin et ajoutez une pause aléatoire
    bot.execute_script(f"window.scrollTo(0, {page_height/2});")
    random_sleep()
    bot.execute_script(f"window.scrollTo({page_height/2}, {page_height});")

    # Attendre un court délai pour le chargement après le scroll
    random_sleep()


#Fonction pour enregistrer les tweets dans la base de données MongoDB
def save_tweets(tweets):
    element = tweets.to_dict()
    # Vérifier si un élément existe avec la valeur spécifique du champ identifiant
    # print('identifiant : ', tweets.identifiant)
    # print(tweet_collection.find_one({"text_tweet": tweets.text_tweet}))
    if tweet_collection.find_one({"identifiant": element["identifiant"]}):
        print("L'élément existe déjà")
        # Si l'élément existe, mettre à jour les valeurs des champs
        tweet_collection.update_one({"identifiant": element["identifiant"]},
                                     {"$set": {"nombre_views" : element["nombre_views"],
                                               "nombre_likes" : element["nombre_likes"],
                                               "nombre_reposts" : element["nombre_reposts"],
                                               "nombre_replies" : element["nombre_replies"],
                                               }
                                      }, upsert=False)
        
    else:
        print("L'élément n'existe pas")
        tweet_collection.insert_one(element)


# Fonction principale
def get_tweets(request, mot_cle, until_date, since_date):

    # On vide la base de données avant de commencer la collecte
    # tweet_collection.delete_many({})

    proxies = open("./twittersearch/proxies.txt").read().splitlines()

    options = webdriver.ChromeOptions()
    
    options.add_argument("--headless") 
    options.add_argument("--enable-javascript")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    
    # Ajouter des options pour éviter la détection automatisée
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False) 
    
    # Création du navigateur Chrome
    bot = webdriver.Chrome(options=options)

    # Initializing a list with two Useragents 
    useragentarray = [ 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
    ]

    bot.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    
    
    # Effectuer le login
    login(bot)

    # Navigation page de recherche
    search_url = f'https://twitter.com/search?q={mot_cle}%20until%3A{until_date}%20since%3A{since_date}&src=typed_query&f=live'
    bot.get(search_url)

    # Attendre que la page se charge
    time.sleep(20)

    # Définir le nombre maximum de défilements
    max_scrolls = 20 # Par exemple, 100 scrolls
    scroll_count = 0
    nombre_tweets = 0
    tweets = []

    while nombre_tweets < 1:
        
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
            user_info2 = user_info2[2]['href']
            identifiant = user_info2.split("/")[3]
            # print(identifiant)

            if mot_cle in tweet_text:
                save_tweets(DonneeCollectee(tweet_text, likes, reposts, replies, views, date, identifiant))
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


