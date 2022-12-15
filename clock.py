import time
import winsound

# Função para formatar a hora atual como hh:mm:ss
def get_time():
    return time.strftime('%H:%M:%S')

# Função para imprimir a hora atual
def print_time():
    print(get_time())

# Função para configurar o despertador para acordar em uma hora específica
def set_alarm(hour, minute, second):
    while True:
        print_time()
        time.sleep(1)
        # Pare o loop quando a hora atual for igual ao horário de despertador
        if get_time() == f'{hour:02d}:{minute:02d}:{second:02d}':
            # Tocar um bip sonoro simples
            while True:
                print('despertou')
                winsound.Beep(1000, 500)
                #break

# Configure o despertador para acordar às 09:30:00
set_alarm(14, 48, 30)
