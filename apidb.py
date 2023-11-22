import api
import db
import threading


def search(query):
    db.create_db()
    result = db.search_by_query(query)

    if any(i[1] for i in result.items()):
        print('getting result from the database')
        return result

    print('getting result from the api')

    api_data = api.search(query)
    print(api_data)
    result = filter_api_results(api_data)
    print('result finishied')

    t = threading.Thread(target=db.add_search_results, args=(query, result))
    t.start()

    return result


def filter_api_results(api_data):
    results = {
        'track': [],
        'album': [],
    }
    for element in api_data:
        obj = parse_element(element['data'])
        if obj:
            results[obj['type']].append(obj)
    return results


def parse_element(data):
    elem_type = data['uri'].split(':')[1]

    print(data)
    result = {
        'uri': data['uri'],
        'type': elem_type,
        'name': '',
        'artist': '',
        'cover': '',
        'duration': ''
    }
    try:
        if elem_type == 'artist':
            result['name'] = data['profile']['name']
            result['cover'] = data['visuals']['avatarImage']['sources'][1]['url']
        else:
            result['name'] = data['name']
            result['artist'] = parse_artists_search(data)

            if elem_type == 'track':
                result['duration'] = calculate_duration(data['duration']['totalMilliseconds'])
                result['cover'] = data['albumOfTrack']['coverArt']['sources'][0]['url']
            else:
                result['cover'] = data['coverArt']['sources'][0]['url']
        return result
    except TypeError as e:
        print(f'Skipping element because of {e}')
        return None


def parse_artists_search(data):
    artist_list = [i['profile']['name'] for i in data['artists']['items']]
    artists = ', '.join(artist_list)
    return artists


def calculate_duration(data):
    seconds = round(data / 1000)
    duration = f'{seconds // 60}:{seconds % 60:02}'
    return duration


def get_similar_tracks(uri):
    playlist_uri = api.get_radio_uri(uri)
    playlist_id = playlist_uri.split(':')[-1]

    print(f'getting playlist tracks by id {playlist_id}')
    playlist_tracks = api.get_playlist_items(playlist_id)
    print(playlist_tracks[0])
    data = {
        'track': []
    }
    for track in playlist_tracks:
        track_obj = parse_similar_tracks(track)
        if track_obj['uri'] != uri:
            data['track'].append(track_obj)
    return data


def parse_similar_tracks(data):
    result = {
        'uri': data['track']['uri'],
        'type': 'track',
        'name': data['track']['name'],
        'artist': parse_artists_for_similar_tracks(data['track']),
        'cover': data['track']['album']['images'][1]['url'],
        'duration': calculate_duration(data['track']['duration_ms']),
        'preview_url': data['track']['preview_url']
    }
    return result


def parse_artists_for_similar_tracks(data):
    artists = [i['name'] for i in data['artists']]
    return ', '.join(artists)


def get_track_by_track_id(track_id):
    return api.find_track_by_id(track_id)
