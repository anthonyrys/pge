import moderngl

class MGLObject:       
    def __init__(self, program: moderngl.Program, 
                 buffer: moderngl.Buffer, array: moderngl.VertexArray):

        self.program: moderngl.Program = program
        self.buffer: moderngl.BUffer = buffer

        self.array: moderngl.VertexArray = array
    
    def render(self, screen) -> None:
        screen.use()
        
        self.array.render(moderngl.TRIANGLE_STRIP)
