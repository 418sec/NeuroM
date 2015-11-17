# Copyright (c) 2015, Ecole Polytechnique Federale de Lausanne, Blue Brain Project
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

import os
import numpy as np
import h5py
from neurom.io import readers
from neurom.io import hdf5
from neurom.core.dataformat import COLS
from nose import tools as nt


_path = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_path, '../../../test_data')
H5_PATH = os.path.join(DATA_PATH, 'h5')
H5V1_PATH = os.path.join(H5_PATH, 'v1')
H5V2_PATH = os.path.join(H5_PATH, 'v2')


def test_read_h5v1_basic():
    data, offset, fmt = readers.H5.read(
        os.path.join(H5V1_PATH, 'Neuron.h5'))

    nt.ok_(fmt == 'H5V1')
    nt.ok_(offset == 0)
    nt.assert_equal(len(data), 847)
    nt.assert_equal(np.shape(data), (847, 7))


def test_read_h5v2_repaired_basic():
    data, offset, fmt = readers.H5.read(
        os.path.join(H5V2_PATH, 'Neuron_2_branch.h5'))

    nt.ok_(fmt == 'H5V2')
    nt.ok_(offset == 0)
    nt.assert_equal(len(data), 442)
    nt.assert_equal(np.shape(data), (442, 7))


def test_read_h5v2_raw_basic():
    data, offset, fmt = readers.H5.read(
        os.path.join(H5V2_PATH, 'Neuron.h5'))

    nt.ok_(fmt == 'H5V2')
    nt.ok_(offset == 0)
    nt.assert_equal(len(data), 847)
    nt.assert_equal(np.shape(data), (847, 7))


def test_get_version():
    v1 = h5py.File(os.path.join(H5V1_PATH, 'Neuron.h5'), mode='r')
    v2 = h5py.File(os.path.join(H5V2_PATH, 'Neuron.h5'), mode='r')
    nt.assert_equal(hdf5.get_version(v1), 'H5V1')
    nt.assert_equal(hdf5.get_version(v2), 'H5V2')
    v1.close()
    v2.close()


def test_unpack_h2():
    v1 = h5py.File(os.path.join(H5V1_PATH, 'Neuron.h5'), mode='r')
    v2 = h5py.File(os.path.join(H5V2_PATH, 'Neuron.h5'), mode='r')
    pts1, grp1 = hdf5._unpack_v1(v1)
    pts2, grp2 = hdf5._unpack_v2(v2, stage='raw')
    nt.assert_true(np.all(pts1 == pts2))
    nt.assert_true(np.all(grp1 == grp2))


def test_consistency_between_v1_v2():
    v1_data = readers.RawDataWrapper(readers.H5.read_v1(
            os.path.join(H5V1_PATH, 'Neuron.h5')))
    v2_data = readers.RawDataWrapper(readers.H5.read_v2(
            os.path.join(H5V2_PATH, 'Neuron.h5')))
    nt.ok_(np.allclose(v1_data.data_block, v1_data.data_block))
    nt.ok_(v1_data.adj_list == v2_data.adj_list)

class DataWrapper_Neuron(object):
    '''Base class for H5 tests'''

    end_pts = [1, 775, 393, 524, 142, 655, 273, 22, 795, 413,
               544, 162, 675, 293, 423, 42, 815, 564, 182, 695,
               313, 444, 62, 835, 584, 202, 715, 333, 846, 845,
               464, 82, 212, 604, 634, 735, 353, 484, 102, 233,
               624, 755, 373, 504, 122, 253]

    end_parents = [0, 774, 392, 523, 141, 654, 272, 21, 794, 412,
                   543, 161, 674, 292, 422, 41, 814, 563, 181, 694,
                   312, 443, 61, 834, 583, 201, 714, 332, 0, 844,
                   463, 81, 211, 603, 633, 734, 352, 483, 101, 232,
                   623, 754, 372, 503, 121, 252]

    fork_pts = [0, 12, 32, 52, 72, 92, 112, 132, 152, 172, 192, 223,
                243, 263, 283, 303, 323, 343, 363, 383, 403, 434, 454,
                474, 494, 514, 534, 554, 574, 594, 614, 645, 665, 685,
                705, 725, 745, 765, 785, 805, 825]

    fork_parents = [-1, 11, 31, 51, 71, 91, 111, 131, 151, 171, 191, 222,
                    242, 262, 282, 302, 322, 342, 362, 382, 402, 433, 453,
                    473, 493, 513, 533, 553, 573, 593, 613, 644, 664, 684,
                    704, 724, 744, 764, 784, 804, 824]

    def test_n_rows(self):
        nt.assert_equal(self.rows, 847)

    def test_first_id_0(self):
        nt.ok_(self.first_id == 0)

    def test_fork_points(self):
        nt.assert_equal(len(self.data.get_fork_points()), 41)
        nt.assert_equal(self.data.get_fork_points(),
                        DataWrapper_Neuron.fork_pts)

    def test_get_endpoints(self):
        nt.assert_equal(self.data.get_end_points(),
                        DataWrapper_Neuron.end_pts)

    def test_end_points_have_no_children(self):
        for p in DataWrapper_Neuron.end_pts:
            nt.ok_(len(self.data.get_children(p)) == 0)

    def test_fork_point_parents(self):
        fpar = [self.data.get_parent(i) for i in self.data.get_fork_points()]
        nt.assert_equal(fpar, DataWrapper_Neuron.fork_parents)

    def test_end_point_parents(self):
        epar = [self.data.get_parent(i) for i in self.data.get_end_points()]
        nt.assert_equal(epar, DataWrapper_Neuron.end_parents)

    @nt.raises(LookupError)
    def test_iter_row_low_id_raises(self):
        self.data.iter_row(-1)

    @nt.raises(LookupError)
    def test_iter_row_high_id_raises(self):
        self.data.iter_row(self.rows + self.first_id)


class TestRawDataWrapper_Neuron_H5V1(DataWrapper_Neuron):
    '''Test HDF5 v1 reading'''
    def setup(self):
        self.data = readers.RawDataWrapper(readers.H5.read_v1(
            os.path.join(H5V1_PATH, 'Neuron.h5')))
        self.first_id = int(self.data.data_block[0][COLS.ID])
        self.rows = len(self.data.data_block)


class TestRawDataWrapper_Neuron_H5V2(DataWrapper_Neuron):
    '''Test HDF5 v2 reading'''
    def setup(self):
        self.data = readers.RawDataWrapper(readers.H5.read_v2(
            os.path.join(H5V2_PATH, 'Neuron.h5'), stage='raw'))
        self.first_id = int(self.data.data_block[0][COLS.ID])
        self.rows = len(self.data.data_block)
