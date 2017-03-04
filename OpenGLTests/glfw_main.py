import glfw
from OpenGL.GL import *


def main():

    # initialize
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "NewWindow", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
