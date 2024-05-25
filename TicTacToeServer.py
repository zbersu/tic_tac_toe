# References:
# [1]“Multiplayer Tic-Tac-Toe Game in Python,” YouTube, Nov. 24, 2021.  [Online]. Available: https://www.youtube.com/watch?v=s6HOPw_5XuY
import socket
import threading
import sys


class TicTacToeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.players = []
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = None
        self.game_over = False

    def run_server(self):
        # open a socket to listen, accept and handle connections
        # SOCK_STREAM for TCP connection, AF_INET for IPv4
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a tuple of chosen host and port

        server.bind((self.host, self.port))
        # listen for two connections
        server.listen(2)
        print("Server started. Waiting for players to connect...")

        while len(self.players) < 2:
            client, addr = server.accept()
            self.players.append(client)
            if len(self.players) == 1:
                print(f"A player connected with the IP address and port number: {addr}")

            if len(self.players) == 2:
                print(f"Another player connected with the IP address and port number: {addr}")
                self.start_game()

    def start_game(self):
        symbols = ["X", "O"]
        # decide which player starts the game
        self.turn = self.players[0]
        # send the information messages to the clients
        self.send_message(self.players[0], f"Connected to the server.\nRetrieved symbol {symbols[0]} and ID=0")
        self.send_message(self.players[1], f"Connected to the server.\nRetrieved symbol {symbols[1]} and ID=1")
        self.send_message(self.players[0], "\nTurn information: Your turn!")
        self.send_message(self.players[1], "\nPlayer 0’s turn! (Wait for player 0’s move).")
        # display information messages on the server side
        print(f"A client is connected, and it is assigned the symbol '{symbols[0]}' and ID = 0")
        print(f"A client is connected, and it is assigned the symbol '{symbols[1]}' and ID = 1")
        print("The game is started")
        print("Waiting for Player 0's move\n")
        # return the board as string for sending to the players
        board_str = self.print_board()
        # send the board to the players
        self.send_message(self.players[0], "\nState of the board:\n")
        self.send_message(self.players[1], "\nState of the board:\n")
        self.send_message(self.players[0], "\n" + board_str)
        self.send_message(self.players[1], "\n" + board_str)

        # create two separate threads for two players
        threading.Thread(target=self.handle_client, args=(self.players[0], symbols[0])).start()
        threading.Thread(target=self.handle_client, args=(self.players[1], symbols[1])).start()

    def handle_client(self, client, symbol):

        player_id = self.players.index(client)
        symbols = ["X", "O"]

        while not self.game_over:
            message = self.receive_message(client)
            # in the case of no messages do not run the rest of the lines in the block
            if not message:
                break
            # notify the player in the case of an invalid move and display the illegal move on the server side
            if not self.is_valid_move(message, player_id):
                self.send_message(client, "Invalid move!")
                row, col = map(int, message.split(","))
                print(f"Received '{symbols[player_id]}' at ({message}). It is an illegal move.")
                self.send_message(self.players[1 - player_id],
                                  f"Player {player_id} made an illegal move and is retrying")
                continue
            # place the move on the table unless it is illegal
            self.process_move(client, symbol, message)

    # check if the move is valid
    def is_valid_move(self, move, player_id):
        try:
            row, col = map(int, move.split(","))
            if not (0 <= row < 3 and 0 <= col < 3):
                return False
            if self.board[row][col] != " ":
                return False
            if self.turn != self.players[player_id]:
                return False
            return True
        except ValueError:
            return False

    # process the move by taking the relevant parts of the move entered
    def process_move(self, client, symbol, move):
        symbols = ["X", "O"]
        row, col = map(int, move.split(","))
        self.board[row][col] = symbol
        player_id = self.players.index(client)
        valid_move = self.is_valid_move(move, player_id)
        self.send_message(self.players[player_id], f"Put {symbols[player_id]} to ({move})\n")
        board_str = self.print_board()
        self.send_message(self.players[0], "\nState of the board:\n")
        self.send_message(self.players[0], "\n" + board_str)
        self.send_message(self.players[1], "\nState of the board:\n")
        self.send_message(self.players[1], "\n" + board_str)

        # display the messages regarding the validity of the move on the server side
        if not valid_move:
            print(f"Received '{symbols[player_id]}' at ({move}). It is a legal move.")
            self.send_message(self.players[1 - player_id], f"Player {player_id} put {symbols[player_id]} to ({move})\n")
        else:
            print(f"Received '{symbols[player_id]}' at ({move}). It is an illegal move.")
            self.send_message(self.players[1 - player_id],
                              f"Player {player_id} made an illegal move by putting {symbols[player_id]} to ({move}).\n")

        # check if there is a winner or a tie after each move processed, if there is set game_over to True for ending the game otherwise go on with the next player's turn
        if self.check_winner(symbol):
            if self.players.index(client) == 0:
                print("The game is finished. Player 0 has won.")
                self.send_message(self.players[0], "You win!")  # player 0 wins
                self.send_message(self.players[1], "You lose!")  # player 1 loses
                self.game_over = True
            else:
                print("The game is finished. Player 1 has won.")
                self.send_message(self.players[1], "You win!")  # player 1 wins
                self.send_message(self.players[0], "You lose!")  # player 0 loses
                self.game_over = True
        elif self.check_tie():
            print("The game is finished. It is a tie!")
            self.send_message(self.players[0], "It's a tie!")
            self.send_message(self.players[1], "It's a tie!")
            self.game_over = True
        else:
            print(f"Waiting for Player {1 - player_id}'s move")
            self.turn = self.players[1 - self.players.index(client)]
            self.send_message(self.turn, "\nTurn information: Your turn!")
            self.send_message(client,
                              f"\nTurn information: Player {1 - self.players.index(client)}'s turn! (Wait for player {1 - self.players.index(client)}'s move)")

    # check the winning conditions for the tic-tac-toe game
    def check_winner(self, symbol):
        for i in range(3):
            # 3 same and successive symbols at a row
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == symbol:
                return True
            # at a column
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == symbol:
                return True
        # at diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == symbol:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == symbol:
            return True
        return False

    # check the tie conditions for the tic-tac-toe game
    def check_tie(self):
        for row in self.board:
            if " " in row:
                return False
        return True

    # define send_message to send messages to the client side
    def send_message(self, client, message):
        client.sendall(message.encode())

    # for messages from the client side
    def receive_message(self, client):
        data = client.recv(1024)
        return data.decode().strip()

    # for returning the board as a string
    def print_board(self):
        board_str = "---------\n"
        for row in self.board:
            board_str += "|"
            for cell in row:
                board_str += cell + "|"
            board_str += "\n---------\n"
        return board_str


# take the port number and start the server
port_num = int(sys.argv[1])
TicTacToeServer("localhost", port_num).run_server()
