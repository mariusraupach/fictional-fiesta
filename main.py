import os
import requests
from typing import List, Dict, Union


def query_database(api_key: str, database_id: str):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, headers=headers)
        return response.json()
    except:
        raise


def main():
    api_key = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    if not api_key:
        raise ValueError()
    if not database_id:
        raise ValueError()
    response = query_database(api_key, database_id)
    results: List[Dict[str, Union[str, float]]] = []
    for result in response.get("results", []):
        properties = result.get("properties", {})
        name = properties.get("Name", {}).get("title", [{}])[0].get("plain_text", "N/A")
        euro = properties.get("Euro", {}).get("number", "N/A")
        url = properties.get("URL", {}).get("url", "N/A")
        results.append({"Name": name, "Euro": euro, "URL": url})

    print(results)


if __name__ == "__main__":
    main()
