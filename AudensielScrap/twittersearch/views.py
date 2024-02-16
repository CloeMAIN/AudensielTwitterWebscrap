from django.http import HttpResponse
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import random
from django.shortcuts import render
from .models import tweet_collection,req_collection
#from playwright.sync_api import sync_playwright 
from playwright.async_api import async_playwright
import asyncio
from datetime import datetime
from django.http import JsonResponse
from bson.json_util import dumps
import asyncio
import aiohttp

from decouple import config
# Variables d'environnement pour stocker les identifiants Twitter
USER_ID = config('USER_ID')
USER_PASSWORD = config('USER_PASSWORD')
proxies = open("./twittersearch/proxies.txt").read().splitlines() # Lire les proxies à partir du fichier proxies.txt pour ne pas être bloqué par Twitter

# Ensemble pour stocker les identifiants des tweets traités
processed_tweets = set()

#fonction pour faire une pause aléatoire
def random_sleep():
    time.sleep(random.uniform(2, 5))
    
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

from playwright.async_api import async_playwright
async def login(page):
    await page.goto('https://twitter.com/i/flow/login')
    
    # Attendre que l'élément d'entrée de l'identifiant de l'utilisateur soit visible
    user_id_input = await page.wait_for_selector('.r-1yadl64', timeout=5000)
    await user_id_input.fill(USER_ID)

    # Cliquer sur le bouton de connexion
    login_button = await page.wait_for_selector('div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox div.css-175oi2r.r-16y2uox.r-1jgb5lz.r-13qz1uu div:nth-child(6)', timeout=5000)
    await login_button.click()

    # Attendre que l'élément d'entrée du mot de passe soit visible
    password_input = await page.wait_for_selector('div.css-175oi2r input[type="password"]', timeout=5000)
    await password_input.fill(USER_PASSWORD)
    
    # Appuyer sur la touche Entrée pour soumettre le formulaire
    await page.keyboard.press("Enter")

    # Faire une pause aléatoire
    random_sleep()

def save_tweets(tweets): # Fonction pour enregistrer les tweets dans la base de données
    element = tweets.to_dict()
    if tweet_collection.find_one({"identifiant": element["identifiant"]}): # Vérifier si l'élément existe déjà
        print("L'élément existe déjà")
        tweet_collection.update_one({"identifiant": element["identifiant"]},
                                     {"$set": {"nombre_views": element["nombre_views"],
                                               "nombre_likes": element["nombre_likes"],
                                               "nombre_reposts": element["nombre_reposts"],
                                               "nombre_replies": element["nombre_replies"],
                                                  "comment_tweet": element["comment_tweet"],
                                               }
                                      }, upsert=False)

    else:
        print("L'élément n'existe pas")
        tweet_collection.insert_one(element)
        
def get_new_proxy():
    # Lire les proxies à partir du fichier proxies.txt et en choisir un aléatoire
    return random.choice(proxies)

def change_proxy(page, new_proxy):
    # Changer le proxy ici
    page.set_extra_http_headers({"Proxy-Authorization": new_proxy})
    
        
async def perform_scroll(page):
    # Faire défiler la page
    await page.evaluate("window.scrollBy(0, window.innerHeight)")

    # Faire une pause aléatoire entre 2 et 5 secondes
    await page.wait_for_timeout(random.randint(2000, 5000))

    # Attendre que de nouveaux éléments de tweet soient chargés
    previous_last_tweet = (await page.query_selector_all('[data-testid="tweet"]'))[-1]
    await page.evaluate("window.scrollBy(0, window.innerHeight)")
    await page.wait_for_timeout(2000)  # Attendre un court instant
    new_last_tweet = (await page.query_selector_all('[data-testid="tweet"]'))[-1]

    if new_last_tweet != previous_last_tweet:
        print("Au moins un nouveau tweet a été chargé.")
        return True
    else:
        print("Aucun nouveau tweet n'a été chargé. Arrêt de l'extraction.")
        return False

       
