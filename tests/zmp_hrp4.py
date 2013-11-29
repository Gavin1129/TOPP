# -*- coding: utf-8 -*-
# Copyright (C) 2013 Quang-Cuong Pham <cuong.pham@normalesup.org>
#
# This file is part of the Time-Optimal Path Parameterization (TOPP) library.
# TOPP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
sys.path.append('..')

import TOPPbindings
import TOPPpy
import TOPPopenravepy
import time
import string

from pylab import *
from numpy import *
from openravepy import *

ion()

########################### Robot ################################
env = Environment()
robotfile = "../robots/hrp4r.dae"
baselinkname = "BODY"
robot = TOPPopenravepy.LoadFloat(env,robotfile,baselinkname) #Load a robot with dummy joints that mimick floating base
n=robot.GetDOF()
dof_lim=robot.GetDOFLimits()
vel_lim=robot.GetDOFVelocityLimits()
robot.SetDOFLimits(-10*ones(n),10*ones(n))
robot.SetDOFVelocityLimits(100*vel_lim)


############################ Tunings ############################
discrtimestep = 1e-2
integrationtimestep = 1e-3
reparamtimestep = 1e-3
passswitchpointnsteps = 5
tuningsstring = "%f %f %f %d"%(discrtimestep,integrationtimestep,reparamtimestep,passswitchpointnsteps)


############################ Trajectory ############################

q0 = array([  1.37383090e-16,   1.37383090e-16,   1.37383090e-16,
         1.37383090e-16,   1.37383090e-16,   1.37383090e-16,
         1.37383090e-16,   1.37383090e-16,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,  -1.32645019e-02,
        -1.00000003e+00,   2.00000006e+00,  -3.27249286e-01,
        -7.85398163e-03,   0.00000000e+00,   2.00712867e-02,
        -3.82052575e-01,   7.19250178e-01,  -3.27074692e-01,
        -1.91986222e-02,   1.39626330e-01,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,  -5.23598696e-02,
        -1.74532927e-01,   0.00000000e+00,  -5.23598789e-01,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         3.20594657e-09,   0.00000000e+00,  -5.23598696e-02,
         1.50000000e+00,   0.00000000e+00,  -5.23598789e-01,
         0.00000000e+00,   0.00000000e+00,   1.37383090e-16,
        -3.20594658e-09,   1.37383090e-16,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00])
q1 = array([  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
        -3.09314791e-16,   0.00000000e+00,  -3.09314791e-16,
         0.00000000e+00,  -3.09314791e-16,   0.00000000e+00,
        -3.09314791e-16,  -5.00000000e-01,   0.00000000e+00,
         1.00000000e+00,   1.00000000e+00,  -3.27249235e-01,
        -7.85398163e-03,   0.00000000e+00,   2.00712864e-02,
        -3.82052573e-01,   7.19250185e-01,  -3.27074702e-01,
        -1.91986218e-02,   1.50000000e+00,   5.00000000e-01,
         0.00000000e+00,   0.00000000e+00,  -1.00000000e+00,
        -5.00000000e-01,   5.00000000e-01,  -5.23598776e-01,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,  -2.00000000e+00,
         1.00000000e+00,   0.00000000e+00,  -1.00000000e+00,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00])
v=0.3
ndoffull = len(q0)
qd0=[v]*ndoffull
qd1=[v]*ndoffull
T = 1.5

activedofs = zeros(ndoffull)
activedofs[16] = 1 #R_HIP_Y
activedofs[17] = 1 #R_HIP_R
activedofs[18] = 1 #R_HIP_P
activedofs[19] = 1 #R_KNEE_P
activedofs[20] = 1 #R_ANKLE_P
activedofs[21] = 1 #R_ANKLE_R
activedofs[22] = 1 #L_HIP_Y
activedofs[23] = 1 #L_HIP_R
activedofs[24] = 1 #L_HIP_P
activedofs[25] = 1 #L_KNEE_P
activedofs[26] = 1 #L_ANKLE_P
activedofs[27] = 1 #L_ANKLE_R
activedofs[28] = 1 #CHEST_P
activedofs[29] = 1 #CHEST_Y
activedofs[32] = 1 #R_SHOULDER_P
activedofs[33] = 1 #R_SHOULDER_R
activedofs[34] = 1 #R_SHOULDER_Y
activedofs[35] = 1 #R_ELBOW_P
activedofs[41] = 1 #L_SHOULDER_P
activedofs[42] = 1 #L_SHOULDER_R
activedofs[43] = 1 #L_SHOULDER_Y
activedofs[44] = 1 #L_ELBOW_P

