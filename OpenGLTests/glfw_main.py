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

    triangle = [-0.5, -0.5, 0.0,
                0.5, -0.5, 0.0,
                0.0, 0.5, 0.0]

    triangle = numpy.array(triangle, dtype=numpy.float32)

    vertex_shader = """
    #version 330

    in vec4 position;

    void main()
    {
        gl_Position = position;
    }

    """

    fragment_shader = """
    #version 330

    void main()
    {
        gl_FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
    }
    """

    shader = shaders.compileProgram(shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                    shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, 36, triangle, GL_STATIC_DRAW)  # Size in bytes

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(position)

    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)

        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
