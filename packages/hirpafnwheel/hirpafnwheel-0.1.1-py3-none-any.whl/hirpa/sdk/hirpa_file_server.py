import io


def put_file(file_name: str, file_io: bytes) -> dict:
    """
      参数：
      file_name：文件名
      file_io：文件二级制，bytes

      返回：
          "code": "HTTP200",
          "msg": "请求/处理成功！",
          "data": {
              "id": "文件id",
              "fileSize": 文件大小,字节,
              "fileName": "文件名称",
              "path": "下载地址url",
              "deadline": 可用期限,
              "bucketName": 存储的桶名
    }

    """
    return {}


def get_file_info(id) -> dict:
    """
    参数：
    id：文件id

    返回：
    {
        "code": "HTTP200",
        "msg": "请求/处理成功！",
        "data": {
            "id": "文件id",
            "fileSize": 文件大小,
            "fileName": "文件名",
            "path": "下载地址url",
            "bucketName": "存储的桶名"
        }
    }
    """
    return {}


def get_file_bytes(id) -> dict:
    """
    参数:
    id: 文件id

    返回：
    {
        "id": 文件id,
        "fileName": 文件名,
        "content": 文件内容,BytesIO格式
    }
    如果为None，表示失败
    """
    return {}
