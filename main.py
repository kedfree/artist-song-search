from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    # Authroization string being encoded with base 64 encoding
    auth_string = client_id + ":" + client_secret
    # now encode with utf-8
    auth_bytes = auth_string.encode("utf-8")
    # now encode with base64
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    #^ will return some json data
    #now want to convert to python dict
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    # &limit=1 says to only give the first most popular result for that search
    # could do "&type=artist,track" (if wanted to do both)

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) ==0:
        print("No artist found :(")
        return None

    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def find_artists_top_songs():
    token = get_token()
    search = input("Enter your search: ")
    result = search_for_artist(token, {search})
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)

    print(f"Showing top songs of {result['name']}")
    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")


def main():
    find_artists_top_songs()

if __name__ == "__main__":
    main()