from flask import Flask, render_template, request
from flask_socketio import SocketIO,emit
from pytube import YouTube,Playlist
from downloader import YtDownloader


app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        global link,ltype
        link = request.form.get("link")
        duration = 0

        if "playlist?list=" in link:
            playlist = Playlist(link)
            title = playlist.title
            ltype = 0
            for video in playlist.videos:
                duration += video.length
                thumbnail = video.thumbnail_url
            
            time = f'{duration // 3600}h {(duration % 3600) // 60}min {duration % 60}sec'
        else:

            if "youtu.be" in link:
                ltype = 1
                video_id = link.split('/')[-1].split('?')[0]
                video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            elif "watch?v=" in link:
                ltype = 1
                video = YouTube(link)

            
            thumbnail = video.thumbnail_url
            title = video.title
            time = f'{video.length // 3600}h {(video.length % 3600) // 60}min {video.length % 60}sec'
        
        return render_template("index.html", link=link, thumbnail=thumbnail,time=time, title=title)

    else:
        return render_template("index.html", link='',thumbnail='https://avatars.githubusercontent.com/u/147595129?s=400&u=30e100ab3626809b081ea15475a08bbf0983b57c&v=4', time='0h 0min 0sec', title='Video Title')


@socketio.on('download')
def download(fio):
    downloader = YtDownloader()
    if ltype == 0:
        if fio:
            downloader.pmp3(link)
            socketio.emit("downloaded")
        else:
            downloader.pmp4(link)
            socketio.emit("downloaded")
    else:
        if fio:
            downloader.mp3(link)
            socketio.emit("downloaded")
        else:
            downloader.mp4(link)
            socketio.emit("downloaded")

    
    

if __name__ == "__main__":
    socketio.run(app,debug=True)
