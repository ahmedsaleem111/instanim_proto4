
from copy import deepcopy

import cairocffi as cairo
import numpy as np
import math 

from PIL import Image

from instanim.utilities import *
from instanim import *

import utilities as ut


'''
Module to defined backend constructs for "displayability".

Structures:

- colors: list of sample colors (as size-3 numpy array)

- colorMap: parent class for "colorMap"

- colorMapLinear: child "colorMap" class for creating a map of colors based on stop-colors 
    where intermediate colors are linear interpolations

    
- gradient2D: structure for defining 


'''



# list of common sample colors (as size-3 numpy array)
colors = {
    'black':                np.array([0,                    0,                  0                   ]),
    'white':                np.array([1,                    1,                  1                   ]),
    'red':                  np.array([1,                    0,                  0                   ]),
    'lime':                 np.array([0,                    1,                  0                   ]),
    'blue':                 np.array([0,                    0,                  1                   ]),
    'yellow':               np.array([1,                    1,                  0                   ]),
    'cyan':                 np.array([0,                    1,                  1                   ]),
    'magenta':              np.array([1,                    0,                  1                   ]),
    'silver':               np.array([0.752941176470588,    0.752941176470588,  0.752941176470588   ]),
    'gray':                 np.array([0.501960784313725,    0.501960784313725,  0.501960784313725   ]),
    'maroon':               np.array([0.501960784313725,    0,                  0                   ]),
    'olive':                np.array([0.501960784313725,    0.501960784313725,  0                   ]),
    'green':                np.array([0,                    0.501960784313725,  0                   ]),
    'purple':               np.array([0.501960784313725,    0,                  0.501960784313725   ]),
    'teal':                 np.array([0,                    0.501960784313725,  0.501960784313725   ]),
    'navy':                 np.array([0,                    0,                  0.501960784313725   ]),
    'dark red':             np.array([0.545098039215686,    0,                  0                   ]),
    'brown':                np.array([0.647058823529412,    0.164705882352941,  0.164705882352941   ]),
    'firebrick':            np.array([0.698039215686274,    0.133333333333333,  0.133333333333333   ]),
    'crimson':              np.array([0.862745098039216,    0.0784313725490196, 0.235294117647059   ]),
    'red':                  np.array([1,                    0,                  0                   ]),
    'tomato':               np.array([1,                    0.388235294117647,  0.27843137254902    ]),
    'coral':                np.array([1,                    0.498039215686275,  0.313725490196078   ]),
    'indian red':           np.array([0.803921568627451,    0.36078431372549,   0.36078431372549    ]),
    'light coral':          np.array([0.941176470588235,    0.501960784313725,  0.501960784313725   ]),
    'dark salmon':          np.array([0.913725490196078,    0.588235294117647,  0.47843137254902    ]),
    'salmon':               np.array([0.980392156862745,    0.501960784313725,  0.447058823529412   ]),
    'light salmon':         np.array([1,                    0.627450980392157,  0.47843137254902    ]),
    'orange red':           np.array([1,                    0.270588235294118,  0                   ]),
    'dark orange':          np.array([1,                    0.549019607843137,  0                   ]),
    'orange':               np.array([1,                    0.647058823529412,  0                   ]),
    'gold':                 np.array([1,                    0.843137254901961,  0                   ]),
    'dark golden rod':      np.array([0.72156862745098,     0.525490196078431,  0.0431372549019608  ]),
    'golden rod':           np.array([0.854901960784314,    0.647058823529412,  0.125490196078431   ]),
    'pale golden rod':      np.array([0.933333333333333,    0.909803921568627,  0.666666666666667   ]),
    'dark khaki':           np.array([0.741176470588235,    0.717647058823529,  0.419607843137255   ]),
    'khaki':                np.array([0.941176470588235,    0.901960784313726,  0.549019607843137   ]),
    'olive':                np.array([0.501960784313725,    0.501960784313725,  0                   ]),
    'yellow':               np.array([1,                    1,                  0                   ]),
    'yellow green':         np.array([0.603921568627451,    0.803921568627451,  0.196078431372549   ]),
    'dark olive green':     np.array([0.333333333333333,    0.419607843137255,  0.184313725490196   ]),
    'olive drab':           np.array([0.419607843137255,    0.556862745098039,  0.137254901960784   ]),
    'lawn green':           np.array([0.486274509803922,    0.988235294117647,  0                   ]),
    'chart reuse':          np.array([0.498039215686275,    1,                  0                   ]),
    'green yellow':         np.array([0.67843137254902,     1,                  0.184313725490196   ]),
    'dark green':           np.array([0,                    0.392156862745098,  0                   ]),
    'green':                np.array([0,                    0.501960784313725,  0                   ]),
    'forest green':         np.array([0.133333333333333,    0.545098039215686,  0.133333333333333   ]),
    'lime':                 np.array([0,                    1,                  0                   ]),
    'lime green':           np.array([0.196078431372549,    0.803921568627451,  0.196078431372549   ]),
    'light green':          np.array([0.564705882352941,    0.933333333333333,  0.564705882352941   ]),
    'pale green':           np.array([0.596078431372549,    0.984313725490196,  0.596078431372549   ]),
    'dark sea green':       np.array([0.56078431372549,     0.737254901960784,  0.56078431372549    ]),
    'medium spring green':  np.array([0,                    0.980392156862745,  0.603921568627451   ]),
    'spring green':         np.array([0,                    1,                  0.498039215686275   ]),
    'sea green':            np.array([0.180392156862745,    0.545098039215686,  0.341176470588235   ]),
    'medium aqua marine':   np.array([0.4,                  0.803921568627451,  0.666666666666667   ]),
    'medium sea green':     np.array([0.235294117647059,    0.701960784313725,  0.443137254901961   ]),
    'light sea green':      np.array([0.125490196078431,    0.698039215686274,  0.666666666666667   ]),
    'dark slate gray':      np.array([0.184313725490196,    0.309803921568627,  0.309803921568627   ]),
    'teal':                 np.array([0,                    0.501960784313725,  0.501960784313725   ]),
    'dark cyan':            np.array([0,                    0.545098039215686,  0.545098039215686   ]),
    'aqua':                 np.array([0,                    1,                  1                   ]),
    'cyan':                 np.array([0,                    1,                  1                   ]),
    'light cyan':           np.array([0.87843137254902,     1,                  1                   ]),
    'dark turquoise':       np.array([0,                    0.807843137254902,  0.819607843137255   ]),
    'turquoise':            np.array([0.250980392156863,    0.87843137254902,   0.815686274509804   ]),
    'medium turquoise':     np.array([0.282352941176471,    0.819607843137255,  0.8                 ]),
    'pale turquoise':       np.array([0.686274509803922,    0.933333333333333,  0.933333333333333   ]),
    'aqua marine':          np.array([0.498039215686275,    1,                  0.831372549019608   ]),
    'powder blue':          np.array([0.690196078431373,    0.87843137254902,   0.901960784313726   ]),
    'cadet blue':           np.array([0.372549019607843,    0.619607843137255,  0.627450980392157   ]),
    'steel blue':           np.array([0.274509803921569,    0.509803921568627,  0.705882352941177   ]),
    'corn flower blue':     np.array([0.392156862745098,    0.584313725490196,  0.929411764705882   ]),
    'deep sky blue':        np.array([0,                    0.749019607843137,  1                   ]),
    'dodger blue':          np.array([0.117647058823529,    0.564705882352941,  1                   ]),
    'light blue':           np.array([0.67843137254902,     0.847058823529412,  0.901960784313726   ]),
    'sky blue':             np.array([0.529411764705882,    0.807843137254902,  0.92156862745098    ]),
    'light sky blue':       np.array([0.529411764705882,    0.807843137254902,  0.980392156862745   ]),
    'midnight blue':        np.array([0.0980392156862745,   0.0980392156862745, 0.43921568627451    ]),
    'navy':                 np.array([0,                    0,                  0.501960784313725   ]),
    'dark blue':            np.array([0,                    0,                  0.545098039215686   ]),
    'medium blue':          np.array([0,                    0,                  0.803921568627451   ]),
    'blue':                 np.array([0,                    0,                  1                   ]),
    'royal blue':           np.array([0.254901960784314,    0.411764705882353,  0.882352941176471   ]),
    'blue violet':          np.array([0.541176470588235,    0.168627450980392,  0.886274509803922   ]),
    'indigo':               np.array([0.294117647058824,    0,                  0.509803921568627   ]),
    'dark slate blue':      np.array([0.282352941176471,    0.23921568627451,   0.545098039215686   ]),
    'slate blue':           np.array([0.415686274509804,    0.352941176470588,  0.803921568627451   ]),
    'medium slate blue':    np.array([0.482352941176471,    0.407843137254902,  0.933333333333333   ]),
    'medium purple':        np.array([0.576470588235294,    0.43921568627451,   0.858823529411765   ]),
    'dark magenta':         np.array([0.545098039215686,    0,                  0.545098039215686   ]),
    'dark violet':          np.array([0.580392156862745,    0,                  0.827450980392157   ]),
    'dark orchid':          np.array([0.6,                  0.196078431372549,  0.8                 ]),
    'medium orchid':        np.array([0.729411764705882,    0.333333333333333,  0.827450980392157   ]),
    'purple':               np.array([0.501960784313725,    0,                  0.501960784313725   ]),
    'thistle':              np.array([0.847058823529412,    0.749019607843137,  0.847058823529412   ]),
    'plum':                 np.array([0.866666666666667,    0.627450980392157,  0.866666666666667   ]),
    'violet':               np.array([0.933333333333333,    0.509803921568627,  0.933333333333333   ]),
    'magenta':              np.array([1,                    0,                  1                   ]),
    'orchid':               np.array([0.854901960784314,    0.43921568627451,   0.83921568627451    ]),
    'medium violet red':    np.array([0.780392156862745,    0.0823529411764706, 0.52156862745098    ]),
    'pale violet red':      np.array([0.858823529411765,    0.43921568627451,   0.576470588235294   ]),
    'deep pink':            np.array([1,                    0.0784313725490196, 0.576470588235294   ]),
    'hot pink':             np.array([1,                    0.411764705882353,  0.705882352941177   ]),
    'light pink':           np.array([1,                    0.713725490196078,  0.756862745098039   ]),
    'pink':                 np.array([1,                    0.752941176470588,  0.796078431372549   ]),
    'antique white':        np.array([0.980392156862745,    0.92156862745098,   0.843137254901961   ]),
    'beige':                np.array([0.96078431372549,     0.96078431372549,   0.862745098039216   ]),
    'bisque':               np.array([1,                    0.894117647058824,  0.768627450980392   ]),
    'blanched almond':      np.array([1,                    0.92156862745098,   0.803921568627451   ]),
    'wheat':                np.array([0.96078431372549,     0.870588235294118,  0.701960784313725   ]),
    'corn silk':            np.array([1,                    0.972549019607843,  0.862745098039216   ]),
    'lemon chiffon':        np.array([1,                    0.980392156862745,  0.803921568627451   ]),
    'light golden yellow':  np.array([0.980392156862745,    0.980392156862745,  0.823529411764706   ]),
    'light yellow':         np.array([1,                    1,                  0.87843137254902    ]),
    'saddle brown':         np.array([0.545098039215686,    0.270588235294118,  0.0745098039215686  ]),
    'sienna':               np.array([0.627450980392157,    0.32156862745098,   0.176470588235294   ]),
    'chocolate':            np.array([0.823529411764706,    0.411764705882353,  0.117647058823529   ]),
    'peru':                 np.array([0.803921568627451,    0.52156862745098,   0.247058823529412   ]),
    'sandy brown':          np.array([0.956862745098039,    0.643137254901961,  0.376470588235294   ]),
    'burly wood':           np.array([0.870588235294118,    0.72156862745098,   0.529411764705882   ]),
    'tan':                  np.array([0.823529411764706,    0.705882352941177,  0.549019607843137   ]),
    'rosy brown':           np.array([0.737254901960784,    0.56078431372549,   0.56078431372549    ]),
    'moccasin':             np.array([1,                    0.894117647058824,  0.709803921568627   ]),
    'navajo white':         np.array([1,                    0.870588235294118,  0.67843137254902    ]),
    'peach puff':           np.array([1,                    0.854901960784314,  0.725490196078431   ]),
    'misty rose':           np.array([1,                    0.894117647058824,  0.882352941176471   ]),
    'lavender blush':       np.array([1,                    0.941176470588235,  0.96078431372549    ]),
    'linen':                np.array([0.980392156862745,    0.941176470588235,  0.901960784313726   ]),
    'old lace':             np.array([0.992156862745098,    0.96078431372549,   0.901960784313726   ]),
    'papaya whip':          np.array([1,                    0.937254901960784,  0.835294117647059   ]),
    'sea shell':            np.array([1,                    0.96078431372549,   0.933333333333333   ]),
    'mint cream':           np.array([0.96078431372549,     1,                  0.980392156862745   ]),
    'slate gray':           np.array([0.43921568627451,     0.501960784313725,  0.564705882352941   ]),
    'light slate gray':     np.array([0.466666666666667,    0.533333333333333,  0.6                 ]),
    'light steel blue':     np.array([0.690196078431373,    0.768627450980392,  0.870588235294118   ]),
    'lavender':             np.array([0.901960784313726,    0.901960784313726,  0.980392156862745   ]),
    'floral white':         np.array([1,                    0.980392156862745,  0.941176470588235   ]),
    'alice blue':           np.array([0.941176470588235,    0.972549019607843,  1                   ]),
    'ghost white':          np.array([0.972549019607843,    0.972549019607843,  1                   ]),
    'honeydew':             np.array([0.941176470588235,    1,                  0.941176470588235   ]),
    'ivory':                np.array([1,                    1,                  0.941176470588235   ]),
    'azure':                np.array([0.941176470588235,    1,                  1                   ]),
    'snow':                 np.array([1,                    0.980392156862745,  0.980392156862745   ]),
    'black':                np.array([0,                    0,                  0                   ]),
    'dim gray':             np.array([0.411764705882353,    0.411764705882353,  0.411764705882353   ]),
    'gray':                 np.array([0.501960784313725,    0.501960784313725,  0.501960784313725   ]),
    'dark gray':            np.array([0.662745098039216,    0.662745098039216,  0.662745098039216   ]),
    'silver':               np.array([0.752941176470588,    0.752941176470588,  0.752941176470588   ]),
    'light gray':           np.array([0.827450980392157,    0.827450980392157,  0.827450980392157   ]),
    'gainsboro':            np.array([0.862745098039216,    0.862745098039216,  0.862745098039216   ]),
    'white smoke':          np.array([0.96078431372549,     0.96078431372549,   0.96078431372549    ]),
    'white':                np.array([1,                    1,                  1                   ])
}






