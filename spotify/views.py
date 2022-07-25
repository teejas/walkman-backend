from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
from django.views.decorators.csrf import csrf_exempt
import spotipy
import json

scope = [
    'ugc-image-upload',
    'user-modify-playback-state',
    'user-read-playback-state',
    'user-read-currently-playing',
    'user-follow-modify',
    'user-follow-read',
    'user-read-recently-played',
    'user-read-playback-position',
    'user-top-read',
    'playlist-read-collaborative',
    'playlist-modify-public',
    'playlist-read-private',
    'playlist-modify-private',
    'app-remote-control',
    'streaming',
    'user-read-email',
    'user-read-private',
    'user-library-modify',
    'user-library-read',
]


auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                            show_dialog=True)
spotify = spotipy.Spotify(client_credentials_manager=auth_manager)

@csrf_exempt
def get_token(request):

    print(request)

    if request.method == "POST":

        data = request.POST
        code = data.get('code')

        return HttpResponse(auth_manager.get_access_token(code)['access_token'])

    return HttpResponse("not a POST request")

@csrf_exempt
def connect_device(request):
    if request.method == "GET":
        devices = spotify.devices()
        print(devices)
        for device in devices['devices']:
            if device['name'] and device['name'] == 'localhost':
                return HttpResponse(device['id'])
            print("%s\t%s" % (device['id'], device['name']))
        return HttpResponse(devices)

    return HttpResponse("not a GET request")

# route to get recommendations using `vibe` as a seed playlist
@csrf_exempt
def get_recommendations(request):
    if request.method == "POST":
        data = request.POST
        playlistId = data.get('playlistId')
        playlist = spotify.playlist(playlistId) # get playlist
        tracks = playlist['tracks']
        track_data = []
        uris = []
        while tracks:
            for item in tracks['items']:
                if "local" not in item['track']['uri']:
                    track_data.append(item['track'])
                    uris.append(item['track']['uri'])
            if tracks['next']:
                tracks = spotify.next(tracks)
                # tracks = None
            else:
                tracks = None

        # generate recommendations with `tracks`
        recommendations = spotify.recommendations(seed_tracks=uris[-5:])
        rec_tracks = recommendations['tracks']
        rec_uris = []
        for item in rec_tracks:
            if "local" not in item['uri']:
                rec_uris.append(item['uri'])

        return HttpResponse(json.dumps(rec_uris), content_type="application/json")

    return HttpResponse("not a POST request")

@csrf_exempt
def skip_track(request):
    if request.method == "POST":
        data = request.POST
        device_id = data.get('device_id')
        spotify.next_track(device_id=device_id)
        return HttpResponse("skipped track")

    return HttpResponse("not a POST request")

@csrf_exempt
def get_playlists(request):
    if request.method == "GET":
        playlists = spotify.user_playlists(user=spotify.me()['id'])
        playlists_data = []
        for playlist in playlists['items']:
            playlists_data.append(playlist)
        return HttpResponse(json.dumps(playlists_data), content_type="application/json")

    return HttpResponse("not a GET request")