from PIL import Image
import numpy as np
import scipy.misc
import scipy.io as scio

obj_root = "/media/psf/Home/Desktop/YCB/YCB_models/002_master_chef_can"

v = []
vn = []
vt = []
f = []

img = np.array(Image.open('{0}/texture_map.png'.format(obj_root)))

print(img.shape)

height = len(img) - 1
width = len(img[0]) - 1

input_file = open('{0}/textured.obj'.format(obj_root), 'r')
while 1:
    input_line = input_file.readline()
    if not input_line:
        break
    if input_line[-1:] == '\n':
        input_line = input_line[:-1]
    if input_line[0:2] == 'v ':
    	input_line = input_line.split(' ')
    	v.append([float(input_line[1]), float(input_line[2]), float(input_line[3])])
    elif input_line[0:2] == 'vt':
    	input_line = input_line.split(' ')
    	x = float(input_line[1])
    	y = float(input_line[2])
    	x = int(x * height)
    	y = int(y * width)
    	if x > height:
    		x = height
    	if y > width:
    		y = width
    	vt.append(img[y][x])
    elif input_line[0:2] == 'vn':
    	input_line = input_line.split(' ')
    	vn.append([float(input_line[1]), float(input_line[2]), float(input_line[3])])
input_file.close()

input_file = open('{0}/textured.ply'.format(obj_root), 'r')
while 1:
    input_line = input_file.readline()
    if not input_line:
        break
    if input_line[-1:] == '\n':
        input_line = input_line[:-1]
    input_line = input_line.split(' ')
    if input_line[0] != '3':
    	continue
    f.append([int(input_line[1]), int(input_line[2]), int(input_line[3])])
input_file.close()


print(len(v), len(vn), len(vt), len(f))

fw = open('{0}/obj.ply'.format(obj_root), 'w')
fw.write('ply\n')
fw.write('format ascii 1.0\n')
fw.write('comment VCGLIB generated\n')
fw.write('element vertex {0}\n'.format(len(v)))
fw.write('property float x\n')
fw.write('property float y\n')
fw.write('property float z\n')
fw.write('property float nx\n')
fw.write('property float ny\n')
fw.write('property float nz\n')
fw.write('property uchar red\n')
fw.write('property uchar green\n')
fw.write('property uchar blue\n')
fw.write('property uchar alpha\n')
fw.write('element face {0}\n'.format(len(f)))
fw.write('property list uchar int vertex_indices\n')
fw.write('end_header\n')

for i in range(len(v)):
	fw.write('{0} {1} {2} {3} {4} {5} {6} {7} {8} 255\n'.format(v[i][0], v[i][1], v[i][2], vn[i][0], vn[i][1], vn[i][2], vt[i][0], vt[i][1], vt[i][2]))
for i in range(len(f)):
	fw.write('3 {0} {1} {2}\n'.format(f[i][0], f[i][1], f[i][2]))
fw.close()
