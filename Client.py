from tkinter import *
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Строка в виджете Текст
line = 1


# Кнопка получения сообщения
def get_massage():
    global line
    massage = str(server.recv(1024))
    if massage == str(b''):
        print('Подключение прервано.')
        text.insert(f'{line}.0', 'Подключение прервано' + '\n')
        line += 1
        return
    text.insert(f'{line}.0', 'Server: ' + massage[2:-1] + '\n')
    line += 1


# Кнопка отправки сообщения
def send_massage():
    global line
    massage = entry.get()
    print(massage)
    try:
        server.send(bytes(massage, encoding='UTF-8'))
        text.insert(f'{line}.0', 'Me: ' + massage + '\n')
        line += 1
    except BrokenPipeError:
        text.insert(f'{line}.0', 'Подключение отсутствует' + '\n')
        line += 1
        return
    entry.delete(0, END)


# Кнопка подключения
def btn_conn():
    global line
    srv_ip = entry_ip.get()
    try:
        print('Ждём подключения...')
        print('Если вы хотите отменить ожидание подключения, выполните сочетание клавиш CTRL + C')
        server.connect((srv_ip, 55000))
        text.insert(f'{line}.0', 'Connected: ' + str(srv_ip) + '\n')
        line += 1
        print('Connected:', srv_ip)
    except socket.gaierror:
        print('Temporary failure in name resolution')
    except KeyboardInterrupt:
        print('Вы отменили ожидание подключения')


window = Tk()
window.title('Клиент')

frame_text = Frame(master=window, width=100, height=50, bg="red")
frame_text.pack(fill=BOTH, side=TOP, expand=True)

frame_conn = Frame(master=window, width=100, height=50)
frame_conn.pack(fill=BOTH, side=TOP, expand=True)

frame_ent_btn = Frame(master=window, width=100, height=50, bg="blue")
frame_ent_btn.pack(fill=BOTH, side=TOP, expand=True)

text = Text(master=frame_text)
text.pack(fill=BOTH, expand=True)

button_get = Button(master=frame_text, text='Получить', command=get_massage)
button_get.pack(fill=BOTH)

button_conn = Button(master=frame_conn, text='Подключиться', command=btn_conn)
button_conn.pack(fill=BOTH, side=RIGHT)

entry_ip = Entry(master=frame_conn)
entry_ip.pack(fill=BOTH, side=RIGHT)

label = Label(master=frame_conn, text='Введите ip компьютера к которому хотите подключиться: ')
label.pack(fill=BOTH, side=RIGHT)

entry = Entry(master=frame_ent_btn)
entry.pack(fill=BOTH, side=LEFT, expand=True)

button_send = Button(master=frame_ent_btn, text='Отправить', command=send_massage)
button_send.pack(fill=BOTH, side=LEFT)

window.mainloop()
server.close()
print('Connect closed')
