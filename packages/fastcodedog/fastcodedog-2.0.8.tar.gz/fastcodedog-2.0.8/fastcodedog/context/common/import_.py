# -*- coding: utf-8 -*-
from fastcodedog.context.contextbase import ContextBase


class Import_(ContextBase):
    def __init__(self):
        super().__init__()
        self.from_ = ''
        self.import_ = ''
        self.as_ = ''
