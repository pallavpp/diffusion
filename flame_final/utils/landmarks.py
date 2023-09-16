'''
Max-Planck-Gesellschaft zur Foerderung der Wissenschaften e.V. (MPG) is holder of all proprietary rights on this
computer program.

You can only use this computer program if you have closed a license agreement with MPG or you get the right to use
the computer program from someone who is authorized to grant you that right.

Any use of the computer program without a valid license is prohibited and liable to prosecution.

Copyright 2019 Max-Planck-Gesellschaft zur Foerderung der Wissenschaften e.V. (MPG). acting on behalf of its
Max Planck Institute for Intelligent Systems and the Max Planck Institute for Biological Cybernetics.
All rights reserved.

More information about FLAME is available at http://flame.is.tue.mpg.de.
For comments or questions, please email us at flame@tue.mpg.de
'''

import cv2
import sys
import pickle
import numpy as np
import tensorflow as tf

def load_binary_pickle(filepath):
    with open(filepath, 'rb') as f:
        if sys.version_info >= (3, 0):
            data = pickle.load(f, encoding='latin1')
        else:
            data = pickle.load(f)
    return data

def load_embedding( file_path ):
    """ funciton: load landmark embedding, in terms of face indices and barycentric coordinates for corresponding landmarks
    note: the included example is corresponding to CMU IntraFace 49-point landmark format.
    """
    lmk_indexes_dict = load_binary_pickle( file_path )
    lmk_face_idx = lmk_indexes_dict[ 'lmk_face_idx' ].astype( np.uint32 )
    lmk_b_coords = lmk_indexes_dict[ 'lmk_b_coords' ]
    return lmk_face_idx, lmk_b_coords

def tf_get_model_lmks(tf_model, f, lmk_face_idx, lmk_b_coords):
    """Get a differentiable landmark embedding in the FLAME surface"""
    faces = f[lmk_face_idx].astype(np.int32)
    return tf.einsum('ijk,ij->ik', tf.gather(tf_model, faces), tf.convert_to_tensor(lmk_b_coords))

def tf_project_points(points, scale, trans):
    '''
    weak perspective camera
    '''

    return tf.scalar_mul(scale, tf.transpose(tf.linalg.matmul(tf.eye(num_rows=2, num_columns=3, dtype=points.dtype), points, transpose_b=True)) + trans)
