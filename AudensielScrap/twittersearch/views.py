from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options
import re

#installer selenium webdriver beautifulsoup4 
# ex de requête : GET http://localhost:8000/api/search/taylor/
def get_tweets(request, mot_cle):
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    # Creation Chrome browser : connexion automatique
    bot = webdriver.Chrome(options=options)

    # Navigation page login
    bot.get('https://twitter.com/i/flow/login')

    # Attends que la section où écrire le mail soit présente
    username_input = WebDriverWait(bot, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'r-1yadl64'))
)
    username_input.send_keys('@UserNumber59901')

    # Attends qu'on puisse apppuyé sur le bouton suivant 
    button = bot.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-6koalj.r-16y2uox div.css-1dbjc4n.r-16y2uox.r-1jgb5lz.r-13qz1uu div:nth-child(6)')
    # Appuie sur le bouton 
    button.click()
    
    # # Vérification si le message de vérification apparaît
    # try:
    #     username_input = WebDriverWait(bot, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, 'r-1yadl64')))
        
    #     # Si le message apparaît, remplir le champ avec le nom d'utilisateur
    #     username = "@UserNumber59901"  # Remplacez ceci par votre nom d'utilisateur
    #     username_input.send_keys(username)
    #     # Cliquez sur le bouton "Suivant"
    #     button = bot.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1m3jxhj.r-sdzlij.r-1phboty.r-rs99b7.r-19yznuf r-64el8z r-icoktb r-1ny4l3l r-1dye5f7 r-o7ynqc r-6416eg r-lrvibr')
    #     button.click()
    
    # except TimeoutException:
    #     pass

     # Attends que la section où écrire le mdp soit présente et y écrire le mdp
    password_input = WebDriverWait(bot, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-1dbjc4n.r-mk0yit.r-13qz1uu label > div > div input')))
    password_input.send_keys('aMkiuzi77/P')
    password_input.send_keys(Keys.RETURN)

    # Attends que la page se charge
    time.sleep(5)

     # Navigation page de recherche 
    search_url = f'https://twitter.com/search?q={mot_cle}&src=typed_query'
    bot.get(search_url)

     # Attends que la page se charge
    time.sleep(20)

    # Définir le nombre maximum de défilements 
    max_scrolls = 5
    scroll_count = 0

    # Collecter les tweets
    tweets = []

   
    
 
    while scroll_count < max_scrolls:
        # Faire défiler la page
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Attendre un court délai pour le chargement
        time.sleep(2)

        # Extraire le contenu de la page avec BeautifulSoup
        soup = BeautifulSoup(bot.page_source, 'html.parser')
       
        #Mettre la page dans un fichier html  : rajouter dans le fichier html pas ecraser le fichier
        with open('page.html', 'a', encoding='utf-8') as file:
            file.write(soup.prettify())
            
    # Construire une réponse avec les tweets
  

    # Fermer le navigateur
    bot.quit()
    file.close()
    return HttpResponse(soup.prettify())

