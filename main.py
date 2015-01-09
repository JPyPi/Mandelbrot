#!/usr/local/bin/python
import pyglet
from pyglet.window import key
import random
import itertools
import sys
import json

##sys.path.append("build/lib.macosx-10.9-x86_64-2.7")
##from tools import chain2D

print "\n\n"
window = pyglet.window.Window()
window.set_vsync(True)

helv_font=pyglet.font.load("Helvetica",14)
fps_display = pyglet.clock.ClockDisplay(helv_font,color=(1,0,0,1))


def mandelbrot(n,c):
    if n==0: return c
    return mandelbrot(n-1,c)**2+c

class frange:
    def __init__(self,start,stop,step=1):
        self.start=start
        self.stop=stop
        self.step=float(step)
        self.iterations=0

    def next(self):
        new_value=self.start+self.step*self.iterations
        self.iterations+=1
        if new_value<self.stop:
            return new_value
        else:
            raise StopIteration
        
    def __iter__(self):
        return self
 
    def __getitem__(self,index):
        print "Index: %s"%index

    def __len__(self):
        return (self.stop-self.step)/self.step




mandelbrot_points=[]
point_colors=[]

iteration_limit=100

scale=250
height=2.0*scale
width=3.5*scale
print "Width: %s"%width

#Auto center
shift_x=int((window.width-width)/2)
shift_y=int((window.height-height)/2)

##3.5    W
##--- = ---
## 2    200
##
## W=3.5/2*height
##200=1
##0  =-2.5
##n/200*3.5
##
##200=1
##0  =-1
##n/200*2-1
window.clear()

portion=int(width)
for x in xrange(portion):
    sx=x/width*3.5-2.5
    print "%.2f%% rendered"%(x/float(portion)*100)
    for y in xrange(int(height)):
        sy=y/height*2.0-1.0
        for i in xrange(1,iteration_limit):
            try:
                test=mandelbrot(i,complex(sx,sy))
                if test.real**2+test.imag**2 >= 4:
                    break
            except OverflowError:
                break
        if i>=1:
            mandelbrot_points.append((x,y,i))

f=open("mandelbrot_points","w")
json.dump(mandelbrot_points,f)
##mandelbrot_points=json.load(f)
f.close()
        
num_points=len(mandelbrot_points)
print "\nNumber of points: %d"%num_points

#mandelbrot_points=list(itertools.chain(*map(lambda elm:(int(elm.real*scale+shift_x),int(elm.imag*scale+shift_y)),mandelbrot_points)))
##mandelbrot_points=list(itertools.chain(*mandelbrot_points))

histogram={}

mandelbrot_drawpoints=[]
for p in mandelbrot_points:
    mandelbrot_drawpoints.append(p[0])
    mandelbrot_drawpoints.append(p[1])

    histogram[p[2]]=histogram.get(p[2],0)+1


for v in histogram.values():
    print v/float(num_points)*1000
    
##percent_correct=float(p[2])/iteration_limit
##point_colors.append((int(250.0*percent_correct),int(100.0*percent_correct),20))
for p in mandelbrot_points:
    color_mul=histogram[p[2]]/float(num_points)*1000
    point_colors.append((int(250*color_mul),int(100*color_mul),20))
    
point_colors=list(itertools.chain(*point_colors))

@window.event
def on_draw():
    window.clear()

    pyglet.gl.glPointSize(1)

    
    pyglet.graphics.draw(num_points,pyglet.gl.GL_POINTS,
        ('v2i',mandelbrot_drawpoints),
        ('c3B',point_colors)
        )
    
    fps_display.draw()


    

##pyglet.clock.schedule_interval(main_update,1/60.0)
##window.push_handlers(pyglet.window.event.WindowEventLogger())

pyglet.app.run()
