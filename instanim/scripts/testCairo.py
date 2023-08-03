import cairo
from instanim.scene import *

class B:

    def __init__(self,
        x = 0,
        y = 1,
        width = 10,
        height = 10,
        border = True,
        borderColor = "white",
        borderAlpha = 1,
        borderWidth = 1,
        fill = False,
        fillColor = "coral",
        fillAlpha = 1    
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border
        self.borderColor = borderColor
        self.borderAlpha = borderAlpha
        self.borderWidth = borderWidth
        self.fill = fill
        self.fillColor = fillColor
        self.fillAlpha = fillAlpha


    def draw(self, context): # cairo context
        assert isinstance(context, cairo.Context)

        bx, by = self.x - self.width/2, self.y - self.height/2

        # Drawing Fill
        if self.fill is True:
            context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

            context.set_source_rgba(*dsp.colorAsNumPy(self.fillColor), self.fillAlpha)

            context.rectangle(self.x, self.y, self.width, self.height)

            context.close_path()

            context.fill()

        # Drawing Border
        context.set_source_rgba(*dsp.colorAsNumPy(self.borderColor), self.borderAlpha)
        context.set_line_width(self.borderWidth)

        context.rectangle(self.x, self.y, self.width, self.height)

        context.close_path()
        context.stroke()



surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)


cx = cairo.Context(surf)
mat = cairo.Matrix(xx=1, xy=0, x0=0, yx=0, yy=-1, y0=1000)
cx.transform(mat)   

cx.set_source_rgba(0, 0, 0, 1)

cx.rectangle(0, 0, 1000, 1000)
cx.fill()


b = B(
    x = 100,
    y = 100,
    height = 800,
    width = 800,
    borderWidth=10,
    fill = True        
)


b.draw(cx)

fileName = 'testCairo.png'
surf.write_to_png(instanim_dir+r"/exports/pics/" + fileName)