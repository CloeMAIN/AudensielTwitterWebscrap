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
    
    #options.add_argument("--headless")  Pour lancer en arrière plan
    options.add_argument("--enable-javascript")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.3")
    
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
