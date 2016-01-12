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

'''Basic functions and iterators for neuron neurite section morphometrics

'''
from itertools import izip
from neurom.core import tree as tr
import neurom.analysis.morphmath as mm


iter_type = tr.isection


def itr(obj, mapping=None, filt=None):
    '''Iterator to a neurite, neuron or neuron population's sections

    Applies a neurite filter function and a section mapping.

    Example:
        Get the lengths of sections in a neuron and a population

        >>> from neurom import sections as sec
        >>> neuron_lengths = [l for l in sec.itr(nrn, sec.length)]
        >>> population_lengths = [l for l in sec.itr(pop, sec.length)]
        >>> neurite = nrn.neurites[0]
        >>> tree_lengths = [l for l in sec.itr(neurite, sec.length)]

    Example:
        Get the number of sections in a neuron

        >>> from neurom import sections as sec
        >>> n = sec.count(nrn)

    '''
    #  TODO: optimize case of single neurite and move code to neurom.core.tree
    neurites = [obj] if isinstance(obj, tr.Tree) else obj.neurites
    return tr.i_chain(neurites, iter_type, mapping, filt)


def length(section):
    return mm.section_length(section)


def _aggregate_segments(section, f):
    '''Sum the result of applying a function to all segments in a section'''
    return sum(f((a, b))
               for a, b in izip(section, section[1:]))


def volume(section):
    '''Calculate the total volume of a segment'''
    return _aggregate_segments(section, mm.segment_volume)


def area(section):
    '''Calculate the surface area of a section'''
    return _aggregate_segments(section, mm.segment_area)


def radial_dist(pos, use_start_point=False):
    '''Return a function that calculates radial distance for a section

    Radial distance calculater WRT pos

    TODO: Can we simplify this to use the middle point?
    '''
    sec_idx = 0 if use_start_point else -1

    def _dist(section):
        '''Hacky closure'''
        return mm.point_dist(pos, section[sec_idx])

    return _dist


def count(neuron):
    """
    Return number of segments in neuron or population
    """
    return sum(1 for _ in itr(neuron))