robot.activedofs = activedofs
ndof = int(sum(activedofs))
trajectorystring = "%f\n%d"%(T,ndof)
for i in range(ndoffull):
    if(activedofs[i])>0.1:
        if(abs(q0[i]-q1[i])>1e-5):
            a,b,c,d = TOPPpy.Interpolate3rdDegree(q0[i],q1[i],qd0[i],qd1[i],T)
        else:
            a,b,c,d = 0,0,0,q0[i]
        trajectorystring += "\n%f %f %f %f"%(d,c,b,a)


trajectorystring = """1.500000
22
0.0 0.0 1.99242076297 -1.32221433021
0.0 0.0 2.53280855643 -1.67759722295
0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0
0.0 0.0 0.967382109132 -0.642750868261
0.0 0.0 -0.519933641176 0.348891374481
0.0 0.0 2.89830573159 -1.93488398449
0.0 0.0 -2.14170672114 1.44939278452
0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0
0.0 0.0 3.13256805344 -2.08537050225
0.0 0.0 4.59613512542 -3.04279209114
0.0 0.0 4.81882377745 -3.21312086562
0.0 0.0 -3.18430860851 2.12838441106
0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0"""

traj0 = TOPPpy.PiecewisePolynomialTrajectory.FromString(trajectorystring)


activelinks = ones(len(robot.GetLinks()))
for i in range(len(activelinks)):
    if(robot.GetLinks()[i].GetMass()<0.1):
        activelinks[i] = 0
robot.activelinks = activelinks

#tvect,xzmp,yzmp = TOPPopenravepy.ComputeZMP(traj0,robot,0.01)

############################ Constraints ############################

taumin = -ones(ndof)*45
taumax = ones(ndof)*30
xmax = 0.15
xmin = 0.02
ymax = 0.15
ymin = -0.08
zmplimits = [xmin,xmax,ymin,ymax]
vmax = ones(ndof)*3
t0 = time.time()
constraintstring = string.join([str(x) for x in activedofs]) + "\n" + string.join([str(x) for x in activelinks]) + "\n" + string.join([str(x) for x in taumin]) + "\n" + string.join([str(a) for a in taumax]) + "\n" +  string.join([str(a) for a in zmplimits]) + "\n" + string.join([str(a) for a in vmax])


############################ Run TOPP ############################
t1 = time.time()
x = TOPPbindings.TOPPInstance("ZMPTorqueLimits",constraintstring,trajectorystring,tuningsstring,robot);

t2 = time.time()
ret = x.RunComputeProfiles(0,0)
t3 = time.time()

if(ret == 1):
    x.ReparameterizeTrajectory()

t4 = time.time()

################ Plotting the MVC and the profiles #################
x.WriteProfilesList()
x.WriteSwitchPointsList()
profileslist = TOPPpy.ProfilesFromString(x.resprofilesliststring)
switchpointslist = TOPPpy.SwitchPointsFromString(x.switchpointsliststring)
TOPPpy.PlotProfiles(profileslist,switchpointslist,5)


##################### Plotting the trajectories #####################
if(ret == 1):
    x.WriteResultTrajectory()
    traj1 = TOPPpy.PiecewisePolynomialTrajectory.FromString(x.restrajectorystring)
    dtplot = discrtimestep
    TOPPpy.PlotKinematics(traj0,traj1,dtplot,vmax)
    TOPPopenravepy.PlotTorques(robot,traj0,traj1,dtplot,taumin,taumax,3)
    TOPPopenravepy.PlotZMP(robot,traj0,traj1,zmplimits,dtplot,4)


print "\n--------------"
print "Python preprocessing: ", t1-t0
print "Building TOPP Instance: ", t2-t1
print "Compute profiles: ", t3-t2
print "Reparameterize trajectory: ", t4-t3
print "Total: ", t4-t0
print "Trajectory duration (estimate): ", x.resduration
if(ret == 1):
    print "Trajectory duration: ", traj1.duration

raw_input()
