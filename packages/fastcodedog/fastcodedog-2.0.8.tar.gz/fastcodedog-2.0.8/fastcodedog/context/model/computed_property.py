# -*- coding: utf-8 -*-
from fastcodedog.context.common.import_ import Import_
from fastcodedog.context.contextbase import ContextBase


class ComputedProperty(ContextBase):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.name = ''
        self.type = ''
        self.pydantic_type = ''
        self.comment = ''
        self.module = ''
        self.model_name = ''
        self.nullable = True
        self.script = ''
        self.import_ = None
        self._types['import_'] = Import_
