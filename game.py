# modulos del programa
#
# tkinter:    tengo entendido que este es un Módulo ya incluido en Python por lo que no requiere instalación.
# random:     tengo entendido que este es un Módulo ya incluido en Python por lo que no requiere instalación.
# getpass:    tengo entendido que este es un Módulo ya incluido en Python por lo que no requiere instalación.
# openpyxl:   este modulo sí Requiere instalación. 
# matplotlib: este modulo sí Requiere instalación. 



from tkinter import *
from tkinter import ttk, messagebox
import random
import openpyxl
import matplotlib.pyplot as grafico

# Aquí creo la ventana raíz de la aplicación y le pongo título e ícono

root = Tk()
root.title('Juego Adivinador')
root.iconbitmap('ICONBIT.ico')

# --- Tema visual (papel, tinta y un acento terracota), coherente con mtorreslanda.com ---
PAPEL, TINTA, ACENTO, TENUE = "#F5F3EE", "#1A1A1A", "#C0522A", "#5E5A54"
FUENTE = ("Segoe UI", 11)
root.configure(bg=PAPEL, padx=28, pady=22)
for clave, valor in {
    "*Background": PAPEL, "*Foreground": TINTA, "*Font": FUENTE,
    "*Toplevel.padX": 24, "*Toplevel.padY": 18,
    "*Label.padY": 3,
    "*Button.Background": TINTA, "*Button.Foreground": PAPEL, "*Button.activeBackground": ACENTO,
    "*Button.activeForeground": PAPEL, "*Button.relief": "flat", "*Button.borderWidth": 0,
    "*Button.padX": 16, "*Button.padY": 6, "*Button.cursor": "hand2",
    "*Entry.Background": "#FFFFFF", "*Entry.relief": "solid", "*Entry.borderWidth": 1,
    "*Entry.Font": ("Segoe UI", 13), "*Entry.Justify": "center",
    "*Radiobutton.selectColor": "#FFFFFF", "*Radiobutton.activeBackground": PAPEL,
    "*Radiobutton.padY": 2, "*Menu.Background": "#FFFFFF", "*Menu.activeBackground": ACENTO,
}.items():
    root.option_add(clave, valor)
ttk.Style().configure("Treeview", font=FUENTE, rowheight=24)
ttk.Style().configure("Treeview.Heading", font=("Segoe UI Semibold", 11))

# FUNCIONES

# Esta función se ejecuta cuando el usuario presiona "Seleccionar" en el menú principal.
# Dependiendo de lo que haya elegido(lo hago a traves de un diccionario), abre la ventana de dificultades, las estadísticas, o cierra el programa.


def clickventanaprinc(valor):
    global opcion
    seleccion = valor
    opcion = diccequiv[seleccion]
        
    if opcion==1:
        dificultad()
    
    if opcion==2:
        dificultad() 
        
    if opcion==3:
        graficador()
         
    if opcion==4:
        root.destroy()


# Abre una ventana nueva que lee el archivo Excel con los datos de los jugadores y los muestra en una tabla. También agregue dos botones para ver gráficas.


