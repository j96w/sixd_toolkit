import torch.utils.data as data
from PIL import Image
import os
import os.path
import numpy.ma as ma
import scipy.misc
import scipy.io as scio
import numpy as np

dep = np.array(Image.open('/Users/jeremywang/Desktop/output/render/01/depth/0000.png'))

cam_cx = 325.26110
cam_cy = 242.04899
cam_fx = 572.41140
cam_fy = 573.57043


width = 640
height = 480

# near = 0.40427
# far = 10.0682
# right = 512.0
# left = 0.0
# top = 512.0
# bottom = 0.0

# resolutionX = 512.0
# resolutionY = 512.0

# print(m)

xmap = np.array([[j for i in range(width)] for j in range(height)])
ymap = np.array([[i for i in range(width)] for j in range(height)])

depth_masked = dep.flatten()[:, np.newaxis].astype(np.float32)
# print(depth_masked)
# depth_masked = depth_masked / np.linalg.norm(depth_masked)
# print(depth_masked)
xmap_masked = xmap.flatten()[:, np.newaxis].astype(np.float32)
ymap_masked = ymap.flatten()[:, np.newaxis].astype(np.float32)

pt2 = depth_masked * 1
pt0 = (ymap_masked - cam_cx) * pt2 / cam_fx
pt1 = (xmap_masked - cam_cy) * pt2 / cam_fy
cloud = np.concatenate((pt0, pt1, pt2), axis=1)



R = [[1.0, 0.0, 0.0], 
    [0.0, -1.0, 0.0],
    [0.0, 0.0, -1.0]]
R = np.array(R)
t = np.array([0, 0, 400])

cloud = np.dot(np.dot(cloud - t, R) - t, R)

fw = open('/Users/jeremywang/Desktop/aaa_cld.xyz', 'w')
for it in cloud:
   fw.write('{0} {1} {2}\n'.format(it[0], it[1], it[2]))
fw.close()