from config import API_ID, API_KEY

headers = {
    "Authorization": f"apikey {API_ID}:{API_KEY}",
    "accept": "text/json"
}