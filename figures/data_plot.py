import os
import sys
import re
import numpy
import json
from time import strftime
from copy import deepcopy

import matplotlib
matplotlib.use('Agg')
matplotlib.rc('xtick', labelsize=6)
matplotlib.rc('ytick', labelsize=6)
matplotlib.rc('font', size=10)
matplotlib.rc('font', size=10)
matplotlib.rc('text', usetex=False)
from matplotlib import pyplot as plt

# load nmpc data
classic_data = []
with open('./data/classic.json', 'r') as f:
    classic_data = json.load(f)

# load classic data
nmpc_data = []
with open('./data/nmpc.json', 'r') as f:
    nmpc_data = json.load(f)

################################################################################
# AERIAL VIEW
################################################################################
# polygons that should be plotted
polygons_mapping = {
    'f_k_x' : {
        'lfoot'     : {'edgecolor':'gray', 'lw':1, 'fill':None,},
        #'rfoot'     : {'edgecolor':'gray', 'lw':1, 'fill':None,},
        'lfcophull' : {'edgecolor':'blue', 'lw':1, 'fill':None,},
        #'rfcophull' : {'edgecolor':'blue', 'lw':1, 'fill':None,},
    },
    #'f_k_y' : {
    #    'lfoot'     : {'edgecolor':'gray', 'lw':1, 'fill':None,},
    #    #'rfoot'     : {'edgecolor':'gray', 'lw':1, 'fill':None,},
    #    'lfcophull' : {'edgecolor':'blue', 'lw':1, 'fill':None,},
    #    #'rfcophull' : {'edgecolor':'blue', 'lw':1, 'fill':None,},
    #},
    'F_k_x' : {
        'lfoot'     : {'edgecolor':'gray', 'lw':1, 'fill':None,},
        #'rfoot'     : {'edgecolor':'gray', 'lw':1, 'fill':None,},
        'lfcophull' : {'edgecolor':'blue', 'lw':1, 'fill':None,},
        #'rfcophull' : {'edgecolor':'blue', 'lw':1, 'fill':None,},
    },
    #'F_k_y' : {
    #    'lfoot'     : {'edgecolor':'gray', 'lw':1, 'fill':None,},
    #    #'rfoot'     : {'edgecolor':'gray', 'lw':1, 'fill':None,},
    #    'lfcophull' : {'edgecolor':'blue', 'lw':1, 'fill':None,},
    #    #'rfcophull' : {'edgecolor':'blue', 'lw':1, 'fill':None,},
    #},
    #'f_k_x' : ('lfposhull', 'rfposhull'),
    }

# general mapping for the bird's eye plots
bird_view_mapping = (
    # CoM
    (
        ('c_k_x',   {'lw':'1', 'ls':'-',  'marker':'.', 'ms':4, 'c':'r', 'label':'$c_{k}^{x}$'}),
        ('c_k_y',   {'lw':'1', 'ls':'-.', 'marker':'.', 'ms':4, 'c':'r', 'label':'$c_{k}^{y}$'}),
        # for rotation
        ('c_k_q',   {'lw':'1', 'ls':'', 'marker':'.', 'ms':4, 'c':'r', 'label':'$c_{k}^{\\theta}$'}),
    ),
    # Feet
    (
        ('f_k_x',   {'lw':'1', 'ls':'-',  'marker':'x', 'ms':4, 'c':'g', 'label':'$f_{k}^{x}$'}),
        ('f_k_y',   {'lw':'1', 'ls':'-.', 'marker':'x', 'ms':4, 'c':'g', 'label':'$f_{k}^{y}$'}),
        # for rotation
        ('f_k_q',   {'lw':'1', 'ls':'',  'marker':'x', 'ms':4, 'c':'g', 'label':'$f_{k}_{\\theta}$'}),
    ),
    # ZMP
    # TODO how to get current ZMP state?
    (
        ('z_k_x',   {'lw':'1', 'ls':'-',  'marker':'.', 'ms':4, 'c':'b', 'label':'$z_{k}^{x}$'}),
        ('z_k_y',   {'lw':'1', 'ls':'-.', 'marker':'.', 'ms':4, 'c':'b', 'label':'$z_{k}^{y}$'}),
    ),
)

