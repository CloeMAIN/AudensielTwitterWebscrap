from django.http import JsonResponse
import requests

def twittersearch(request, keyword):
    base_url = 'https://twitter.com/search?q='
    search_url = f'{base_url}{keyword}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36',
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        # Check if the response contains the expected data
        if 'content-type' in response.headers and 'text/html' in response.headers['content-type']:
            # Process the content if needed
            # For example, you can use BeautifulSoup for HTML parsing

            # Return a JSON response with the content of the page
            return JsonResponse({'content': response.text})
        else:
            # Return an error response if the content type is not as expected
            return JsonResponse({'error': 'Unexpected content type'}, status=500)

    except requests.HTTPError as e:
        return JsonResponse({'error': f"HTTPError: {str(e)}"}, status=500)
    except requests.RequestException as e:
        return JsonResponse({'error': f"RequestException: {str(e)}"}, status=500)
    except Exception as e:
        return JsonResponse({'error': f"Error: {str(e)}"}, status=500)