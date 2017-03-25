import cv2
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

    #           positions         colors           Texture coords
    quad = [-0.5, -0.5, 0.0,      1.0, 0.0, 0.0,   0.0, 0.0,
             0.5, -0.5, 0.0,      0.0, 1.0, 0.0,   1.0, 0.0,
             0.5,  0.5, 0.0,      0.0, 0.0, 1.0,   1.0, 1.0,
            -0.5,  0.5, 0.0,      1.0, 1.0, 1.0,   0.0, 1.0
            ]

    indices = [0, 1, 2,  # Each line represents a triangle
               2, 3, 0]

    indices = numpy.array(indices, dtype=numpy.uint32)

    quad = numpy.array(quad, dtype=numpy.float32)

    vertex_shader = """
    #version 330

    in layout(location = 0) vec3 position;
    in layout(location = 1) vec3 color;
    in layout(location = 2) vec2 inTexCoords;
    
    out vec3 newColor;
    out vec2 outTexCoords;

    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
        outTexCoords = inTexCoords;
    }

    """

    fragment_shader = """
    #version 330

    in vec3 newColor;
    in vec2 outTexCoords;
    
    out vec4 outColor;
    uniform sampler2D samplerTex;

    void main()
    {
        outColor = texture(samplerTex, outTexCoords);
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

    # position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    # texture_coords = glGetAttribLocation(shader, "inTexCoords")
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img_data = cv2.imread(r"D:\Dev\Resources\Images for products\TIMOTHY-HULL-1005_lg.jpg",
                          cv2.CV_LOAD_IMAGE_COLOR).astype(numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_data.shape[1], img_data.shape[0], 0,
                 GL_RGB, GL_UNSIGNED_BYTE, img_data)

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
