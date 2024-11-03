from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# long_description(後述)に、GitHub用のREADME.mdを指定
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='HSS.py', # パッケージ名(プロジェクト名)
    packages=['HSS'], # パッケージ内(プロジェクト内)のパッケージ名をリスト形式で指定

    version='1.2.1', # バージョン

    license='MIT', # ライセンス

    install_requires=['requests'], # pip installする際に同時にインストールされるパッケージ名をリスト形式で指定

    author='HSS-Project', # パッケージ作者の名前
    author_email='kazuma1112@munesky.net', # パッケージ作者の連絡先メールアドレス

    url='https://github.com/HSS-Project/HSS.py', # パッケージに関連するサイトのURL(GitHubなど)

    description='Easy to use HSS API.', # パッケージの簡単な説明
    long_description=long_description, # PyPIに'Project description'として表示されるパッケージの説明文
    long_description_content_type='text/markdown', # long_descriptionの形式を'text/plain', 'text/x-rst', 'text/markdown'のいずれかから指定
    keywords='HSS Schedule School', # PyPIでの検索用キーワードをスペース区切りで指定

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ], # パッケージ(プロジェクト)の分類。https://pypi.org/classifiers/に掲載されているものを指定可能。
)
