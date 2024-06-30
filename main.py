import argparse
import datetime
import requests
import urllib3
import json
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyPKCE
parser = argparse.ArgumentParser(
    prog='SWR to Spotify' ,
    description="A simple program that parses the SWR playlist, searches the songs on spotify and puts them in a spotify playlist.",
    epilog="adsf"
)
datetimeFormat =  '%m/%d/%Y %H:%M'
def toDateTime(string):
    return datetime.datetime.strptime(string,datetimeFormat)

today = datetime.date.today()
lastTuesday = today + datetime.timedelta(days=-today.weekday() + 1)
group = parser.add_mutually_exclusive_group()
group.add_argument("-c", help="Provide a custom time frame to search songs in. Requires the start and end date and time." , type=toDateTime, nargs=2)
group.add_argument("-l", action="store_true", help="Searches the songs of the last Musik Klub Deutschland from " + lastTuesday.strftime("%d, %b %Y"))
parser.add_argument("-p", help="The name of the playlist to save the songs into. If the playlist does not exist, it is created.", required=True)
args = parser.parse_args()
# set the start and end datetime to the last Musik Klub Deutschland
if(args.l):
    print("passed l")
    start = datetime.datetime(lastTuesday.year, lastTuesday.month, lastTuesday.day, 20) 
    end = start + datetime.timedelta(hours=4)
    print("Start: " + start.strftime("%d, %b %Y %H %M"))
    print("End: " + end.strftime("%d, %b %Y %H %M"))

if (args.c):
    start = args.c[0]
    end = args.c[1]

# the swr page only ever displays the songs within one hour, so we need to do some magic to get all the songs within the timeframe

difference = end - start
differenceInHours = difference.seconds/60/60


songs =  []
artists = []
offset = 0
while differenceInHours > 0:
    url = "https://www.swr.de/swr1/bw/playlist/index.html?swx_date={year}-{month}-{day}&swx_time={hour}%3A00".format(year= start.year, month=str(start.month).zfill(2), day=str(start.day).zfill(2), hour = start.hour + offset)
    print(url)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    for dd in soup.find_all('dd', class_='playlist-item-song'):
        songs.append(dd.contents[0])

    for dd in soup.find_all('dd', class_='playlist-item-artist'):
        artists.append(dd.contents[0].strip())

    differenceInHours -= 1;
    offset += 1

songs_and_artists = set(zip(songs, artists))
print(songs_and_artists)
# put the songs into a spotify playlist
scope="playlist-modify-public,playlist-modify-private"
spotify = spotipy.Spotify(auth_manager=SpotifyPKCE(open_browser=True, scope=scope))
playlists = spotify.current_user_playlists()
has_playlist = False;
current_user = spotify.current_user()
current_user_id = current_user["id"]
for x in playlists["items"]:
    if x["name"] == args.p:
        playlist_id = x["id"]
        has_playlist = True


if not has_playlist:
    res = spotify.user_playlist_create(current_user_id, args.p)
    playlist_id = res["id"]


# search the songs and add them to the playlist
song_uris = []
for (song, artist) in songs_and_artists:
    result = spotify.search("{song} {artist}".format(song=song, artist=artist),limit=1)
    track_result = result["tracks"]
    if "items" in track_result:
        for track in track_result["items"]:
            song_uris.append(track["uri"])

spotify.playlist_add_items(playlist_id, song_uris)
print("Successfully added the songs to your playlist.")
