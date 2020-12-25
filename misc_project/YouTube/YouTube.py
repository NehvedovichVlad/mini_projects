import pytube

url = 'https://www.youtube.com/watch?v=OqIhXi1E7e8'

video = pytube.YouTube(url)

stream = video.streams.get_by_itag(22)
print("Downloading...")
stream.download(filename="get_video")
print("Done!")

"""
for stream in video.streams:
    if 'video' in str(stream) and 'mp4' in str(stream):
        print(stream)
"""
