import requests

def google_image_search(query, api_key, cse_id, num=6):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": cse_id,
        "key": api_key,
        "searchType": "image",
        "num": num
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        return []
