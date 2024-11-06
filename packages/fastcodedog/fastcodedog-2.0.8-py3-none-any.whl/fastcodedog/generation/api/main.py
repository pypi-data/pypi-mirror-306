# -*- coding: utf-8 -*-
from fastcodedog.context.context import ctx_instance
from fastcodedog.generation.api.config import Config
from fastcodedog.generation.api.oauth2 import Oauth2
from fastcodedog.generation.base.file import File
from fastcodedog.generation.base.function import Function
from fastcodedog.generation.base.line_break import LineBreak
from fastcodedog.generation.base.location_finder import LocationFinder
from fastcodedog.generation.base.required_import import Import
from fastcodedog.generation.base.text import Text
from fastcodedog.generation.base.variable import Variable
from fastcodedog.util.case_converter import camel_to_snake


class Main(File):
    def __init__(self):
        super().__init__('main',
                         file_path=LocationFinder.get_path('main'),
                         package=LocationFinder.get_package('main'))
        self._init_blocks()

    def _init_blocks(self):
        self.blocks.append(
            Variable('app', value='FastAPI()', possible_imports='from fastapi import FastAPI'))
        self._init_swagger()
        self._init_sqlalchemy_error_handler()
        # 异常捕捉定义和配置之间加空行
        self.blocks.append(LineBreak())
        # 日志配置
        self.blocks.append(Text(f"""logging.basicConfig(**get_configs("logging"))
logging.getLogger('sqlalchemy.engine').setLevel(get_config('logging', 'level', logging.INFO))""",
                                possible_imports=['import logging', Import('get_configs', Config().package),
                                                  Import('get_config', Config().package)]))
        # 配置和路由之间加空行
        self.blocks.append(LineBreak())
        # 加入各种路由
        if ctx_instance.oauth2.enabled:
            self.blocks.append(Text(f"""app.include_router(oauth2_app.router)""",
                                    possible_imports=Import('app', Oauth2().package, as_='oauth2_app')))
        for app in ctx_instance.extend_apps.values():
            self.blocks.append(Text(f"""app.include_router({app.alias}.router)""",
                                    possible_imports=Import(app.import_, app.from_, app.alias)))
        for module, apis in ctx_instance.apis.items():
            for api_context in apis.values():
                from_ = LocationFinder.get_package(api_context.name, 'api', module)
                import_ = 'app'
                alias = f'{camel_to_snake(api_context.name)}_app'
                self.blocks.append(Text(f"""app.include_router({alias}.router)""",
                                        possible_imports=Import(import_, from_, alias)))
        # main和各种路由之间加空行
        self.blocks.append(LineBreak())
        # 写入main
        self.blocks.append(Text(f"""if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(port))""",
                                possible_imports=['uvicorn', Import('port', Config().package)]))

    def _init_swagger(self):
        function = Function('custom_swagger_ui_html', async_=True)
        function.decorators.append(Function.Decorator('app.get', params=['\'/swagger\'', 'include_in_schema=False']))
        function.blocks.append(Text(f"""return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.9.0/swagger-ui.css"
    )""", possible_imports=['from fastapi.openapi.docs import get_swagger_ui_html']))
        self.blocks.append(function)

    def _init_sqlalchemy_error_handler(self):
        self.blocks.append(Text("""@app.exception_handler(IntegrityError)
@app.exception_handler(DataError)
@app.exception_handler(ValidationError)
async def fastapi_exception_handler_400(request, exc):
    logging.warning(traceback.format_exc())
    if f"{exc}".find("duplicate key") != -1:
        p = r'(Key\s+.*already\s+exists)'
        detail = re.findall(p, f"{exc}")
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"数据重复{exc if not detail else detail[0]}",
        )
    raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=f"数据请求错误{exc}",
    )


@app.exception_handler(SQLAlchemyError)
async def fastapi_exception_handler_500(request, exc):
    logging.error(traceback.format_exc())
    raise HTTPException(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Database operation failed: {exc}",
    )""", possible_imports=['from fastapi import HTTPException', 'from sqlalchemy.exc import IntegrityError',
                            'from sqlalchemy.exc import DataError', 'from sqlalchemy.exc import SQLAlchemyError',
                            'from pydantic import ValidationError',
                            'from starlette.status import HTTP_400_BAD_REQUEST',
                            'from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR',
                            'import re', 'import traceback']))
