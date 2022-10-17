from threading import Thread
import socket


def sendMsg(client):
    while True:
        data = input("")
        client.send(data.encode("utf-8"))
        if data == "quit":
            running = False
            break


def recvMsg(client, thead2):
    username = input("Username: ")
    client.send(username.encode("utf-8"))

    thead2.start()
    while running:
        try:
            data = client.recv(1024).decode("utf-8")
            if not data:
                break
            print(data)
        except:
            print("There was a problem connecting")


if __name__ == '__main__':
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432
    running = False

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        running = True
        thread2 = Thread(target=sendMsg, args=(client,))
        thread1 = Thread(target=recvMsg, args=(client, thread2))
        thread1.start()
        thread1.join()
        thread2.join()

    except:
        print("There was a problem connecting")

    finally:
        print("exit chat room")
        client.close()
