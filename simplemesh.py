import os
import trimesh
import argparse
import math
import shutil
import einops
import numpy as np
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_dir', type=str, required=True)
parser.add_argument('-I', '--info', action='store_true')
parser.add_argument('-r', '--rotate', nargs='+')
parser.add_argument('-n', '--normalize', type=float)
parser.add_argument('-o', '--output_dir', nargs='?', const=True)

pi = math.pi
args = parser.parse_args()

#skip_textures = True if opt.skip_textures else False


def get_obj(dir_path):
    # print("dir_path:", dir_path)
    if dir_path[-1] == '/':
        dir_path = dir_path[:-1]
    sub_name = dir_path.split('/')[-1]
    # print(sub_name)
    obj_path = os.path.join(dir_path, sub_name + '.obj')
    jpg_path = os.path.join(dir_path, sub_name + '.jpg')

    return obj_path, jpg_path


def display_info(mesh):
    print('[In simplemesh] --info specified, displaying object info...')
    print(f'| Object type: {mesh}')
    print(f'| Object bbox:\n{mesh.bounds}')


def normalize_by_bbox_(mesh, bound):
    """
    Normalizes the mesh to [-bound, bound]^3.

    Note that this is in-place.
    """
    print(f'[In simplemesh] --normalize specified, target bounding box is [-{bound:.4f}, {bound:.4f}]')

    bbox_min, bbox_max = mesh.bounds
    # mesh_vertices = np.array(mesh.vertices)
    # print(np.min(mesh_vertices, axis=0))
    # print(np.max(mesh_vertices, axis=0))
    # print("bound:", bound)
    # print(bbox_min, bbox_max)
    bbox_cent = .5 * (bbox_min + bbox_max)

    axis_extent = bbox_max - bbox_min
    max_extent = axis_extent.max()

    scale_transfm = trimesh.transformations.scale_matrix(factor=2*bound/max_extent)
    trans_transfm = trimesh.transformations.translation_matrix(direction=-bbox_cent)

    mesh.apply_transform(trans_transfm)
    mesh.apply_transform(scale_transfm)


def rotate_by_deg_(mesh, axis, deg):
    if axis == 'x':
        direction = [1,0,0]
    elif axis == 'y':
        direction = [0,1,0]
    elif axis == 'z':
        direction = [0,0,1]
    else:
        print(f'[In simplemesh] --rotate specified, but with invalid rotation axis: {axis}')
        return
        
    print(f'[In simplemesh] --rotate specified, will rotate {deg:.4f} degrees around the {axis} axis')

    rot_transfm = trimesh.transformations.rotation_matrix(
        angle=deg*pi/180,
        direction=direction,
        point=[0,0,0])
    mesh.apply_transform(rot_transfm)


def export(mesh, subject_name, output_dir, jpg_path):
    os.makedirs(os.path.join(output_dir, subject_name), exist_ok=True)
    mesh.export(os.path.join(output_dir, subject_name, subject_name + ".obj"))
    jpg_new_path = os.path.join(output_dir, subject_name, subject_name + ".jpg")
    shutil.copyfile(jpg_path, jpg_new_path)


if __name__ == '__main__':
    input_dirs = [dirnames for _, dirnames, _ in os.walk(args.input_dir)]
    print("length of input_dirs:", len(input_dirs[0]))
    count = 0
    for subject_name in tqdm(input_dirs[0]):
        count += 1
        print("the number of {0}:", format(count))
        obj_path, jpg_path = get_obj(os.path.join(args.input_dir, subject_name))
        mesh = trimesh.load(obj_path)#, skip_textures=skip_textures)
    
        if args.info:
            display_info(mesh)

        if args.rotate is not None:
            i = 0
            while i < len(args.rotate):
                axis = args.rotate[i]
                deg = eval(args.rotate[i+1])
                rotate_by_deg_(mesh, axis, deg)
                i = i + 2
            del i, axis, deg

        if args.normalize is not None:
            bound = args.normalize
            normalize_by_bbox_(mesh, bound)
            del bound

        if args.output_dir is not None:
            output_dir = args.output_dir
            export(mesh, subject_name, output_dir, jpg_path)

    print("finished................")