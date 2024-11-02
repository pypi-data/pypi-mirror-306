from setuptools import setup, find_packages

# requirements.txtから依存関係を読み込む
with open("new_requirements.txt", encoding="utf-8") as f:
    required_packages = f.read().splitlines()

# README.md から long_description を読み込む
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="MultilingualSpeaker",  # パッケージ名。PyPI上でユニークである必要があります
    version="0.0.1",    # バージョン番号
    author="NPO_KS_903", # 作者の名前
    author_email="xksxkatuyoshi0009@gmail.com", # 作者のメール
    description="A brief description of the library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NPO_KS903/MultilingualSpeaker", # GitHubリポジトリのURL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required_packages,  # 依存関係を追加
)
