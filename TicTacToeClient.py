# References:
# [1]“Multiplayer Tic-Tac-Toe Game in Python,” YouTube, Nov. 24, 2021.  [Online]. Available: https://www.youtube.com/watch?v=s6HOPw_5XuY
import socket
import sys


class TicTacToeClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the host and port tuple entered
        self.client.connect((self.host, self.port))
        self.symbol = None
        self.player_id = None

    def run_client(self):
        self.receive_symbol_and_id()
        self.play_game()

    def receive_symbol_and_id(self):
        data = self.client.recv(1024).decode()
        print(data)
        self.symbol = data.split()[6]
        self.player_id = int(data.split()[-1][3])

    def play_game(self):
        while True:
            message = self.receive_message()
            print(message)
            # get the move input from the client if it is their turn or they need to enter again
            if ("Your turn!" in message) or ("Invalid move!" in message):
                move = input("Enter your move (row,col): ")
                self.send_message(move)

    # send messages to the server
    def send_message(self, message):
        self.client.sendall(message.encode())

    # receive messages from the server
    def receive_message(self):
        data = self.client.recv(1024)
        return data.decode().strip()


# take the port number and start the client
port_num = int(sys.argv[1])
TicTacToeClient("localhost", port_num).run_client()