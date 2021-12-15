import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import urllib.request
import re
from pytube import YouTube
import os

# Authentication
client_id = 'CLIENT_ID' # Add your own client_id
client_secret = 'CLIENT_SECRET' #Add your own client secret
user_id = 'USER_ID' #Add user id
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def getTrackIDs(user, playlist_id):
    id_list = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        id_list.append(track['id'])
    return id_list


def getTrackFeatures(single_id):
    meta = sp.track(single_id)
    name = meta['name']
    artist = meta['album']['artists'][0]['name']
    return [name, artist]


if __name__ == '__main__':
    playlists_uri_list = []
    playlist_names_list = []
    playlists = sp.user_playlists(user_id)
    while playlists:
        for current_playlist, playlist in enumerate(playlists['items']):
            playlist_names_list.append(playlist['name'])
            playlists_uri_list.append(playlist['uri'].lstrip("spotify:playlist:"))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

    print("Playlist of the user_id given : ")
    print(playlist_names_list)
    os.mkdir("Downloaded Music")

    # Tracks of all the playlists and number of tracks in the playlist
    for i in range(len(playlists_uri_list)):
        current_playlist = playlists_uri_list[i]
        current_playlist_name = playlist_names_list[i]
        os.mkdir("Downloaded Music/" + current_playlist_name)
        ids = getTrackIDs(user_id, current_playlist)
        print(f"\nNumber of tracks in the playlist '{current_playlist_name}' : {len(ids)}")
        print("Starting Downloading .................")

        # loop over track ids
        tracks = []
        for j in range(len(ids)):
            time.sleep(.5)
            track = getTrackFeatures(ids[j])
            tracks.append(track)

        index = 1
        for track in tracks:
            song_name = track[0]
            artist_name = track[1]
            search_terms = song_name + ' ' + artist_name
            print(str(index) + ". " + search_terms)

            html = urllib.request.urlopen(
                "https://www.youtube.com/results?search_query=" + search_terms.replace(' ', '+'))
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            youtube_link = "https://www.youtube.com/watch?v=" + video_ids[0]
            # url input from user
            yt = YouTube(youtube_link)
            # extract only audio
            video = yt.streams.filter(only_audio=True).first()
            # download the file
            out_file = video.download(output_path="Downloaded Music/" + current_playlist_name)
            # save the file
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            # result of success
            print(yt.title + " has been successfully downloaded.")
            index += 1
