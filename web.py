import requests
import os


BING_API_KEY = os.getenv("BING_API_KEY")


def search(query):

    endpoint = "https://api.bing.microsoft.com/v7.0/search"


    headers = {
        "Ocp-Apim-Subscription-Key": BING_API_KEY
    }


    params = {

        "q": query,
        "textDecorations": True,
        "textFormat": "HTML",
        "count": 5

    }


    response = requests.get(
        endpoint,
        headers=headers,
        params=params
    )


    if response.status_code != 200:

        return f"API Error: {response.text}"


    data = response.json()


    results = []


    for item in data.get("webPages", {}).get("value", []):


        title = item.get("name")

        snippet = item.get("snippet")

        url = item.get("url")


        results.append(

            f"""
### {title}

{snippet}

🔗 {url}

---
            """

        )


    return "\n".join(results)