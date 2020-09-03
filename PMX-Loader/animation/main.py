import pymeshio.pmx
import pymeshio.common
import pymeshio.pmx.reader

class Animation:
    def __init__(self, model):
        #print("Original coordinate : {0}".format(model.vertices[24203].position))
        for i in range(len(model.bones)):
            model.bones[i].position = model.bones[i].position + pymeshio.common.Vector3(1, 1, 1)