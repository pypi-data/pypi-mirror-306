# 原子能力的代码怎么写

“原子能力”，可以是实现一个API接口的访问、一个大模型的调用、一个数据的校验等等。
需要用python来编写“原子能力”的代码，不是从头到尾去写一个python程序，而是按照业务逻辑写一段可以用的python函数，来实现智能体的“原子能力”。
在编写python的时候要注意，不能随意发挥，需要在一定的条条款款下来编码，原因是只能这样编写智能体才能调用起来你的原子能力。

## 基本要求

- 人：有基础的python编程能力
- python版本：基于3.10.*
- python依赖库，只能用智能体现有的依赖库，常用的都具备（requests、json这些基础的都有），特殊的库没法自行添加（可以尝试自行封装一个API服务，让原子能力调用）。

## 代码编写指导

先配置环境，创建一个python环境，并使用pip安装hirpafnwheel

```shell
pip install hirpafnwheel
```

再新建一个新的python文件，在里面写业务逻辑，并且单元测试没有问题后，再把代码并入到“原子能力”的代码中。

“原子能力”的代码有个固定结构，class和里面的exec函数不能修改，业务代码放到exec里面就可以了，需要用到的库直接在最外面import就行。

示例如下：
这是一个把智能体抽取的入参当出参的“原子能力”，通常用于测试智能体的参数抽取功能。

```py
# ===================这里的都不要动================
# 此部分为插件引擎环境的相关引用

import sys
sys.path.insert(0, ".")

from hirpa.biz.services.fn.fn_code import FnCode
from hirpa.biz.services.fn.fn_tool_base import FnToolBase
from hirpa.utils.result import gen_result


# ===================可以根据需求自定引用===================
# 可以根据自己的业务需求，自行引用相关组件
# 注意：当前环境局限，只有常用库可用，后期会加入自动拉去加载依赖库功能

import logging as logger # 日志库
import requests, json # 常用的http请求、json解析等

# ===================调用的函数=======================
# 类、函数、入参，均不要修改
class FnCodePlug(FnCode):
    def exec(self, fnTool: FnToolBase, extend: dict = None) -> dict:
    # fnTool，为插件的上下文信息
    # entend，为扩展的信息，
# ==============此处可以根据需求编写代码==============
    
        try:
            in_args = fnTool.get_in_args() # 获取所有的入参
            msg = {}
            for _, a in in_args.items():
                av = {}
                av["field_type"] = "text"
                av["cn_name"] = a.cn_name
                av["value"] = a.value
                msg[a.name] = av

            if extend != None:
            for k, v in extend.items():
                msg[k] = {"field_type": "text", "cn_name": f"extend_{v}", "value": v}

    # 返回结果，必须按照此格式返回
            return gen_result(
                status="9", # 参考[结果状态]，9=成功
                unique_no=fnTool.get_unique_no(), # 不动
                msg=msg, # 返回给用户的内容，需要按照规范来，参考[返回的内容]章节
                biz_name=fnTool.get_name(), # 不动
                biz_cn_name=fnTool.get_cn_name(), # 不动
            )
    # 异常处理
        except Exception as ex:
            logger.exception(ex)
            return gen_result(
                status="0", # 参考[结果状态]，0=异常
                unique_no=fnTool.get_unique_no(),
                biz_name=fnTool.get_name(),
                biz_cn_name=fnTool.get_cn_name(),
                msg=f"执行失败,【{ex}】",
            )

```

### 结果状态

- "0" ，执行异常
- "1" ， 提示用户输入，目的是抽取动态参数，或者入参不合规，重新抽取
- "3" ， 提醒消息，自定义信息给用户展示
- "9" ， 执行成功

### 返回的内容

结果状态=0时，执行异常
格式：字符串
内容：放入详细异常信息，格式于聊天页面商量

----

结果状态=1时，提示用户输入
格式：dict
内容：为要从用户那获取的参数，参数必须在原子能力的入参中，包含动态参数
示例：

```json
{
    "出参1英文名":{
        "human_prompt":"出参值"
    },
    "出参2英文名":{
        "human_prompt":""
    }
}

```

----

结果状态=3时，发提醒信息给用户
格式：字符串
内容：提醒的内容，格式跟聊天页面的开发要协商好

----

结果状态=9，执行成功
dict对象，要与“原子能力”的出入参匹配，不允许输出
示例：

```json
{
    "出参1英文名":{
        "value":"出参值"
    },
    "出参2英文名":{
        "value":"出参值"
    }
}
```

## 示例

一个查询当前天气的原子能力代码

```py
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
```
