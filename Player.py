from dotenv import load_dotenv
import os
import time
import random
from playsound import playsound
from flask import Flask, render_template

 
# Provide the path to your sound file
recordScratch = 'babyscratch-87371.mp3'
 


load_dotenv()#loading the environment values (the spotify client IDs)

#setting env values to python variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

scope = "app-remote-control streaming user-read-playback-state user-read-currently-playing playlist-read-private user-modify-playback-state"

#print(client_id, client_secret)

#spotipy library imported to make easier API calls
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#authorising access using two IDs
sp_oauth = SpotifyOAuth(client_id,client_secret,redirect_uri="http://localhost:5500/callback",scope= scope)
sp = spotipy.Spotify(auth_manager=sp_oauth)
#getting access token using the authorisation line above
access_token = sp_oauth.get_cached_token()
#print(access_token)


#setting sp as variable by passing in authorisation key into spotify "manager"
#sp = spotipy.Spotify(auth=access_token)

#pull these values from a dictionary, using the key value
songs = {1: {'name': "All By My Self", 'uri': "0gsl92EMIScPGV1AU35nuD", 'start': "177000", 'duration': 30},
     17: {"name" : "Dancing Queen", "uri" : "0GjEhVFGZW8afUYGChu3Rr", "start" : "150000", "duration" : 25},
     8: {"name" : "Eight Days a Week", "uri" : "1Dg4dFJr3HW7sbA7vPejre", "start" : "48000", "duration" : 28},
     16: {"name" : "Sweet Little Sixteen", "uri" : "4GWHrdyVTC0AWwuRgoWzE7", "start" : "15000", "duration" : 10},
     63: {"name" : "December 1963 (Oh, What a Night)", "uri" : "1hQFF33xi8ruavZNyovtUN", "start" : "10000", "duration" : 22},
     69: {"name" : "Summer Of '69", "uri" : "0GONea6G2XdnHWjNZd6zt3", "start" : "75000", "duration" : 23},
     21: {"name" : "September", "uri" : "2grjqo0Frpf2okIBiifQKs", "start" : "16000", "duration" : 30},
     5: {"name" : "Mambo No. 5", "uri" : "6x4tKaOzfNJpEJHySoiJcs", "start" : "49000", "duration" : 38},
     95: {"name" : "9 To 5", "uri" : "4w3tQBXhn5345eUXDGBWZG", "start" : "0", "duration" : 50},
     27: {"name" : "Heaven", "uri" : "37Q5anxoGWYdRsyeXkkNoI", "start" : "0", "duration" : 25},
     80: {"name" : "Acceptable In The 80s", "uri" : "00cxhG668jV6gU6VK2FUVI", "start" : "232000", "duration" : 38},
     33: {"name" : "Tell Me Ma", "uri" : "7BZOYDhoCAR2AkvGBrj6vw", "start" : "3000", "duration" : 29},
     60: {"name" : "Welcome To The 60s", "uri" : "5BZjrgYjBlPD2iNdFn1nOk", "start" : "35000", "duration" : 22},
     22: {"name" : "22", "uri" : "3WC5CVAahvn98hiseoIvbw", "start" : "37200", "duration" : 28},
     3: {"name" : "abc", "uri" : "6D8kc7RO0rqBLSo2YPflJ5", "start" : "72000", "duration" : 27},
     55: {"name" : "I Can't Drive 55", "uri" : "1MqGKtY9L5qjPi8s7gX645", "start" : "57000", "duration" : 15},
}
#!!!change number 5 timing!!!

#making it so that the called numbers array can be synced across files

def volUp(volume):
    while(volume < 100):
        volume += 6
        sp.volume(volume_percent=volume)
        time.sleep(0.2)
#fades music out over 2.5 seconds
def volDown(volume):
    while(volume != 0):
        volume = volume - 4
        sp.volume(volume_percent=volume)
        time.sleep(0.1)
def randomNumber():
    new = False
    while new == False:
        called = open("calledNumbers.txt", "r")
        newNumber = random.randint(1,99)
        CalledContent = called.read()
        called.close()
        if str(newNumber) in CalledContent:
            new = False
            print("duplicate found")
        else:
            new = True
            called = open("calledNumbers.txt", "r")
            called.write(str(newNumber))
            calledlist = called.readlines()
            calledlist.sort()
        print(CalledContent)
    return newNumber
        

#starts selected track on vol 40
def NewNumber(newNumber):
    #newNumber = randomNumber()
    #newNumber = 17
    print(newNumber)

    #check number is in the list of songs
    if newNumber in songs:
        currentSongInfo=sp.currently_playing(market=None, additional_types=None)
        #print(currentSongInfo)
        currentURI = currentSongInfo['item']['uri']
        currentProgress = currentSongInfo['progress_ms']
        currentLength = currentSongInfo['item']['duration_ms']
        runfor = (currentLength - currentProgress)/1000
        print(runfor)
        playlist = sp.playlist_tracks(playlist_id="5CbD9BzcxhqSKzLEHFOajC", fields= "items.track(uri)")
        playlist = playlist['items']
        index = 0
        for item in playlist:
            if (item['track']['uri']) == currentURI:
                break
            else:
                index += 1
                
        print("index: " + str(index))
            
        #print(playlist)

        print(currentURI)
        print(currentProgress)
        song_uri = songs[newNumber]['uri']
        startFrom = songs[newNumber]['start']
        duration = songs[newNumber]['duration']
        #sp.pause_playback()
        sp.volume(50)
        playsound(recordScratch) 
        sp.volume(40)
        sp.start_playback(device_id=None, uris = ["spotify:track:" + song_uri], position_ms = startFrom)
        #increases volume to 100 over 3 secs
        volUp(40)
        #plays song for set duration
        time.sleep(duration)
        #reduces volume to 0 over 2 seconds
        volDown(100)
        #stops playing song (pauses)
        sp.pause_playback(device_id=None)
        sp.start_playback(context_uri='spotify:playlist:5CbD9BzcxhqSKzLEHFOajC', offset={"position": index}, position_ms= currentProgress)    #currently can't pick next number while this is occuring. might have split code between picking A random number and playing the next song- will be a good cool down incase two specialty songs play successively.
        volUp(50)
        sp.shuffle(state=True)
        


#!!!make it so that the called numbers are saved in order. after each new number, loop text file to create a new list, use sort() function and then write back into text file with another loop