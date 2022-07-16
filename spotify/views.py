from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
from django.views.decorators.csrf import csrf_exempt
import spotipy

@csrf_exempt
def index(request):

    print(request)

    if request.method == "POST":

        scope = [
            'playlist-read-collaborative',
            'playlist-modify-public',
            'playlist-read-private',
            'playlist-modify-private',
            'app-remote-control',
            'streaming',
            'user-read-email',
            'user-read-private',
            'web-playback'
        ]
        
        auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                                    show_dialog=True)
        data = request.POST
        code = data.get('code')

        return HttpResponse(auth_manager.get_access_token(code)['access_token'])

    return HttpResponse("not a POST request")
