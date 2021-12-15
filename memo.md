


## 第5回用メモ
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
| 1  |  朝食   |    ja         |
| 2  | lunch  |    en         |
```
前者の```categoryテーブル```はカテゴリカードを管理するためのデータベースで、後者の```ToDoListWithCategoryテーブル```はToDoListを管理するデータベースである。
### データベースを扱うためのpythonのクラスについて
SQLAlchemyを介してsqlite3オブジェクトをpythonのオブジェクトにマッピングするためのclassを用意した。
### categoryテーブル
```python
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
今回新たに8つのルーティングを追加した。

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
上記の新規ルーティングに併せて、前回作成した6つのルーティングも用いる。
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