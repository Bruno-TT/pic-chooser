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

def display_image():
    #the current image path
    global image_path

    #empty the display
    display_surface.fill(bg)

    #pick a random image
    image_path=random.choice(glob.glob("images/*"))

    #load it
    image=pygame.image.load(image_path)

    #display the image
    display_surface.blit(image, (0,0))

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