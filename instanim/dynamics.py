from instanim.entities import *





class ffmpegCairoPipe:
    def __init__(self, width, height, output_path, fps=30):
        self.dimensions = (width, height,)
        self.pixel_encode = "bgra"
        self.fps = fps
        self.output_path = str(output_path)
    def _make_command(self,):
         args = ['ffmpeg',]  # ffmpeg command
         #input args
         args += ['-f', 'rawvideo', '-vcodec', 'rawvideo',
                  '-s', '%dx%d' % self.dimensions, '-pix_fmt',
                  self.pixel_encode, '-r', str(self.fps), '-i', '-', '-y']
        #output args
         args += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', self.output_path ]
         return args
    def open(self):
        import subprocess
        command = self._make_command() 
        self._ffmpeg_subproc = subprocess.Popen(command, shell=False,
            stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)
        self._stream = self._ffmpeg_subproc.stdin
    def add_frame(self, frame_data):
        self._stream.write(frame_data)
    def close(self):
        self._stream.close()
        return self._ffmpeg_subproc.wait()

async def pre_proc_frame(i, frame, length):
    print('('+str(round((i+1)/length*100, 2))+'%) Processing Frame '+str(i))
    frame.flush()
    return (i, frame.get_data())

def render_with_ffmpeg(frame_data, pipe):
    assert isinstance(pipe, ffmpegCairoPipe)
    pipe.add_frame(frame_data)




'''
In the future, have capability:
- To check if curve is one-to-one within specified domain (x0, x1)
- With above ^^ satisifed, calculate "inv_curve" automatically; no need to input separately
'''
class rateForm():

    def __init__(self, x0=0, x1=1, curve=lambda x:x, invCurve=None):
        self.curve = curve # must be a one-to-one y=f(x) lambda (f(x)=x by default)
        self.curveStart = x0
        self.curveEnd = x1

        if not (invCurve is None):
            inSet = np.linspace(x0, x1, 1000)
            outSet = self.curve(inSet)
            invSet = invCurve(outSet)

            if not np.allclose(inSet, invSet, rtol=0, atol=1e-9):
                raise Exception('Inverse curve must be exact inverse of original curve within specified domain [x0, x1].')

            self.inverseCurve = invCurve
        else: self.inverseCurve = None


    # apply rateform curve on time vector t relative to time interval [t0, t1] 
    def apply(self, t0, t1, t):

        i0, i1 = self.curveStart, self.curveEnd # input side of time curve
        o0, o1 = self.curve(i0), self.curve(i1) # output side of time curve
        # step 1: go from dynamics time to input side of rateform curve
        t = ut.rangeform(t, t0, t1, i0, i1)
        # step 2: apply rateform curve
        t = self.curve(t)
        # step 3: go from output side of rateform curve back to dynamics time
        return ut.rangeform(t, o0, o1, t0, t1) 


    def inverseApply(self, t0, t1, t):
        if self.inverseCurve is None:
            raise Exception('"inverseApply" method only accessible if "inverseCurve" is defined.')

        i0, i1 = self.curveStart, self.curveEnd # input side of time curve
        o0, o1 = self.curve(i0), self.curve(i1) # output side of time curve
        # step 1: go from dynamics time to input side of rateform curve
        t = ut.rangeform(t, t0, t1, o0, o1)
        # step 2: apply rateform curve
        t = self.inverseCurve(t)
        # step 3: go from output side of rateform curve back to dynamics time
        return ut.rangeform(t, i0, i1, t0, t1) 






# def patternGroup(overallDur, method='STEP_LINEAR_SCALE_CONSTANT', acts=[], vals=[]):
#     LEN = len(acts)
    
#     if method=='STEP_LINEAR_SCALE_CONSTANT':
#         print('hereeeA')


#         # takes a single value between 0 and 1
#         assert len(vals)==1
#         scale = vals[0]

#         assert scale>0 and scale<1
        
#         dur = scale*overallDur
        
#         finalStep = overallDur-dur
#         step = finalStep/(LEN-1)

#         if LEN==0: return acts # essentially do nothing
#         elif LEN==1: 
#             act = acts[0]
#             act.start=0
#             act.dur = dur
#             return [act]        
#         elif LEN>=2:

#             print('hereee')
#             newActs=[]
#             for k, act in enumerate(acts):
#                 assert isinstance(act, Action)
#                 act.start = step*k
#                 act.dur = dur
#                 newActs.append(act)
#             return newActs
        
#     elif method=='STEP_LINEAR_SCALE_CONSTANT_REVERSED':
#         # takes a single value between 0 and 1
#         assert len(vals)==1
#         scale = vals[0]

#         assert scale>0 and scale<1
        
#         dur = scale*overallDur
        
#         firstStep = overallDur-dur
#         step = firstStep/(LEN-1)

#         if LEN==0: return acts # essentially do nothing
#         elif LEN==1: 
#             act = acts[0]
#             act.start=firstStep
#             act.dur = dur
#             return [act]        
#         elif LEN>=2:
#             newActs=[]
#             for k, act in enumerate(acts):
#                 assert isinstance(act, Action)
#                 act.start = step*(LEN-1-k)
#                 act.dur = dur
#                 newActs.append(act)
#             return newActs
        
        





