import glfw
import numpy
from OpenGL.GL import *
from OpenGL.GL import shaders


def main():

    # initialize
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "NewWindow", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    #           positions         colors
    quad = [-0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
            0.5, -0.5, 0.0,   0.0, 1.0, 0.0,
            0.5, 0.5, 0.0,    0.0, 0.0, 1.0,
            -0.5, 0.5, 0.0,   1.0, 1.0, 1.0]

    indices = [0, 1, 2,  # Each line represents a triangle
               2, 3, 0]

    indices = numpy.array(indices, dtype=numpy.uint32)

    quad = numpy.array(quad, dtype=numpy.float32)

    vertex_shader = """
    #version 330

    in vec3 position;
    in vec3 color;
    out vec3 newColor;

    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }

    """

    fragment_shader = """
    #version 330

    in vec3 newColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """

    shader = shaders.compileProgram(shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                    shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, quad.nbytes, quad, GL_STATIC_DRAW)  # Size in bytes

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, indices.size, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