def colorAsNumPy(c):
    f"""
    Function to convert color "c" from any of it structures (see "instanim.structs["color"]")
    to only NumPy structure.
    """
    if isinstance(c, str): return colors[c]
    elif isinstance(c, list): return np.array([*c])
    elif isinstance(c, tuple): return np.array([*c])
    else: return c # assumed to numpy array



def colorLerpFunc(c0, c1, t):
    f"""
    Linear interpolation between two color values. 
    
    t is interpolation position, such that color is "c0" at t=0 and "c1" at t=1.
    Let c0 and c1 have color-structure (see "instanim.structs["color"]")
    Let t be a scalar or a size-N array. All values of t must be within [0, 1].
    """ # not printing doc-string (more on this...)
    
    c0 = colorAsNumPy(c0)
    c1 = colorAsNumPy(c1)

    try: 
        len(t) # then it is an array

        # expand dimensions
        c0 = np.expand_dims(c0, axis=0) # 1x3
        c1 = np.expand_dims(c1, axis=0) # 1x3
        t = np.expand_dims(t, axis=1) # Nx1

        return np.ones((len(t), 1))*c0 + np.matmul(t, c1-c0) # Nx3
    except: # it is not an array
        return c0 + (c1-c0)*t # size-3




class colorMap(): 
    """
    Base class for "colorMap" constructs.
    It is not instantiable.
    """





