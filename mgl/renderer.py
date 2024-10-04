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
        def create(name: str, primary: typing.Optional[bool] = True,
                   dimensions: typing.Optional[tuple[int, int]] = None,
                   dtype: typing.Optional[str] = 'f1') -> None:

            assert MGLRenderer.instanced
            mgl: MGLRenderer = MGLRenderer()

            if dimensions:
                texture: moderngl.Texture = mgl.context.texture(dimensions, 4, dtype=dtype)
            else:
                texture: moderngl.Texture = mgl.context.texture(mgl.screen_dimensions, 4, dtype=dtype)

            if primary:
                texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
                texture.swizzle = 'BGRA'
            else:
                texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
                texture.swizzle = 'RGBA'

            mgl.textures[name] = (texture, mgl.t_i)
            mgl.textures[name][0].use(mgl.t_i)

            mgl.t_i += 1

        @staticmethod
        def write(name: str, data: any) -> None:       
            assert MGLRenderer.instanced

            mgl: MGLRenderer = MGLRenderer()

            if isinstance(data, pygame.Surface):
                mgl.textures[name][0].write(data.get_view('1'))
            else:
                mgl.textures[name][0].write(data)

    class Framebuffer:
        @staticmethod
        def create(buffer_name: str, texture_name: str) -> None:
            assert MGLRenderer.instanced
            mgl: MGLRenderer = MGLRenderer()

            if texture_name not in mgl.textures:
                mgl.Texture.create(texture_name, primary=False)

            framebuffer: moderngl.Framebuffer = mgl.context.framebuffer(color_attachments=[mgl.textures[texture_name][0]])
            mgl.framebuffers[buffer_name] = framebuffer

    class Object:
        @staticmethod
        def create(name: str, vert: typing.Union[None, str], 
                   frag: typing.Union[None, str], textures: typing.Sequence[str],
                   framebuffer: typing.Optional[str] = None) -> None:

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

            if framebuffer:
                buffer: moderngl.Buffer = mgl.buffers[1]
                framebuffer: moderngl.Framebuffer = mgl.framebuffers[framebuffer]
            else:
                buffer: moderngl.Buffer = mgl.buffers[0]        

            array: moderngl.VertexArray =  mgl.context.vertex_array(
                program,
                [(buffer, '2f 2f', 'vert', 'texcoord')]
            )

            for texture in textures:
                program[texture] = mgl.textures[texture][1]

            obj: MGLObject = MGLObject(program, array, framebuffer)
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

        self.framebuffers: dict[str, moderngl.Framebuffer] = {}
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
