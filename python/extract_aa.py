import requests
import csv
import time
import sys
import json

prefix_url = 'https://api.spotify.com/v1/'
csv.field_size_limit(sys.maxsize)

def API_get_several_albums_request(album_ids):
    url = prefix_url + 'albums/'
    params = {'ids': ','.join(album_ids)}
    resp = requests.get(url, params=params)

    return resp

def API_get_several_artists_request(artist_ids):
    '''
    Makes a Spotify API request to get information on several albums given
    a list of their ids.

    INPUT:
    album_ids - a list of strings representing artist ids
    OUTPUT:
    response object from request (use .json() to extract data)
    '''
    url = prefix_url + 'artists'
    params = {'ids': ','.join(artist_ids)}
    resp = requests.get(url, params=params)

    return resp

def parse_genres(genres_array):
    # All the 5's here refer to the fact that there are 5 columns in the DB for genres
    genres = [''] * 5
    iter_size = min(5, len(genres_array))

    for i in range(0, iter_size):
        genres[i] = genres_array

    return genres


def main():
    album_ids = set()
    artist_ids = set()
    with open ('../data/songs.csv', 'r', encoding="utf8") as song_csv:
        r = csv.DictReader(song_csv)
        for song in r:
            album_ids.add(song["album_id"][2 : len(song["album_id"]) - 1])
            artist_ids.add(song["artist_id"][2 : len(song["artist_id"]) - 1])
    album_ids = list(album_ids)
    artist_ids = list(artist_ids)
    print (len(album_ids))
    print (album_ids[0])
    ###########################################################################
    ###########################################################################
    ##########                                                       ##########
    ##########                      Albums                           ##########
    ##########                                                       ##########
    ###########################################################################
    ###########################################################################
    # Make calls to /albums route to get genre and release date information
    print('spotify API: albums')
    album_results = []
    with open ('../data/albums.csv', 'w', encoding="utf8") as album_csv:
        write_album = csv.writer(album_csv)
        write_album.writerow([
            'album_id',
            'album_name',
            'release_date',
            'genre1',
            'genre2',
            'genre3',
            'genre4',
            'genre5',
            'album_image_url'])
        for idx in range (0, len(album_ids), 20):
            response = API_get_several_albums_request(album_ids[idx:idx+20])
            if (response.status_code == 200):
                data = response.json()
                if (data['albums']):
                    for album in data['albums']:
                        if (album['release_date_precision'] == 'day'):
                            genres = parse_genres(album['genres'])
                            print (genres)
                            images  = ("" if  len(album['images']) == 0 else album['images'][0]['url'])
                            write_album.writerow([
                                album['id'],
                                album['name'],
                                album['release_date'],
                                genres[0],
                                genres[1],
                                genres[2],
                                genres[3],
                                genres[4],
                                images])
            time.sleep(0.3)

    #print(len(album_results))
    # with open ('../data/albums.csv', 'w', encoding="utf8") as album_csv:
    #     write_album = csv.writer(album_csv)
    #     write_album.writerow([
    #         'album_id',
    #         'album_name',
    #         'release_date',
    #         'genre1',
    #         'genre2',
    #         'genre3',
    #         'genre4',
    #         'genre5',
    #         'album_image_url'])
    #     for album in album_results:
    #         if (album['release_date_precision'] == 'day'):
    #             genres = parse_genres(album['genres'])
    #             write_album.writerow([
    #                 album['id'],
    #                 album['name'],
    #                 album['release_date'],
    #                 genres[0],
    #                 genres[1],
    #                 genres[2],
    #                 genres[3],
    #                 genres[4],
    #                 album['images'][0]['url']])


    ###########################################################################
    ###########################################################################
    ##########                                                       ##########
    ##########                     Artists                           ##########
    ##########                                                       ##########
    ###########################################################################
    ###########################################################################
    # Make calls to /artists route to get genre and release date information
    print('spotify API: artists')

    artist_results = []
    for idx in range (0, len(artist_ids), 50):
        response = API_get_several_artists_request(artist_ids[idx:idx+50])
        if (response.status_code == 200):
            data = response.json()
            if (data['artists']):
                for artist in data['artists']:
                    artist_results.append(artist)
        time.sleep(0.1)

    print(len(artist_results))
    print('writing artists.csv')
    with open ('../data/artists.csv', 'w', encoding="utf8") as artist_csv:
        write_artist = csv.writer(artist_csv)
        write_artist.writerow([
            'artist_id',
            'artist_name',
            'artist_image_url',
            'spotify_artist_popularity'])
        for artist in artist_results:
            images  = ("" if  len(artist['images']) == 0 else artist['images'][0]['url'])
            write_artist.writerow([
                artist['id'],
                artist['name'],
                images,
                artist['popularity']])


if __name__ == '__main__':
    main()
