import numpy as np
import h5py
from PIL import Image
import os
import os.path
import random
import numpy.ma as ma
import copy
import math
import scipy.misc
import scipy.io as scio

root_dir = '/Users/jeremywang/Desktop/my_six'
obj_id_list = [i for i in range(2, 16)]


def load_batch(target_choose, target_obj, target_frame):
    i = 0
    rgb = np.array(Image.open('{0}/{1}/render/{2}/rgb/{3}.png'.format(root_dir, '%02d' % target_choose[i], '%02d' % target_obj[i], '%04d' % target_frame[i])))

    rgb = rgb[:, :, np.newaxis, :]

    dep = np.array(Image.open('{0}/{1}/render/{2}/depth/{3}.png'.format(root_dir, '%02d' % target_choose[i], '%02d' % target_obj[i], '%04d' % target_frame[i])))
    seg = copy.deepcopy(dep)

    dep = dep[:, :, np.newaxis]

    seg[seg.nonzero()] = target_obj[i]
    seg = seg[:, :, np.newaxis]

    pose = [np.load('{0}/{1}/render/{2}/pose/{3}.npy'.format(root_dir, '%02d' % target_choose[i], '%02d' % target_obj[i], '%04d' % target_frame[i]), encoding="latin1")]
    obj_id = [target_obj[i]]


    for i in range(1, 5):
        t_rgb = np.array(Image.open('{0}/{1}/render/{2}/rgb/{3}.png'.format(root_dir, '%02d' % target_choose[i], '%02d' % target_obj[i], '%04d' % target_frame[i])))
        t_rgb = t_rgb[:, :, np.newaxis, :]
        rgb = np.concatenate((rgb, t_rgb), axis=2)

        t_dep = np.array(Image.open('{0}/{1}/render/{2}/depth/{3}.png'.format(root_dir, '%02d' % target_choose[i], '%02d' % target_obj[i], '%04d' % target_frame[i])))
        t_seg = copy.deepcopy(t_dep)
        t_dep = t_dep[:, :, np.newaxis]
        dep = np.concatenate((dep, t_dep), axis=2)

        t_seg[t_seg.nonzero()] = target_obj[i]
        t_seg = t_seg[:, :, np.newaxis]

        seg = np.concatenate((seg, t_seg), axis=2)

        pose.append(np.load('{0}/{1}/render/{2}/pose/{3}.npy'.format(root_dir, '%02d' % target_choose[i], '%02d' % target_obj[i], '%04d' % target_frame[i]), encoding="latin1"))

        obj_id.append(target_obj[i])


    h, w, d = dep.shape
    dep[dep == 0.0] = 1000000.0

    idx = dep.argmin(axis=2).reshape(-1)
    dep[dep == 1000000.0] = 0.0

    rgb = rgb.reshape(-1, d, 3)
    dep = dep.reshape(-1, d)
    seg = seg.reshape(-1, d)

    rgb = rgb[range(h*w), idx].reshape(h, w, 3)
    dep = dep[range(h*w), idx].reshape(h, w)
    seg = seg[range(h*w), idx].reshape(h, w)

    return rgb, dep, seg, pose, obj_id



def check_exist(seg_merge, pose_batch, id_batch, remain_list, frame_id):
    if frame_id == 0:
        for idx in range(len(id_batch)):
            idd = id_batch[idx]
            mask = ma.getmaskarray(ma.masked_equal(seg_merge, idd))
            if len(mask.nonzero()[0]) > 100:
                remain_list.append(idx)

    rtn_pose = []
    rtn_id = []

    for idx in range(len(id_batch)):
        if idx in remain_list:
            rtn_pose.append(pose_batch[idx])
            rtn_id.append(id_batch[idx])

    return rtn_pose, rtn_id, remain_list




for video_id in range(10000):
    os.makedirs('{0}/syn_data/{1}'.format(root_dir, video_id))

    target_obj = random.sample(obj_id_list, 5)
    target_choose = [random.randint(0, 7), random.randint(0, 7), random.randint(0, 7), random.randint(0, 7), random.randint(0, 7), random.randint(0, 7)]
    target_frame = np.array([random.randint(0, 1980), random.randint(0, 1980), random.randint(0, 1980), random.randint(0, 1980), random.randint(0, 1980), random.randint(0, 1980)])

    frame_id = 0
    remain_list = []

    rgb_merge, depth_merge, seg_merge, pose_batch, id_batch = load_batch(target_choose, target_obj, target_frame)
    pose_batch, id_batch, remain_list = check_exist(seg_merge, pose_batch, id_batch, remain_list, frame_id)

    scipy.misc.imsave('{0}/syn_data/{1}/{2}_rgb.png'.format(root_dir, video_id, frame_id), rgb_merge)
    np.save('{0}/syn_data/{1}/{2}_dep.npy'.format(root_dir, video_id, frame_id), depth_merge)
    scipy.misc.imsave('{0}/syn_data/{1}/{2}_seg.png'.format(root_dir, video_id, frame_id), seg_merge)
    np.save('{0}/syn_data/{1}/{2}_pose.npy'.format(root_dir, video_id, frame_id), pose_batch)
    np.save('{0}/syn_data/{1}/{2}_id.npy'.format(root_dir, video_id, frame_id), id_batch)

    print(id_batch)

    target_frame += 1


    for frame_id in range(1, 10):
        rgb_merge, depth_merge, seg_merge, pose_batch, id_batch = load_batch(target_choose, target_obj, target_frame)
        pose_batch, id_batch, remain_list = check_exist(seg_merge, pose_batch, id_batch, remain_list, frame_id)

        scipy.misc.imsave('{0}/syn_data/{1}/{2}_rgb.png'.format(root_dir, video_id, frame_id), rgb_merge)
        np.save('{0}/syn_data/{1}/{2}_dep.npy'.format(root_dir, video_id, frame_id), depth_merge)
        scipy.misc.imsave('{0}/syn_data/{1}/{2}_seg.png'.format(root_dir, video_id, frame_id), seg_merge)
        np.save('{0}/syn_data/{1}/{2}_pose.npy'.format(root_dir, video_id, frame_id), pose_batch)
        np.save('{0}/syn_data/{1}/{2}_id.npy'.format(root_dir, video_id, frame_id), id_batch)

        target_frame += 1




