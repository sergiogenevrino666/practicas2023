import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import mido
from mido import Message

# Configurar la ventana de la interfaz gráfica
window = tk.Tk()
window.title("OBXD MIDI CC CONTROLLER")
window.geometry('600x400')
window.config(background='black')


# Lista de dispositivos MIDI disponibles
input_devices = mido.get_input_names()
output_devices = mido.get_output_names()

# Función para enviar el mensaje CC al dispositivo seleccionado
def send_cc_message(cc_number, cc_value):
    selected_output_device = output_device_var.get()
    with mido.open_output(selected_output_device) as port:
        cc_message = Message(
            'control_change', control=cc_number, value=int(cc_value))
        port.send(cc_message)

# Función para manejar el cambio de valor del slider CC74
def on_slider_cc74_change(value):
    send_cc_message(74, value)

# Función para manejar el cambio de valor del slider CC71
def on_slider_cc71_change(value):
    send_cc_message(71, value)

# Función para recibir los mensajes MIDI de entrada y transmitirlos al MIDI Thru
def midi_thru_callback(message):
    selected_input_device = input_device_var.get()
    selected_output_device = output_device_var.get()

    # Si el mensaje proviene del dispositivo de entrada seleccionado, se envía al MIDI Thru
    # Asumiendo el canal 0 (canal 1 en MIDI)
    if message.type == 'control_change' and message.channel == 0:
        with mido.open_output(selected_output_device) as port:
            port.send(message)

fontStyle = tkFont.Font(family="Helvetica", size=11)
fontStyle1 = tkFont.Font(family="Helvetica", size=9)
titulo = tk.Label(window, text="ISFT 151",height=5,font=fontStyle )
titulo.grid(row=1, column=0)
titulo.config(bg='black',fg='white')
titulo1 = tk.Label(window, text="Seleccione un parametro y deslice el slider :",height=5, font=fontStyle)
titulo1.grid(row=1, column=1)
titulo1.config(bg='black',fg='white')



# Etiqueta y slider para el CC74
cc74_label = tk.Label(window, text="VALOR DEL CC74 (Modulación):",height=4, font=fontStyle1 )
cc74_label.grid(row=3, column=0,padx=18)
cc74_label.config(bg='black',fg='white')


cc74_slider = tk.Scale(window, from_=0, to=127,
                       orient=tk.HORIZONTAL, command=on_slider_cc74_change)
cc74_slider.grid(row=3, column=1)
cc74_slider.config(bg='black',fg='white')

# Etiqueta y slider para el CC71
cc71_label = tk.Label(window, text="VALOR DEL CC71 (Filtro):" ,height=4, font=fontStyle1)
cc71_label.grid(row=4, column=0,padx=18)
cc71_label.config(bg='black',fg='white')

cc71_slider = tk.Scale(window, from_=0, to=127,
                       orient=tk.HORIZONTAL, command=on_slider_cc71_change)
cc71_slider.grid(row=4, column=1)
cc71_slider.config(bg='black',fg='white')


# Lista desplegable para seleccionar el dispositivo de entrada MIDI
input_device_var = tk.StringVar()
# Dispositivo de entrada inicial seleccionado
input_device_var.set(input_devices[0])

input_device_label = tk.Label(
    window, text="DISPOSITIVO DE ENTRADA MIDI:",height=7, font=fontStyle1)
input_device_label.grid(row=5, column=0,padx=18)
input_device_label.config(bg='black',fg='white')


input_device_menu = tk.OptionMenu(window, input_device_var, *input_devices)
input_device_menu.grid(row=5, column=1)
input_device_menu.config(bg='black',fg='white')

# Lista desplegable para seleccionar el dispositivo de salida MIDI
output_device_var = tk.StringVar()
# Dispositivo de salida inicial seleccionado
output_device_var.set(output_devices[0])

output_device_label = tk.Label(
    window, text="DISPOSITIVO DE SALIDA MIDI:")
output_device_label.grid(row=6, column=0,padx=18)
output_device_label.config(bg='black',fg='white')

output_device_menu = tk.OptionMenu(window, output_device_var, *output_devices)
output_device_menu.grid(row=6, column=1)
output_device_menu.config(bg='black',fg='white')










# Abrir el puerto de entrada MIDI para recibir los mensajes
selected_input_device = input_device_var.get()
with mido.open_input(selected_input_device, callback=midi_thru_callback):
    pass

# Mantener la ventana de la interfaz gráfica abierta
window.mainloop()
