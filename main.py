import pygame, glob, random, time
from shutil import copy2
from os import remove
from pygame.locals import K_UP, K_DOWN, KEYDOWN, FULLSCREEN
pygame.init()

#initialise the display
bg=(0,0,0)
green=(0,255,0)
red=(255,0,0)
orange=(255,165,0)
width, height=1920, 1080
display_surface=pygame.display.set_mode((0,0), FULLSCREEN)

#directories to move the images to
KEEP="like/"
DELETE="dislike/"

def flash(colour):
    #flash green
    display_surface.fill(colour)

    #update the display
    pygame.display.update()
    
    #flash it for .1 seconds
    time.sleep(0.1)


#modified from http://www.pygame.org/pcr/transform_scale/
def get_scaled_coords(img,bx,by):
    ix,iy = img.get_size()
    if ix > iy:
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor*ix
            sy = by
        else:
            sx = bx
    else:
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return (int(sx), int(sy))


#function to display an image
def display_image():

    #the current image path
    global image_path

    #empty the display
    display_surface.fill(bg)

    #pick a random image
    image_path=random.choice(glob.glob("images/*"))

    #load it
    image=pygame.image.load(image_path)

    #calculate 
    new_size=get_scaled_coords(image, width, height) #width,height

    #rescale the image
    scaled_image=pygame.transform.scale(image, new_size)

    #if the width is entirely filled
    if new_size[0]==width:
        
        #blip to x=0 obviously
        x=0

        #calculate the y value so that it's blipped centrally
        y=(height-new_size[1])/2
    
    #see above
    elif new_size[1]==height:
        x=(width-new_size[0])/2
        y=0
    
    #probably unreachable, but if neither dimension are filled (most likely a rounding error)
    #once I'm happy this is well written, then I'll delete this
    else:

        #print them out, hopefully it's just a case of a +-1 rounding error
        print(new_size)

        #debug blip to the top left corner
        x,y=0,0

        #flash orange
        flash(orange)

    #display the image
    display_surface.blit(scaled_image, (x,y))

#called when up gets pressed
def up_pressed():

    #copy2 (preserves metadata + accepts dir as 2nd arg) the image to the keep directory
    copy2(image_path, KEEP)

    #remove it from the original directory
    remove(image_path)

    print("moved {} to {}".format(image_path, KEEP))

    #flash green
    flash(green)

    #get a new image
    display_image()

#see above
def down_pressed():
    copy2(image_path, DELETE)
    remove(image_path)
    print("moved {} to {}".format(image_path, DELETE))
    flash(red)
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