class colorMapLinear(colorMap):

    def __init__(self, startColor, endColor, *colorsStops):
        """
        Object to generate a linear color-map. A linear color-map generates color
        values that are linear interpolation of the nearest "stop" color values.
    
        All interpolation positions (t) are within [0, 1]. Every linear color-map 
        must have "start_color" (at t=0) and "end_color" (at t=1) "stops" defined. 
        More colors-stops can be added as list-pairs ("colors_stops" input) at other t within [0, 1].
        All color values must have color structure (see "instanim.structs["color"]")
        
        DO NOT set "colorsStops" attribute.
        """ # not printing docstring...

        startColor = colorAsNumPy(startColor)
        endColor = colorAsNumPy(endColor)

        if len(colorsStops)==0: colorsStops = np.vstack(([*startColor, 0], [*endColor, 1]))
        else:            
            colorsStops = np.array([[*colorAsNumPy(colorStop[0]), colorStop[1]] for colorStop in colorsStops])
            colorsStops = np.vstack(([*startColor, 0], colorsStops))
            colorsStops = np.vstack((colorsStops, [*endColor, 1]))

        self.colorsStops = colorsStops[colorsStops[:, 3].argsort()]




    @property
    def reversed(self):
        stops = self.stops
        clrs = self.colors

        colorsStops = [
            [clr, stop] 
        for stop, clr in zip(reversed(stops[1:len(stops)-1]), clrs[1:len(clrs)-1])]
        cmap = colorMapLinear(clrs[len(clrs)-1], clrs[0], *colorsStops)

        return cmap


    @property
    def colors(self):
        return self.colorsStops[:,:3] # Nx3
    @property
    def stops(self):
        return self.colorsStops[:,3] # Nx1


    @property
    def startColor(self):
        return self.colors[0] # 1x3
    @property
    def endColor(self):
        return self.colors[-1]


    def getColors(self, inds):
        """
        Method to get an array of colors (Nx3) based on array of inds (N).
        All values in inds must be within [0, 1].
        """
        colors, stops = self.colorsStops[:,:3], self.colorsStops[:,3]

        for i, end_stop in enumerate(stops[1:]):
            start_stop = stops[i]        

            if i==len(stops)-1:
                sub_inds = inds[inds>=start_stop]
            else:
                sub_inds = inds[inds>=start_stop]
                sub_inds = sub_inds[sub_inds<end_stop]

            if len(sub_inds)>0:
                start_color = colors[i]
                end_color = colors[i+1]                                
                sub_inds = ut.rangenorm(sub_inds, start_stop, end_stop)

                try: out_colors = np.vstack((out_colors, colorLerpFunc(start_color, end_color, sub_inds)))
                except: out_colors = colorLerpFunc(start_color, end_color, sub_inds)

        return out_colors


    def getColor(self, ind):
        """
        Method to get a single (1x3) based on single "ind".
        "ind" must be within [0, 1].        
        """
        colors, stops = self.colorsStops[:,:3], self.colorsStops[:,3]

        for i, end_stop in enumerate(stops[1:]):    
            if i==len(stops)-1: break
            else:
                if ind<end_stop: break

        start_stop = stops[i]

        ind = ut.rangenorm(ind, start_stop, end_stop)

        start_color = colors[i]
        end_color = colors[i+1]    

        return colorLerpFunc(start_color, end_color, ind)                    


    def fromAngles(self, angs, degrees=False):
        ''' 
        Will convert angles into colors based on the linear-colormap; all "angs" must be
        within [-pi, pi] where -pi & pi correspond to start and end colors, respectively.
        Further, "angs" must be an N array of real numbers. 
        If "degrees" is "True", the bounds are taken as [-180, 180] instead.
                
        Return will be Nx3 array of color values.    
        '''

        if degrees: angs = (angs*np.pi)/180 # converting to radians, if degrees True
        angs = ut.rangenorm(angs,-np.pi,np.pi)   

        return self.getColors(angs)



    def getGradient2DColors(self,
        colorFunc, xPixels=1000, yPixels=1000, 
        color_x1=0, color_x2=1, color_y1=0, color_y2=1,
    ):
        
        '''
        Will generate a grid of values for each color component 
        "xPixels" and "yPixels" will determine the size of the grid; they are the M and N, 
        respectively, for an MxN array.
        Output will be a size-3 list containing each component array [r, g, b]
        '''

        # Step 1: generate MxN grid of func-output values. Assume output IS single MxN grid
        # and that all output values MUST be within [0, 1]  
        x = np.linspace(color_x1, color_x2, xPixels) # x-vector (x_pxls points)
        y = np.linspace(color_y1, color_y2, yPixels) # y-vector (y_pxls points)
        
        X, Y = np.meshgrid(x, y)
        f = colorFunc(X, Y)

        # Step 2: initialize MxN BASE arrays for each color component (values initialized to zero).
        # The respective component "lerps" values from each stop-stop interval will be added to
        # these base arrays. All "lerps" values from each interval will have UNIQUE positions 
        # (indices) meaning they won't overlap in positions with "lerps" values from other intervals.
        # In the end, each base component grid will be filled COMPLETELY with "lerps" values; 
        # no position will be without a "lerps" value from an interval.
        rs = np.zeros((yPixels, xPixels))
        gs = np.zeros((yPixels, xPixels))
        bs = np.zeros((yPixels, xPixels))

        stops, clrs = self.stops, self.colors
        for k in range(len(stops)-1):
            # All remaining steps are for EACH stop-stop interval

            # Step 3: extract start and end stops and colors.
            beg, end = stops[k], stops[k+1]
            [ri, gi, bi], [rf, gf, bf] = clrs[k], clrs[k+1]

            # Step 4: generate MxN arrays of linear interpolations ("lerps") for each component 
            # where only values of interpolation are properly calculated (other values garbage)
            ft = deepcopy(f) # use copy of func-outputs grid
            ft = ut.rangenorm(ft, beg, end)

            r_ = ri+(rf-ri)*ft
            g_ = gi+(gf-gi)*ft
            b_ = bi+(bf-bi)*ft

            # Step 5: remove garbage values from each component MxN "lerps" arrays (set to zero)
            if k == len(stops)-2: cond = ut.arraysBetweenAlmost(f, beg, end, rtol=rel_tol, atol=abs_tol)
            else: cond = ut.arraysBetweenAlmost(f, beg, end, rtol=rel_tol, atol=abs_tol, endClose=False) 

            r_[np.logical_not(cond)] = 0 # setting values outside to zero
            g_[np.logical_not(cond)] = 0 # setting values outside to zero
            b_[np.logical_not(cond)] = 0 # setting values outside to zero

            # Step 6: Add "lerps" values to the base component grids, at their determined positions
            rs += r_
            gs += g_
            bs += b_

        return [rs, gs, bs]




    # def preview(self, file_name, override=False):
    #     dir_ = instanim_dir+r"/outputs/color_maps/"

    #     s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 200)
    #     cx = cairo.Context(s)

    #     v=np.linspace(0, 1, 1000)

    #     clrs = self.getColors(v)
    #     for k, clr in enumerate(clrs):
    #         cx.set_source_rgb(*clr)

    #         cx.rectangle(k, 0, 1, 200)
    #         cx.fill()

    #     if override: s.write_to_png(file_name)
    #     else: s.write_to_png(dir_+file_name)



