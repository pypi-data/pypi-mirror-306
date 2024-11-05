import enum, json
from abc import abstractmethod


class Enum_Data_Type(enum.Enum):
    number = 1
    text = 2
    bool = 3
    file = 4
    img = 5
    url = 6
    markdown = 7
    html = 8
    custom = 9
    others = 99


class FnToolExecBase:
    def __init__(
        self,
        base_url: str,
        code: str,
        exec_type: int,
        passport: str,
        rpa_info: str,
        rpa_type: str,
        file_args: str,
        file_name: str,
    ):
        self.base_url = base_url
        self.code = code
        self.exec_type = exec_type
        self.passport = passport
        self.rpa_info = rpa_info
        self.rpa_type = rpa_type
        self.file_args = file_args
        self.file_name = file_name
        self.file_args_dict = None

    def set_base_url(self, base_url):
        self.base_url = base_url

    def get_base_url(self):
        return self.base_url

    def set_code(self, code):
        self.code = code

    def get_code(self):
        return self.code

    def set_exec_type(self, exec_type):
        self.exec_type = exec_type

    def get_exec_type(self):
        return self.exec_type

    def set_passport(self, passport):
        self.passport = passport

    def get_passport(self):
        return self.passport

    def set_rpa_info(self, rpa_info):
        self.rpa_info = rpa_info

    def get_rpa_info(self):
        return self.rpa_info

    def set_rpa_type(self, rpa_type):
        self.rpa_type = rpa_type

    def get_rpa_type(self):
        return self.rpa_type

    def set_file_args(self, file_args):
        self.file_args = file_args

    def get_file_args(self):
        """获取执行模块的入参"""
        if self.exec_type == 0:
            return self.passport
        else:
            return self.file_args

    def get_file_name(self):
        """
        获取执行素材文件名
        """
        return self.file_name

    def get_file_args_dict(self) -> dict:
        """
        获取执行模板的参数，用dict输出
        {"parma0": "value0", "parma1": "value1"}
        """
        if self.file_args_dict is None:
            fn_args_str = self.get_file_args()
            self.file_args_dict = {}
            if fn_args_str is not None and fn_args_str != "":
                for item in json.loads(fn_args_str):
                    self.file_args_dict[item["key"]] = item["value"]

            return self.file_args_dict
        else:
            return self.file_args_dict


class FnToolOutArgBase:
    def __init__(
        self,
        data_format: str,
        cn_name: str,
        name: str,
        data_type: str,
        default_value: str,
        human_prompt: str,
        order: int,
    ):
        self.value = ""
        self.data_format = data_format
        self.cn_name = cn_name
        self.name = name
        self.data_type = data_type
        self.default_value = default_value
        self.human_prompt = human_prompt
        self.order = order

    def set_value(self, value):
        """
        设置参数值
        """
        self.value = value

    def get_value(self):
        """
        获取参数值
        """
        return self.value

    def set_data_format(self, data_format):
        """
        data_format: 设置数据格式校验
        """
        self.data_format = data_format

    def get_data_format(self):
        return self.data_format

    def set_cn_name(self, cn_name):
        self.cn_name = cn_name

    def get_cn_name(self):
        return self.cn_name

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_data_type(self, data_type):
        self.data_type = data_type

    def get_data_type(self):
        return self.data_type

    def get_data_type_enum(self) -> Enum_Data_Type:
        return Enum_Data_Type(self.data_type)

    def set_default_value(self, default_value):
        self.default_value = default_value

    def get_default_value(self):
        return self.default_value

    def set_human_prompt(self, human_prompt):
        self.human_prompt = human_prompt

    def get_human_prompt(self):
        return self.human_prompt

    def get_order(self):
        return self.order


