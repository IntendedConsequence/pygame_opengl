"""
this is a minimal(well, almost minimal) amount of code required to run pygame and opengl.
however, instead of using opengl textured quads to render all the stuff, this example
draws everything on a regular pygame surface which is then converted to an opengl texture
which is then rendered. I know, terribly inefficient, but it works for simple stuff.
Why not just forget about opengl and use regular pygame blitting? Somehow regular pygame
skips frames. It can run 999 fps but once or twice a second you notice a hiccup - even though
the fps stays the same. I don't know what causes this shit but with opengl it seems to be
reduced.
"""
from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame as pg

from random import randint

import time



def render_text(surface, font, text, x, y, color):
    #draw text on provided surface
    msg_surf = font.render(text, False, color)
    surface.blit(msg_surf, (x, y, 0, 0))

def render_start(tex, surf):
    #bind the texture and clear the surface
    glBindTexture(GL_TEXTURE_2D, tex)
    surf.fill(pg.Color('black'))

def render_end(tex, surf):
    #recreate the opengl texture from pygame surface and draw it on the screen
    glClear(GL_DEPTH_BUFFER_BIT)

    tex_data = pg.image.tostring(surf, "RGBA", 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 800, 600, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)

    glBegin(GL_QUADS)

    glTexCoord2i(0, 1)
    glVertex2f(0, 0)

    glTexCoord2i(1, 1)
    glVertex2f(800, 0)

    glTexCoord2i(1, 0)
    glVertex2f(800, 600)

    glTexCoord2i(0, 0)
    glVertex2f(0, 600)
    glEnd()


def run():
    #pygame init
    pg.init()
    screen = pg.display.set_mode((800, 600), pg.HWSURFACE|pg.OPENGL|pg.DOUBLEBUF)
    pg.display.set_caption("blitting on the opengl textures with pygame basics")

    #opengl init
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.5, 0.5, 0.5, 0)

    glViewport(0, 0, 800, 600)

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(0, 800, 600, 0, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #clock to track frametime and limit fps
    clock = pg.time.Clock()

    #default pygame font
    fnt = pg.font.Font(None, 24)

    #surface
    bbuffer_surf = pg.Surface((800, 600))
    bbuffer_surf.fill(pg.Color('black'))
    
    #generating opengl texture from surface
    bbuffer_tex = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, bbuffer_tex)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    tex_data = pg.image.tostring(bbuffer_surf, "RGBA", 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 800, 600, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)

    #some stars to render
    stars = [(randint(0, 800), randint(0, 600), randint(2, 6)) for i in range(100)]

    
    ms = 0
    while True:
        sec = ms / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                return

        

        #move stars
        for i, (x, y, r) in enumerate(stars):
            stars[i] = (x - 1 - r * sec * 30, y, r) if x > -20 else (820, randint(0, 600), r)

        #start drawing stuff
        render_start(bbuffer_tex, bbuffer_surf)

        #draw some stars
        for x, y, r in stars:
            pg.draw.circle(bbuffer_surf, pg.Color(0x8a8a9bff), (int(x),y), r)

        #draw some text
        render_text(bbuffer_surf, fnt, "blit stuff on opengl texture like this text", 200, 200, pg.Color('red'))

        
        #end drawing stuff
        render_end(bbuffer_tex, bbuffer_surf)

        #show the updated frame
        pg.display.flip()

        #limit fps to 60 and get the frame time in milliseconds
        ms = clock.tick(60)
        

run()