from hexgrid import HexGrid
from tkinter import *
from hexagon import Hexagon
# importing the choosecolor package 
from tkinter.colorchooser import *
import math

canvas_width  = 400
canvas_height = 400

global color_pick
color_pick = "#000000"
 
def choose_color(): 
    global color_pick
    # variable to store hexadecimal code of color 
    color_pick = askcolor()[1] 
    print(color_pick)
    
def left_click(event):
    x = event.x
    y = event.y
    item = event.widget.find_closest(x, y)[0]
    hexagon = grid.ret_hex_id(item)
    if variable.get() == 'neighbor':
        neighbor=grid.show_neighbors(hexagon.x,hexagon.y,hexagon.z) 
        for hexagon in neighbor:
            hexagon.set_color(color_pick)
    elif variable.get() == 'point':     
        hexagon.set_color(color_pick)
    elif variable.get() == 'distance':
        global hex_dist_a
        hex_dist_a = hexagon
        hexagon.set_color(color_pick)
        #hexagon.print_coord()
        hex_dist_a.print_coord()
        hex_dist_b.print_coord()
        print(grid.get_dist(hex_dist_a,hex_dist_b))
    elif variable.get() == 'line draw':
      draw_line(hex_dist_a,hex_dist_b)
        

def right_click(event):
    x = event.x
    y = event.y
    item = event.widget.find_closest(x, y)[0]
    hexagon = grid.ret_hex_id(item)
    if variable.get() == 'neighbor':
        neighbor=grid.show_neighbors(hexagon.x,hexagon.y,hexagon.z) 
        for hexagon in neighbor:
            hexagon.set_color(color_pick)
    elif variable.get() == 'point':     
        hexagon.set_color(color_pick)
    elif variable.get() == 'distance':
        global hex_dist_b 
        hex_dist_b = hexagon
        hexagon.set_color(color_pick)
        #hexagon.print_coord()
        hex_dist_a.print_coord()
        hex_dist_b.print_coord()
        print(grid.get_dist(hex_dist_a,hex_dist_b))
    elif variable.get() == 'line draw':
        draw_line(hex_dist_a,hex_dist_b)

def lerp(a, b, t):
    '''
    Linear interpolation of the data.
    '''
    return(a+(b-a)*t)

def cube_lerp(a,b,t):
    '''
    Linear interpolation for the three coordinates of the hexagons. 
    Need to pass in two hexagons.
    Returns a hex coordinate that needs to be rounded.
    '''
    return([lerp(a.x,b.x,t),
            lerp(a.y,b.y,t),
            lerp(a.z,b.z,t)])

def cube_round(x,y,z):
    rx = round(x)
    ry = round(y)
    rz = round(z)

    x_diff = abs(rx-x)
    y_diff = abs(ry-y)
    z_diff = abs(rz-z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry-rz
    elif y_diff > z_diff:
        ry = -rx-rz
    else:
        rz = -rx-ry

    return([rx,ry,rz])

def ret_line(a, b):
        N = grid.get_dist(a,b)
        results = []
        for x in range(1,N+1,1):
            results.append(cube_round(cube_lerp(a, b, 1.0/N * x)[0],cube_lerp(a, b, 1.0/N * x)[1],cube_lerp(a, b, 1.0/N * x)[2]))
        return results

def draw_line(a, b):
        N = grid.get_dist(a,b)
        results = []
        for x in range(1,N+1,1):
            results.append(cube_round(cube_lerp(a, b, 1.0/N * x)[0],cube_lerp(a, b, 1.0/N * x)[1],cube_lerp(a, b, 1.0/N * x)[2]))
        for gon in results:
            hexagon = grid.ret_hex_cube(gon[0],gon[1],gon[2])
            hexagon.set_color('#000000')


# init tk
root = Tk()

# create canvas
myCanvas = Canvas(root, bg="white", height=canvas_height, width=canvas_width)

# create frame to put control buttons onto
frame = Frame(root, bg='grey', width=canvas_width, height=canvas_height/5)
frame.pack(fill='x')

# draw grid
grid = HexGrid(myCanvas,6,'pointy',15)
grid.draw_grid()

myCanvas.pack()

# create variables for hex distance
hex_dist_a = grid.ret_hex_cube(0,0,0)
hex_dist_b = grid.ret_hex_cube(0,0,0)

# create frame to put control buttons onto
frame = Frame(root, bg='grey', width=canvas_width, height=canvas_height/5)
frame.pack(fill='x')
rot_button = Button(frame, text="orientation", command=grid.change_orientation)
rot_button.pack(side='bottom', padx=10)
button = Button(frame, text = "Select color", 
                   command = choose_color) 
button.pack() 

global variable 
variable = StringVar(root)
variable.set("point") # default value

w = OptionMenu(root, variable, "point", "neighbor","distance","line draw")
w.pack()

myCanvas.bind("<Button-1>", left_click)
myCanvas.bind("<Button-3>", right_click)

    

# add to window and show
root.mainloop()