preview_mapping = (
    # Preview
    (
        ('C_kp1_x', {'lw':'1', 'ls':':', 'marker':'.', 'ms':4, 'c':'r', 'label':'$C_{k+1}^{x}$'}),
        ('C_kp1_y', {'lw':'1', 'ls':':', 'marker':'.', 'ms':4, 'c':'r', 'label':'$C_{k+1}^{y}$'}),
        # for rotation
        ('C_kp1_q', {'lw':'1', 'ls':':', 'marker':'.', 'ms':4, 'c':'r', 'label':'$C_{k+1}^{\\theta}$'}),
    ),
    (
        ('F_k_x', {'lw':'1', 'ls':':', 'marker':'x', 'ms':4, 'c':'k', 'label':'$F_{k}^{x}$'}),
        ('F_k_y', {'lw':'1', 'ls':':', 'marker':'x', 'ms':4, 'c':'k', 'label':'$F_{k}^{y}$'}),
        # for rotation
        ('F_k_q', {'lw':'1', 'ls':':', 'marker':'x', 'ms':4, 'c':'k', 'label':'$F_{k}^{\\theta}$'}),
    ),
    (
        ('Z_kp1_x', {'lw':'1', 'ls':':', 'marker':'.', 'ms':4, 'c':'b', 'label':'$Z_{k+1}^{x}$'}),
        ('Z_kp1_y', {'lw':'1', 'ls':':', 'marker':'.', 'ms':4, 'c':'b', 'label':'$Z_{k+1}^{y}$'}),
    ),
)

def create_bird_view_plot(data, fname):
    # BIRD'S EYE VIEW
    # initialize figure with proper size
    fig = plt.figure()

    ax = fig.add_subplot(1,1,1)
    ax.set_title('Aerial View')
    ax.set_ylabel('y [m]')
    ax.set_xlabel("x [m]")

    # assemble different trajectories
    bird_view_axis  = ax
    bird_view_background = fig.canvas.copy_from_bbox(ax.bbox)
    bird_view_lines = {}

    for item in bird_view_mapping:
        # get mapping for x values
        name      = item[0][0]
        settings  = item[0][1]

        # layout line with empty data, but right settings
        # remove identifier from label
        settings['label'] = re.sub(r'_{[xy]}', '', settings['label'])
        line, = ax.plot([], [], **settings)

        # store lines for later update
        bird_view_lines[name] = line

    T = numpy.zeros((2,2))
    time = numpy.asarray(data['time'])

    for item in bird_view_mapping:
        # get names from mapping
        x_name = item[0][0]
        y_name = item[1][0]
        q_name = None
        # get theta name only if defined
        if len(item) > 2:
            q_name = item[2][0]

        # get line
        line = bird_view_lines[x_name]

        # define data
        x_data = numpy.ones(time.shape[0])*numpy.nan
        y_data = numpy.ones(time.shape[0])*numpy.nan

        # assemble data
        for i in range(time.shape[0]):
            # x value
            val = numpy.asarray(data[x_name])
            if len(val.shape) > 1:
                val = val[i,0]
            else:
                val = val[i]
            x_data[i] = val

            # y value
            val = numpy.asarray(data[y_name])
            if len(val.shape) > 1:
                val = val[i,0]
            else:
                val = val[i]
            y_data[i] = val

            # draw CoP and foot position hull
            for poly_name, poly_map in polygons_mapping.get(x_name, {}).iteritems():
                add_poly = False
                if i == 0:
                    add_poly = True
                else:
                    if not x_data[i] == x_data[i-1] \
                    or not y_data[i] == y_data[i-1]:
                        add_poly = True

                if add_poly:
                    q = 0.0
                    if q_name:
                        val = numpy.asarray(data[q_name])
                        if len(val.shape) > 1:
                            val = val[i,0]
                        else:
                            val = val[i]
                        q = val

                    # update transformation matrix
                    c = numpy.cos(q); s = numpy.sin(q)
                    T[0,0] = c; T[0,1] = -s
                    T[1,0] = s; T[1,1] =  c

                    hull = numpy.asarray(data[poly_name][i])
                    points = numpy.asarray((x_data[i], y_data[i]))

                    # first rotate
                    hull = T.dot(hull.transpose()).transpose()
                    hull = hull + points

                    poly = plt.Polygon(hull, **poly_map)
                    bird_view_axis.add_patch(poly)

        # after data is assembled add them to plots
        line.set_xdata(x_data)
        line.set_ydata(y_data)

        # AFTERMATH
        # recalculate x and y limits
        bird_view_axis.relim()
        bird_view_axis.autoscale_view(scalex=True, scaley=True, tight='True')
        bird_view_axis.set_aspect('equal')

        # define legend
        bird_view_axis.legend(loc='upper left')#, bbox_to_anchor=(1, 0.5))

        # save pictures
        plot_options = {
            #'format' : 'eps',
            #'dpi' : 300,
            #'bbox_inches' : 'tight',
        }

        # convert numpy arrays into lists
        fig.savefig(fname , **plot_options)

