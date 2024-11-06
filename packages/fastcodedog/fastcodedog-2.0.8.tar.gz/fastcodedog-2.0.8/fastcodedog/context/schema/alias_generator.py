# -*- coding: utf-8 -*-
from fastcodedog.context.common.import_ import Import_
from fastcodedog.context.contextbase import ContextBase


class AliasGenerator(ContextBase):
    def __init__(self):
        super().__init__()
        self.import_ = None
        self._types['import_'] = Import_
        self.function = ''
