import typing
import moderngl

class MGLObject:       
    def __init__(self, program: moderngl.Program, array: moderngl.VertexArray,
                 framebuffer: typing.Union[moderngl.Framebuffer, None]):

        self.program: moderngl.Program = program
        self.array: moderngl.VertexArray = array

        self.framebuffer: moderngl.Framebuffer = framebuffer
    
    def render(self, screen) -> None:
        if self.framebuffer:
            self.framebuffer.use()
        else:
            screen.use()
        
        self.array.render(moderngl.TRIANGLE_STRIP)
