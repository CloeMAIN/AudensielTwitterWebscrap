from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options


def get_tweets(request, mot_cle):
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    # Create a new Chrome browser instance with the specified options
    bot = webdriver.Chrome(options=options)

    # Navigate to the login page
    bot.get('https://twitter.com/i/flow/login')

    # Wait for the email input field to be present
    username_input = WebDriverWait(bot, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'r-1yadl64'))
)
    username_input.send_keys('Koolashley21')

    # Wait for the "Suivant" button to be clickable
    button = bot.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-6koalj.r-16y2uox div.css-1dbjc4n.r-16y2uox.r-1jgb5lz.r-13qz1uu div:nth-child(6)')
# Perform actions on the button (e.g., click)
    button.click()


    # Wait for the password input field to be present
    password_input = WebDriverWait(bot, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-1dbjc4n.r-mk0yit.r-13qz1uu label > div > div input')))
            

 # class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu
    # Enter email and password
    
    password_input.send_keys('Ashleyaïsma2021')

    # Submit the form
    password_input.send_keys(Keys.RETURN)

    # Wait for some time to let the page load
    time.sleep(5)

     # Naviguer vers la page de recherche
    search_url = f'https://twitter.com/search?q={mot_cle}&src=typed_query'
    bot.get(search_url)

    
    time.sleep(20)

    # Définir le nombre maximum de défilements (ajustez selon vos besoins)
    max_scrolls = 50
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
        tweet_elements = soup.select('div.css-1dbjc4n span.css-901oao')

        # Ajouter les tweets à la liste
        tweets.extend([tweet.get_text() for tweet in tweet_elements])

        scroll_count += 1

    # Construire une réponse avec les tweets
    response_text = "\n".join(tweets)

    # Fermer le navigateur
    bot.quit()
    
   
    with open('twitter.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
        
    # Retourner le texte de réponse en tant qu'objet HttpResponse
    return HttpResponse(response_text, content_type='text/plain')

