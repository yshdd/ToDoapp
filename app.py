from typing import List
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from sqlalchemy import Table, MetaData


#インスタンスの生成
app = Flask(__name__)

#sqlalchemyを扱うためのオブジェクト
ENGINE = create_engine("sqlite:///todoDB.sqlite3") #connect DB
Base = declarative_base() #DBテーブルをpythonオブジェクトにマップする
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

class CategoryTable(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    category = Column(String(255))

    def toDict(self):
        return {
            'id': int(self.id),
            'category': str(self.category)
        }


def getDataBase(clss, filter=False):
    Session = sessionmaker(bind=ENGINE)
    ses = Session()
    if filter != False:
        res = ses.query(clss).filter(clss.category_name==filter).all()
    else:
        res = ses.query(clss).all()
    ses.close()
    List = []
    for item in res:
        Dict = item.toDict() #DBオブジェクトを辞書型に変換
        #List.append([Dict["id"], Dict["todo"]])
        List.append(Dict)
    return List

def getAllCategory():
    Session = sessionmaker(bind=ENGINE)
    ses = Session()
    res = ses.query(CategoryTable).all()
    ses.close()
    Set = set()
    for item in res:
        Dict = item.toDict() #DBオブジェクトを辞書型に変換
        #Set.add(Dict["category"])
        Set.add(Dict["id"])
    return Set

#最初の画面: データベースの一覧を表示
@app.route('/')
def index():
    #カテゴリを管理するデータベース
    #category_table = getAllCategory()
    category_table = getDataBase(clss=CategoryTable)
    return render_template('first_page.html',
                            DATA=category_table)

@app.route('/read_db/<category_name>')
def read_DB(category_name):
    print(f'enterd id: {category_name}')
    #db = get_filteredRow(category_name)
    category_name = str(category_name)
    db = getDataBase(clss=DB, filter=category_name)
    print(db)
    return render_template('index.html',
                            title='TODOリスト',
                            DATA=db)


#category card を新規作成
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

#category cardをupdate
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
#category cardをdelete
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


#以下、todolistの追加、変更、削除機能

##create
#1. create用のフォームを送る
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
    

##update
#1. update用のフォームをブラウザへ送る
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
    data = ses.query(DB).filter(DB.id==id, DB.category_name==category_name).one_or_none() #data.toDict["todo"]
    #one_or_none(): 複数の場合は例外が返る
    #存在しないIDを指定した場合
    if data is None:
        ses.close()
        AllCategory = list(getAllCategory())
        print(AllCategory, category_name)
        if str(category_name) in str(AllCategory):
            flg = True
        else:
            flg = False
        print(flg)
        return render_template(
            "result.html",
            msg="ID: {} は存在しません.".format(id),
            category_name=category_name,
            flg = flg
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

## delete
#1. 削除用のフォームをブラウザへ送信
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
        AllCategory = list(getAllCategory())
        print(AllCategory, category_name)
        if str(category_name) in str(AllCategory):
            flg = True
        else:
            flg = False
        print(flg)
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

if __name__ == '__main__':
    app.debug = True
    app.run(host="localhost")
