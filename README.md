# Introduction

This is the backend for the `walkman` project. The first iteration of this is essentially Juko pt 2, a recreation-from-scratch of a project I developed a couple years ago (Spring 2019).

This Django backend provides API endpoints to get an OAuth access token, get a list of device IDs, and get a list of song recommendations based on the five most recently added tracks to the "vibe" playlist.

# Components

`spotify` Django app: gets recommendations, OAuth access tokens, and a list of device IDs
  endpoints:
    - `api/spotify/get_token` POST request, provide an authorization code (from the `/authorize` endpoint, refer to Spotify API documentation) and receive an access token. Used to enable the Spotify web player.
    - `api/spotify/get_playlists` GET request, fetches all playlists for the current user (issue: currently only fetches Tejas' playlists).
    - `api/spotify/get_recommendations` POST request, provide a playlist URI and receive an array of recommended track URIs generated from the five tracks most recently added to that playlist.
    - `api/spotify/skip_track` POST request, provide a device ID to skip playback to the next track.


## Other endpoints

`/health/` healthcheck path, returns 200
`/admin` Django admin console

# Known Issues

- Currently auth is weird. A user can login using their Spotify credentials but for some reason it still loads Spotify data from Tejas' personal account (not from the logged-in user's account).