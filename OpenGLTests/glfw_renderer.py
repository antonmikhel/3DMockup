import glfw
import pyrr
import numpy
import ctypes
import ObjLoader
import ShaderLoader
from PIL import Image
from OpenGL import GL


def main():

    # initialize glfw
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    obj = ObjLoader.ObjLoader()
    obj.load_model(r"Objects\coffee_mug_uv_small.obj")
    model = obj.model

    stride = (9 * obj.num_vertex) * model.itemsize

    shader = ShaderLoader.compile_shader(r"Shaders\cube_vs.vert", r"Shaders\cube_fs.frag")

    vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, model.nbytes, model, GL.GL_STATIC_DRAW)

    # position
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, model.itemsize * 3, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)

    # texture
    GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, model.itemsize * 2, ctypes.c_void_p(stride))
    GL.glEnableVertexAttribArray(1)

    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)

    # Set the texture wrapping parameters
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)

    # Set texture filtering parameters
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

    # load image
    image = Image.open(r"D:\Dev\Resources\Images for products\512x512tex.jpg")
    img_data = numpy.array(list(image.getdata()), numpy.uint8)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, image.width, image.height, 0,
                    GL.GL_RGB, GL.GL_UNSIGNED_BYTE, img_data)
    GL.glEnable(GL.GL_TEXTURE_2D)

    GL.glUseProgram(shader)

    GL.glClearColor(0.2, 0.3, 0.2, 1.0)
    GL.glEnable(GL.GL_DEPTH_TEST)
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -15.0]))

    projection = pyrr.matrix44.create_perspective_projection_matrix(45.0, 800/600, 0.1, 100.0)

    model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, -5.0, 0.0]))

    view_loc = GL.glGetUniformLocation(shader, "view")
    proj_loc = GL.glGetUniformLocation(shader, "projection")
    model_loc = GL.glGetUniformLocation(shader, "model")

    GL.glUniformMatrix4fv(view_loc, 1, GL.GL_FALSE, view)
    GL.glUniformMatrix4fv(proj_loc, 1, GL.GL_FALSE, projection)
    GL.glUniformMatrix4fv(model_loc, 1, GL.GL_FALSE, model)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
        # rot = numpy.array(rot_x * rot_y)
        rot = numpy.array(rot_y)

        transform_loc = GL.glGetUniformLocation(shader, "transform")
        GL.glUniformMatrix4fv(transform_loc, 1, GL.GL_FALSE, rot)

        GL.glDrawArrays(GL.GL_TRIANGLES, 0, obj.num_vertex)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
