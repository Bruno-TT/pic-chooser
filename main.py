import pygame, glob, random
from shutil import copy2
from os import remove
from pygame.locals import K_UP, K_DOWN, KEYDOWN, FULLSCREEN
pygame.init()

#initialise the display
bg=(0,0,0)
display_surface=pygame.display.set_mode((0,0), FULLSCREEN)

#directories to move the images to
KEEP="like/"
DELETE="dislike/"

#modified from http://www.pygame.org/pcr/transform_scale/
def aspect_scale(img,bx,by):
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (int(sx), int(sy)))


def display_image():
    #the current image path
    global image_path

    #empty the display
    display_surface.fill(bg)

    #pick a random image
    image_path=random.choice(glob.glob("images/*"))

    #load it
    image=pygame.image.load(image_path)

    #resize image but keep aspect ratio
    scaled_image=aspect_scale(image, 1920, 1080)

    #display the image
    display_surface.blit(scaled_image, (0,0))

#called when up gets pressed
def up_pressed():

    #copy2 (preserves metadata + accepts dir as 2nd arg) the image to the keep directory
    copy2(image_path, KEEP)

    #remove it from the original directory
    remove(image_path)

    print("moved {} to {}".format(image_path, KEEP))

    #get a new image
    display_image()

#see above
def down_pressed():
    copy2(image_path, DELETE)
    remove(image_path)
    print("moved {} to {}".format(image_path, DELETE))
    display_image()

#display the initial image
display_image()

#main loop
while 1:

    #gotta do this or it breaks - we ignore all non keypress events
    for event in pygame.event.get():

        #whenever a keys pressed
        if event.type==KEYDOWN:

            #call the appropriate function
            if event.key==K_UP:up_pressed()
            if event.key==K_DOWN:down_pressed()

    #update the display
    pygame.display.update()