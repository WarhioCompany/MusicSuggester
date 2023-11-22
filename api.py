from api_requets import post_request, get_request

spotify_api_url = 'spotify23.p.rapidapi.com'
shazam_api_url = 'shazam.p.rapidapi.com'

current_key = 0
keys = [
    "89488e69a4mshcb628c81e41961ep142676jsn3ea877f26d40",
    #"50a30822eamsh5b12b6abf4cb78dp1b77d8jsn0106d78b94a0",
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
    result = data['tracks']['items'] + data['albums']['items']
    return result


def get_radio_uri(uri):
    url = make_url(spotify_api_url, 'seed_to_playlist')
    headers = make_header(spotify_api_url)
    args = {
        'uri': uri
    }
    data = get_request(url, args, headers)
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