###############################################################################
# slideshow.py
###############################################################################
import pygame
import sys
from pygame.locals import *
import urllib
from smugpy import SmugMug
import re
import ConfigParser
import os
import logging

#    Functions


def get_playlist():
    file_name = settings['slideshow']['file_name']
    return (file_name)


def read_config():
    config = ConfigParser.RawConfigParser()
    config.read('slideshow.cfg')
    sections = config.sections()
    settings = {}
    for section in sections:
        settings[section] = {}
        for option in config.options(section):
            settings[section][option] = config.get(section, option)
            logging.debug('%s', settings[section][option])
    return settings


def load_array(file_name):
    done = False
    array = []

    file = open(file_name)

    while not done:
        pic_id = file.readline()
        pic_id = pic_id.strip()
        if pic_id == '':
            done = True
        else:
            array.append(pic_id)
    file.close()
    logging.debug('%d %s', len(array), 'pictures loaded')
    return array


def get_picture(array, index):
    if index >= len(array):
        return False
    else:
        pic_id = array[index]
        #split the line
        pic_id = re.split('\W+', pic_id)
        #get the URL
        logging.debug('getting URL')
        image_url = smugmug.images_getURLs(ImageID=int(pic_id[0]),\
         ImageKey=pic_id[1],\
         CustomSize=settings['slideshow']['screensize'])
        image_url = image_url["Image"]["CustomURL"]
        logging.debug('%s', image_url)
        #get the picture using the url and save locally
        urllib.urlretrieve(image_url, "/home/lwuser/slideshow/next_pic.jpg")
        logging.debug('image retreived')
        #create an image using the picture and resize
        image = pygame.Surface((window.get_rect().width,\
         window.get_rect().height))
        image = pygame.image.load("/home/lwuser/slideshow/next_pic.jpg")
        image = image.convert()
        if image.get_rect() != window.get_rect():
            logging.debug('resizing image')
            temp_image = pygame.Surface((window.get_rect().width,\
             window.get_rect().height))
            temp_image.fill((0, 0, 0))
            ratio = min(float(window.get_rect().width) / \
             float(image.get_rect().width),\
             float(window.get_rect().height) / float(image.get_rect().height))
            width = int(ratio * image.get_rect().width)
            height = int(ratio * image.get_rect().height)
            image = pygame.transform.smoothscale(image, (width, height))
            horiz_offset = (window.get_rect().width - width) / 2
            vert_offset = (window.get_rect().height - height) / 2
            temp_image.blit(image, (horiz_offset, vert_offset))
            image = temp_image
        return image


def crossfade(image1, image2):
    # fade out image1 and fade in image2
    for alpha in [255]:
        image1.set_alpha(255 - alpha)
        image2.set_alpha(alpha)
        window.blit(image1, (0, 0))
        window.blit(image2, (0, 0))
        pygame.display.flip()


def smug_init():

    smugmug = SmugMug(api_key=settings['smugmug']['api_key'],\
     oauth_secret=settings['smugmug']['oauth_secret'],\
     app_name=settings['smugmug']['app'])

    #oauth handshake
    #smugmug.auth_getRequestToken()
    #raw_input("Authorize app at %s\n" % (smugmug.authorize(access="Full")))
    #result = smugmug.auth_getAccessToken()

    oauth_token_id = settings['smugmug']['oauth_token_id']
    oauth_token_secret = settings['smugmug']['oauth_token_secret']
    smugmug.set_oauth_token(oauth_token_id, oauth_token_secret)

    return smugmug

# ... Main program

settings = read_config()
file_name = get_playlist()

print settings['slideshow']['log_file']
logging.basicConfig(filename=settings['slideshow']['log_file'],\
 format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

logging.debug('----Open Log File----')

smugmug = smug_init()

pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
current_image = pygame.Surface((window.get_rect().width, \
    window.get_rect().height))
current_image.fill((0, 0, 0))
next_image = pygame.Surface((window.get_rect().width,\
 window.get_rect().height))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)



# initialize loop
id_array = load_array(file_name)
index = 0
done = False

# set timestamp of file
current_file_time = os.stat(file_name).st_mtime

# main program loop
while not done:
    # get key input
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            elif event.key == K_p:
                logging.debug('paused')
                index -= 1
            elif event.hey == K_b:
                logging.debug('back up')
                index -= 2

    # check for new piclist
    if os.stat(file_name).st_mtime != current_file_time:
        id_array = load_array(file_name)
        index = 0
        current_file_time = os.stat(file_name).st_mtime

    # check for new config file

    # get next picture
    next_image = get_picture(id_array, index)

    if next_image == False:
        id_array = load_array(file_name)
        index = 0
    else:
        # wait
        clock.tick(1.0 / float(settings['slideshow']['delay']))

        # change image
        crossfade(current_image, next_image)
        current_image = next_image
        index += 1
        logging.debug('%d', index)
