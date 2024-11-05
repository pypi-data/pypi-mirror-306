#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from collections import defaultdict

import torch
from torch_scatter import scatter_sum

from hakkero.dataset import IGNORE_INDEX
from hakkero.util import distributed


class TaskMetrics:
    def __init__(self, names, prefix="metrics"):
        self.names = names
        self.prefix = prefix

        self.n_tasks = len(self.names)
        self.samples, self.samples_accum = 0.0, 0.0
        self.group = {name: name for name in self.names}

    def set_group(self, dataset_config):
        self.group = dict()
        for d, config in dataset_config.items():
            self.group[d] = config.get("group", d)

    def reset(self):
        self.samples = 0.0

    def add(self, task_ids, cu_seqlens=None):
        with torch.no_grad():
            if cu_seqlens is None:
                tasks = task_ids[:, 0]
            else:
                cu_seqlens = cu_seqlens.view(-1) - 1
                task_ids = task_ids.view(-1)
                tasks = task_ids[cu_seqlens[cu_seqlens.ge(0)]]

            all_samples = scatter_sum(torch.ones_like(tasks), tasks, dim_size=self.n_tasks)
            # all_samples = distributed.all_sum(samples)
            self.samples += all_samples
            self.samples_accum += all_samples

    def read(self, group=True, keep_null=False):
        metrics = dict()

        group_metrics = defaultdict(lambda: defaultdict(float))
        for name, sample, sample_accum in zip(
            self.names,
            self.samples.tolist(),
            self.samples_accum.tolist(),
        ):
            group_metrics[self.group[name]]["sample"] += sample
            group_metrics[self.group[name]]["sample_accum"] += sample_accum

        for name, value in group_metrics.items():
            metrics[f"{self.prefix}/sample/{name}"] = value["sample"]
            metrics[f"{self.prefix}/sample_accum/{name}"] = value["sample_accum"]

        metrics[f"{self.prefix}/sample/all"] = self.samples.sum().item()
        metrics[f"{self.prefix}/sample_accum/all"] = self.samples_accum.sum().item()

        return metrics