async def fetch_comments(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_comment_tweet(bot, utilisateur, identifiant, search_url, tweet_text):
    tweet_url = f'https://twitter.com/{utilisateur}/status/{identifiant}'
    async with aiohttp.ClientSession() as session:
        async with session.get(tweet_url) as response:
            html_content = await response.text()

    # Votre logique d'extraction des commentaires ici
    comments = extract_comments(html_content, 10, tweet_text)
    print(f"Comments for tweet {identifiant}: {comments}")

    # Vous pouvez retourner les commentaires ou effectuer d'autres traitements ici
    return comments


async def extract_comments(page, num_comments, tweet_text):
    comments = set()

    # Scroll down to load comments
    for _ in range(num_comments // 5):
        await page.evaluate("window.scrollBy(0, window.innerHeight)")
        await asyncio.sleep(1)  # Wait for the comments to load
        
        # Extract comments
        soup = BeautifulSoup(await page.content(), 'html.parser')
        comment_elements = soup.find_all(attrs={'data-testid': 'tweet'})
        
        for comment in comment_elements:
            comment_text = comment.find(attrs={'data-testid': 'tweetText'})
            if comment_text is not None and comment_text.get_text(strip=True) != tweet_text:
                comment_text = comment_text.get_text(strip=True)
                comments.add(comment_text)
            else:
                continue
        await asyncio.sleep(1)  # Add a short delay before scrolling again

    return list(comments)



async def scrap_tweets(tweet_elements, mot_cle, nombre_tweets, nb_tweets, req_id, response_text, liste_tweets, utilisateurs):
    for tweet_element in  tweet_elements:
        tweet_div_text = tweet_element.find(attrs={'data-testid': 'tweetText'})
        if tweet_div_text is not None:
            tweet_text = tweet_div_text.get_text(strip=False)
        else:
            continue

        details = tweet_element.find_all(attrs={'data-testid': 'app-text-transition-container'})
        replies = details[0].get_text(strip=True)
        reposts = details[1].get_text(strip=True)
        likes = details[2].get_text(strip=True)
        views = details[3].get_text(strip=True) if len(details) >= 4 else ""

        user_info = tweet_element.find(attrs={'data-testid': 'User-Name'})
        user_info2 = user_info.find_all('a', href=True)
        user_info = user_info.find('time')
        date = user_info['datetime'][0:10]

        user_info2 = user_info2[2]['href']
        url_segments = user_info2.split("/")
        identifiant = url_segments[3]
        utilisateur = url_segments[1]

        if (mot_cle in tweet_text) and (nombre_tweets < nb_tweets) and (identifiant not in processed_tweets):
            if not tweet_collection.find_one({"identifiant": identifiant}):
                tweets_instance = DonneeCollectee(tweet_text, likes, reposts, replies, views, date, identifiant, req_id, [])
                liste_tweets.append(tweets_instance)
                utilisateurs.append(utilisateur)
                nombre_tweets += 1
                response_text += f"\n{identifiant}"
                processed_tweets.add(identifiant)
                print (f"Nombre de tweets : {nombre_tweets}")
                if nombre_tweets >= nb_tweets:
                    break

                save_tweets(tweets_instance)  # Appel de la fonction save_tweets

    return nombre_tweets, response_text, liste_tweets, utilisateurs



async def get_tweet_url(tweet_instance, utilisateur):
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            await login(page)  # Assurez-vous d'attendre que la connexion se termine

            await page.goto(f'https://twitter.com/{utilisateur}/status/{tweet_instance.identifiant}')

            await asyncio.sleep(3)  # Attendre 3 secondes pour que la page se charge complètement

            # Extraction des commentaires
            comments = await extract_comments(page, 10, tweet_instance.text_tweet)
            tweet_instance.comment_tweet = comments
            # Sauvegarde du tweet dans la base de données
            save_tweets(tweet_instance)
    except Exception as e:
        print(f"Une exception s'est produite lors de la récupération des données pour le tweet {tweet_instance.identifiant}: {e}")
    finally:
        if browser:
            await browser.close()  # Assurez-vous que le navigateur est fermé même en cas d'exception


    
    
import asyncio
from playwright.async_api import async_playwright

async def get_tweets(request, mot_cle, until_date, since_date, nb_tweets):
    try:
        # Génère un identifiant unique basé sur la date et le temps pour retrouver les tweets scraper par une requête en particulier
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

        start_time_total = datetime.now()

        browser = None  # Définir browser en dehors du bloc try/except pour garantir son existence

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            # Se connecter à Twitter
            await login(page)

            # Recherche du mot clé
            search_url = f'https://twitter.com/search?q={mot_cle}%20until%3A{until_date}%20since%3A{since_date}&src=typed_query&f=live'
            await page.goto(search_url)

            # Attendre que la page se charge
            await asyncio.sleep(5)

            max_scrolls = 20
            scroll_count = 0
            nombre_tweets = 0
            liste_tweets = []
            utilisateurs = []

            start_time_extraction = datetime.now() # Temps de début de l'extraction des tweets

            while((nombre_tweets <= nb_tweets) or (nb_tweets == 0)) :
                # Récupérer les éléments de tweet
                html_content = await page.content()
                # Utiliser BeautifulSoup pour analyser le contenu HTML
                soup = BeautifulSoup(html_content, 'html.parser')   
                # Ensuite, pour trouver les éléments de tweet, vous pouvez utiliser le sélecteur CSS correspondant :
                tweet_elements = soup.select('[data-testid="tweet"]')

                response_text = ""

                # Appel de la fonction qui permet de récupérer les tweets et toutes leurs informations
                nombre_tweets, response_text, liste_tweets, utilisateurs = await scrap_tweets(tweet_elements, mot_cle, nombre_tweets, nb_tweets, req_id, response_text, liste_tweets, utilisateurs)
                
                # Faire défiler la page
                if not await perform_scroll(page):
                    break  # Sortir de la boucle si aucun nouveau tweet est chargé
                if nombre_tweets >= nb_tweets:
                    print("Le nombre de tweets souhaité a été atteint.")
                    break
                random_sleep()

                scroll_count += 1  
                print(f"Scroll count: {scroll_count}")

            # Imprimer le nombre final de tweets insérés dans la base de données
            print(f"Nombre de tweets : {nombre_tweets}")


            end_time_extraction = datetime.now() # Temps de fin de l'extraction des tweets

            print(f"Temps d'extraction des tweets en minutes : {(end_time_extraction - start_time_extraction).seconds / 60}")

            # Récupérer les commentaires de chaque tweet et sauvegarder le tweet dans la base de données
            start_time_comments = datetime.now() # Temps de début de l'exécution de la fonction pour calculer le temps d'exécution

            tasks = []  # Liste pour stocker les tâches asyncio
            compteur = 0
            for (tweet_instance, utilisateur) in zip(liste_tweets, utilisateurs):
                compteur += 1
                #seulement si le tweet a au moins un commentaire
                if tweet_instance.nombre_replies > 0:
                    tasks.append(get_tweet_url(tweet_instance, utilisateur))
                    #je veux quon exécute nb_tweets bots en parallèle
                    if len(tasks) == 15:
                        await asyncio.gather(*tasks)
                        tasks = []
                    print(f"Le tweet {compteur} a des commentaires.")
                else:
                    print(f"Le tweet {compteur} n'a pas de commentaires.")
                    
            if len(tasks) > 0:
                await asyncio.gather(*tasks)
               

            end_time_comments = datetime.now() # Temps de fin de l'extraction des commentaires
            print(f"Temps d'extraction des commentaires en minutes : {(end_time_comments - start_time_comments).seconds / 60}")

            end_time_total = datetime.now() # Temps de fin de l'exécution de la fonction pour calculer le temps d'exécution
            print(f"Temps d'exécution total en minutes : {(end_time_total - start_time_total).seconds / 60}")
            print(f"Nombre de tweets : {nombre_tweets}")

    except Exception as e:
        print(f"Une exception s'est produite : {e}")

    finally:
        if browser:
            await browser.close() 

    # Récupérer les tweets de la base de données
    tweets = tweet_collection.find({"req_id": req_id})
    tweet_data = [json.loads(dumps(tweet)) for tweet in tweets]
    
    return JsonResponse(tweet_data, safe=False)




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

#foncton pour récupérer une requête par son id
def get_req_by_id(request, req_id):
    req = req_collection.find_one({"req_id": req_id})
    req_data = json.loads(json_util.dumps(req))
    return JsonResponse(req_data, safe=False)