from setuptools import setup, find_packages

setup(
    name='csdn-mzh',
    version='0.4',
    packages=find_packages(),
    description="这里是包的简短描述",  # 项目描述
    long_description=open('README.md', encoding='utf-8').read(),  # 详细描述，通常放在 README 文件中
    long_description_content_type='text/markdown',  # 确定 README 格式（如 markdown）
    author="你的名字",
    author_email="你的邮箱@qq.com",
    url="https://github.com/your-repo",  # 项目网址（可选）
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['csdn'],  # 如果有依赖包，请在此列出,
)