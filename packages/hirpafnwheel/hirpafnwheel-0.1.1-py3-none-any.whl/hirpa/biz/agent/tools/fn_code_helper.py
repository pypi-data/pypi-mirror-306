from hirpa.biz.agent.tools.fn_tool_base import (
    FnToolBase,
    Enum_Data_Type,
)
import hirpa.utils.result as rlt
import json, traceback


def get_in_args_dict(fnTool: FnToolBase) -> dict:
    """
    获取原子能力入参的内容，用dict输出

    返回：{
        "参数英文名": {
            "field_type": "类型", # Enum_Data_Type
            "cn_name": "参数中文名",
            "value": "参数的值"
        },
        ...
    }
    """
    in_args = fnTool.get_in_args()
    data = {}
    for _, a in in_args.items():
        av = {}
        av["field_type"] = a.get_data_type_enum().name
        av["cn_name"] = a.cn_name
        av["value"] = a.value
        data[a.name] = av

    return data


def get_file_args_dict(fnTool: FnToolBase) -> dict:
    """
    获取原子能力执行模块的入参，用dict输出

    返回：{
        "key":"value",
    }

    """

    fn_args_str = fnTool.get_tool_exec().get_file_args()
    file_args = {}
    if fn_args_str is not None and fn_args_str != "":
        for item in json.loads(fn_args_str):
            file_args[item["key"]] = item["value"]

    return file_args


def return_exception(fnTool: FnToolBase, data) -> dict:
    """
    返回异常
    msg: 要返回的消息
    """

    return rlt.gen_result(
        status=rlt.STATUS_EXCEPTION,
        unique_no=fnTool.get_unique_no(),
        biz_cn_name=fnTool.get_cn_name(),
        biz_name=fnTool.get_name(),
        msg=data,
    )


def return_next_round(fnTool: FnToolBase, data: dict) -> dict:
    """
    返回下一轮入参提取，根据human_prompt提示词提示用户输入，大模型自动提取该入参的实体
    data:
    {
        "入参英文名":{
            "human_prompt": f"亲，方便问一下您的年龄吗？",
        }
    }
    """
    return rlt.gen_result(
        status=rlt.STATUS_NEXT_ROUND,
        unique_no=fnTool.get_unique_no(),
        biz_cn_name=fnTool.get_cn_name(),
        biz_name=fnTool.get_name(),
        msg=data,
    )


def return_notification(fnTool: FnToolBase, data: str | dict) -> dict:
    """
    返回提醒消息，data为消息内容，可以为字符串或字典，具体内容可以自行定义

    """
    return rlt.gen_result(
        status=rlt.STATUS_PLANNING_CONFIRM,
        unique_no=fnTool.get_unique_no(),
        biz_cn_name=fnTool.get_cn_name(),
        biz_name=fnTool.get_name(),
        msg=data,
    )


def return_need_confirm(fnTool: FnToolBase, data: dict) -> dict:
    """
    返回需要确认的入参，data为要确认的内容
    data:
    {
        "入参英文名":{
            "field_type":"参数类型，选填", # Enum_Data_Type
            "cn_name":"中文名，选填",
            "value":"值，必填"
        }
    }
    """

    return rlt.gen_result(
        status=rlt.STATUS_NEED_CONFIRM,
        unique_no=fnTool.get_unique_no(),
        biz_cn_name=fnTool.get_cn_name(),
        biz_name=fnTool.get_name(),
        msg=data,
    )


def return_success(fnTool: FnToolBase, data: dict) -> dict:
    """
    返回执行成功，data为执行结果，与出参一致
    data:
    {
        "出参英文名":{
            "field_type":"参数类型，选填", # Enum_Data_Type
            "cn_name":"中文名，选填",
            "value":"值，必填"
        },
    }
    """

    return rlt.gen_result(
        status=rlt.STATUS_SUCCESS,
        unique_no=fnTool.get_unique_no(),
        biz_cn_name=fnTool.get_cn_name(),
        biz_name=fnTool.get_name(),
        msg=data,
    )
