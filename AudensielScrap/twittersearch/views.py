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
from .models import tweet_collection

# Global set to store processed tweet identifiers
processed_tweets = set()

class DonneeCollectee:
    
    def __init__(self, text_tweet, nombre_likes, nombre_reposts, nombre_replies, nombre_views, date_tweet, identifiant_tweet, comment_tweet=None):
        self.text_tweet = text_tweet
        self.date_tweet = date_tweet
        self.identifiant = int(identifiant_tweet)
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

    def convert_number(self, value):
        if value[-1] == "K":
            return int(float(value[:-1]) * 1000)
        elif value[-1] == "M":
            return int(float(value[:-1]) * 1000000)
        else:
            return int(value)

    def add_comment(self,comment):
        self.comment_tweet.append(comment)  

    def to_dict(self):
        return {
            "text_tweet": self.text_tweet,
            "nombre_likes": self.nombre_likes,
            "nombre_reposts": self.nombre_reposts,
            "nombre_replies": self.nombre_replies,
            "nombre_views": self.nombre_views,
            "date_tweet": self.date_tweet,
            "identifiant": self.identifiant,
            "comment_tweet": self.comment_tweet
        }

def login(bot):
    bot.get('https://twitter.com/i/flow/login')

    username_input = WebDriverWait(bot, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'r-1yadl64'))
    )
    username_input.send_keys('@UserNumber59901')

    button = bot.find_element(By.CSS_SELECTOR, 'div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox div.css-175oi2r.r-16y2uox.r-1jgb5lz.r-13qz1uu div:nth-child(6)')
    button.click()

    password_input = WebDriverWait(bot, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-175oi2r input[type="password"]')))
    password_input.send_keys('aMkiuzi77/P')
    password_input.send_keys(Keys.RETURN)

    time.sleep(random.uniform(2, 5))




""" def get_comment_tweet(bot, utilisateur, identifiant, search_url):
    tweet_url = f'https://twitter.com/{utilisateur}/status/{identifiant}'
    bot.get(tweet_url)

    time.sleep(5)

    comment_elements = bot.find_elements(By.XPATH, '//div[@data-testid="tweet"]//div[@data-testid="reply"]')[:10]

    comments_text = []
    for comment_element in comment_elements:
        comment_text = comment_element.text
        comments_text.append(comment_text)

    tweet_data = DonneeCollectee("", "", "", "", "", "", "")
    for comment_text in comments_text:
        tweet_data.add_comment(comment_text)

    bot.get(search_url)
    random_sleep()
 """
def save_tweets(tweets):
    element = tweets.to_dict()

    if tweet_collection.find_one({"identifiant": element["identifiant"]}):
        print("L'élément existe déjà")
        tweet_collection.update_one({"identifiant": element["identifiant"]},
                                     {"$set": {"nombre_views": element["nombre_views"],
                                               "nombre_likes": element["nombre_likes"],
                                               "nombre_reposts": element["nombre_reposts"],
                                               "nombre_replies": element["nombre_replies"],
                                               "comment_tweet": element["comment_tweet"]
                                               }
                                      }, upsert=False)

    else:
        print("L'élément n'existe pas")
        tweet_collection.insert_one(element)


def random_sleep():
    time.sleep(random.uniform(2, 5))

def perform_scroll(bot):
    page_height = bot.execute_script("return document.body.scrollHeight")
    bot.execute_script(f"window.scrollTo(0, {page_height/2});")
    random_sleep()
    bot.execute_script(f"window.scrollTo({page_height/2}, {page_height});")
    random_sleep()



def get_comment_tweet(bot, utilisateur, identifiant, search_url, tweet_text):
    tweet_url = f'https://twitter.com/{utilisateur}/status/{identifiant}'
    bot.get(tweet_url)

    time.sleep(5)

    scroll_position_before_click = bot.execute_script("return window.scrollY;")
    # Wait for the comments section to load
    WebDriverWait(bot, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"] [data-testid="tweetText"]')))
    # Extract comments from the individual tweet page here
    comments = extract_comments(bot, 10, tweet_text)
    print(f"Comments for tweet {identifiant}: {comments}")

    bot.get(search_url)
    random_sleep()
    bot.execute_script(f"window.scrollTo(0, {scroll_position_before_click});")
    random_sleep()
    return comments

def extract_comments(bot, num_comments, tweet_text):
    comments = set()  # Using a set to avoid duplicates

    # Scroll to load additional comments if necessary
    for _ in range(num_comments // 5):  # Assuming 5 comments load with each scroll
        # faire un scroll
        page_height = bot.execute_script("return document.body.scrollHeight")
        bot.execute_script(f"window.scrollTo(0, {page_height/2});")
        soup = BeautifulSoup(bot.page_source, 'html.parser')
        commententaires = soup.find_all(attrs={'data-testid': 'tweet'})
        
        for comment in commententaires:
            comment_text = comment.find(attrs={'data-testid': 'tweetText'})
            if comment_text is not None and comment_text.get_text(strip=True) != tweet_text:
                comment_text = comment_text.get_text(strip=True)
                comments.add(comment_text)  # Use add() to add unique comments to the set
            else:
                continue
        random_sleep()

    return list(comments)  # Convert set back to a list



def get_tweets(request, mot_cle, until_date, since_date, nb_tweets):
    global processed_tweets  # Utiliser l'ensemble global
    proxies = open("./twittersearch/proxies.txt").read().splitlines()

    options = webdriver.ChromeOptions()

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

    login(bot)

    search_url = f'https://twitter.com/search?q={mot_cle}%20until%3A{until_date}%20since%3A{since_date}&src=typed_query&f=live'
    bot.get(search_url)

    time.sleep(10)

    max_scrolls = 20
    scroll_count = 0
    nombre_tweets = 0

    while nombre_tweets <= nb_tweets :
        
        soup = BeautifulSoup(bot.page_source, 'html.parser')
        tweet_elements = soup.find_all(attrs={'data-testid': 'tweet'})

        response_text = ""

        for tweet_element in tweet_elements:
            tweet_div_text = tweet_element.find(attrs={'data-testid': 'tweetText'})
            if tweet_div_text is not None:
                tweet_text = tweet_div_text.get_text(strip= False)
            else:
                continue

            details = tweet_element.find_all(attrs={'data-testid': 'app-text-transition-container'})
            replies = details[0].get_text(strip=True)
            reposts = details[1].get_text(strip=True)
            likes = details[2].get_text(strip=True)

            # Make sure there are at least 4 items in details before trying to access index 3
            views = details[3].get_text(strip=True) if len(details) >= 4 else ""

            user_info = tweet_element.find(attrs={'data-testid': 'User-Name'})
            user_info2 = user_info.find_all('a', href=True)
            user_info = user_info.find('time')
            date = user_info['datetime'][0:10]

            user_info2 = user_info2[2]['href']
            url_segments = user_info2.split("/")
            identifiant = url_segments[3]
            utilisateur = url_segments[1]

            if mot_cle in tweet_text and nombre_tweets <= nb_tweets:
                scroll_position_before_click = bot.execute_script("return window.scrollY;")
                comments = get_comment_tweet(bot, utilisateur, identifiant, search_url, tweet_text)
                tweets_instance = DonneeCollectee(tweet_text, likes, reposts, replies, views, date, identifiant, comments)
                # Save the tweet with comments to the database
                save_tweets(tweets_instance)

                nombre_tweets += 1
                response_text += ("\n" + str(identifiant))

                processed_tweets.add(identifiant)  # Ajouter l'identifiant du tweet traité à l'ensemble
                
        useragent = random.choice(useragentarray)
        bot.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragent})

        if scroll_count % 5 == 0:
            options.add_argument("--proxy-server=%s" % proxies[scroll_count % 5])
        perform_scroll(bot)

        random_sleep()

        if scroll_count % 10 == 0:
            time.sleep(10)
            
        print(f"Scroll count: {scroll_count}")
        scroll_count += 1

    print(f"Nombre de tweets : {nombre_tweets}")

    bot.quit()

    with open('twitter.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    return HttpResponse(response_text, content_type='text/plain')


