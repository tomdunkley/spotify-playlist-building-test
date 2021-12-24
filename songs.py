import csv, bs4, urllib3
import spotipy
import spotipy.util as util

username = "dunkertheepic13"
playlist_name = "Test"
reference_playlist_name = "just a shit tonne of songs"

Array = []
with open('songs.csv', newline='\n') as csvfile:
     spamreader = csv.reader(csvfile, quotechar='"')
     for row in spamreader:
         Array.append([row[0],row[1]])

def GetPlaylistID(username, playlist_name):
    playlist_id = ''
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:  # iterate through playlists I follow
        if playlist['name'] == playlist_name:  # filter for newly created playlist
            playlist_id = playlist['id']
    return playlist_id

token = util.prompt_for_user_token(username,
                                   scope="playlist-read-private",
                                   client_id="070c3cd48f1b48f3bf5c4bb9737265ca",
                                   client_secret="7c87cdfee4874fb4b0f2ed1fe8ca5b2a",
                                   redirect_uri='http://localhost:8888/callback')

sp = spotipy.Spotify(auth=token)
playlist_info = sp.user_playlist(username, GetPlaylistID(username, reference_playlist_name))["tracks"]
print(playlist_info)



completeList = [["Song", "Artist", "Energy", "Danceability", "Happiness", "Loudness", "Acousticness", "Instrumental", "Liveness", "Speechiness"]]
for i in range(1, len(Array)):
    try:
        current = [Array[i][0],Array[i][1]]
        
        http = urllib3.PoolManager()
        r = http.request('GET', 'https://tunebat.com/Search?q='+Array[i][0]+" "+Array[i][1])
        soup = bs4.BeautifulSoup(r.data, features="html.parser")

        r = http.request('GET', "https://tunebat.com"+soup.find_all('a')[5].get("href"))
        soup = bs4.BeautifulSoup(r.data, features="html.parser")
        tdArray = soup.findAll("td")

        divArray = []

        for ul in soup.find_all('div', {'class' : 'row  main-attribute-value'}):
            divArray.extend(ul.find_all('div', {'class' : 'name'}))

        a=0
        for td in tdArray:
            found = False
            string = ""
            for j in td:
                if  8 <= a <= 15:
                    current.append(j)
            a+=1

        completeList.append(current)
        print(str(i)+": "+Array[i][0]+", "+Array[i][1])

    except:
        print("FAILED: "+Array[i][0]+", "+Array[i][1])
        completeList.append(Array[i][:2])
        pass

#with open('songsfile.csv', mode='w',newline="") as employee_file:
#	employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#	for row in completeList:
#		employee_writer.writerow(row)


finalArray = []
for item in completeList:
    if item[2] > 90:
        finalArray.append(item)







token = util.prompt_for_user_token(username,
                                   scope="playlist-modify-public",
                                   client_id="070c3cd48f1b48f3bf5c4bb9737265ca",
                                   client_secret="7c87cdfee4874fb4b0f2ed1fe8ca5b2a",
                                   redirect_uri='http://localhost:8888/callback') 
sp = spotipy.Spotify(auth=token)
sp.user_playlist_create(username, name=playlist_name)

def GetTrackID(artist, title):
    #Track Info Box Flow
    results = sp.search(q=f"{title} {artist} ", limit=1, type='track') #get 5 responses since first isn't always accurate
    if results['tracks']['total'] == 0: #if track isn't on spotify as queried, go to next track
        return None
    else:
        track_id = results['tracks']['items'][0]['id']
    return track_id

def GetTrackIDs(array, artist_column=0, title_column=1):
    IDs = []
    for song in array:
        track_id = GetTrackID(song[artist_column], song[title_column])
        if track_id != None:
            IDs.append(track_id)
        else:
            print("FAIL:",song[artist_column], song[title_column])



def addTracks(trackIDs, username, playlistID):
    sp.user_playlist_add_tracks(username, playlistID, trackIDs)



addTracks(GetTrackIDs(finalArray,1,0),username,GetPlaylistID(username,playlist_name))


