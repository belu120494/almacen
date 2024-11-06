from flask import Flask,  render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Creacion de la base de datos y las tablas
def init_database():
    conn = sqlite3.connect("almacen.db") # Crea la base de datos si es que no existiera, caso contrario realiza la conexion
    
    cursor = conn.cursor() # El cursor nos permite realizar sentencias SQL dentro de la DB
    
    # Creando la tabla personas usando DML
    cursor.execute(
        """
        create table if not exists producto(
            id integer primary key, --en sqlite crea una secuencia automatica a las PK
            descripcion text not null,
            cantidad int not null,
            precio float not null
        )
        """
    )
    conn.commit() # Confirma la ejecucion de la sentencia
    conn.close() # Cierra la conexion con la DB
    
init_database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/producto")
def producto():
    conn = sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row # Permite manejar los registros como diccionarios
    
    cursor = conn.cursor()
    cursor.execute("select * from producto")
    producto = cursor.fetchall()
    return render_template("producto/index.html", producto = producto)

@app.route("/producto/create")
def create():
    return render_template('producto/create.html')

@app.route("/producto/create/save",methods=['POST'])
def producto_save():
    descripcion =  request.form['descripcion']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    
    cursor.execute("insert into producto (descripcion, cantidad, precio) values (?, ?, ?)", (descripcion, cantidad, precio))
    
    conn.commit()
    conn.close()
    return redirect('/producto')

# Editar producto
@app.route("/producto/edit/<int:id>")
def producto_edit(id):
    conn =  sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row
    cursor =  conn.cursor()
    cursor.execute("select * from producto where id = ?", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template("producto/edit.html", producto = producto)

@app.route("/producto/update", methods = ['POST'])
def producto_update():
    id = request.form['id']
    descripcion = request.form['descripcion']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    
    conn  = sqlite3.connect("almacen.db")
    cursor =  conn.cursor()
    
    cursor.execute("update producto SET descripcion = ? ,cantidad = ?, precio = ? where id=?", (descripcion, cantidad, precio, id))
    conn.commit()
    conn.close()
    return redirect("/producto")

# Eliminar registro
@app.route("/producto/delete/<int:id>")
def producto_delete(id):
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("delete from producto where id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/producto')

    
if __name__ == "__main__":
    app.run(debug = True)