rainbow = colorMapLinear('red', 'violet',
    ['blue', .67],
    ['green', .5],
    ['orange', .17],
    ['indigo', .83],
    ['yellow', .33]
)
hotNcold = colorMapLinear('blue', 'red')
parula = colorMapLinear('indigo', 'gold')



class bitMap2D: pass # more on this...

class gradient: pass



class alphaGradient2D(gradient):
    def __init__(self,
        x1=0, x2=1, y1=0, y2=1,
        func = lambda x,y:1                              
    ):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        self.func = func



class colorGradient2D(gradient):
    def __init__(self,
        x1=0, x2=1, y1=0, y2=1,
        func = lambda x,y:1,   
        cMap=hotNcold                              
    ):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        self.func = func
        self.colorMap = cMap





''' Possible Pipelines... '''


'''
Pipeline 1:

Image -> Nump Array (RGBA) -> Cairo ImamgeSurface (for source)

Pipeline 2:

Gradient Definition (color & alpha) -> NumPy Array -> Cairo ImageSurface (for source)

Pipeline 3:

Single RGBA -> NumPyArray (skip?) -> Cairo ImageSurface (for source)

'''


def imageToArray(path, xResize=None, yResize=None):


    img = Image.open(path)
    w, h = img.size

    # resizing image, if resize options specified
    if xResize: 
        if yResize: img = img.resize((xResize, yResize))
        else: img.resize((xResize, h))
    else: 
        if yResize: img.resize((w, yResize))


    mode, frmt = img.mode, img.format

    if frmt == "PNG": pass # more on this...
    elif frmt == "JPEG": pass # more on this...
    else: pass # more on this...
    # some array processing?...

    arr = np.asarray(img)
    shp = arr.shape

    if mode == "RGBA": pass # more on this...
    elif mode == "RGB": arr = np.dstack((arr, np.ones((shp[0], shp[1]), dtype=int)*255))
    else: pass # more on this...
    # some array processing?...

    arr = arr.astype(np.uint8)

    # reformatting from RGBA to BGRA for Cairo compatibility (which is given preference)
    arr = np.dstack((
        arr[:,:,2], 
        arr[:,:,1],
        arr[:,:,0],
        arr[:,:,3]
    ))

    return arr


