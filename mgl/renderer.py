from pge.types import Singleton

from pge.mgl import MGLObject

import moderngl
import pygame
import typing
import array
import os

@Singleton
class MGLRenderer:
    '''
    Singleton class handling for Moderngl rendering.
    '''

    class Texture:
        '''
        Container for `moderngl.Texture` related functions.
        '''

        @staticmethod
        def create(name: str, sequential: typing.Optional[bool] = False) -> None:
            '''
            Creates a `moderngl.Texture` with a given `name`.

            Can optionally specify if it is `sequential`.
            '''

            assert MGLRenderer.instanced
            mgl: MGLRenderer = MGLRenderer()

            texture: moderngl.Texture = mgl.context.texture(mgl.screen_dimensions, 4)

            if sequential:
                texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
                texture.swizzle = 'RGBA'
            else:
                texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
                texture.swizzle = 'BGRA'

            mgl.textures[name] = (texture, mgl.t_i)
            mgl.textures[name][0].use(mgl.t_i)

            mgl.t_i += 1

        @staticmethod
        def write(name: str, surface: pygame.Surface) -> None:
            '''
            Writes to a given texture given a `name` and a pygame `surface`.
            '''
                        
            assert MGLRenderer.instanced

            mgl: MGLRenderer = MGLRenderer()
            mgl.textures[name][0].write(surface.get_view('1'))

    class Object:
        '''
        Container for `MGLObject` related functions.
        '''

        @staticmethod
        def create(sequential: bool, name: str, vert: typing.Union[None, str], 
                   frag: typing.Union[None, str], textures: typing.Sequence[str]) -> None:
            '''
            Creates a `MGLObject`, must specify if it is `sequential`. 
            
            Must also provide a `name`, a `vert` and `frag` shader and a sequence of `textures`.

            If `vert` or `frag` is passed `None`. It will use the default shader.
            '''

            assert MGLRenderer.instanced
            mgl: MGLRenderer = MGLRenderer()

            if vert == None:
                vert = 'default'
            
            if frag == None:
                frag = 'default'

            program: moderngl.Program = mgl.context.program(
                vertex_shader=mgl._shaders['vert'][vert],
                fragment_shader=mgl._shaders['frag'][frag]
            )

            if sequential:
                buffer: moderngl.Buffer = mgl.buffers[1]
            else:
                buffer: moderngl.Buffer = mgl.buffers[0]            

            array: moderngl.VertexArray =  mgl.context.vertex_array(
                program,
                [(buffer, '2f 2f', 'vert', 'texcoord')]
            )

            for texture in textures:
                program[texture] = mgl.textures[texture][1]

            obj: MGLObject = MGLObject(sequential, program, buffer, None, array)
            mgl.objects[name] = obj

        def uniform(name: str, attribute: str, value: any) -> None:
            '''
            Adds a uniform variable to an `MGLObject`.

            Takes the `name` of the object, the `attribute` and as its `value`.
            '''

            assert MGLRenderer.instanced
            mgl: MGLRenderer = MGLRenderer()       

            obj: MGLObject = mgl.objects[name]
            obj.program[attribute] = value
            
    def __init__(self, screen_dimensions: tuple[int, int]) -> None:
        '''
        Initializes the renderer given `screen_dimensions` 
        '''

        self.screen_dimensions: tuple[int, int] = screen_dimensions
        self.context: moderngl.Context = moderngl.create_context()

        self._shaders: dict[str, dict[str, str]] = { 'vert': {}, 'frag': {} }
        path = os.path.join('pge', '_data', 'shaders')
        for shader in os.listdir(path):
            with open(os.path.join(path, shader), 'r') as s:
                self._shaders[shader.split('.')[1]][shader.split('.')[0]] = s.read()  

        self.buffers: tuple[moderngl.Buffer, moderngl.Buffer] = (
            self.context.buffer(
                data=array.array('f', [
                    -1.0, 1.0, 0.0, 0.0,
                    1.0, 1.0, 1.0, 0.0,
                    -1.0, -1.0, 0.0, 1.0,
                    1.0, -1.0, 1.0, 1.0
                ])
            ),

            self.context.buffer(
                data=array.array('f', [
                    -1.0, 1.0, 0.0, 1.0,
                    1.0, 1.0, 1.0, 1.0,
                    -1.0, -1.0, 0.0, 0.0,
                    1.0, -1.0, 1.0, 0.0
                ])
            ),
        )

        self.textures: dict[str, tuple[moderngl.Texture, int]] = {}
        self.t_i: int = 0

        self.objects: dict[str, MGLObject] = {}

    @property
    def shaders(self) -> dict[str, list[str]]:
        '''
        Returns a dictionary of all currently stored vertex and fragment 
        shaders.
        '''

        shaders: dict[str, list[str]] = {}
        for shader in self._shaders:
            shaders[shader] = list(self._shaders[shader].keys())

        return shaders
    
    def load(self, path) -> None:
        '''
        Loads all of the shaders into the shader dictionary given a 
        `path` to a directory.
        '''
                
        for shader in os.listdir(path):
            with open(os.path.join(path, shader), 'r') as s:
                self._shaders[shader.split('.')[1]][shader.split('.')[0]] = s.read()  

    def render(self) -> None:
        '''
        Render all of the current `MGLObjects`.
        '''

        objs: list[MGLObject] = list(o for o in self.objects.values())
        for obj in objs:
            obj.render(self.context.screen)
