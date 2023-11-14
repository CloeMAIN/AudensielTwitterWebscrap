from django.shortcuts import render

# twittersearch/views.py
from django.http import JsonResponse
import requests

def get_tweets(request, keyword):
    url = f'https://twitter.com/i/search/timeline?f=tweets&q={keyword}&src=typd'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Traitement des données, vous pouvez extraire les informations pertinentes ici
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to fetch tweets'}, status=500)
