import os
import sys
import math
import numpy as np
import cv2
import math
import random
from pysixd.transformations import random_rotation_matrix, euler_matrix

class pose_change():
    def __init__(self):
        self.x_x = 0.0
        self.x_y = 0.0
        self.x_z = 0.0

        self.v_x = 0.0
        self.v_y = 0.0
        self.v_z = 0.0

        self.a_x = 0.0
        self.a_y = 0.0
        self.a_z = 0.0

        self.bound_x = [-200.0, 200.0]
        self.bound_y = [-200.0, 200.0]
        self.bound_z = [-500.0, 10.0]

        self.bound_vx = [-10.0, 10.0]
        self.bound_vy = [-10.0, 10.0]
        self.bound_vz = [-10.0, 10.0]

        self.bound_ax = [-1.0, 1.0]
        self.bound_ay = [-1.0, 1.0]
        self.bound_az = [-1.0, 1.0]

        self.x_x = random.uniform(self.bound_x[0], self.bound_x[1])
        self.x_y = random.uniform(self.bound_y[0], self.bound_y[1])
        self.x_z = random.uniform(self.bound_z[0], self.bound_z[1])

        self.v_x = random.uniform(self.bound_vx[0], self.bound_vx[1])
        self.v_y = random.uniform(self.bound_vy[0], self.bound_vy[1])
        self.v_z = random.uniform(self.bound_vz[0], self.bound_vz[1])

        self.a_x = random.uniform(self.bound_ax[0], self.bound_ax[1])
        self.a_y = random.uniform(self.bound_ay[0], self.bound_ay[1])
        self.a_z = random.uniform(self.bound_az[0], self.bound_az[1])

        ########################################################################

        self.Rx_x = 0.0
        self.Rx_y = 0.0
        self.Rx_z = 0.0

        self.Rv_x = 0.0
        self.Rv_y = 0.0
        self.Rv_z = 0.0

        self.Ra_x = 0.0
        self.Ra_y = 0.0
        self.Ra_z = 0.0

        self.Rbound_vx = [-math.pi/28.0, math.pi/28.0]
        self.Rbound_vy = [-math.pi/28.0, math.pi/28.0]
        self.Rbound_vz = [-math.pi/28.0, math.pi/28.0]

        self.Rbound_ax = [-math.pi/180.0, math.pi/180.0]
        self.Rbound_ay = [-math.pi/180.0, math.pi/180.0]
        self.Rbound_az = [-math.pi/180.0, math.pi/180.0]

        self.Rx_x = random.uniform(-math.pi, math.pi)
        self.Rx_y = random.uniform(-math.pi, math.pi)
        self.Rx_z = random.uniform(-math.pi, math.pi)

        self.Rv_x = random.uniform(self.Rbound_vx[0], self.Rbound_vx[1])
        self.Rv_y = random.uniform(self.Rbound_vy[0], self.Rbound_vy[1])
        self.Rv_z = random.uniform(self.Rbound_vz[0], self.Rbound_vz[1])

        self.Ra_x = random.uniform(self.Rbound_ax[0], self.Rbound_ax[1])
        self.Ra_y = random.uniform(self.Rbound_ay[0], self.Rbound_ay[1])
        self.Ra_z = random.uniform(self.Rbound_az[0], self.Rbound_az[1])

        #######################################################################

        self.start_frame = 0

    def step(self, model, frame):
        if frame == 0:
            R = euler_matrix(self.Rx_x, self.Rx_y, self.Rx_z)[:3, :3]
            t = np.array([self.x_x, self.x_y, self.x_z])
        else:
            if (frame - self.start_frame) > 10:
                self.a_x = random.uniform(self.bound_ax[0], self.bound_ax[1])
                self.a_y = random.uniform(self.bound_ay[0], self.bound_ay[1])
                self.a_z = random.uniform(self.bound_az[0], self.bound_az[1])
                self.Ra_x = random.uniform(self.Rbound_ax[0], self.Rbound_ax[1])
                self.Ra_y = random.uniform(self.Rbound_ay[0], self.Rbound_ay[1])
                self.Ra_z = random.uniform(self.Rbound_az[0], self.Rbound_az[1])
                self.start_frame = frame
            
            self.v_x += self.a_x
            self.v_y += self.a_y
            self.v_z += self.a_z

            self.x_x += self.v_x
            self.x_y += self.v_y
            self.x_z += self.v_z

            self.Rv_x += self.Ra_x
            self.Rv_y += self.Ra_y
            self.Rv_z += self.Ra_z

            self.Rx_x += self.Rv_x
            self.Rx_y += self.Rv_y
            self.Rx_z += self.Rv_z

            if self.x_x < self.bound_x[0]:
                self.v_x = -self.v_x
            if self.x_x > self.bound_x[1]:
                self.v_x = -self.v_x

            if self.x_y < self.bound_y[0]:
                self.v_y = -self.v_y
            if self.x_y > self.bound_y[1]:
                self.v_y = -self.v_y

            if self.x_z < self.bound_z[0]:
                self.v_z = -self.v_z
            if self.x_z > self.bound_z[1]:
                self.v_z = -self.v_z

            R = euler_matrix(self.Rx_x, self.Rx_y, self.Rx_z)[:3, :3]
            t = np.array([self.x_x, self.x_y, self.x_z])

            # print(R, t)

        model['pts'] = np.dot(model['pts'], R.T) + t

        return model, R, t