class FnToolInArgBase:
    def __init__(
        self,
        default_value: str,
        data_type: int,
        cn_name: str,
        name: str,
        human_prompt: str,
        control_type: str,
        llm_prompt: str,
        required: int,
        input_configure: str,
        order: int,
        dynamic: int,
        independent: int,
        out_mark: int,
    ):
        self.value = ""
        self.default_value = default_value
        self.data_type = data_type
        self.cn_name = cn_name
        self.name = name
        self.human_prompt = human_prompt
        self.control_type = control_type
        self.llm_prompt = llm_prompt
        self.required = required
        self.input_configure = input_configure
        self.order = order
        self.dynamic = dynamic
        self.independent = independent
        self.out_mark = out_mark

    def set_value(self, value):
        """设置入参的值"""
        self.value = value

    def get_value(self):
        """获取入参的值"""
        return self.value

    def set_default_value(self, default_value):
        """设置入参默认值"""
        self.default_value = default_value

    def get_default_value(self):
        """获取入参默认值"""
        return self.default_value

    def set_data_type(self, data_type):
        """设置参数的类型"""
        self.data_type = data_type

    def get_data_type(self):
        """获取参数的类型，输出int"""
        return self.data_type

    def get_data_type_enum(self) -> Enum_Data_Type:
        """
        获取参数的类型，输出枚举Enum_Data_Type
        """
        try:
            return Enum_Data_Type(self.data_type)
        except ValueError:
            return Enum_Data_Type.others

    def set_cn_name(self, cn_name):
        """设置入参中文名"""
        self.cn_name = cn_name

    def get_cn_name(self):
        """获取入参中文名"""
        return self.cn_name

    def set_name(self, name):
        """设置入参英文名"""
        self.name = name

    def get_name(self):
        """获取入参英文名"""
        return self.name

    def set_human_prompt(self, human_prompt):
        """设置入参人类提示词"""
        self.human_prompt = human_prompt

    def get_human_prompt(self):
        """获取入参人类提示词"""
        return self.human_prompt

    def set_control_type(self, control_type):
        """设置入参控件类型"""
        self.control_type = control_type

    def get_control_type(self):
        """设置入参控件类型"""
        return self.control_type

    def set_llm_prompt(self, llm_prompt):
        """设置入参的大模型提示词，在大模型实体抽取时使用"""
        self.llm_prompt = llm_prompt

    def get_llm_prompt(self):
        """获取入参的大模型提示词"""
        return self.llm_prompt

    def set_required(self, required):
        """设置入参是否必填"""
        self.required = required

    def get_required(self):
        """获取入参是否必填"""
        return self.required

    def set_input_configure(self, input_configure):
        """设置入参类型的相关配置"""
        self.input_configure = input_configure

    def get_input_configure(self):
        """获取入参配置"""
        return self.input_configure

    def get_order(self):
        """获取当前参数在函数中的顺序，排第几"""
        return self.order

    def get_dynamic(self):
        """参数是否动态，动态在原子能力被调用的过程中使用"""
        return self.dynamic

    def get_independent(self):
        """参数是否独立提取"""
        return self.independent

    def get_out_mark(self):
        """参数是否作为输出参数"""
        return self.out_mark


