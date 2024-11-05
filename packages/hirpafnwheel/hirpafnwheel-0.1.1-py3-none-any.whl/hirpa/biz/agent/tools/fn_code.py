from hirpa.biz.agent.tools.fn_tool_base import FnToolBase
import logging


class FnCode:
    def __init__(self):
        logging.debug("FnCode init 初始化！")
        pass

    async def exec(self, fnTool: FnToolBase, extend: dict = None) -> dict:
        logging.debug("FnCode exec 运行！")
        return None
