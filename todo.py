from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #Bir application oluşturduk.
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////Users/esra/Desktop/TodoApp/todo.db'  #Oluşturduğumuz db dosyamızın uzantısını başında ki C:\ yi silerek ekledik. Bu sayede db dosyamız ile python arasında ki köprüyü kurmuş olduk. 
db = SQLAlchemy(app) #app objesine göre bir db objesi oluşturduk.

#Ana ekranımızı oluşturduk.
@app.route("/")
def index():
    todos = Todo.query.all() #query.all fonksiyonu, tablomuzdaki tüm verileri alamızı sağlar.
    return render_template("index.html",todos = todos)

#Todo tamamlama
@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first() #id si o olan veriyi almak için query.filter_by ı kullandık.
    """if todo.complete == True:
        todo.complete = False

    else:
        todo.complete =True"""
    
    #Yukarıdaki işlem yerine aşağıdakini kullanabiliriz.
    todo.complete = not todo.complete

    db.session.commit()

    return redirect(url_for("index"))

#Todo silme
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first() #Veri tabanından veri silmek için ilk önce o veriyi alıp todo objesine eşitledik.
    db.session.delete(todo) #Daha sonra o objeyi sildik.
    db.session.commit() #Tabloyu güncelledik.
    return redirect(url_for("index"))


#Form sayfası oluşturduk.
@app.route("/add",methods=[("POST")]) #Sadece post request gelmesini istediğimiz için methods içinde sadece post u yazdık.
def addTodo():
    title = request.form.get("title") #İndexteki form ekranında girilen title bilgisini alıp title objesine ekledik.
    newTodo = Todo(title = title,complete = False) #title ı index ekranında girileni kullandık.complete daha tamamlanmamış varsaydığımız için false olarak başlattık.
    db.session.add(newTodo) #newTodo objemizi veri tabanına ekledik. Veri tabanıyla işlemleri ORM üzerinden yaptığımız için session kullanıyoruz.
    db.session.commit()
    return redirect(url_for("index"))

class Todo(db.Model): #db dosyamız içinde tablo oluşturmamızı sağlayacak olan class yazılırken db objesinin içinde ki .Model kullanılır.
    id = db.Column(db.Integer, primary_key=True) #id isimli bir (özellik)sütun oluşturduk. db. şeklinde özelliğimizin türünü belirttik. Her id den bir tane olmasını istediğimiz için primary_key i True yaptık.
    title = db.Column(db.String(80)) #title isimli bir (özellik)sütun oluşturduk. db. şeklinde özelliğimizin türünü belirttik. title özelliğimizin maksimum 80 karakter olmasını istediğimiz için String() şekline belirttik.
    complete = db.Column(db.Boolean) # İşin tamamlanıp tamamlanmama durumuna göre True ya da False değeri alacağı için complete özelliğimizi boolean olarak oluşturduk. Tamamlandıysa True tamamlanmadıysa False değeri alacağı için False olarak başlatıyoruz.

if __name__ == "__main__": #Flaskta survır ı ayağa kaldırdık.
    with app.app_context():#Tablomuzun uygulama çalışmadan hemen önce oluşmasını istediğimiz için buraya koyduk. createall fonksiyonu daha önce oluşturulmuş olan tabloyu tekrar tekrar çalıştırmaz.
        db.create_all()
    app.run(debug=True)



 