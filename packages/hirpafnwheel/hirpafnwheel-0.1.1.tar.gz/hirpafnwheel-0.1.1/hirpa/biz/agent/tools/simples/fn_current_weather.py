import sys

sys.path.insert(0, ".")

from hirpa.biz.agent.tools.fn_code import FnCode
from hirpa.biz.agent.tools.fn_tool_base import FnToolBase
from hirpa.llm.message import BaseMessage, SystemMessage, UserMessage

import hirpa.biz.agent.tools.fn_code_helper as fn_code_helper
import requests, json, traceback
import logging as logger


class FnCodePlug(FnCode):
    async def exec(self, fnTool: FnToolBase, extend: dict = None) -> dict:
        try:
            in_args = fnTool.get_in_args()
            logger.debug(f"查询城市:{in_args[list(in_args.keys())[0]].get_value()}")
            response = requests.get(
                f"https://free.wqwlkj.cn/wqwlapi/weather.php?city={in_args[list(in_args.keys())[0]].get_value()}",
            )

            resp_str = response.text
            logger.debug(f"接口返回:{resp_str}")

            messages: list[BaseMessage] = []
            messages.append(
                SystemMessage(
                    content="你是一个天气预报员，并帮我把一下内容整理为一份完成天气预报，通过markdown格式输出，必须包含markdown特有的格式、图标、表情、引用等，其中生活指数与建议用table展示，内容简要精确，总共不超过200个字。"
                )
            )
            messages.append(
                UserMessage(
                    content=f"{resp_str}",
                    example=True,
                )
            )
            data = fnTool.chat(messages)

            return fn_code_helper.return_success(
                fnTool,
                {
                    "result": {
                        "field_type": "text",
                        "cn_name": "查询结果",
                        "value": data,
                    }
                },
            )

        except Exception as ex:
            logger.exception(f"代码执行异常:{ex}")
            return fn_code_helper.return_exception(fnTool, f"执行失败,系统内部错误")
