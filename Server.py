from select import select
from tkinter import *
import socket

my_ip = socket.gethostbyname_ex(socket.gethostname())
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((my_ip[-1][-1], 55000))
server.listen(5)

sock_monitoring = [server]

print('Server is running')

# Строка в виджете Текст
line = 1


# Кнопка получения сообщения
def get_massage():
    global line
    massage = str(conn.recv(1024))
    if massage == str(b''):
        print('Подключение отсутствует.')
        text.insert(f'{line}.0', 'Подключение прервано' + '\n')
        line += 1
        return
    text.insert(f'{line}.0', 'Client: ' + massage[2:-1] + '\n')
    line += 1


# Кнопка отправки сообщения
def send_massage():
    global line
    massage = entry.get()
    conn.send(bytes(massage, encoding='UTF-8'))
    text.insert(f'{line}.0', 'Server: ' + massage + '\n')
    line += 1
    entry.delete(0, END)


# Кнопка ожидания подключения
def btn_conn():
    global conn, addr, line
    print('Ждём подключения...')
    print('Ваш IP для подключения:', my_ip[-1][-1])
    # text.insert(f'{line}.0', 'Ваш IP для подключения:' + str(my_ip[-1][-1]) + '\n')
    # line += 1
    print('Если вы хотите отменить ожидание подключения, выполните сочетание клавиш CTRL + C')
    try:
        conn, addr = server.accept()
    except KeyboardInterrupt:
        print('Вы отменили ожидание подключения')
        return
    text.insert(f'{line}.0', 'Connected: ' + str(addr) + '\n')
    line += 1
    print('Connected:', addr)


window = Tk()
window.title('Сервер')

frame_text = Frame(master=window, width=100, height=50, bg="red")
frame_text.pack(fill=BOTH, side=TOP, expand=True)

frame_ent_btn = Frame(master=window, width=100, height=50, bg="blue")
frame_ent_btn.pack(fill=BOTH, side=TOP, expand=True)

text = Text(master=frame_text)
text.pack(fill=BOTH, expand=True)

button_get = Button(master=frame_text, text='Получить', command=get_massage)
button_get.pack(fill=BOTH)

button_conn = Button(master=frame_text, text='Подключение', command=btn_conn)
button_conn.pack(fill=BOTH)

entry = Entry(master=frame_ent_btn)
entry.pack(fill=BOTH, side=LEFT, expand=True)

button_send = Button(master=frame_ent_btn, text='Отправить', command=send_massage)
button_send.pack(fill=BOTH, side=LEFT)

window.mainloop()

server.close()
print('Connect closed')
