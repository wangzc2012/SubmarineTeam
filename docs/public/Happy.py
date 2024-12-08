import requests
import threading
import tkinter as tk
from tkinter import ttk
from time import time,sleep
from tkinter import messagebox
from tkinter import filedialog


def download_chunk(url, start_byte, end_byte, filename, item):
    global file_size,download_size
    headers = {'Range': f'bytes={start_byte}-{end_byte}'}
    r = requests.get(url, headers=headers, stream=True)
    threads_data[item]=[int(r.headers.get('content-length', 0)),0]
    thread_download=0
    with open(filename, 'r+b') as f:
        f.seek(start_byte)
        for chunk in r.iter_content(chunk_size=65535):
            if chunk:
                f.write(chunk)
                in_thread_block_size=len(chunk)
                download_size+=in_thread_block_size
                thread_download+=in_thread_block_size
                threads_data[item][1]=thread_download
                
                
def update() :
    
    global file_size,start_time,is_downloading,show_download,speed_show,num_threads,main_f
    main_f=tk.Frame(sd)
    sd.create_window((0,0),window=main_f,anchor="nw")
    show_download=tk.Canvas(main_f,height=250,width=300)
    show_download.grid(row=0,column=0,columnspan=3)
    speed_show=show_download.create_line(0,0,300,0,fill="black",width=2)
    
    pros={}
    labs={}
    speeds={}
    
    for i in range(num_threads) :
        pros[i]=ttk.Progressbar(main_f,orient=tk.HORIZONTAL,length=200)
        labs[i]=tk.Label(main_f,text="Thread-"+str(i+1))
        speeds[i]=tk.Label(main_f,text="speed: 0|KBs")
        pros[i].grid(row=i+1,column=1)
        labs[i].grid(row=i+1,column=0)
        speeds[i].grid(row=i+1,column=2)
    sd.update()
    sd.config(scrollregion=sd.bbox("all"))
    
    last=0
    while is_downloading :
        last=update_show(last)
        
        for i in range(num_threads) :
            if i in threads_data :
                m=threads_data[i][1]
                if m!=0 :
                    pros[i]["value"]=int(m/threads_data[i][0]*100)
                    if m<threads_data[i][0] :
                        speeds[i].config(text="speed: "+str(round(m/((time()-start_time))/1000,2))+"|KBs")
                    else :
                        speeds[i].config(text="Complete!")
        

def multi_thread_download(url, num_threads, filename, progress_var):
    global file_size,start_time,is_downloading
    r = requests.head(url)
    file_size = int(r.headers.get('content-length', 0))
    chunk_size = file_size // num_threads
    with open(filename, 'wb') as f:
        f.truncate(file_size)
    start_time=time()
    threads = []
    for i in range(num_threads):
        start_byte = i * chunk_size
        end_byte = start_byte + chunk_size - 1
        if i == num_threads - 1 :
            end_byte = file_size
        thread = threading.Thread(target=download_chunk, args=(url, start_byte, end_byte, filename, i))
        threads.append(thread)
        thread.start()
        sleep(0.5)
    threading.Thread(target=update).start()
    for thread in threads:
        thread.join()
    sleep(1)
    is_downloading=False

    messagebox.showinfo("Tip","Download Complete")

def update_show(last) :
    global file_size,show_download,download_size,speed_show,main_f
    
    if (time()-start_time)!=0 and file_size!=0 :
        now_speed=round((download_size/(time()-start_time))/1024,2)
        speed["text"]=str(now_speed)+"KB/S"
        progress_var.set(download_size/file_size*100)
        return 887
    else :
        window.update()
        main_f.update()
        sd.update()
        return 0
    
    
def start_download():
    global download_size,last_speed,show_download,last_progress,speed_show,is_downloading,num_threads
    sd.delete(tk.ALL)
    
    is_downloading=True
    download_size=0
    url = entry_url.get()
    last_speed=0
    last_progress=0
    num_threads = int(entry_threads.get())
    filename = entry_filename.get()
    threading.Thread(target=multi_thread_download, args=(url, num_threads, filename, progress_var)).start()

def check_fill(event) :
    if entry_url.get()!="" and entry_filename.get()=="" :
        entry_filename.insert(0,entry_url.get().split("/")[-1])
def on_vertical_scroll(*args):
    global main_f,sd
    window.update()
    sd.yview(*args)
    main_f.update()

def close_window() :
    global is_downloading
    if not is_downloading : 
        window.destroy()
    else :
        messagebox.showwarning("Tip","Don't exit while downloading")

if "__main__" == __name__ :
    download_size=0
    is_downloading=False
    threads_data={}
    window = tk.Tk()
    window.protocol("WM_DELETE_WINDOW",close_window)
    window.resizable(False,False)
    window.geometry("750x250")
    window.title("Downloader fast(1.9)")
    label_url = tk.Label(window, text="URL:")
    label_url.grid(row=0, column=0, padx=5, pady=5)
    entry_url = tk.Entry(window)
    entry_url.grid(row=0, column=1, padx=5, pady=5)
    entry_url.bind("<Key>",check_fill)

    label_threads = tk.Label(window, text="Number of Threads:")
    label_threads.grid(row=1, column=0, padx=5, pady=5)
    entry_threads = tk.Scale(window,label="",length=200,from_=1,to=1025,tickinterval=256,resolution=1,orient=tk.HORIZONTAL)
    entry_threads.grid(row=1, column=1, padx=5, pady=5)

    label_filename = tk.Label(window, text="Save As:")
    label_filename.grid(row=2, column=0, padx=5, pady=5)
    entry_filename = tk.Entry(window)
    entry_filename.grid(row=2, column=1, padx=5, pady=5)

    button_download = tk.Button(window, text="Download", command=start_download)
    button_download.grid(row=4, columnspan=2, padx=5, pady=5)
    progress_var = tk.DoubleVar()
    progress = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate", variable=progress_var)
    progress.grid(row=5, columnspan=2, padx=5, pady=5)
    progress_var.set(0.0)

    speed=tk.Label(window,text="Speed:0")
    speed.grid(row=3,columnspan=2)
    sd=tk.Canvas(height=250,width=380)
    sd.grid(row=0,column=2,rowspan=6)

    vsb = tk.Scrollbar(window, orient="vertical", command=on_vertical_scroll)
    vsb.grid(row=0, column=3, sticky="ns",rowspan=6)
    sd.configure(yscrollcommand=vsb.set)

    window.mainloop()
