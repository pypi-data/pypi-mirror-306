#!/usr/bin/env python
# -*- coding: utf-8 -*-


import torch
import torch.distributed


def all_reduce(tensor, op, group=None):
    torch.distributed.all_reduce(tensor, op=op, group=group)
    return tensor


def all_mean(tensor, group=None):
    return all_reduce(tensor, torch.distributed.ReduceOp.AVG, group=group)


def all_sum(tensor, group=None):
    return all_reduce(tensor, torch.distributed.ReduceOp.SUM, group=group)


def all_gather_objects(obj):
    if torch.distributed.get_world_size() == 1:
        return [obj]

    res = [None for _ in range(torch.distributed.get_world_size())]
    torch.distributed.barrier()
    torch.distributed.all_gather_object(res, obj)
    return res
