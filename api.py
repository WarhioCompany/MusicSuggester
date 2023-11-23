from api_requets import get_request

spotify_api_url = 'spotify23.p.rapidapi.com'

current_key = 0
keys = [
    "d9e1c630d5msh09b2e09c2748e73p13b4c4jsnd78cb5044a29"
]


def make_header(host):
    global current_key
    header = {
        'X-RapidAPI-Key': keys[current_key],
        'X-RapidAPI-Host': host
    }
    current_key = (current_key + 1) % len(keys)
    return header


def make_url(host, endpoint):
    return f"https://{host}/{endpoint}/"


def search(query):
    url = make_url(spotify_api_url, 'search')
    headers = make_header(spotify_api_url)
    args = {
        'q': query,
        'type': 'multi',
    }
    print('Sending request...')
    data = get_request(url, args, headers)

    print('Got Response!')
    print(data)
    result = data['tracks']['items'] + data['albums']['items']
    return result


def get_radio_uri(uri):
    print(uri)
    url = make_url(spotify_api_url, 'seed_to_playlist')
    headers = make_header(spotify_api_url)
    args = {
        'uri': uri
    }
    data = get_request(url, args, headers)
    print(data)
    return data['mediaItems'][0]['uri']


def get_playlist_items(playlist_id):
    url = make_url(spotify_api_url, 'playlist_tracks')
    headers = make_header(spotify_api_url)
    args = {
        'id': playlist_id,
        'limit': 20
    }
    data = get_request(url, args, headers)
    return data['items']


def find_track_by_id(track_id):
    url = make_url(spotify_api_url, 'tracks')
    headers = make_header(spotify_api_url)
    args = {
        'ids': track_id,
    }
    data = get_request(url, args, headers)
    return data['tracks'][0]