import numpy


class ObjLoader(object):
    def __init__(self):
        self.__vert_coords = []
        self.__text_coords = []
        self.__norm_coords = []

        self.__vertex_index = []
        self.__texture_index = []
        self.__normal_index = []

        self.__model = []

        self.model = None

    def load_model(self, file_path):
        with open(file_path) as obj_file:
            for line in obj_file.readlines():

                if line.startswith("#"):
                    continue

                values = line.split()
                if not values:
                    continue

                if values[0].lower() == "v":
                    self.__vert_coords.append(values[1:4])
                    continue

                if values[0].lower() == "vt":
                    self.__text_coords.append(values[1:3])
                    continue

                if values[0].lower() == "vn":
                    self.__norm_coords.append(values[1:4])
                    continue

                if values[0].lower() == "f":
                    face_i = []
                    text_i = []
                    norm_i = []
                    for v in values[1:4]:
                        w = v.split("/")
                        face_i.append(int(w[0]) - 1)
                        text_i.append(int(w[1]) - 1)
                        norm_i.append(int(w[2]) - 1)

                    self.__vertex_index.append(face_i)
                    self.__texture_index.append(text_i)
                    self.__normal_index.append(norm_i)

        self.__vertex_index = [item for sublist in self.__vertex_index for item in sublist]
        self.__texture_index = [item for sublist in self.__texture_index for item in sublist]
        self.__normal_index = [item for sublist in self.__normal_index for item in sublist]

        for i in self.__vertex_index:
            self.__model.extend(self.__vert_coords[i])

        for i in self.__texture_index:
            self.__model.extend(self.__text_coords[i])

        for i in self.__normal_index:
            self.__model.extend(self.__norm_coords[i])

        self.model = numpy.array(self.__model, dtype=numpy.float32)
