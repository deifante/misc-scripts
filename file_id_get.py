#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import string

import cx_Oracle

from illustration_check import TeamsOracle 

if __name__ == '__main__':
    id_buffer = []
    max_buffer_size = 200
    for line in sys.stdin:
        istock_id, teams_id = string.strip(line).split()
        id_buffer.append(istock_id)
        if len(id_buffer) > max_buffer_size:
            teams_oracle = TeamsOracle()
            teams_ids = teams_oracle.get_teams_ids(id_buffer)
            id_buffer = []
            for teams_id in teams_ids:
                print teams_id[0], teams_id[1]

    if len(id_buffer):
        teams_oracle = TeamsOracle()
        teams_ids = teams_oracle.get_teams_ids(id_buffer)
        for teams_id in teams_ids:
            print teams_id[0], teams_id[1]
