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
from .models import TweetModele

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
    time.sleep(random.uniform(2, 5))


#Fonction pour enregistrer les tweets dans la base de données MongoDB
def save_tweets(tweets):
    for tweet in tweets:
        tweet_modele = TweetModele()
        tweet_modele.text = tweet
        tweet_modele.save()


# Fonction principale
def get_tweets(request, mot_cle, until_date, since_date):
    proxies = open("./twittersearch/proxies.txt").read().splitlines()
    
    options = webdriver.ChromeOptions()
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
    search_url = f'https://twitter.com/search?q={mot_cle}%20until%{until_date}%20since%{since_date}&src=typed_query&f=live'
    bot.get(search_url)

    # Attendre que la page se charge
    time.sleep(20)

    # Définir le nombre maximum de défilements
    max_scrolls = 10  # Par exemple, 100 scrolls
    scroll_count = 0
    nombre_tweets = 0
    tweets = []

    while scroll_count < max_scrolls:
        
         # Randomly selecting a user agent
        useragent = random.choice(useragentarray)
    
        bot.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragent})
        
        options.add_argument("--proxy-server=%s" % random.choice(proxies))
        
        perform_scroll(bot)

        # Ajouter une pause aléatoire
        random_sleep()

        # Extraire le contenu de la page avec BeautifulSoup
        soup = BeautifulSoup(bot.page_source, 'html.parser')

        # Trouver les tweets grâce au data-testid spécifique
        tweet_elements = soup.find_all(attrs={'data-testid': 'tweet'})

        for tweet_element in tweet_elements:
            tweet_div_text = tweet_element.find(attrs={'data-testid': 'tweetText'})
            if tweet_div_text is not None:
                tweet_text = tweet_div_text.get_text(strip=True)
            else:
                continue

            details_tweet = tweet_element.find('div', {'aria-label': True})
            details_tweet_str = str(details_tweet)

            pattern = r'(\d+)\s+(\w+)'
            matches = re.findall(pattern, details_tweet_str)
            matches_str = [f"{match[0]} {match[1]}" for match in matches]

            if mot_cle in tweet_text:
                tweets.append(tweet_text)
                tweets.extend(matches_str)
                nombre_tweets += 1

        print(f"Scroll count: {scroll_count}")
        scroll_count += 1

    print(f"Nombre de tweets : {nombre_tweets}")
    # Construire une réponse avec les tweets
    response_text = "\n".join(tweets)

    # Fermer le navigateur
    bot.quit()

    with open('twitter.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    # Enregistrer les tweets dans la base de données MongoDB
    save_tweets(response_text.split('\n'))

    # Retourner le texte de réponse en tant qu'objet HttpResponse
    return HttpResponse(response_text, content_type='text/plain')