class FnToolBase:
    def __init__(
        self,
        fn_id: str,
        name: str,
        cn_name: str,
        llm_corpus: str,
        human_prompt: str,
        arg_prompt: str,
        app_id: str,
        unique_no: str,
        need_confirm: int,
        description: str,
        cosplay_id: str,
        cn_name_alias: str,
    ):
        self.name = name
        self.cn_name = cn_name
        self.llm_prompt = llm_corpus
        self.human_prompt = human_prompt
        self.app_id = app_id
        self.unique_no = unique_no
        self.need_confirm = need_confirm
        self.description = description
        self.tool_exec: FnToolExecBase = None
        self.in_args: dict[str, FnToolInArgBase] = {}
        self.out_args: dict[str, FnToolOutArgBase] = {}
        self.cosplay_id = cosplay_id
        self.cn_name_alias: list[str] = []
        if cn_name_alias != None and cn_name_alias != "":
            self.cn_name_alias = json.loads(cn_name_alias)
        self.cache = {}
        self.fn_id = fn_id

    def get_fn_id(self) -> str:
        """获取原子能力的id"""
        return self.fn_id

    def set_cache(self, data: dict):
        """设置缓存，缓存的内容可自定义，输入为dict"""
        self.cache = data

    def get_cache(self) -> dict:
        """获取缓存"""
        return self.cache

    def set_name(self, name):
        """设置原子能力英文名"""
        self.name = name

    def get_name(self):
        """获取原子能力英文名"""
        return self.name

    def set_cn_name(self, cn_name):
        """设置原子能力中文名"""
        self.cn_name = cn_name

    def get_cn_name(self):
        """获取原子能力中文名"""
        return self.cn_name

    def set_llm_prompt(self, llm_corpus):
        """设置原子能力大模型提示词"""
        self.llm_prompt = llm_corpus

    def get_llm_prompt(self):
        """获取原子能力大模型提示词"""
        return self.llm_prompt

    def set_human_prompt(self, human_prompt):
        """设置原子能里人类提示词"""
        self.human_prompt = human_prompt

    def get_human_prompt(self):
        """获取原子能里人类提示词"""
        return self.human_prompt

    def set_app_id(self, app_id):
        """设置app_id"""
        self.app_id = app_id

    def get_app_id(self):
        """获取app_id"""
        return self.app_id

    def set_unique_no(self, unique_no):
        """设置unique_no"""
        self.unique_no = unique_no

    def get_unique_no(self):
        """获取unique_no"""
        return self.unique_no

    def set_need_confirm(self, need_confirm):
        """设置是否需要确认开关"""
        self.need_confirm = need_confirm

    def get_need_confirm(self):
        """获取是否需要确认开关"""
        return self.need_confirm

    def set_tool_exec(self, tool_exec):
        self.tool_exec = tool_exec

    def set_description(self, description):
        """设置描述"""
        self.description = description

    def get_description(self):
        """获取描述"""
        return self.description

    def get_tool_exec(self) -> FnToolExecBase:
        return self.tool_exec

    def set_in_args(self, in_args: dict[str, FnToolInArgBase]):
        self.in_args = in_args

    def set_in_args_value(self, name: str, value):
        if self.in_args is not None and len(self.in_args) > 0:
            arg = self.in_args.get(name)
            if arg is not None:
                arg.set_value(value)

    def get_in_args(self) -> dict[str, FnToolInArgBase]:
        return self.in_args

    def inArgsObj2kv(self) -> dict[str, str]:
        """
        入参字典，{"入参英文名":"入参的值"}
        """
        kv = {}
        if self.get_in_args() is not None:
            for a in self.get_in_args().values():
                kv[a.name] = a.value
        return kv

    def get_file_in_args(self) -> dict[str, FnToolInArgBase]:
        return {
            k: v
            for k, v in self.in_args.items()
            if v.get_data_type_enum() == Enum_Data_Type.file
        }

    def get_in_args_key_value(self) -> dict | None:
        if self.in_args is not None and len(self.in_args) > 0:
            return {k: v.value for k, v in self.in_args.items()}
        else:
            return None

    def set_out_args(self, out_args):
        self.out_args = out_args

    def get_out_args(self) -> dict[str, FnToolOutArgBase]:
        return self.out_args

    def get_cosplay_id(self) -> str:
        return self.cosplay_id

    def get_cn_name_alias(self) -> list[str]:
        """中文别名，例如：["头条新闻","热点新闻"]"""
        return self.cn_name_alias

    @abstractmethod
    def exec(self) -> dict:
        pass

    @abstractmethod
    def addArg(self, cn_name: str, name: str, human_prompt: str | None):
        pass

    @abstractmethod
    def setArgsValue(self, name: str, value: str):
        pass

    @abstractmethod
    def setArgsValues(self, values: dict):
        pass

    @abstractmethod
    def getEmptyInArg(self) -> FnToolInArgBase:
        pass

    @abstractmethod
    def genArgsLLMPrompt(self, t: str, fn_name: str) -> str:
        pass

    @abstractmethod
    def chat(messages: list) -> str:
        pass


# if __name__ == '__main__':
#     import sys
#     sys.path.insert(0, ".")
#     import hirpa.utils.utils as u
#     ins = FnToolBase('','','','','','','')
#     u.genGetSetCode(ins)
