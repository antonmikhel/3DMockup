from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileProgram, compileShader


def load_shader(shader_file):
    with open(shader_file) as sh_f:
        shader_source = sh_f.read()

    return str.encode(shader_source)


def compile_shader(vertex_shader, fragment_shader):
    vert_shader = load_shader(vertex_shader)
    frag_shader = load_shader(fragment_shader)

    shader = compileProgram(compileShader(vert_shader, GL_VERTEX_SHADER),
                            compileShader(frag_shader, GL_FRAGMENT_SHADER))

    return shader
