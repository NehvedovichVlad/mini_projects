import pytube

url = 'some playlist'

playlist = pytube.Playlist(url)
for url in playlist:
    video = pytube.YouTube(url)
    stream = video.streams.get_by_itag(22)
    print("Downloading video...")
    stream.download()
    print("Done!")
