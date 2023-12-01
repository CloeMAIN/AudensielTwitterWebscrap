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
    button = bot.find_element(By.CSS_SELECTOR, ' div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox div.css-175oi2r.r-16y2uox.r-1jgb5lz.r-13qz1uu div:nth-child(6)')
    
    # Appuie sur le bouton 
    button.click()
    

    # Attends que la section où écrire le mdp soit présente et y écrire le mdp
    password_input = WebDriverWait(bot, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-175oi2r input[type="password"]')))
    password_input.send_keys('aMkiuzi77/P')
    password_input.send_keys(Keys.RETURN)
    #div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox div.css-175oi2r.r-16y2uox.r-1jgb5lz.r-13qz1uu.r-1ye8kvj div.css-175oi2r.r-1fq43b1.r-16y2uox.r-1wbh5a2.r-1dqxon3 div.css-175oi2r.r-mk0yit.r-13qz1uu div.css-175oi2r.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1wzrnnt.r-1udh08x.r-xd6kpl.r-1pn2ns4.r-ttdzmv > div.css-1rynq56.r-bcqeeo.r-qvutc0.r-37j5jr.r-135wba7.r-16dba41.r-1awozwy.r-6koalj.r-1inkyih.r-13qz1uu > input
    # Attends que la page se charge
    time.sleep(5)

     # Navigation page de recherche 
    search_url = f'https://twitter.com/search?q={mot_cle}&src=typed_query&f=live'
    bot.get(search_url)

     # Attends que la page se charge
    time.sleep(20)

    # Définissez le nombre maximum de défilements 
    max_scrolls = 10  # Par exemple, 10 sections pour le défilement progressif
    scroll_count = 0
    nombre_tweets = 0
    # Collecter les tweets
    tweets = []

    while scroll_count < max_scrolls:
        # Définissez la hauteur totale de la page
        page_height = bot.execute_script("return document.body.scrollHeight")

        # Définissez le nombre de sections que vous souhaitez
        num_sections = 10
        section_height = page_height // num_sections

        # Faites défiler chaque section à la fois
        for i in range(num_sections):
            bot.execute_script(f"window.scrollTo(0, {i * section_height});") # Défilement progressif de la page : 10 sections de 10% de la page à chaque fois et on récupère les tweets à chaque fois pour ne pas être bloqué par le site
            
            # Attendre un court délai pour le chargement
            time.sleep(2)

            # Extraire le contenu de la page avec BeautifulSoup
            soup = BeautifulSoup(bot.page_source, 'html.parser')

            # Trouver les tweets grâce au data-testid spécifique
            tweet_elements = soup.find_all(attrs={'data-testid': 'tweet'})

            # Iterate through each tweet element
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

    # Retourner le texte de réponse en tant qu'objet HttpResponse
    return HttpResponse(response_text, content_type='text/plain')