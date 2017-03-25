import pyrr
import glfw
import numpy
from PIL import Image
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
    cube = [-0.5, -0.5, 0.5,  1.0, 0.0, 0.0,
            0.5, -0.5, 0.5,   0.0, 1.0, 0.0,
            0.5, 0.5, 0.5,    0.0, 0.0, 1.0,
            -0.5, 0.5, 0.5,   1.0, 1.0, 1.0,

            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
            0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
            0.5, 0.5, -0.5, 0.0, 0.0, 1.0,
            -0.5, 0.5, -0.5, 1.0, 1.0, 1.0]

    indices = [0, 1, 2, 2, 3, 0,  # Each line represents a triangle
               4, 5, 6, 6, 7, 4,
               4, 5, 1, 1, 0, 4,
               6, 7, 3, 3, 2, 6,
               5, 6, 2, 2, 1, 5,
               7, 4, 0, 0, 3, 7]

    indices = numpy.array(indices, dtype=numpy.uint32)

    cube = numpy.array(cube, dtype=numpy.float32)

    vertex_shader = """
    #version 330

    in vec3 position;
    in vec3 color;
    uniform mat4 transform;
    out vec3 newColor;

    void main()
    {
        gl_Position = transform * vec4(position, 1.0f);
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
    glBufferData(GL_ARRAY_BUFFER, cube.nbytes, cube, GL_STATIC_DRAW)  # Size in bytes

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
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
        rot = numpy.array(rot_x * rot_y)

        transform_loc = glGetUniformLocation(shader, "transform")
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, rot)

        glDrawElements(GL_TRIANGLES, indices.size, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
