import sys, json, tracer

sys.path.insert(0, ".")

from hirpa.biz.agent.tools.fn_code import FnCode
from hirpa.biz.agent.tools.fn_tool_base import FnToolBase
import hirpa.biz.agent.tools.fn_code_helper as fn_code_helper


class FnCodePlug(FnCode):
    async def exec(self, fnTool: FnToolBase, extend: dict = None) -> dict:

        return fn_code_helper.return_success(
            fnTool, fn_code_helper.get_in_args_dict(fnTool)
        )