# later add bitmap capability...
def gradients2DToArray(
    xPixels=1000, yPixels=1000, 
    alpha=1, color='black'
):        
    f'''
    There are four possible color-alpha combinations. For the case of single (not gradient)
    "alpha" and "color", output is a size-6 list [r, g, b, a, xPixels, yPixels]. For all
    other cases, output is an MxNx4 array with B-G-R-A component ordering along final dimension.
    "
    '''
    

    if isinstance(alpha, alphaGradient2D):
        x = np.linspace(alpha.x1, alpha.x2, xPixels) # x-vector (x_pxls points)
        y = np.linspace(alpha.y1, alpha.y2, yPixels) # y-vector (y_pxls points)
        
        X, Y = np.meshgrid(x, y)
        f = alpha.func(X, Y)

        if isinstance(color, colorGradient2D):
            ''' CASE 4: alphaGradient & colorGradient '''
            cMap = color.colorMap

            assert isinstance(cMap, colorMapLinear) # for now

            [rs, gs, bs] = cMap.getGradient2DColors(
                color.func, xPixels, yPixels, 
                color.x1, color.x2, color.y1, color.y2,
            )

            # not sure about this step...
            rs = np.multiply(rs, f)
            gs = np.multiply(gs, f)
            bs = np.multiply(bs, f)

            arr = np.dstack((bs, gs, rs, f))*255       
            arr = arr.astype(np.uint8)      
        else:               
            ''' CASE 3: alphaGradient & color '''
            color = colorAsNumPy(color)

            rs = np.ones((yPixels, xPixels))*color[0]
            gs = np.ones((yPixels, xPixels))*color[1]
            bs = np.ones((yPixels, xPixels))*color[2]

            # not sure about this step...
            rs = np.multiply(rs, f)
            gs = np.multiply(gs, f)
            bs = np.multiply(bs, f)

            arr = np.dstack((bs, gs, rs, f))*255       
            arr = arr.astype(np.uint8)                 
    else:
        if isinstance(color, colorGradient2D):
            ''' CASE 2: alpha & colorGradient '''
            cMap = color.colorMap

            assert isinstance(cMap, colorMapLinear) # for now

            [rs, gs, bs] = cMap.getGradient2DColors(
                color.func, xPixels, yPixels, 
                color.x1, color.x2, color.y1, color.y2,
            )

            f = np.ones((yPixels, xPixels))*alpha

            # not sure about this step...
            rs = np.multiply(rs, f)
            gs = np.multiply(gs, f)
            bs = np.multiply(bs, f)

            arr = np.dstack((bs, gs, rs, f))*255       
            arr = arr.astype(np.uint8)
        else:            
            ''' CASE 1: alpha & color '''
            color = colorAsNumPy(color)
            
            # formatted in [r, g, b, a, xp, yp]
            arr = [*color, alpha, int(xPixels), int(yPixels)]


    return arr


