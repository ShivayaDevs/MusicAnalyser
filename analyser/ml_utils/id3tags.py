import eyed3

def get_tags(filename):
    audiofile = eyed3.load(filename)
    artist = audiofile.tag.artist
    album = audiofile.tag.album
    title = audiofile.tag.title

    data = {}
    data['artist'] = artist
    data['album'] = album
    data['title'] = title

    return data
