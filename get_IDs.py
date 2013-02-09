import sys
import urllib
from smugpy import SmugMug
import re
import ConfigParser

#    Functions


def read_config():
    config = ConfigParser.RawConfigParser()
    config.read('slideshow.cfg')
    sections = config.sections()
    settings = {}
    for section in sections:
        settings[section] = {}
        for option in config.options(section):
            settings[section][option] = config.get(section, option)
    return settings


def get_albums():
#    Create list of albums
    file_name = "albums.txt"
    file = open(file_name, 'w')
    albums = smugmug.albums_get(NickName="ethanc")
    for album in albums["Albums"]:
        file.writelines((str(album["id"]), '\n', str(album["Key"]), '\n'))
    file.close()


def get_picIDs(file_name):
#    Create list of pictures id, Key in all albums
    images_file = open(file_name, 'w')
    albums = smugmug.albums_get(NickName="ethanc")
    for album in albums["Albums"]:
        images = smugmug.images_get(AlbumID=str(album["id"]),\
         AlbumKey=str(album["Key"]))
        for image in images["Album"]["Images"]:
            images_file.writelines((str(image["id"]),\
             ', ', str(image["Key"]), '\n'))
    images_file.close()
    return True


def smug_init():

    smugmug = SmugMug(api_key=settings['smugmug']['api_key'],\
     oauth_secret=settings['smugmug']['oauth_secret'],\
     app_name=settings['smugmug']['app'])

    oauth_token_id = settings['smugmug']['oauth_token_id']
    oauth_token_secret = settings['smugmug']['oauth_token_secret']
    smugmug.set_oauth_token(oauth_token_id, oauth_token_secret)

    return smugmug

# ... Main program

settings = read_config()
file_name = "piclist_id.txt"
smugmug = smug_init()
get_picIDs(file_name)
