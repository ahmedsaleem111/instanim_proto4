import svgelements as svgel
import utils.utilities as ut


'''
Module currently tested for svg fonts generated in inkscape only.
Prior to use, good practice is to scope .svg file; each glyph
should be tied to its own path and output for each glyph
can be 1 or more contours.
'''

''' 
    scans file and will output a list of open or close paths. For consistency with
    svg formatting, output will have two levels of nesting; a 'paths_list' which is a 
    a list of path lists which is a list of paths. There is option of flattening list.
    
    DISCLAIMERS: 
        i.  Some svg elements missing from testing (i.e. 'arc'). Will include later. 
        ii. Some elements get saved as strokes (with a prominent width) when they really 
            should be saved as close-paths (contours) (i.e. a division-line). These objects
            will not get extracted because they cannot be converted to contours. Currently,
            there is no precise work-around for this, so will have to manually add an 
            "approximate" shape corresponding to the "apparent" contour inside the target 
            entity (i.e. text2D).
'''

def pathsParse(file, flatten=False):
    svg = svgel.SVG.parse(file)
    els = list(svg.elements())

    paths_list=[]
    for el in els:
        if isinstance(el, svgel.Path):
    
            paths=[]
            segs = el._segments
            path_='close' # identifier to initiate new path (once path is closed, new path must start)
            for i in segs:
                if isinstance(i, svgel.Close):
                    # 'Close' element always signifies that a path is closing. If path has content
                    #  it adds the content as a close path to paths (with tag 'closePath'). If path
                    #  has no content (i.e. '[]'), does nothing. This is like hitting 'Close' after
                    # 'Move' so it's not really a path. If close path is added, path is set to 'close' 
                    # so next iteration knows it was preceded by a close path.

                    if path_!=[]: # path has content so closing valid
                        path_.append('closePath') # add tag to specify that path is closed
                        paths.append(path_) # add close path to paths
                        path_='close'
                    
                elif isinstance(i, svgel.Move):
                    # 'Move' element always signifies new path. If path is 'close' it iniates a new path 
                    # and if path has content it adds content as an open path (since it was never 'closed' 
                    # prior) to paths and then iniates new. If path has no content (i.e. '[]'), does nothing. 
                    # This is like hitting 'Move' after 'Move' so it's not really a path.

                    if path_=='close':
                        path_=[] # iniating new path since 'close' identified
                    elif path_!=[]: # path has content 
                        path_.append('openPath') # add tag to specify that path is open
                        paths.append(path_)  # add open path to paths
                        path_=[] # iniating new
                        
                elif isinstance(i, svgel.Line):
                    if path_=='close': 
                        raise Exception('A closed path needs to be followed by a new path (a "Move" element).')
                    
                    p0 = [i.start.x,i.start.y]
                    p1 = [i.end.x,i.end.y]
                    path_.append(ut.linearInterpolateSegment2D(p0, p1))

                elif isinstance(i, svgel.QuadraticBezier):
                    if path_=='close': 
                        raise Exception('A closed path needs to be followed by a new path (a "Move" element).')

                    p0 = [i.start.x,i.start.y]
                    p1 = [i.control.x,i.control.y]
                    p2 = [i.end.x,i.end.y]
                    path_.append(ut.quadraticBezierSegment2D(p0, p1, p2))

                elif isinstance(i, svgel.CubicBezier):
                    if path_=='close': 
                        raise Exception('A closed path needs to be followed by a new path (a "Move" element).')

                    p0 = [i.start.x,i.start.y]
                    p1 = [i.control1.x,i.control1.y]
                    p2 = [i.control2.x,i.control2.y]
                    p3 = [i.end.x,i.end.y]
                    path_.append(ut.cubicBezierSegment2D(p0, p1, p2, p3))               

            paths_list.append(paths)


    paths_list_new=[]
    for paths in paths_list:
        for path_ in paths:
            if path_[-1] == 'closePath': 
                paths_list_new.append([ut.parametricJoin2D(*path_[:len(path_)-1], res=30, N=500),'closePath'])
            elif path_[-1] == 'openPath': 
                paths_list_new.append([ut.parametricJoin2D(*path_[:len(path_)-1], res=30, N=500),'openPath'])

    if flatten: paths_list_new=[path_ for paths in paths_list_new for path_ in paths]

    return paths_list_new

