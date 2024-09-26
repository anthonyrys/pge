from pge.types import Singleton

from pge.mgl import MGLObject

import moderngl
import pygame
import typing
import array
import os

@Singleton
class MGLRenderer:
    class Texture:
        @staticmethod
        def create(name: str) -> None:
            assert MGLRenderer.instanced
            mgl: MGLRenderer = MGLRenderer()

            texture: moderngl.Texture = mgl.context.texture(mgl.screen_dimensions, 4)

            texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
            texture.swizzle = 'BGRA'

            mgl.textures[name] = (texture, mgl.t_i)
            mgl.textures[name][0].use(mgl.t_i)

            mgl.t_i += 1

        @staticmethod
        def write(name: str, surface: pygame.Surface) -> None:       
            assert MGLRenderer.instanced

            mgl: MGLRenderer = MGLRenderer()
            mgl.textures[name][0].write(surface.get_view('1'))

    class Object:
        @staticmethod
        def create(name: str, vert: typing.Union[None, str], 
                   frag: typing.Union[None, str], textures: typing.Sequence[str]) -> None:

            assert MGLRenderer.instanced
            mgl: MGLRenderer = MGLRenderer()

            if isinstance(textures, str):
                textures = [textures]

            if vert == None:
                vert = 'default'
            
            if frag == None:
                frag = 'default'

            program: moderngl.Program = mgl.context.program(
                vertex_shader=mgl._shaders['vert'][vert],
                fragment_shader=mgl._shaders['frag'][frag]
            )

            buffer: moderngl.Buffer = mgl.buffers[0]            

            array: moderngl.VertexArray =  mgl.context.vertex_array(
                program,
                [(buffer, '2f 2f', 'vert', 'texcoord')]
            )

            for texture in textures:
                program[texture] = mgl.textures[texture][1]

            obj: MGLObject = MGLObject(program, None, array)
            mgl.objects[name] = obj

        @staticmethod
        def uniform(name: str, attribute: str, value: any) -> None:
            assert MGLRenderer.instanced
            mgl: MGLRenderer = MGLRenderer()       

            obj: MGLObject = mgl.objects[name]
            obj.program[attribute] = value
            
    def __init__(self, screen_dimensions: tuple[int, int]):
        self.screen_dimensions: tuple[int, int] = screen_dimensions
        self.context: moderngl.Context = moderngl.create_context()

        self._shaders: dict[str, dict[str, str]] = { 'vert': {}, 'frag': {} }
        path = os.path.join('pge', '_resources', 'shaders')
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
        shaders: dict[str, list[str]] = {}
        for shader in self._shaders:
            shaders[shader] = list(self._shaders[shader].keys())

        return shaders
    
    def load(self, path: str) -> None:     
        for shader in os.listdir(path):
            with open(os.path.join(path, shader), 'r') as s:
                self._shaders[shader.split('.')[1]][shader.split('.')[0]] = s.read()  

    def render(self) -> None:
        objs: list[MGLObject] = list(o for o in self.objects.values())
        for obj in objs:
            obj.render(self.context.screen)
