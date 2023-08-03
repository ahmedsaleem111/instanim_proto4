from instanim.scene import *





b = box('box',
    startFrame = 30,
    frames = 30,
    x = 100,
    y = 100,
    height = 400,
    width = 600,
    fill = True,
    borderColor = 'red',
    borderWidth=10        
)
b.addKeyFrame('x', 300, frame=9, method = keyFrameMethods.LINEAR)
b.addKeyFrame('y', 300, frame=9, method = keyFrameMethods.LINEAR)
b.addKeyFrame('x', 500, frame=19, method = keyFrameMethods.LINEAR)
b.addKeyFrame('y', 100, frame=19, method = keyFrameMethods.LINEAR)
b.addKeyFrame('x', 700, frame=29, method = keyFrameMethods.LINEAR)
b.addKeyFrame('y', 300, frame=29, method = keyFrameMethods.LINEAR)

b.addKeyFrame('height', 200, frame=9, method = keyFrameMethods.LINEAR)
b.addKeyFrame('width', 200, frame=9, method = keyFrameMethods.LINEAR)
b.addKeyFrame('height', 100, frame=19, method = keyFrameMethods.LINEAR)
b.addKeyFrame('width', 100, frame=19, method = keyFrameMethods.LINEAR)
b.addKeyFrame('height', 200, frame=29, method = keyFrameMethods.LINEAR)
b.addKeyFrame('width', 200, frame=29, method = keyFrameMethods.LINEAR)



b2 = box('box1',
    startFrame = 15,
    frames = 30,
    x = 100,
    y = 100,
    height = 400,
    width = 600,
    fill = True,
    borderColor = 'lime',
    borderWidth=10        
)
b2.addKeyFrame('x', 300, frame=9, method = keyFrameMethods.LINEAR)
b2.addKeyFrame('y', 300, frame=9, method = keyFrameMethods.LINEAR)
b2.addKeyFrame('x', 500, frame=19, method = keyFrameMethods.LINEAR)
b2.addKeyFrame('y', 100, frame=19, method = keyFrameMethods.LINEAR)
b2.addKeyFrame('x', 700, frame=29, method = keyFrameMethods.LINEAR)
b2.addKeyFrame('y', 300, frame=29, method = keyFrameMethods.LINEAR)

b2.addKeyFrame('height', 200, frame=9, method = keyFrameMethods.LINEAR)
b2.addKeyFrame('width', 200, frame=9, method = keyFrameMethods.LINEAR)
b2.addKeyFrame('height', 100, frame=19, method = keyFrameMethods.LINEAR)
b2.addKeyFrame('width', 100, frame=19, method = keyFrameMethods.LINEAR)
b2.addKeyFrame('height', 200, frame=29, method = keyFrameMethods.LINEAR)
b2.addKeyFrame('width', 200, frame=29, method = keyFrameMethods.LINEAR)


b3 = box('box2',
    startFrame = 45,
    frames = 30,
    x = 100,
    y = 100,
    height = 400,
    width = 600,
    fill = True,
    borderColor = 'cyan',    
    borderWidth=10        
)
b3.addKeyFrame('x', 300, frame=9, method = keyFrameMethods.LINEAR)
b3.addKeyFrame('y', 300, frame=9, method = keyFrameMethods.LINEAR)
b3.addKeyFrame('x', 500, frame=19, method = keyFrameMethods.LINEAR)
b3.addKeyFrame('y', 100, frame=19, method = keyFrameMethods.LINEAR)
b3.addKeyFrame('x', 700, frame=29, method = keyFrameMethods.LINEAR)
b3.addKeyFrame('y', 300, frame=29, method = keyFrameMethods.LINEAR)

b3.addKeyFrame('height', 200, frame=9, method = keyFrameMethods.LINEAR)
b3.addKeyFrame('width', 200, frame=9, method = keyFrameMethods.LINEAR)
b3.addKeyFrame('height', 100, frame=19, method = keyFrameMethods.LINEAR)
b3.addKeyFrame('width', 100, frame=19, method = keyFrameMethods.LINEAR)
b3.addKeyFrame('height', 200, frame=29, method = keyFrameMethods.LINEAR)
b3.addKeyFrame('width', 200, frame=29, method = keyFrameMethods.LINEAR)





for key, val in b.keyFrames.items():
    print(key, val)


s = Scene(entities=[b, b2, b3], frames=90)
# s.exportImage('box.png', frame = 10)


s.export('testBox.mp4')