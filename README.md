# ToDoapp

# メモ
## 用いるディレクトリの中身について
```
---- todoDB.sqlite3 #データベースファイル
|
|--- app.py         #サーバー用ファイル
|--- templates
    |--- first_page.html # categoryテーブルの一覧表示
    |--- form_create_card.html #カテゴリカードを作成するためのフォーム
    |--- form_update_card.html #カテゴリカードを変更するためのフォーム
    |--- form_delete_card.html #カテゴリカードを削除するためのフォーム
    |
    |--- index.html            # todoリストの中身を一覧表示
    |--- form_for_create.html  #todoリストを作成するためのフォーム
    |--- form_for_update.html  #todoリストを変更するためのフォーム
    |--- form_for_delete.html  #todoリストを削除するためのフォーム
    |
    |--- form_layout.html      #入力フォームの体裁を管理するhtmlファイル
    |--- result.html           #フォーム送信後の結果を表示する画面


```
### 用いるデータベースについて
2つのデータベースを利用する
```
テーブル名: category
| id | category |
| 1  |   ja     |
| 2  |   en     |
```
```
テーブル名: ToDoListWithCategory
| id |  todo  | category_name |
| 1  |  朝食  |    ja         |
| 2  | 　　帰宅  |    ja         |
| 3  | lunch |    en         |
```
前者の```categoryテーブル```はカテゴリカードを管理するためのデータベースで、後者の```ToDoListWithCategoryテーブル```はToDoListを管理するデータベースです。

### データベースを扱うためのpythonのクラスについて
以下の2つのpythonクラスを用意します。これらを介して、SQLAlchemyはsqlオブジェクトをpythonオブジェクトに変換します。
### categoryテーブル
```python
#app.py
class CategoryTable(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    category = Column(String(255))

    def toDict(self):
        return {
            'id': int(self.id),
            'category': str(self.category)
        }
```
### ToDoListWithCategoryテーブル
```python
#app.py
class DB(Base):
    __tablename__ = "ToDoListWithCategory"
    id = Column(Integer, primary_key=True)
    todo = Column(String(255))
    category_name = Column(String(255))
    def toDict(self):
        return {
            'id': int(self.id),
            'todo': str(self.todo),
            'category_name':str(self.category_name)
        }
```


## ルーティング一覧
今回新たに8つのルーティングを追加しました。全ルーティングはapp.pyに記述。

### 今回新たに作成したルーティング
```python
##read機能
GET  /  categoryテーブルの一覧表示、およびカードの作成・変更・削除ボタン
GET /read_db/<category_name>    todoテーブルから指定のcategory_idを持つ行のみを抽出して表示

## create機能
GET /form_create_card  カテゴリカードを作成するフォーム画面を表示
POST /create_card  フォームの内容に従ってデータベースに追加

## update機能
GET /form_update_card  カテゴリカードを変更するフォーム画面を表示
POST /update_card  フォームに従ってデータベースを変更

## delete機能
GET /form_delete_card  カテゴリカードを削除するフォームを表示
POST /delete_card  フォームに従ってデータベースから削除

```

### 前回作成したルーティング
前回作成したルーティングのうち、以下の6つも用います。
```python

#create機能
GET  /form_create  createの内容を記述するフォームを表示
POST /create       todoリストに新規追加する

#update機能
GET  /form_update   updateの内容を記述するフォームを表示
POST /update       todoリストを変更する

#delete機能
GET  /form_delete  deleteの内容を記述するフォームを表示
POST /delete       todoリストから特定の項目を削除

```

## ブラウザの表示画面
```templates/first_page.html```の画面

<img src="https://user-images.githubusercontent.com/70735561/146122758-d89453a8-8226-46d6-8cf2-19d3ebf0909e.png">


緑の四角(以下、カテゴリカード)がToDoリストのカテゴリ分けを表しています。青いボタンを押すと```templates/index.html```が呼び出されます。
また、下の3つの灰色のボタンはカテゴリカードの作成、変更、削除をするためのフォームを呼び出すためのもの。

```templates/index.html```の画面
<img src="https://user-images.githubusercontent.com/70735561/146122991-3457c62c-d357-4bf4-8855-12cc6beb9345.png">

```ToDoListWithCategory```テーブルから、クリックした青いボタンのカテゴリ名だけを表示します。
上の3つの灰色のボタンはtodoリストを作成、変更、削除するためのボタンです。
また、下の灰色のボタンを押すとカテゴリカードの一覧画面(```emplates/first_page.html```)に戻ります。
