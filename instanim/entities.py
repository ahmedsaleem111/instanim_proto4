from instanim import *
import instanim.utilities.displays as dsp


keyFrameMethods = [
    'NA'
    'SMOOTH',
    'LINEAR'
]
# method applies for previous-to-"select" keyFrame
# for this, keyFrame always has 'NA' (not applicable)


def startKeyFrame(ent, **pars):
    for par in ent.pars:
        if par in pars.keys(): val = pars[par]
        else: val = ent.pars[par]            
        ent.keyFrame(par, val, 0, 'NA') # setting to 0th frame by default


class entity: 

    def __init__(self, tag):
        self.tag = tag
        self.keyFrames = {}

    def keyFrame(self, par, val, frame, method='SMOOTH'):
        self.keyFrames[par] = [frame, val, method]

    
    # more on this.... may incorporate somehow in "dynamics" for combined efficiency...
    def interpolate(self, frame):
        # get previous key-Frame
        # get next key-Frame (None, if no next)
        # interpolate based on method (don't if no next)
        pass



# assuming insertion at center
class box(entity):

    pars = {
        'x':0, 
        'y':1,
        'width':10,
        'height':10,
        'border':True,
        'borderColor': 'white',
        'borderAlpha': 1,
        'borderWidth': 1,
        'fillColor': 'coral',
        'fillAlpha': 1
    }

    def __init__(self, tag, **pars):
        super().__init__(tag)
        startKeyFrame(self, **pars)


    def draw(self, context): # cairo context
        assert isinstance(context, cairo.Context)

        bx, by = self.x - self.width/2, self.y - self.height/2
        
        # Drawing Border
        context.set_source_rgba(*dsp.colorAsNumPy(self.borderColor), self.borderAlpha)
        context.set_line_width(self.borderWidth)

        context.line_to(bx, by)
        context.move_to(bx + self.width, by)
        context.move_to(bx + self.width, by + self.height)
        context.move_to(bx, by + self.height)
        context.close_path()

        # Drawing Fill
        context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

        context.set_source_rgba(*dsp.colorAsNumPy(self.fillColor), self.fillAlpha)

        context.line_to(bx, by)
        context.move_to(bx + self.width, by)
        context.move_to(bx + self.width, by + self.height)
        context.move_to(bx, by + self.height)
        context.close_path()

        context.fill()






class wheelBox(entity):

    pars = {
        'x':0, 
        'y':1,
        'width':10,
        'height':10,
        'borderColor': 'white',
        'borderAlpha': 1,
        'borderWidth': 1,
        'wheelStart': 0, # 0 degrees
        'wheelCoverage': 1, # complete coverage
    }

    def __init__(self, tag, **pars):
        super().__init__(tag)
        startKeyFrame(self, **pars)






# assuming insertion at center?
class text(entity):
    pars = {
        'x':0,
        'y':1,
        'scale': [1, 1],
        'fillColor': 'coral',
        'fillAlpha': 1,
        'lineColor': 'white',
        'fillAlpha': 1,
    }

    def __init__(self,
        tag,
        LaTeX_string = r'Hello World!',
        mainFont = r'Consolas',
        mathFont = r'Cambria',
        **pars
    ):
        super().__init__(tag)        
        startKeyFrame(self, **pars)
        self.LaTeX_string = LaTeX_string
        self.mainFont = mainFont
        self.mathFont = mathFont        


        WIDTH = 3
        HEIGHT = 2
        PIXEL_SCALE = 200

        surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                    WIDTH*PIXEL_SCALE,
                                    HEIGHT*PIXEL_SCALE)
        ctx = cairo.Context(surface)
        ctx.scale(PIXEL_SCALE, PIXEL_SCALE)

        ctx.rectangle(0, 0, WIDTH, HEIGHT)
        ctx.set_source_rgb(0.8, 0.8, 1)
        ctx.fill()

        # Drawing code
        ctx.set_source_rgb(1, 0, 0)
        ctx.set_font_size(0.25)
        ctx.select_font_face("Arial",
                            cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_NORMAL)
        ctx.move_to(0.5, 0.5)
        ctx.show_text("Drawing text")
        # End of drawing code

        surface.write_to_png('text.png')    
