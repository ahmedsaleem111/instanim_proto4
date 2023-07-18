from instanim.dynamics import *





class Scene:

    def __init__(self,
        entities=[],
        frames=600, 
        width=1920, height=1080,
        backgroundColor='black',               
        backgroundAlpha=1,
    ):                 
        self.entities = entities
        self.frames = frames
        self.width = width
        self.height = height
        self.backgroundColor = backgroundColor
        self.backgroundAlpha = backgroundAlpha


    # will return a cairo ImageSurface object
    def frame(self, frame): # frame must be integer >= 0 and <= frames
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)

        context = cairo.Context(surf)    
        mat = cairo.Matrix(xx=1, xy=0, x0=0, yx=0, yy=-1, y0=self.height)
        context.transform(mat)   

        for ent in self.entities:
            assert isinstance(ent, entity)
            ent.interpolate(frame) # interpolate between keyFrames
            ent.draw(context)

        return surf



    async def a_preview(self, fileName, fps=30, override=False):
        if override: pth_ = fileName
        else: pth_ = instanim_dir+r"/exports/clips/" + fileName

        frame_tasks = list()
        length = len(t)
        for frameNumber in range(self.frames):

            task = asyncio.create_task(pre_proc_frame(i, self.frame(frameNumber), length))
            frame_tasks.append(task)
            task.add_done_callback(frame_tasks.remove)

        all_frames_data = await asyncio.gather(*frame_tasks)

        pipe = ffmpegCairoPipe(self.width, self.height, pth_, fps=fps)
        pipe.open()

        for i, frame_data in all_frames_data: render_with_ffmpeg(frame_data, pipe)

        pipe.close()


    ''' fps is for ALL frames within interval [0, scene_dur] where first frame is at t = 0 '''
    ''' incomplete'''
    def export(self, fileName, fps=30):
        asyncio.run(self.a_preview(fileName, fps))







