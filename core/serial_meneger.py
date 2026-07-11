import serial
import serial.tools.list_ports

ser = None

def find_adr():
    """
    Поиск и открытие COM-порта.
    """

    global ser

    # если уже подключены
    if ser is not None and ser.is_open:
        return ser.port

    ports = serial.tools.list_ports.comports()

    for port in ports:

        try:
            ser = serial.Serial(
                port=port.device,
                baudrate=9600,
                timeout=0.5
            )



            return port.device

        except Exception:
            continue

    return None

def check_connection():
    """
    Проверка соединения.
    Вызывать каждую секунду из QTimer.
    """

    global ser

    # если соединения нет — пробуем подключиться
    if ser is None:

        port = find_adr()

        if port:
            return True, port

        return False, None

    try:

        # проверяем открыт ли объект
        if not ser.is_open:

            ser = None
            return False, None

        # проверяем существует ли COM в Windows
        ports = [
            p.device
            for p in serial.tools.list_ports.comports()
        ]

        if ser.port not in ports:



            try:
                ser.close()
            except:
                pass

            ser = None

            return False, None

        return True, ser.port

    except Exception as e:



        try:
            ser.close()
        except:
            pass

        ser = None

        return False, None

def close_connection():

    global ser

    if ser:

        try:
            ser.close()

        except:
            pass

    ser = None



def send_pack(data):

    global ser

    if ser is None or not ser.is_open:
        return False

    try:

        msg = str(data) + "\n"

        ser.write(
            msg.encode()
        )

        return True

    except serial.SerialException as e:

        print("Send error:", e)

        try:
            ser.close()
        except:
            pass

        ser = None

        return False

def recv_pack():

    global ser

    if ser is None or not ser.is_open:
        return None

    try:

        if ser.in_waiting > 0:

            data = (
                ser.readline()
                .decode(errors="ignore")
                .strip()
            )

            if data.startswith("RX:"):

                return data[3:]

    except serial.SerialException as e:

        print("Receive error:", e)

        try:
            ser.close()
        except:
            pass

        ser = None

    return None