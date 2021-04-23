# encoding:utf-8
import os
import trimesh
import numpy as np
import argparse


class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class MyFile(object):
    folders = []
    outFolders = []
    count = 0

    def get_obj(self, dir_path):
        # print("dir_path:", dir_path)
        if dir_path[-1] == '/':
            dir_path = dir_path[:-1]
        sub_name = dir_path.split('/')[-1]
        # print(sub_name)
        obj_path = os.path.join(dir_path, sub_name + '.obj')

        return obj_path


class MyNormalize(object):
    # def __init__(self, x):
    #     self.x =
    minP = Point(1000, 10000, 10000)
    maxP = Point(0, 0, 0)

    def get_bounding_box(self, mesh_array):
        """
        获取物体的最小x,y,z和最大的x,y,z
        :param p:
        :return:
        """
        self.minP.x, self.minP.y, self.minP.z = np.min(mesh_array, axis=0)
        self.maxP.x, self.maxP.y, self.maxP.z = np.max(mesh_array, axis=0)
        # self.minP.x = p.x if p.x < self.minP.x else self.minP.x
        # self.minP.y = p.y if p.y < self.minP.y else self.minP.y
        # self.minP.z = p.z if p.z < self.minP.z else self.minP.z
        # self.maxP.x = p.x if p.x > self.maxP.x else self.maxP.x
        # self.maxP.y = p.y if p.y > self.maxP.y else self.maxP.y
        # self.maxP.z = p.z if p.z > self.maxP.z else self.maxP.z

    def get_bounding_box_length(self):
        """
        获取包围盒的最大长度
        :return:
        """
        box_len = self.maxP.x - self.minP.x
        if box_len < (self.maxP.y - self.minP.y):
            box_len = self.maxP.y - self.minP.y
        if box_len < (self.maxP.z - self.minP.z):
            box_len = self.maxP.z - self.minP.z
        return box_len

    def do_normalize(self, box_len, points):
        """
        归一化处理
        :param center_p: 物体的中心点
        :param box_len: 包围盒的一半
        :param points:要进行归一化处理的点
        :return:
        """
        new_points = []
        for point in points:
            x = (point.x - self.minP.x) * 2 / box_len - 1
            y = (point.y - self.minP.y) * 2 / box_len - 1
            z = (point.z - self.minP.z) * 2 / box_len - 1
            # new_points.append(Point(x, y, z))
            new_points.append([x,y,z])
        return new_points

    def read_points(self, mesh):
        """
        读取一个obj文件里的点
        :param filename:
        :return:
        """
        points = []
        vertice = mesh.vertices
        for v in vertice:
            points.append(Point(float(v[0]), float(v[1]), float(v[2])))
        return points


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-i', '--input', type=str, required=True)
    # parser.add_argument('-I', '--info', action='store_true')
    # parser.add_argument('-r', '--rotate', nargs='+')
    # parser.add_argument('-n', '--normalize', type=float)
    # parser.add_argument('-o', '--output', nargs='?', const=True)
    #
    # args = parser.parse_args()

    myFile = MyFile()
    myNormalize = MyNormalize()
    basePath = "/home/bbnc/papers_with_code/OBJ_normalize/homework"

    input_dirs = [dirnames for _, dirnames, _ in os.walk(basePath)]
    print(len(input_dirs[0]))
    count = 0
    for subject_name in input_dirs[0]:
        count += 1
        obj_path = myFile.get_obj(os.path.join(basePath, subject_name))
        print("obj_path:", obj_path)
        print("count:", count)
        mesh = trimesh.load(obj_path, process=False)
        print("mesh:", mesh.vertices)
        points = myNormalize.read_points(mesh)
        break
        # print("points:", points)

        # for point in points:
        #     myNormalize.get_bounding_box(point)
        # boxLength = myNormalize.get_bounding_box_length()
        # points = myNormalize.do_normalize(boxLength, points)
        #
        # mesh.vertices = points
        # mesh.export(obj_path)
        # print("obj_path:{0}|count:{1}|".format(obj_path, count))
