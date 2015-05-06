# Copyright (c) 2015, Ecole Polytechnique Federal de Lausanne, Blue Brain Project
# All rights reserved.
#
# This file is part of NeuroM <https://github.com/BlueBrain/NeuroM>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#     3. Neither the name of the copyright holder nor the names of
#        its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from nose import tools as nt
from neurom.io.utils import make_neuron
from neurom.io.readers import load_data
from neurom.view import view
from neurom.analysis.morphtree import find_tree_type
import os
import numpy as np
import pylab as plt


DATA_PATH = './test_data'
SWC_PATH = os.path.join(DATA_PATH, 'swc/')

data = load_data(SWC_PATH + 'Neuron.swc')
neuron0 = make_neuron(data, find_tree_type)
soma0 = neuron0.soma


def test_tree():
    axes = []
    for tree in neuron0.neurite_trees:
        print tree.type
        fig, ax = view.tree(tree)
        axes.append(ax)
    nt.ok_(axes[0].get_data_ratio > 1.00 )
    nt.ok_(axes[1].get_data_ratio > 0.80 )
    nt.ok_(axes[2].get_data_ratio > 1.00 )
    nt.ok_(axes[3].get_data_ratio > 0.85 )
    tree0 = neuron0.neurite_trees[0]
    fig, ax = view.tree(tree0, treecolor='black', diameter=False, alpha=1., linewidth=1.2)
    c = ax.collections[0]
    nt.ok_(c.get_linewidth()[0] == 1.2 )
    nt.ok_(np.allclose(c.get_color(), np.array([[ 0.,  0.,  0.,  1.]])) )
    fig, ax = view.tree(tree0, plane='wrong')
    nt.ok_(ax == 'No sunch plane found! Please select one of: xy, xz, yx, yz, zx, zy.')
    plt.close('all')


def test_soma():
    fig, ax = view.soma(soma0)
    nt.ok_(np.allclose(ax.get_xlim(), (0.0, 0.12)) )
    nt.ok_(np.allclose(ax.get_ylim(), (0.0, 0.20)) )
    fig, ax = view.soma(soma0, outline=False)
    nt.ok_(np.allclose(ax.get_xlim(), (0.0, 1.0)) )
    nt.ok_(np.allclose(ax.get_ylim(), (0.0, 1.0)) )
    fig, ax = view.soma(soma0, plane='wrong')
    nt.ok_(ax == 'No sunch plane found! Please select between: xy, xz, yx, yz, zx, zy, all.')
    plt.close('all')


def test_neuron():
    fig, ax = view.neuron(neuron0)
    nt.ok_(np.allclose(ax.get_xlim(), (-70.328535157399998, 94.7472627179)) )
    nt.ok_(np.allclose(ax.get_ylim(), (-87.600171997199993, 78.51626225230001)) )
    fig, ax = view.neuron(neuron0, plane='wrong')
    nt.ok_(ax == 'No sunch plane found! Please select between: xy, xz, yx, yz, zx, zy, all.')
    plt.close('all')