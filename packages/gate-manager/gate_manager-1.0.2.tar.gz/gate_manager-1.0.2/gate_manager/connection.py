# -*- coding: utf-8 -*-
"""
Gate class to interface with the Nanonis system for reading and setting voltages.

Created on Tue Oct 22 16:08:06 2024
@author: Chen Huang <chen.huang23@imperial.ac.uk>
"""
from nanonis_tramea import Nanonis


class SemiqonLine:
    def __init__(self, label: str = None):
        self.label = label


class SemiqonLinesConnection:
    def __init__(self):
        self.lines = [
            SemiqonLine(),  # empty
            # top
            SemiqonLine(label='t_D'),
            SemiqonLine(label='t_bar_4D'),
            SemiqonLine(label='t_P4'),
            SemiqonLine(label='t_bar_34'),
            SemiqonLine(label='t_P3'),
            SemiqonLine(label='t_bar_23'),
            SemiqonLine(label='t_P2'),
            SemiqonLine(label='t_bar_12'),
            SemiqonLine(label='t_P1'),
            SemiqonLine(label='t_bar_S1'),
            SemiqonLine(label='t_s'),
            SemiqonLine(label='res_S'),
            # bottom
            SemiqonLine(label='b_S'),
            SemiqonLine(label='b_bar_S1'),
            SemiqonLine(label='b_P1'),
            SemiqonLine(label='b_bar_12'),
            SemiqonLine(label='b_P2'),
            SemiqonLine(label='b_bar_23'),
            SemiqonLine(label='b_P3'),
            SemiqonLine(label='b_bar_34'),
            SemiqonLine(label='b_P4'),
            SemiqonLine(label='b_bar_4D'),
            SemiqonLine(label='b_D'),
            SemiqonLine(label='res_D'),
        ]


class NanonisSource:
    def __init__(self, label: str = None, read_index=None, write_index: int = None, nanonisInstance: Nanonis = None):
        self.label = label
        self.read_index = read_index
        self.write_index = write_index
        self.nanonisInstance = nanonisInstance


class NanonisSourceConnection:
    def __init__(self, nanonisInstance: Nanonis = None):
        self.outputs = [
            NanonisSource(),
            NanonisSource(label='Nanonis output1', read_index=24, write_index=1, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis output2', read_index=25, write_index=2, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis output3', read_index=26, write_index=3, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis output4', read_index=27, write_index=4, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis output5', read_index=28, write_index=5, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis output6', read_index=29, write_index=6, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis output7', read_index=30, write_index=7, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis output8', read_index=31, write_index=8, nanonisInstance=nanonisInstance),
        ]

        self.inputs = [
            NanonisSource(),
            NanonisSource(label='Nanonis input1', read_index=0, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis input2', read_index=1, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis input3', read_index=2, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis input4', read_index=3, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis input5', read_index=4, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis input6', read_index=5, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis input7', read_index=6, nanonisInstance=nanonisInstance),
            NanonisSource(label='Nanonis input8', read_index=7, nanonisInstance=nanonisInstance),
        ]
