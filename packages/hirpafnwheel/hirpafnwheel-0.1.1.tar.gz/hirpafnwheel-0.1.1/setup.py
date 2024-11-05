from setuptools import setup, find_packages

content = ""
with open("README.md", "r", encoding="utf-8") as file:
    content = file.read()

setup(
    name="hirpafnwheel",
    version="0.1.1",
    author="AISware RPA Team",
    author_email="airpa@asiainfo.com",
    description="用于编写hirpa中原子能里的脚手架，对应Hirpa引擎0.8.5以上版本",
    long_description=content,
    long_description_content_type="text/markdown",
    url="http://airpa.asiainfo.com.cn",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=["pydantic==1.10.12", "Requests==2.31.0", "openpyxl==3.1.2"],
)

# setup(
#     name="my_library",
#     version="0.1.0",
#     author="Your Name",
#     author_email="your.email@example.com",
#     description="A simple example library",
#     long_description=open("README.md", encoding="utf-8").read(),
#     long_description_content_type="text/markdown",
#     url="https://github.com/yourusername/my_library",
#     packages=find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.6",
#     install_requires=[
#         # 列出你的库依赖的其他包
#     ],
#     test_suite="tests",
# )

## python setup.py sdist bdist_wheel
