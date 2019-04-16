from PIL import Image
import numpy as np
import scipy.misc
import scipy.io as scio

obj_root = "/Users/jeremywang/Desktop/YCB/YCB_models/061_foam_brick"
obj_id = 21

fw = open('{0}/obj_{1}.ply'.format(obj_root, '%02d' % obj_id), 'w')
input_file = open('{0}/obj.ply'.format(obj_root), 'r')
while 1:
    input_line = input_file.readline()
    if not input_line:
        break
    if input_line[-1:] == '\n':
        input_line = input_line[:-1]

    ori_input_line = input_line
    input_line = input_line.split(' ')
    
    #print(input_line)
    if len(input_line) == 11:
    	fw.write('{0} {1} {2} {3} {4} {5} {6} {7} {8} 255\n'.format(float(input_line[0]) * 1000.0, float(input_line[1]) * 1000.0, float(input_line[2]) * 1000.0, input_line[3], input_line[4], input_line[5], input_line[6], input_line[7], input_line[8]))
    else:
    	fw.write('{0}\n'.format(ori_input_line))
input_file.close()
fw.close()