create_bird_view_plot(nmpc_data,    './nmpc_vs_classic_nmpc_motion.eps')
create_bird_view_plot(classic_data, './nmpc_vs_classic_classic_motion.eps')

################################################################################
# CPUTIME
################################################################################
width = 0.3
data_cpu_fig  = plt.figure()
ax  = data_cpu_fig.add_subplot(1,1,1)
ax.set_title('CPU Time of Solvers')
ax.set_ylabel("CPU time [ms]")
ax.set_xlabel("no. of iterations")

# retrieve data from classic generator
ori_cpu = numpy.asarray(classic_data['ori_qp_cputime'])
pos_cpu = numpy.asarray(classic_data['pos_qp_cputime'])
idx = numpy.asarray(range(len(ori_cpu)))

# get bar plots
ori_bar = ax.bar(idx, ori_cpu, width, linewidth=0, color='r')
pos_bar = ax.bar(idx, pos_cpu, width, linewidth=0, color='y',
    bottom=ori_cpu
)

# retrieve nmpc_data from nmpc generator
qp_cpu = numpy.asarray(nmpc_data['qp_cputime'])
idx = numpy.asarray(range(len(qp_cpu)))

# get bar plots
width = 0.4
qp_bar = ax.bar(idx+width, qp_cpu, width, linewidth=0, color='g')

# define legend position
# Put a legend to the right of the current axis
legend = ax.legend(
    (ori_bar[0],       pos_bar[0],   qp_bar[0]),
    ('$QP_{\\theta}$', '$QP_{x,y}$', '$QP_{x,y,\\theta}$')
)

# recalculate x and y limits
ax.relim()
ax.autoscale_view(scalex=True, scaley=True, tight='True')
#ax.set_aspect('equal')

################################################################################
# NWSR
################################################################################
data_nwsr_fig = plt.figure()
ax  = data_nwsr_fig.add_subplot(1,1,1)
ax.set_title('Working Set Recalculation of Solvers')
ax.set_ylabel("no. of WSR")
ax.set_xlabel("no. of iterations")

# retrieve nmpc_data from classic generator
ori_cpu = numpy.asarray(classic_data['ori_qp_nwsr'])
pos_cpu = numpy.asarray(classic_data['pos_qp_nwsr'])
idx = numpy.asarray(range(len(ori_cpu)))

# get bar plots
ori_bar = ax.bar(idx, ori_cpu, width, linewidth=0, color='r')
pos_bar = ax.bar(idx, pos_cpu, width, linewidth=0, color='y',
    bottom=ori_cpu
)

# retrieve data from nmpc generator
qp_cpu = numpy.asarray(nmpc_data['qp_nwsr'])
idx = numpy.asarray(range(len(qp_cpu)))

# get bar plots
width = 0.3
qp_bar = ax.bar(idx+width, qp_cpu, width, linewidth=0, color='g')

# define legend position
# Put a legend to the right of the current axis
legend = ax.legend(
    (ori_bar[0],       pos_bar[0],   qp_bar[0]),
    ('$QP_{\\theta}$', '$QP_{x,y}$', '$QP_{x,y,\\theta}$')
)

# recalculate x and y limits
ax.relim()
ax.autoscale_view(scalex=True, scaley=True, tight='True')
#ax.set_aspect('equal')

# save pictures
plot_options = {
    #'format' : 'eps',
    #'dpi' : 300,
    #'bbox_inches' : 'tight',
}

# convert numpy arrays into lists
data_cpu_fig.savefig('./nmpc_vs_classic_cputime.eps', **plot_options)
data_nwsr_fig.savefig('./nmpc_vs_classic_nwsr.eps', **plot_options)