def graficador():
    global listaintentos,superlista, listaresultados_binarios
    ventanagrafica= Toplevel() ##creo la ventana.
    ventanagrafica.title('Estadisticas')
    ventanagrafica.iconbitmap('ICONBIT.ico')
    #esto de aqui hace que no se pueda interactuar con las ventana que esta debajo para evitar bugs o interacciones raras 
    ventanagrafica.transient(root)   
    ventanagrafica.grab_set()       
    ventanagrafica.focus_force()
    documentoexcel= openpyxl.load_workbook('datosjug.xlsx') # cargo la hoja de excel
    Hoja = documentoexcel['Hoja 1']
    tabla = ttk.Treeview(ventanagrafica,show='tree headings') # aqui es donde creo la tabla con treeview
    
    #defino las columnas y les pongo titulos para que aparezcan en la tabla
    tabla['columns'] = ("Nombre", "Intentos", "Resultado")
    tabla.column("#0", width=40)
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Intentos", text="Intentos")
    tabla.heading("Resultado", text="Resultado")
    
    #a partir de aqui empiezo a rellenar la tabla usando for y haciendo listas para poblar la tabla
    j = 1
    superlista = []
    for fila in range(2, Hoja.max_row + 1):  
        valores = []
        for col in range(1, 4):  
            celda = Hoja.cell(row=fila, column=col).value
            valores.append(celda)
        tabla.insert("", "end", text=str(j), values=valores)
        superlista.append(valores)
        j =j + 1
        
    #aqui creo una lista con 0 y 1 para poder hacer la grafica de ganadores y perdedores
    listaresultados_binarios = []
    for fila in superlista:
        if fila[2] == 'gano':
            listaresultados_binarios.append(1)
        else:
            listaresultados_binarios.append(0)
            
    #aqui hago otra lista con los numeros de intentos para la otra grafica
    listaintentos = [fila[1] for fila in superlista]
    
    #con esto pongo la barra de la derecha para desplazarnos por la tabla
    scroll = Scrollbar(ventanagrafica, orient=VERTICAL, command=tabla.yview)
    tabla.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)
    #aqui le damos el tamaño a la tabla para que llene el espacio disponible
    tabla.pack(expand=True, fill=X)
    #y al final hago los dos botones para que se hagan las graficas
    boton1 = Button(ventanagrafica, text='Histograma número de intentos', command=graficarintentos)
    boton1.pack()
    boton2 = Button(ventanagrafica, text='Grafica ganadores/perdedores', command=graficarresultados)
    boton2.pack()

    # Centro esta ventana en la pantalla (no encontre una manera de hacerlo mas facil)
    ventanagrafica.update_idletasks()
    root.update_idletasks()
    anchoventana = ventanagrafica.winfo_width()
    altoventana = ventanagrafica.winfo_height()
    pantallancho = root.winfo_screenwidth()
    pantallalto = root.winfo_screenheight()
    x = int((pantallancho / 2) - (anchoventana / 2))
    y = int((pantallalto / 2) - (altoventana / 2))
    ventanagrafica.geometry("+" + str(x) + "+" + str(y))



#despues hago las graficas! la verdad es muy facil con este modulo

def graficarintentos():
    grafico.hist(listaintentos,50)
    grafico.title("Distribución de intentos")
    grafico.xlabel("Números de intentos")
    grafico.ylabel("Frecuencia")
    grafico.show()

def graficarresultados():
    n, bins, patches = grafico.hist(listaresultados_binarios, bins=[-0.5, 0.5, 1.5])
    grafico.title("Ganadores vs Perdedores")
    grafico.ylabel("Cantidad de jugadores")        
    grafico.xticks([0, 1], ["Perdedores", "Ganadores"])
    patches[0].set_facecolor("#C0522A")
    patches[1].set_facecolor("#2D6AA8")
        
    grafico.show()



