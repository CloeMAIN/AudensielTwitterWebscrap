import bs4



def test():
    with open('AudensielScrap/data/twitterComment0.26257098476937135.html') as f:
        html = f.read()
    comments_set = set()  # Ensemble pour stocker les commentaires, éviter les doublons
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # Find all the comments
    commententaires = soup.find_all(attrs={'data-testid': 'tweet'})
    
    time_elements = soup.find_all('time')
    for time in time_elements:
        # get date inside the class
        print(time['datetime'][0:10])

    print(len(commententaires))
    print(len(time_elements))
    for comment, time in zip(commententaires, time_elements):
        comment_text = comment.find(attrs={'data-testid': 'tweetText'})
        print(time['datetime'][0:10], comment_text)
        if comment_text is not None : # On vérifie que le commentaire n'est pas le même que le tweet
            comment_text = comment_text.get_text(strip=True)
            comments_set.add(comment_text)  # Ajouter le commentaire à l'ensemble
        else:
            continue

    # print(comments_set)
    # for comment in comments_set:
    #     print(comment)
    #     print('---')

if __name__ == '__main__':
    test()