from tkcalendar import Calendar, DateEntry
import tkinter as tk

import tkinter.ttk as ttk
import mysql.connector
from tkinter import messagebox

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="")

db_cursor = db_connection.cursor(buffered=True)


class Aplicacion:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Login")
        self.ventana.resizable(0,0)
        self.ventana.geometry("200x200+500+250")
       

        self.usuario = tk.StringVar()
        self.clave = tk.StringVar()

        self.admin = tk.Entry(self.ventana,textvariable=self.usuario)
        self.admin.place(x=40,y=50)

        self.passww = tk.Entry(self.ventana,show="*",textvariable=self.clave)
        self.passww.place(x=40,y=100)


        self.label1 = tk.Label(self.ventana,text="Usuario")
        self.label1.place(x=80,y=20)
        self.label2 = tk.Label(self.ventana,text="Constraseña")
        self.label2.place(x=70,y=70)

        self.boton = tk.Button(self.ventana,text="Acceder",command=self.Acceder)
        self.boton.place(x=70,y=150)
        self.ventana.mainloop()

    def Acceder(self):
        if (self.usuario.get() =="admin" and self.clave.get() == "admin"):
            self.Nuevo()
        else:
            messagebox.showerror(title="Error",message="Datos incorrectos")

    def Nuevo(self):
        self.ventana.destroy()
        self.nueva_ventana= tk.Tk()        
        
        self.nueva_ventana.geometry("500x500+351+174")
        self.nueva_ventana.title("Sistema de Acceso")

        self.label1 = tk.Label(self.nueva_ventana,text="Registro Nuevo Automovil",font=("Helvetica",12))
        self.label1.place(x=150,y=20)

        self.entrada1 = tk.Entry(self.nueva_ventana)
        self.entrada1.place(x=200,y=50)
        
        self.entrada2 = tk.Entry(self.nueva_ventana)
        self.entrada2.place(x=200,y=80)
        
        self.entrada3 = tk.Entry(self.nueva_ventana)
        self.entrada3.place(x=200,y=110)

        self.entrada4 = tk.Entry(self.nueva_ventana)
        self.entrada4.place(x=200,y=200)

        self.busqueda = tk.Entry(self.nueva_ventana)
        self.busqueda.place(x=150,y=200)

        self.busqueda1 = tk.Label(self.nueva_ventana,text="Buscar :",font=("Helvetica",10))
        self.busqueda1.place(x=80,y=200)


        self.label2 = tk.Label(self.nueva_ventana,text="Nombre :",font=("Helvetica",10))
        self.label2.place(x=100,y=50)
        self.label3 = tk.Label(self.nueva_ventana,text="Apellido :",font=("Helvetica",10))
        self.label3.place(x=100,y=80)
        self.label4 = tk.Label(self.nueva_ventana,text="Placa :",font=("Helvetica",10))
        self.label4.place(x=100,y=110)

        self.guardar = tk.Button(self.nueva_ventana,text="Guardar",border=5,command=self.Guardar)
        self.guardar.place(x=80,y=150)

        self.borrar = tk.Button(self.nueva_ventana,text="Eliminar ",border=5,command=self.borrar_registro)
        self.borrar.place(x=215,y=150)

        self.editar = tk.Button(self.nueva_ventana,text="Actualizar",border=5,command=self.editar_tabla)
        self.editar.place(x=350,y=150)

        self.editar1 = tk.Button(self.nueva_ventana,text="Buscar",border=5,command=self.buscar_registro)
        self.editar1.place(x=350,y=200)

        self.editar1 = tk.Button(self.nueva_ventana,text="Mostar",border=5,command=self.actualizar_tabla)
        self.editar1.place(x=420,y=200)

        



        columns = ("#1", "#2", "#3", "#4")
        

        self.tvStudent = ttk.Treeview(self.nueva_ventana, show="headings", height="5", columns=columns)
        self.tvStudent.heading('#1', text='Numero', anchor='center')
        self.tvStudent.column('#1', width=60, anchor='center', stretch=False)
        self.tvStudent.heading('#2', text='Nombre', anchor='center')
        self.tvStudent.column('#2', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#3', text='Apellido', anchor='center')
        self.tvStudent.column('#3', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#4', text='Placa', anchor='center')
        self.tvStudent.column('#4', width=10, anchor='center', stretch=True)        
        
        vsb = ttk.Scrollbar(self.nueva_ventana, orient=tk.VERTICAL, command=self.tvStudent.yview)
        vsb.place(x=40 + 400 + 1, y=250, height=180 + 20)
        self.tvStudent.configure(yscroll=vsb.set)
        hsb = ttk.Scrollbar(self.nueva_ventana, orient=tk.HORIZONTAL, command=self.tvStudent.xview)
        hsb.place(x=40, y=310+200+1, width=620 + 20)
        self.tvStudent.configure(xscroll=hsb.set)
        self.tvStudent.place(x=40, y=250, height=200, width=400)
        self.tvStudent.configure(xscroll=hsb.set)
        self.tvStudent.bind("<<TreeviewSelect>>", self.mostrar_seleccion)
       

        self.create_table()
        self.actualizar_tabla()

        self.nueva_ventana.mainloop()

    def clear_form(self):
        self.entrada1.delete(0, tk.END)
        self.entrada2.delete(0, tk.END)
        self.entrada3.delete(0, tk.END)


    def create_table(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
            
        db_cursor.execute("CREATE DATABASE IF NOT EXISTS Datos")
        db_cursor.execute("use Datos") 
        db_cursor.execute("create table if not exists registro(Id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,codigo INT(15),nombre VARCHAR(30),apellido VARCHAR(30),placa VARCHAR(20))AUTO_INCREMENT=1")
        db_connection.commit()  

   
    
    def Guardar(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        nombre = self.entrada1.get() 
        apellido = self.entrada2.get()  
        placa = self.entrada3.get() 
        
        if nombre == "":
            messagebox.showinfo('Información', "Introduzca el Nombre")
            self.entrada1.focus_set()
            return
        if apellido == "":
            messagebox.showinfo('Información', "Introduzca el Apellido")
            self.entrada2.focus_set()
            return
        if placa == "":
            messagebox.showinfo('Información', "Introduzca la Placa")
            self.entrada3.focus_set()
            return
  
        try:
            codigo = int(self.ordenar())
            print("Identificación de auto nuevo: " + str(codigo))
            query2 = "INSERT INTO registro (codigo, nombre,apellido,placa) VALUES (%s, %s,%s, %s)"
            
            db_cursor.execute(query2, (codigo, nombre, apellido, placa))
            messagebox.showinfo('Información', "Registro de Automovil con éxito")
            
            db_connection.commit()
            self.actualizar_tabla()
        except mysql.connector.Error as err:
            print(err)
            
            db_connection.rollback()
            messagebox.showinfo('Información', "¡¡¡La inserción de datos falló !!!")
        finally:
            db_connection.close()
    
    def ordenar(self):
    
        if db_connection.is_connected() == False:
            db_connection.connect()
        db_cursor.execute("use Datos")  
        codigo = 0
        query1 = "SELECT codigo FROM registro order by id DESC LIMIT 1"
           
        db_cursor.execute(query1) 
        print("No de registro obtenido:" + str(db_cursor.rowcount))
        if db_cursor.rowcount == 0:
                codigo = 1
        else:
            rows = db_cursor.fetchall()
            for row in rows:
                codigo = row[0]
                codigo = codigo + 1
                print("Número máximo de identificación del coche:" + str(codigo))
        return codigo

    def actualizar_tabla(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        
        self.tvStudent.delete(*self.tvStudent.get_children())
            
        db_cursor.execute("use Datos")  
        sql = "SELECT codigo,nombre,apellido,placa FROM registro"
        db_cursor.execute(sql)
        total = db_cursor.rowcount
            
        print( "Total de entradas de datos:" + str(total))
        rows = db_cursor.fetchall()
        RollNo = ""
        First_Name = ""
        Last_Name = ""
        City = ""
        
        for row in rows:
            RollNo = row[0]
            First_Name = row[1]
            Last_Name = row[2]
            City = row[3]            
            self.tvStudent.insert("", 'end', text=RollNo, values=(
                    RollNo, First_Name, Last_Name, City))


    
    
    def mostrar_seleccion(self, event):
    
        self.clear_form()
        for selection in self.tvStudent.selection():
            item = self.tvStudent.item(selection)
            global roll_no
            roll_no, first_name, last_name, city = item["values"][0:4]
            self.entrada1.insert(0, first_name)
            self.entrada2.insert(0, last_name)
            self.entrada3.insert(0, city)            
        return roll_no

    def editar_tabla(self):
    
        if db_connection.is_connected() == False:
            db_connection.connect()
        print("Cargando....")
        db_cursor.execute("use Datos")  
        First_Name = self.entrada1.get()
        Last_Name = self.entrada2.get()
        Phone_Number = self.entrada3.get()
        
        print(roll_no)
        Update = "Update registro set nombre='%s', apellido='%s', placa='%s' where codigo='%s'" % (First_Name, Last_Name, Phone_Number, roll_no)
        db_cursor.execute(Update)
        db_connection.commit()
        messagebox.showinfo("Información", "Registro del estudiante seleccionado actualizado con éxito")

        self.actualizar_tabla()
    def borrar_registro(self):
        MsgBox = messagebox.askquestion('Eliminar registro', '¿Estás seguro? desea eliminar el registro de automóvil seleccionado ', icon='warning')
        if MsgBox == 'yes':
            if db_connection.is_connected() == False:
                db_connection.connect()
            db_cursor.execute("use Datos")  
            Delete = "delete from registro where codigo='%s'" % (roll_no)
            db_cursor.execute(Delete)
            db_connection.commit()
            messagebox.showinfo("Información", "Registro de automóvil eliminado con éxito")
            self.actualizar_tabla()
            self.entrada1.delete(0, tk.END)
            self.entrada2.delete(0, tk.END)
            self.entrada3 .delete(0, tk.END)

    def buscar_registro(self):
    

        if db_connection.is_connected() == False:
            db_connection.connect()
        s_roll_no = self.busqueda.get()  
        print(s_roll_no)
        if s_roll_no == "":
            messagebox.showinfo('Información', "Por favor ingrese la placa del Automovil")
            self.busqueda.focus_set()
            return
    
        self.tvStudent.delete(*self.tvStudent.get_children())
    
        db_cursor.execute("use Datos")  
        sql = "SELECT codigo,nombre,apellido,placa FROM registro where placa='" + \
        s_roll_no + "'"
        db_cursor.execute(sql)
        total = db_cursor.rowcount
   
        print("Total de entradas de datos:" + str(total))
        rows = db_cursor.fetchall()
        RollNo = ""
        First_Name = ""
        Last_Name = ""
        City = ""
        for row in rows:
            RollNo = row[0]
            First_Name = row[1]
            Last_Name = row[2]
            City = row[3]
            self.tvStudent.insert("", 'end', text=RollNo, values=(
            RollNo, First_Name, Last_Name, City))
            

login = Aplicacion()