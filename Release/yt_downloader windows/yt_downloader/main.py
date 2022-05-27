from blessed import Terminal
from pytube import Playlist
from pytube import YouTube
from os import system, name
import os

term = Terminal()

def clear():
      
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def get_input():
    with term.cbreak():
        val = ''
        getting_input = True
        while getting_input:
            val = term.inkey()
            if val.name == 'KEY_UP':
                input = "up"
                break
            elif val.name == "KEY_DOWN":
                input = "down"
                break
            elif val.name == "KEY_ENTER":
                input = "enter"
                break
            else:
                continue
        return input

def ui_list(options):
    loop = True
    selection_index = 0
    selected = False
    while loop:
        option_index = 0
        for option in options:
            if option_index == selection_index:
                print(term.yellow + option + term.normal)
            else:
                print(option)
            option_index += 1
        input = get_input()
        match input:
            case "up":
                selection_index -= 1
            case "down":
                selection_index += 1
            case "enter":
                selected = True
        if selection_index > len(options) - 1:
            selection_index = len(options) - 1
        if selection_index < 0:
            selection_index += 1
        if selected == True:
            loop = False
        clear()
    return selection_index

def download_video():
    try:
        os.mkdir("videos")
    except:
        pass
    video_link = input("paste video link here: ")
    print("link inputed finding video...")
    video = YouTube(video_link)
    print("converting " + video.title + " to mp4...")
    video = video.streams.filter(only_audio=True).first()
    print("downloading " + video.title + "...")
    out_file = video.download("videos")
    print("converting " + video.title + " from mp4 to mp3")
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(video.title + " has been succesfully downloaded")

def download_playlist():
    playlist_link = input("paste playlist link here: ")
    print("link inputed finding playlist...")
    playlist = Playlist(playlist_link)
    print("creating folder for playlist " + playlist.title)
    try: 
        os.mkdir(playlist.title)
    except:
        print("directory already exists")
    print("starting downloads")
    for video in playlist.videos:
        try:
            print("converting " + video.title + " to mp4...")
            video = video.streams.filter(only_audio=True).first()
            print("downloading " + video.title + "...")
            out_file = video.download(playlist.title)
            print("converting " + video.title + " from mp4 to mp3")
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            print(video.title + " has been succesfully downloaded")
        except:
            print("there was an error in downloading " + video.title)
    print("playlist " + playlist.title + " has been succesfully downloaded")

def start_menu():
    clear()
    app = True
    while app:
        choice = ui_list(["download playlist", "download video", "exit"])
        match choice:
            case 0:
                download_playlist()
            case 1:
                download_video()
            case 2:
                print("closing app...")
                app = False
            
start_menu()