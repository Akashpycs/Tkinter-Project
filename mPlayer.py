import tkinter, os, psutil
from tkinter import ttk

main = tkinter.Tk()
main.title("mPlayer")
main.geometry("380x400")

path_frame = ttk.LabelFrame(main, text='Path')
path_frame.grid(row=0, column = 0, padx=10, pady=10)

music_frame = ttk.LabelFrame(main, text="Music")
music_frame.grid(row=1, column = 0, padx=10, pady=20)

controller_frame = ttk.LabelFrame(main, text="Controller")
controller_frame.grid(row=2, column = 0, padx=10, pady=20)

path_label = ttk.Label(path_frame, text="Path :").grid(row=0, column=0, pady=10)
path_entry = ttk.Entry(path_frame, width=35)
path_entry.grid(row=0, column=1, pady=10, padx=10)

song_list = []
last_song = current_song =  None
song_number = 1

def get_proc():
    process_name = 'vlc.exe'
    for proc in psutil.process_iter(attrs=['pid','name']):
        if proc.info['name']=='vlc.exe':
            vlc = psutil.Process(proc.info['pid'])
            return vlc
    return None



def use_curPath(): 
    path_entry.delete(0,tkinter.END)
    path_entry.insert(0,os.getcwd())
    

def dirsic():
    global song_list, current_song
    path = path_entry.get()
    if os.path.exists(path):
        os.chdir(path)
    else : return
    song_list = [i for i in os.listdir(os.getcwd()) if i.endswith('.mp3')]
    song_count = ttk.Label(music_frame, text=f"Files : {len(song_list)}").grid(row=0, column=0, padx=10, pady=10)
    if len(song_list): current_song = song_list[0]
    else: current_song = "None"
    current_song_label = ttk.Label(music_frame, text = f"Current Song : {current_song[:15]+'...'}").grid(row=1, column=0, padx=10, pady=10)
    
def nexic():
    global  current_song, song_number
    if song_number<=(len(song_list)-1): 
        song_number+=1
        current_song = song_list[song_number]
    else:
        current_song_label = ttk.Label(music_frame, text = f"No Song detected untill Now").grid(row=1, column=0, padx=10, pady=10)
        return 
    current_song_label = ttk.Label(music_frame, text = f"Current Song : {current_song[:10]+'...'}").grid(row=1, column=0, padx=10, pady=10)

def previc():
    global current_song, song_number
    if song_number>0 and song_list: 
        song_number-=1
        current_song = song_list[song_number]
    else:
        current_song_label= ttk.Label(music_frame, text = f"No Song detected untill Now").grid(row=1, column=0, padx=10, pady=10)
        return 
    current_song_label = ttk.Label(music_frame, text = f"Current Song : {current_song[:15]+'...'}").grid(row=1, column=0, padx=10, pady=10)

def stop_music():
    proc = get_proc()
    if proc is not None: proc.kill()

def play_music():
    global last_song
    print(f"{last_song=},{current_song=}", end='\n')
    proc = get_proc()
    song_path = os.path.join(os.getcwd(),current_song)
    if proc is None: 
        os.startfile(song_path)
        last_song = current_song
    elif current_song==last_song : proc.resume()
    else : stop_music(), play_music()

def pause_music():
    proc = get_proc()
    if proc.status()='stopped' : return
    elif proc is not None: proc.suspend()

path_conf = ttk.Button(path_frame, width=35, text="OK", command = dirsic).grid(row=2, column=1)
path_def = ttk.Button(path_frame, width=10, text="Current", command = use_curPath).grid(row=2, column=0, padx=20)
    
play_button = ttk.Button(controller_frame, text = "|>", command=play_music).grid(row=0,column=0,pady=10)

pause_button = ttk.Button(controller_frame, text="||", command = pause_music).grid(row=0, column=1,padx=10)

stop_button = ttk.Button(controller_frame, text="[]", command=stop_music).grid(row=0, column=2)

forward_btn = ttk.Button(controller_frame, text=">>", command = nexic).grid(row=1,column=2, pady=10)
backward_btn = ttk.Button(controller_frame, text="<<", command = previc).grid(row=1,column=0, pady=10)



main.mainloop()