def arrayToCairo(arr):
    ''' Must either be MxNx4 array or size-6 list '''

    if isinstance(arr, np.ndarray): # MxNx4 array

        shp = arr.shape

        s = cairo.ImageSurface.create_for_data(
            arr, cairo.FORMAT_ARGB32, shp[1], shp[0]
        )          
    
    else: # size-6 list
        [r, g, b, a, xp, yp] = arr

        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, xp, yp) 
        cx = cairo.Context(s)

        cx.set_source_rgba(r, g, b, a)
        cx.rectangle(0, 0, xp, yp)
        cx.fill()            
        
    return s


def colorToCairo(colorVal='red', alphaVal=1, xPixels=1000, yPixels=1000):
    colorVal = colorAsNumPy(colorVal)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, xPixels, yPixels) 
    cx = cairo.Context(s)

    cx.set_source_rgba(*colorVal, alphaVal)
    cx.rectangle(0, 0, xPixels, yPixels)
    cx.fill()           

    return s














if __name__ == "__main__":


    ''' Pipe-line 1 '''


    arr = imageToArray(getSamplePath('lambo.png'))
    s = arrayToCairo(arr)
    
    s.write_to_png(makePreviewPath('lambo_out1.png'))

    arr = imageToArray(getSamplePath('lambo.png'), xResize=300, yResize=700)
    s = arrayToCairo(arr)
    
    s.write_to_png(makePreviewPath('lambo_out2.png'))



    ''' Pipe-Line 2 '''

    arr = gradients2DToArray(
        xPixels=1000, yPixels=1000, 
        alpha=.5, 
        color=colorGradient2D(
            func=lambda x, y: (np.sin(2*np.pi*x) + 1)*.5, 
            cMap=hotNcold        
        )
    )
    s = arrayToCairo(arr)

    name = 'colorGradient1.png'
    filePath = instanim_dir + r'/previews/pics/' + name
    s.write_to_png(filePath)


    arr = gradients2DToArray(
        xPixels=600, yPixels=800, 
        alpha=.8, 
        color=colorGradient2D(
            func=lambda x, y: (np.sin(2*np.pi*x)*np.cos(2*np.pi*y) + 1)*.5, 
            cMap=parula
        )
    )
    s = arrayToCairo(arr)

    name = 'colorGradient2.png'
    filePath = instanim_dir + r'/previews/pics/' + name
    s.write_to_png(filePath)



    arr = gradients2DToArray(
        xPixels=1000, yPixels=1000, 
        color='lime', 
        alpha=alphaGradient2D(
            func=lambda x, y: (np.sin(2*np.pi*x) + 1)*.5
        )        
    )
    s = arrayToCairo(arr)

    name = 'alphaGradient1.png'
    filePath = instanim_dir + r'/previews/pics/' + name
    s.write_to_png(filePath)


    arr = gradients2DToArray(
        xPixels=600, yPixels=800, 
        color='teal', 
        alpha=alphaGradient2D(
            func=lambda x, y: y
        )
    )
    s = arrayToCairo(arr)

    name = 'alphaGradient2.png'
    filePath = instanim_dir + r'/previews/pics/' + name
    s.write_to_png(filePath)


    arr = gradients2DToArray(
        xPixels=600, yPixels=800, 
        alpha=alphaGradient2D(
            func=lambda x, y: x        
        ),
        color=colorGradient2D(
            func=lambda x, y: (np.sin(2*np.pi*x)*np.cos(2*np.pi*y) + 1)*.5, 
            cMap=rainbow        
        )
    )
    s = arrayToCairo(arr)

    name = 'alphaColorGradient1.png'
    filePath = instanim_dir + r'/previews/pics/' + name
    s.write_to_png(filePath)


    ''' Pipe-line 3 '''

    s = colorToCairo('red', .5)

    name = 'alphaColor1.png'
    filePath = instanim_dir + r'/previews/pics/' + name
    s.write_to_png(filePath)




    arr = gradients2DToArray(
        alpha=.5,
        color='purple'
    )
    s = arrayToCairo(arr)

    name = 'alphaColor2.png'
    filePath = instanim_dir + r'/previews/pics/' + name
    s.write_to_png(filePath)

