import moderngl

class MGLObject:
    '''
    Container for storing rendering information.
    '''
            
    def __init__(self, sequential: bool, program: moderngl.Program, 
                 buffer: moderngl.Buffer, framebuffer: moderngl.Framebuffer,
                 array: moderngl.VertexArray) -> None:
        '''
        Initializes the object given the `sequential`, the `program`, 
        `buffer`, `framebuffer`, and `array`.
        '''

        self.sequential: bool = sequential

        self.program: moderngl.Program = program
        self.buffer: moderngl.BUffer = buffer
        self.framebuffer: moderngl.Framebuffer = framebuffer

        self.array: moderngl.VertexArray = array
    
    def render(self, screen) -> None:
        '''
        Renders the object onto the `screen`.

        If it is `sequential`, it will render onto the framebuffer
        instead.
        '''

        if self.sequential:
            self.framebuffer.use()
        else:
            screen.use()
        
        self.array.render(moderngl.TRIANGLE_STRIP)
