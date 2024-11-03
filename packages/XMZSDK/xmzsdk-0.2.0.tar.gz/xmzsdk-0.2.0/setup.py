from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="XMZSDK",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        # 这里添加你的包依赖，例如：
        "opentelemetry-api",
        "opentelemetry-sdk",
        "opentelemetry-exporter-otlp",
        "requests",
        "huaweicloudsdkcore",
        "huaweicloudsdknlp",
        "esdk-obs-python",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="小米粥",
    author_email="mzapi@x.mizhoubaobei.top",
    url="https://github.com/xiaomizhoubaobei/XMZAPI",  # 你的项目URL
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
