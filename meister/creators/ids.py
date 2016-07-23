#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from farnsworth.models.job import IDSJob

import meister.creators
LOG = meister.creators.LOG.getChild('ids')


class IDSCreator(meister.creators.BaseCreator):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    @property
    def jobs(self):
        LOG.debug("Collecting jobs")
        for cs in self.challenge_sets():
            job = IDSJob(payload={'cs_id': cs.id}, request_cpu=1, request_memory=1024)
            priority = 15
            LOG.debug("Yielding IDSJob for %s", cs.id)
            yield (job, priority)
