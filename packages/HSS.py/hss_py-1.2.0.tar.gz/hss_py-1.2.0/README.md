# HSSAPI-Python  
[![PyPI](https://img.shields.io/badge/-Pypi-000.svg?logo=pypi&style=plastic)](https://pypi.org/project/HSS.py/) <img src="https://img.shields.io/badge/-Python-ffd700.svg?logo=python&style=plastic">
  
## 目的
HSSAPIをPythonで簡単にしようできるようにしたAPIラッパー

# 使用方法
***[HSS API ドキュメント](https://hss-dev-docs.aknet.tech/)***  
***APIラッパーは一部の機能をサポートしています。  API機能を全て活用したい場合、Request_HHSAPI.pyやHSS.pyのget_data関数を使用することにより処理ができると思われます。***  
## インストール
```
pip install HSS.py
```
### githubから直接インストールする
```
pip install git+https://github.com/HSS-Project/HSS.py.git
```
or 
```
pip install git+git@github.com:HSS-Project/HSS.py.git
```

## 初期設定
***HSS APIでtokenを発行してください。***  
**tokenをUser NewSchoolに渡してください。またNewSchoolには学校idを渡してください。**  
```py
from HSS import NewSchool
from HSS import User

token = "HSS API token"
user = User(token=token)
school = NewSchool(token=token,schoolid=schoolid)
```

### User

```py 
def get_permission() -> list:
    """（GET /v1/permission）"""
```   
```py
def get_permission_discordUserID(DiscordUserID) -> list: 
    """(GET /v1/permission/discordUserID) DiscurdUserIDからそのユーザーが閲覧できる学校listを取得します。(DIscord Bot作成に使用してください。)"""
```
```py
def get_id(ID) -> dict:
    """(GET /v1/users/{HSSUserID}) user情報を取得します。"""
```
**レスポンス ( Example )**
```py
{
    "developer": bool,
    "hid": int,
    "discordAccount": bool,
    "username": str,
    "isBot": bool or None,
    "description": str or None
}
```
|  値名  |  型  | 説明  | かならず出現するか  |
| ---- | ---- | ---- | ---- |
|  developer  |  bool  | 開発者が有効かどうかです。全てのアカウントでtrueになります。  |true |
|  hid  |  int  | ユーザーのUniqueIDです。  |true |
|  discordAccount  |  bool  | Discordアカウントでの登録が有効かどうかです。  |true |
|  username  |  str  | ユーザーの名前です。  |true |
|  isBot  |  bool  | ユーザーがBotかどうかを判別します。Botの場合出現します。 | false  |
|  description  |  str  | Botの説明です。  | false  |

```py
def get_me() -> dict:
    """(GET /v1/users/@me) """
```
**レスポンス ( Example )**

```py
{
    "developer" : bool.
    "hid" : int,
    "discordAccount" : bool,
    "username" : str,
    "email" : str
}
```

|  値名  |  型  | 説明  | かならず出現するか  |
| ---- | ---- | ---- | ---- |
|  developer  |  bool  | 開発者が有効かどうかです。 | true |
|  hid  |  int | ユーザーのUniqueIDです。   | true |
|  discordAccount  |  bool  | Discordアカウントでの登録が有効かどうかです。   | true |
|  username  |  str  | ユーザーの名前です。  | true |
|  email  |  str  | ユーザーのメールアドレスです。 <br />※`@me`の場合のみ出現します。  | true |

### NewScool

```py
def get_classes() -> list:
    """クラスlistを取得します"""
```
```py
def search_class(grade:int,classname:int) -> int: 
    """学年-クラスからUserDatasのlistのindexを取得します。"""
```
***今後のnumberはこれを使用してください。***  
***class,classnameは必ずint型で渡してください。今後strでもいけるよう修正されると思われます。***   

### MonthData
```py
"MonthData" 
= {

    "sun" : [],
    "mon" : [],
    "tue" : [],
    "wed" : [],
    "thu" : [],
    "fri" : [],
    "sat" : []
}
```

```py
def grade(number:int) -> int:
    """学年を取得します。"""
```
```py
def classname(number:int) -> int:
    """クラスを取得します。"""
```

```py
def get_timeline(number:int,MonthData:str) -> list[dict]:
```
**レスポンス ( Example )**
```py
{
    "name": str,
    "place": None or str,
    "IsEvent": bool
}
```
| プロパティ | 型 | 説明 |
| --- | --- | --- |
| name | str | 名 |
| place | None \| str | 場所 |
| IsEvent | bool | イベントかどうか |


```py
def get_default_timeline(number:int,MonthData:str) -> list[dict]:
    """基本時間割を取得します(timelineと同じ)"""
```
```py
def get_homework(number:int) -> list[dict]:
    """宿題を取得します。  """
```
**レスポンス ( Example )**  
```py
{
    "name" : str,
    "istooBig" : bool,
    "page" : {
        "start" : str or int,
        "end" : str or int,
        "comment" : str or None
    }
}
```
| プロパティ名 | 型 | 内容 |
| ---- | ---- | ---- |
| name | str | 名前 |
| istooBig | bool | とっても大きくてやるのに時間がかかるものか |
| page | dict | ページ情報 |
| page.start | str or int | はじまり |
| page.end | str or int | おわり |
| page.comment | str or int | 補足等 |

```py
def get_event(number:int,MonthData:str) -> list[dict]:
    """イベント情報を取得します。  """
``` 
**レスポンス ( Example )**  
```py
{
    "name": str,
    "timeData" : TimeData,
    "place": str or None
}
```
| プロパティ名 | 型 | 説明 |
| --- | --- | --- |
| name | str | イベント名 |
| timeData | [TimeData](./timedata) | イベントの時間データ |
| place | str | イベントの場所 |

```py
def default_timelineindex(number:int) -> int:
    """基本的な時間割数"""
```
```py
def patch_timeline(grade:int,classname:int,date:str,name:str,isEvent:bool,state:str = "add", index:int=None, place:str=None): 
```
(PATCH /v1/school/:id/userdatas/:grade/:class/:mon) TimeLineの変更  
stateに応じて、追加、削除、更新します。  
***updateやremoveの場合は、indexを指定してください。そのindexで上書きをします。***  
| パラメータ | 形 | 説明 |
| --- | --- | --- |
| state | str | "add" or "remove" or "update"|  
  
***addはdefaultTimeLineIndexより多い場合には追加されません。エラーがスローされます。***       
  
```py
def update_timelineindex(grade:int,classname:int,date:str,index:int):
```
***非推奨***
  
```py
def patch_defaulttimeline(grade:int,classname:int,date:str,name:str,isEvent:bool,state:str = "add", index:int=None, place:str="なし"):  
    """標準時間割の変更。 patch_timelineと同じ """
```

```py
def patch_event(grade:int, _class:int, date:str, name:str, isEndofDay:bool, start:datetime, end:datetime, place:str=None , state :str = "add" , index : int = None):
```
EventDataの変更  
stateに応じて、追加、削除、更新します。  
***updateやremoveの場合は、indexを指定してください。そのindexで上書きをします。***    
  
```py
def patch_homework(grade:int, _class:int, date:str, name:str, start, end, istooBig:bool = False, comment:str=None, state :str = "add" , index : int = None): 
    """Homeworkの変更"""
```
 
