# 新規作成したルーティングについて
新規作成したルーティングの一覧
```
##read機能
GET  /  categoryテーブルの一覧表示、およびカードの作成・変更・削除ボタン
GET /read_db/<category_name>    todoテーブルから指定のcategory_nameを持つ行のみを抽出して表示

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

### カテゴリカードの一覧表示
```python
@app.route('/')
def index():
    #カテゴリカードを管理するデータベース
    category_table = getDataBase(clss=CategoryTable)
    return render_template('first_page.html',
                            DATA=category_table)
```
### カテゴリカードの作成
2つのルーティングを作成しました。```form_create_card```関数はカテゴリカードの名前を指定するためのフォームを呼び出します。```create_card```関数はフォームの内容に従って```category```テーブルに追加します。
```python
@app.route('/form_create_card')
def form_create_card():
    #db = getAllCategory()
    db = getDataBase(clss=CategoryTable)
    return render_template('form_create_card.html',
                            title="create card",
                            DATA=db)
@app.route('/create_card', methods=["POST"])
def create_card():
    category = request.form["category"]
    new_card = CategoryTable(category=category)
    with Session(ENGINE) as session:
        session.add(new_card)
        session.commit()
    return render_template("result.html",
                            msg=f'create new card')
```
### カテゴリカードの変更
2つのルーティングを作成しました。```form_update_card```関数はカテゴリカードを指定するためのフォームを呼び出します。```update_card```関数はフォームの内容に従って```category```テーブルを変更します。

```python
@app.route('/form_update_card')
def form_update_card():
    #db = getAllCategory()
    db = getDataBase(clss=CategoryTable)
    return render_template('form_update_card.html',
                            title="update a card",
                            DATA=db)
@app.route('/update_card', methods=["POST"])
def update_card():
    category_name = request.form.get("ID")
    new_category = request.form.get("category")
    with Session(ENGINE) as ses:
        data = ses.query(CategoryTable)\
                .filter(CategoryTable.id==category_name).one_or_none()
        if data is None:
            return render_template(
                "result.html",
                msg=f"指定したid {category_name} は存在しません"
            )
        data.category = new_category
        ses.add(data)
        ses.commit()
    return render_template("result.html",
                            msg=f'update a card')
```

### カテゴリカードの削除
2つのルーティングを作成しました。```form_delete_card```関数はカテゴリカードを指定するためのフォームを呼び出します。```delete_card```関数はフォームの内容に従って```category```テーブルから削除します。
```python
@app.route('/form_delete_card')
def form_delete_card():
    #db = getAllCategory()
    db = getDataBase(clss=CategoryTable)
    return render_template('form_delete_card.html',
                            title="delete",
                            DATA=db)
@app.route('/delete_card', methods=["POST"])
def delete_card():
    id = request.form.get("ID")
    Session = sessionmaker(bind=ENGINE)
    ses = Session()
    data = ses.query(CategoryTable).filter(CategoryTable.id==str(id)).one_or_none()
    #存在しないidを入力した場合
    if data is None:
        ses.close()
        return render_template(
            "result.html",
            msg="指定したid: {} は存在しません.".format(id)
        )
    ses.delete(data)
    ses.commit()
    ses.close()
    return render_template("result.html",
                            msg=f'delete a card')
```

### カテゴリカードの中身を表示
URLにある```category_name```をもつデータを```ToDoListWithCategory```テーブルから抽出して表示します。

```python
@app.route('/read_db/<category_name>')
def read_DB(category_name):
    #print(f'enterd id: {category_name}')
    #db = get_filteredRow(category_name)
    category_name = str(category_name)
    db = getDataBase(clss=DB, filter=category_name)
    print(db)
    return render_template('index.html',
                            title='TODOリスト',
                            DATA=db)
```

# 補足: 前回作成したルーティング
前回作成したルーティングのうち、以下の6つを引き続き利用する。
```
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
### ToDoリストの作成
index.htmlにはcreate用のボタンがあり、このボタンをクリックすることで起動します。createの詳細を記述するためのフォームである ```form_for_create.html``` を返します。
また、```create```関数はフォームの内容に従って```ToDoListWithCategory```テーブルに追加します。
```python
@app.route('/form_create', methods=["GET"])
def edit_for_create():
    #db = getAll()
    db = getDataBase(clss=DB)
    return render_template("form_for_create.html", 
                            title="新規作成",
                            DATA=db)
#2. postされた内容をデータベースに追加
@app.route('/create', methods=['POST'])
def create():
    new_todo = DB(todo=request.form["TODO"],category_name=request.form["category_name"])
    category_name = request.form["category_name"]
    with Session(ENGINE) as session:
        session.add(new_todo)
        #追加したものを取り出す
        session.commit() #追加を永続的に反映させる
    return render_template(
        'result.html',
        msg=f'{request.form["TODO"]}を create しました',
        category_name=category_name)
```

### ToDoリストの変更
index.htmlにはupdate用のボタンがあり、このボタンをクリックすることで起動します。updateの詳細を記述するためのフォームである ```form_for_update.html``` を返します。
また、```update```関数はフォームの内容に従って```ToDoListWithCategory```テーブルを変更します。
```python
@app.route('/form_update', methods=['GET'])
def edit_for_update():
    #db = getAll()
    db = getDataBase(clss=DB)
    return render_template("form_for_update.html", 
                            title="todoリストを変更",
                            DATA=db)
#2. postされた内容でデータベースを変更
@app.route('/update', methods=['POST'])
def update():
    #リクエストからid, todo内容を抽出
    id = request.form.get("ID")
    new_todo = request.form.get("TODO")
    category_name = request.form.get("category_name")
    #データベースにアクセスして変更
    Session = sessionmaker(bind=ENGINE)
    ses = Session()
    #filter関数ではidとcategory_nameのAND条件を適用
    data = ses.query(DB).filter(DB.id==id, DB.category_name==category_name).one_or_none() 
    if data is None:
        ses.close()
        return render_template(
            "result.html",
            msg="ID: {} は存在しません.".format(id),
            category_name=category_name
        )
    data.todo = new_todo
    ses.add(data)
    ses.commit()
    ses.close()
    return render_template(
        'result.html',
        msg="id:{}を {} へ updateしました.".format(id, new_todo),
        category_name=category_name
        )
```

### ToDoリストの削除
index.htmlにはdelete用のボタンがあり、このボタンをクリックすることで起動します。deleteの詳細を記述するためのフォームである ```form_for_delete.html``` を返します。
また、```delete```関数はフォームの内容に従って```ToDoListWithCategory```テーブルから削除します。
```python
@app.route('/form_delete', methods=['GET'])
def edit_for_delete():
    #db = getAll()
    db = getDataBase(clss=DB)
    return render_template("form_for_delete.html", 
                            title="todoを削除",
                            DATA=db)
#2. postされたidをデータベースから削除
@app.route('/delete', methods=['POST'])
def delete():
    id = request.form.get("ID")
    category_name = request.form.get("category_name")
    Session = sessionmaker(bind=ENGINE)
    ses = Session()
    #id AND categiry_nameでフィルタ
    data = ses.query(DB).filter(DB.id==id, DB.category_name==category_name).one_or_none()
    #存在しないidを入力した場合
    if data is None:
        ses.close()
        return render_template(
            "result.html",
            msg="ID: {} は存在しません.".format(id),
            category_name=category_name,
            flg = flg
        )
    ses.delete(data)
    ses.commit()
    ses.close()
    return render_template(
        "result.html",
        msg="id:{} をdelete しました.".format(id),
        category_name=category_name
        )
```