# Aquí es donde defino si el jugador elige entre fácil, medio o difícil. Dependiendo de lo que elija, se asignan 20, 12 o 5 intentos.

    
def dificultad():
    global ventanadif, d
    ventanadif= Toplevel()
    ventanadif.title('Escoge la dificultad')
    ventanadif.iconbitmap('ICONBIT.ico')
    #esto de aqui hace que no se pueda interactuar con las ventana que esta debajo para evitar bugs o interacciones raras 
    ventanadif.transient(root)   
    ventanadif.grab_set()       
    ventanadif.focus_force()
    
    #lo hago con radiobuttons para cambiarle un poco al inicial!
    Radiobutton(ventanadif, text='1.- Facil (20 intentos)', variable=d, value=20).pack()
    Radiobutton(ventanadif, text='2.-Medio (12)', variable=d, value=12).pack()
    Radiobutton(ventanadif, text='3.- Dificil (5 intentos)', variable=d, value=5).pack()
    
    boton1 = Button(ventanadif, text='Elegir', command=lambda: clickdif(d.get()))
    
    boton1.pack()
    #igual centro la ventana
    ventanadif.update_idletasks()
    root.update_idletasks()
    rootx = root.winfo_x()
    rooty = root.winfo_y()
    anchoventana = ventanadif.winfo_width()
    altoventana = ventanadif.winfo_height()
    y = int(rooty + (altoventanaroot//2))
    x = int(rootx)
    ventanadif.geometry(str(anchoventanaroot) + "x" + str(altoventana) + "+" + str(x) + "+" + str(y))


#el boton de la funcion anterior    
def clickdif(valor):
    global opciondif,valoradivinar
    opciondif=int(valor)
    ventanadif.destroy()
    if opcion == 1:
        valoradivinar = random.randint(1, 1000)
        juego()
    if opcion == 2: 
        eleccionnum()



        
# Esta es la ventana para elegir número en el modo 2 jugadores. Mientras que el jugador 1 escribe el número que el jugador 2 tendrá que adivinar, y el campo tiene show='*' para que no se vea lo que se escribe.
def eleccionnum():
    global ventanaeleccionnum, numeroelegido, imagenpeq1
    ventanaeleccionnum= Toplevel()
    ventanaeleccionnum.title('Escoge tu número')
    ventanaeleccionnum.iconbitmap('ICONBIT.ico')
    #esto de aqui hace que no se pueda interactuar con las ventana que esta debajo para evitar bugs o interacciones raras 
    ventanaeleccionnum.transient(root)   
    ventanaeleccionnum.grab_set()       
    ventanaeleccionnum.focus_force()
    #pongo una imagen
    imagen1 = PhotoImage(file="QuesM.png")
    imagenpeq1 = imagen1.subsample(2, 2)  
    etiqim1 = Label(ventanaeleccionnum, image=imagenpeq1)
    etiqim1.pack()
    
    etiqueta5 = Label(ventanaeleccionnum, text='Pon el numero que quieras que se adivine:')
    etiqueta5.pack()
    numeroelegido = Entry(ventanaeleccionnum, width=10, show='*') # aqui esta el truco para que no se vea el numero
    numeroelegido.pack()
    numeroelegido.focus_set() #esto es para que sea mas facil interactuar con el programa desde el teclado sin tener que usar mouse porque enfoca el entry y puedes escribir directo
    numeroelegido.bind("<Return>", lambda event: clickeleccionnum(numeroelegido.get())) # esto igual es como de ux para que se pueda elegir con el boton de enter
    boton1 = Button(ventanaeleccionnum, text='Elegir', command=lambda: clickeleccionnum(numeroelegido.get()))
    boton1.pack()
    # igual para centrar la pantalla
    ventanaeleccionnum.update_idletasks()
    root.update_idletasks()
    rootx = root.winfo_x()
    rooty = root.winfo_y()
    anchoventana = ventanaeleccionnum.winfo_width()
    altoventana = ventanaeleccionnum.winfo_height()
    y = int((pantallalto / 2) - (altoventana / 2))
    x = int(rootx)
    ventanaeleccionnum.geometry(str(anchoventanaroot) + "x" + str(altoventana) + "+" + str(x) + "+" + str(y))

#esta es la funcion para el click de la ventana anterior y veruifica que este entre 1 y 1000    
def clickeleccionnum(valor):
    global numeroelegido1,valoradivinar
    valoradivinar=int(valor)
    if valoradivinar<1 or valoradivinar>1000:
        messagebox.showerror('Error', 'Recuerda que el numero tiene que estar entre 1 y 1000')
        numeroelegido.delete(0, END)
    
    else:
        ventanaeleccionnum.destroy()
        juego()

# Aqui creo la ventana para guardar el nombre de los jugadores para la estadistica.Al terminar la partida (ganando o perdiendo) se le pide el nombre al jugador para guardarlo junto con su resultado en el Excel.
 
def nombre():
    global ventananombre
    ventananombre= Toplevel()
    ventananombre.iconbitmap('ICONBIT.ico')
    ventananombre.title('Nombre')
    #esto de aqui hace que no se pueda interactuar con las ventana que esta debajo para evitar bugs o interacciones raras    
    ventananombre.transient(root)
    ventananombre.grab_set()        
    ventananombre.focus_force()
    etiqueta2= Label(ventananombre, text='Me puedes dar tu nombre para registrar tus resultados:')
    etiqueta2.grid(row=1, column=0)
    nombr = Entry(ventananombre, width=20)
    nombr.grid(row=2, column=0)
    nombr.focus_set()
    nombr.bind("<Return>", lambda event: clicknombre(nombr.get())) #igual creo esto para que se pueda interactuar solo con el teclado y mejorar ux
    boton1 = Button(ventananombre, text='Elegir', command=lambda: clicknombre(nombr.get()))
    boton1.grid(row=3, column=0)

    #y vuelvo a centrar la ventana
    ventananombre.update_idletasks()
    root.update_idletasks()
    rootx = root.winfo_x()
    rooty = root.winfo_y()
    anchoventana = ventananombre.winfo_width()
    altoventana = ventananombre.winfo_height()
    y = int(rooty + (altoventanaroot//2))
    x = int((pantallancho / 2) - (anchoventana / 2))
    ventananombre.geometry(str(anchoventana) + "x" + str(altoventana) + "+" + str(x) + "+" + str(y))

    ventananombre.grid_columnconfigure(1, weight=0)



#este es el click de la ventana anterior, donde guardo el nombre del jugador como variable string y lo inserto(append) a la hoja de excel.     
def clicknombre(valor):
    global nombrejugador
    nombrejugador = str(valor)
    documentoexcel= openpyxl.load_workbook('datosjug.xlsx')
    Hoja = documentoexcel['Hoja 1']
    Hoja.append([nombrejugador, intentos+1, resultado])
    documentoexcel.save('datosjug.xlsx')
    ventananombre.destroy()
    messagebox.showinfo('Gracias por jugar', 'Gracias por jugar ' + str(nombrejugador))



    
# Esta es como la ventana principla donde se desarrolla el juego, donde el jugador trata de adivinar el número y quise hacer algo igual como para ux y que me parecio guay mostrando los intentos restantes con corazones (♥ para vidas restantes y ♡ para vidas perdidas).       
def juego():
    
    global ventanajueg, d, etiqueta3, intentos,num,imagenpeq2, imagenpeq3, etiquetacor, corazones
    intentos=0
    ventanajueg= Toplevel()
    ventanajueg.iconbitmap('ICONBIT.ico')
    ventanajueg.title('Juego')
    #lo mismo para que no haya bugs lockeo la ventana 
    ventanajueg.transient(root)
    ventanajueg.grab_set()        
    ventanajueg.focus_force()     
    etiqueta2= Label(ventanajueg, text='Perfecto! Ya podemos empezar a jugar.')
    etiqueta2.grid(row=1, column=0)
    imagen2 = PhotoImage(file="start.png")
    imagenpeq3 = imagen2.subsample(4,4)  #hice pequeña la imagen
    etiqim2 = Label(ventanajueg, image=imagenpeq3)
    etiqim2.grid(row=2, column=0)
    #aqui hago la lista con el numero de corazones igual al numero de intentos que tiene el jugador, dependiendo de la dificulltad que eligio
    corazones = ""    
    for i in range(opciondif):
        corazones = corazones + "♥"    
    etiquetacor = Label(ventanajueg, text=corazones, fg=ACENTO, font=("Segoe UI Symbol", 16))
    etiquetacor.grid(row=3, column=0)

    
    etiqueta3= Label(ventanajueg, text='Recuerda que tienes ' + str(opciondif) + ' intentos.')
    etiqueta3.grid(row=4, column=0)
    imagen1 = PhotoImage(file="detective.png")
    imagenpeq2 = imagen1.subsample(4, 4)  #igual achique la imagen
    etiqim1 = Label(ventanajueg, image=imagenpeq2)
    etiqim1.grid(row=5, column=0)
    etiqueta4= Label(ventanajueg, text='Pon el numero que quieras intentar aqui abajo:')
    etiqueta4.grid(row=6, column=0)
    num = Entry(ventanajueg, width=10)
    num.grid(row=7, column=0)
    num.focus_set()
    num.bind("<Return>", lambda event: clickjuego(num.get())) #igual creo esto para que se pueda interactuar solo con el teclado
    boton1 = Button(ventanajueg, text='Elegir', command=lambda: clickjuego(num.get()))
    boton1.grid(row=8, column=0)
    #y centro la ventana en la pantalla
    ventanajueg.update_idletasks()
    root.update_idletasks()
    rootx = root.winfo_x()
    rooty = root.winfo_y()
    anchoventana = ventanajueg.winfo_width()
    altoventana = ventanajueg.winfo_height()
    y = int((pantallalto / 2) - (altoventana / 2))
    x = int(rootx)
    ventanajueg.geometry(str(anchoventanaroot) + "x" + str(altoventana) + "+" + str(x) + "+" + str(y))

    ventanajueg.grid_columnconfigure(0, weight=1)


# este es el click de la ventana anterior, y creo que es donde esta la logica del juego. 
# Se verifica si el número ingresado es correcto, mayor o menor, si se acaban los intentos, el jugador pierde y si acierta, gana, pidiendo siempre el nombre del jugador al final.

def clickjuego(value):
    global intentos, resultado,ventanajueg3
    numeroverificar= int(value)
    #primero defino si ya pasaste de los intentos, pero como puedes ganar con ese ultimo intento, igual tengo que verificar las 2 condiciones
    if numeroverificar!=valoradivinar and intentos>=opciondif-1:
        ventanajueg.destroy()
        messagebox.showerror('Perdiste', 'PERDISTE, se acabaron tus vidas.')
        resultado='perdio'
        nombre()
        ventanajueg.destroy()
    #luego defino que pasa si es menor o mayor al numero a adivinar
    if numeroverificar<valoradivinar and intentos<opciondif-1:
        #creo una nueva ventana para que nos de el resultado
        ventanajueg3= Toplevel()
        ventanajueg3.iconbitmap('ICONBIT.ico')
        ventanajueg3.title('No es el numero')
        #lo mismo de lockear la ventana
        ventanajueg3.transient(ventanajueg)
        ventanajueg3.grab_set()        
        ventanajueg3.focus_force()
        ventanajueg3.bell() #aqui hago que suene si te equivocas como cue sonoro 
        etiqueta2= Label(ventanajueg3, text= 'El numero es mayor que ' + str(numeroverificar))
        etiqueta2.grid(row=1, column=0)        
        intentos=intentos+1
        boton1 = Button(ventanajueg3, text='Aceptar', command=clickjuego3)
        boton1.grid(row=5, column=0)
        ventanajueg3.bind("<Return>", lambda event: clickjuego3()) #igual creo esto para que se pueda interactuar con el teclado
        #centro la ventana
        ventanajueg3.update_idletasks()
        root.update_idletasks()
        rootx = root.winfo_x()
        rooty = root.winfo_y()
        anchoventana = ventanajueg3.winfo_width()
        altoventana = ventanajueg3.winfo_height()
        y = int(rooty + (altoventanaroot//2))
        x = int(rootx)
        ventanajueg3.geometry(str(anchoventanaroot) + "x" + str(altoventana) + "+" + str(x) + "+" + str(y))

        ventanajueg3.grid_columnconfigure(0, weight=1)
        
    #igual que el anterior pero para el numero mayor
    if numeroverificar>valoradivinar and intentos<opciondif-1:
        ventanajueg3= Toplevel()
        ventanajueg3.iconbitmap('ICONBIT.ico')
        ventanajueg3.title('No es el numero')
        ventanajueg3.transient(ventanajueg)
        ventanajueg3.grab_set()        
        ventanajueg3.focus_force()
        ventanajueg3.bell()
        etiqueta2= Label(ventanajueg3, text='El numero es menor que ' + str(numeroverificar))
        etiqueta2.grid(row=1, column=0)
        intentos=intentos+1
        boton1 = Button(ventanajueg3, text='Aceptar', command=clickjuego3)
        boton1.grid(row=5, column=0) 
        ventanajueg3.bind("<Return>", lambda event: clickjuego3())
        
        ventanajueg3.update_idletasks()
        root.update_idletasks()
        rootx = root.winfo_x()
        rooty = root.winfo_y()
        anchoventana = ventanajueg3.winfo_width()
        altoventana = ventanajueg3.winfo_height()
        y = int(rooty + (altoventanaroot//2))
        x = int(rootx)
        ventanajueg3.geometry(str(anchoventanaroot) + "x" + str(altoventana) + "+" + str(x) + "+" + str(y))

        ventanajueg3.grid_columnconfigure(0, weight=1)
    #aqui se define si ganas
    if numeroverificar==valoradivinar and intentos<=opciondif-1:
        ventanajueg.destroy()
        messagebox.showinfo('ACERTASTE!!!!', 'El numero era ' + str(numeroverificar) + '!!!')
        resultado='gano'
        nombre()


#aqui defino el click de la ventana anterior cuando todavia no se acaban los intentos. y aqui es donde manejo lo de los corazones y como se van haciendo las listas para mostrar las vidas que tiene y las que ha perdido. me gusto mucho esta solucion!! siento que es algo muy sencillo y sube mucho el juego      
def clickjuego3():
    etiqueta3.config (text='Te quedan ' + str(opciondif-intentos) + ' intentos.')
    etiqueta3.grid(row=4, column=0)

    corazones = ""
    for i in range(opciondif-intentos):
        corazones = corazones + "♥"
    muertes = ""
    for i in range(intentos):
        muertes = muertes + "♡"
    
    etiquetacor.config(text=corazones + muertes, fg=ACENTO, font=("Segoe UI Symbol", 16))
    etiquetacor.grid(row=3, column=0) #aqui actualizo la etiquetacor que esta en la otra ventana! me gusto que con facilidad puedes mover cosas entre diferentes pantallas. siento que tkinter facilita mucho hacer este juego!!
    #esto de aqui abajo lo tuve que poner porque como estaba regresando entre pantallas, habia un bug raro y permitia otra vez interactuar con la pantalla de abajo y podia dar problemas, entonces tuve que hacer el release y volver a hacer el grab para que funcionara
    ventanajueg3.grab_release()
    ventanajueg3.destroy()
    num.delete(0, END)
    num.focus_set()
    ventanajueg.transient(root)
    ventanajueg.grab_set()        
    ventanajueg.focus_force() 
    num.focus_set()

#esta ya es la pantalla de inicio, me parece raro que en la estructura quede hasta el final, pero como todo lo manejo con funciones supongo que es lo correcto! solo como que no es taaan logico.    
    
d = IntVar() #aqui defini el valor de los radiobuttons de la ventana de dificultad
d.set(20)                                               
#primero pongo una imagen para estetica
imagen = PhotoImage(file="arcade.png")
imagenpeq = imagen.subsample(2, 2)  
etiqim = Label(root, image=imagenpeq)
etiqim.grid(row=0, column=1)
#luego puse espacios para que se viera mejor
etiqesp = Label(root, text=' ')
etiqesp.grid(row=0, column=0)
etiqesp2 = Label(root, text=' ')
etiqesp2.grid(row=0, column=2)
etiqesp3 = Label(root, text=' ')
etiqesp3.grid(row=1, column=2)
#aqui ya hago el menu desplegable (igual quise hacerlo de maneras diferentes para aprender diferentes parametros)
opcionm = StringVar()
opcionm.set("Partida modo solitario")
drop = OptionMenu(root, opcionm, "Partida modo solitario", "Partida 2 Jugadores", "Estadistica", "Salir")
drop.config(width=28, font=("Segoe UI Semibold", 12), anchor="center", bg="#FFFFFF", fg=TINTA, activebackground=ACENTO, activeforeground=PAPEL, relief="solid", borderwidth=1, highlightthickness=0, padx=10, pady=6) #aqui configuro la lista deplegable
drop.grid(row=2, column=1)
#aqui hago el diccionario para usarlo en la funcion
diccequiv = { "Partida modo solitario": 1, "Partida 2 Jugadores": 2, "Estadistica": 3, "Salir": 4}
#creo el boton
boton1 = Button(root, font=("Segoe UI Semibold", 11), text='Seleccionar', command=lambda: clickventanaprinc(opcionm.get()))
boton1.grid(row=4, column=1, padx=10, pady=12)

root.update_idletasks()
anchoventanaroot = root.winfo_width()
altoventanaroot = root.winfo_height()
pantallancho = root.winfo_screenwidth()
pantallalto = root.winfo_screenheight()
x = int((pantallancho / 2) - (anchoventanaroot / 2))
y = int((pantallalto / 2) - (altoventanaroot / 2))
root.geometry("+" + str(x) + "+" + str(y))

mainloop()

