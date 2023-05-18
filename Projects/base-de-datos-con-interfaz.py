from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title("Database")
root.geometry("650x500")

mId = StringVar()
mNombre = StringVar()
mContacto = StringVar()
mTitulo = StringVar()
mProfesion = StringVar()

def conexionBBDD():
    iConexion = sqlite3.connect("idata.db")
    iCursor = iConexion.cursor()

    try:
        iCursor.execute("""
            CREATE TABLE member (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE VARCHAR(50) NOT NULL,
            CONTACTO VARCHAR(50) NOT NULL,
            TITULO VARCHAR(50) NOT NULL,
            PROFESION VARCHAR(50) NOT NULL
            )  
            """) 
        messagebox.showinfo("CONEXION", "Base de datos creada exitosamente.")
    except:
        messagebox.showinfo("CONEXION","Conexión exitosa con la base de datos.")

def eliminarBBDD():
    iConexion = sqlite3.connect("idata.db")
    iCursor = iConexion.cursor()
    if messagebox.askyesno(message="Los datos se perderan definitivamente, ¿Desea continuar?", title = "ADVERTENCIA"):
        iCursor.execute("DROP TABLE member")
    else:
        pass
    cleanCamp()
    mostrar()

def salirApp():
    valor = messagebox.askquestion("Salir","¿Está seguro que desea salir de la aplicación?")
    if valor=="yes":
        iConexion = sqlite3.connect("idata.db")
        iCursor = iConexion.cursor()
        iConexion.close()
        root.destroy()
    else:
        pass

def cleanCamp():
    mId.set("")
    mNombre.set("")
    mContacto.set("")
    mTitulo.set("")
    mProfesion.set("")

def mensaje():
    acerca = """
    Aplicación CRUD
    Creado por Aarón Aldair García Miranda
    Versión 1.0
    Tecnología Python Tkinter
    """
    messagebox.showinfo(title="INFORMACIÓN", message=acerca)

###### Métodos CRUD #######

def mostrar():
    iConexion = sqlite3.connect("idata.db")
    iCursor = iConexion.cursor()
    registros = tree.get_children()
    for i in registros:
        tree.delete(i)
    try:
        iCursor.execute("SELECT * FROM member")
        for row in iCursor:
            tree.insert("",0,text=row[0], values = (row[1], row[2], row[3], row[4]))
    except:
        pass

def crear():
    iConexion = sqlite3.connect("idata.db")
    iCursor = iConexion.cursor()
    try:
        datos = mNombre.get(), mContacto.get(), mTitulo.get(), mProfesion.get()
        iCursor.execute("INSERT INTO member VALUES(NULL,?,?,?,?)", (datos))
        iConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al crear el registro, verifique la conexión a la BBDD.")
        pass
    cleanCamp()
    mostrar()

##### CREACIÓN DE TABLA #####
tree = ttk.Treeview(height = 10, columns=('#0', '#1', '#2', '#3', '#4',))
tree.place(x=0, y=200)

tree.column('#0', width=60)
tree.heading('#0', text="ID", anchor='center')

tree.heading('#1', text="Nombre", anchor='center')

tree.heading('#2', text="Contacto", anchor='center')

tree.heading('#3', text="Título", anchor='center')

tree.heading('#4', text="Profesión", anchor='center')

def selectClick(event):
    item = tree.identify('item',event.x,event.y)
    mId.set(tree.item(item, "text"))
    mNombre.set(tree.item(item, "values")[0])
    mContacto.set(tree.item(item, "values")[1])
    mTitulo.set(tree.item(item, "values")[2])
    mProfesion.set(tree.item(item, "values")[3])

tree.bind("<Double-1>", selectClick)

def actualizar():
    iConexion = sqlite3.connect("idata.db")
    iCursor = iConexion.cursor()
    try:
        datos = mNombre.get(), mContacto.get(), mTitulo.get(), mProfesion.get()
        iCursor.execute("UPDATE member SET NOMBRE=?, CONTACTO=?, TITULO=?, PROFESION=? WHERE ID=" + mId.get(), (datos))
        iConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al actualizar el registro.")
        pass
    cleanCamp()
    mostrar()

def borrar():
    iConexion = sqlite3.connect("idata.db")
    iCursor = iConexion.cursor()
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title= "ADVERTENCIA"):
            iCursor.execute("DELETE FROM member WHERE ID=" + mId.get())
            iConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al tratar de eliminar el registro.")
        pass
    cleanCamp()
    mostrar()

##### DISEÑO #####
menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar base de datos", command = conexionBBDD)
menubasedat.add_command(label="Eliminar base de datos", command = eliminarBBDD)
menubasedat.add_command(label="Salir", command = salirApp)
menubar.add_cascade(label="Inicio", menu = menubasedat)

ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Resetear campos", command = cleanCamp)
ayudamenu.add_command(label="Acerca de", command = mensaje)
menubar.add_cascade(label="Ayuda", menu = ayudamenu)

e1 = Entry(root, textvariable=mId)

l2 = Label(root, text="Nombre")
l2.place(x=50, y=40)
e2 = Entry(root, textvariable=mNombre, width=50)
e2.place(x=110, y=40)

l3 = Label(root, text="Contacto")
l3.place(x=50, y=70)
e3 = Entry(root, textvariable=mContacto, width=30)
e3.place(x=110, y=70)

l4 = Label(root, text="Título")
l4.place(x=50, y=100)
e4 = Entry(root, textvariable=mTitulo, width=30)
e4.place(x=110, y=100)

l5 = Label(root, text="Profesión")
l5.place(x=50, y=130)
e5 = Entry(root, textvariable=mProfesion, width=30)
e5.place(x=110, y=130)

##### CREACIÓN DE BOTONES #####
b1 = Button(root, text="Crear registro", bg="pale green", command=crear)
b1.place(x=500, y=50)
b2 = Button(root, text="Modificar registro", command=actualizar)
b2.place(x=500, y=80)
b3 = Button(root, text="Mostrar lista", command=mostrar)
b3.place(x=500, y=110)
b4 = Button(root, text="Eliminar registro", bg="tomato", command=borrar)
b4.place(x=500, y=140)

root.config(menu=menubar)
    
root.mainloop()
