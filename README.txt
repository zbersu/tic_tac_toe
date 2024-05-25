# Tic-Tac-Toe Game over TCP

This project implements a Tic-Tac-Toe game using a client-server architecture over TCP in Python. The game lets two players to connect to a server and play against each other in a standard game of Tic-Tac-Toe.

## Features

- Server-side implementation manages game logic and client connections.
- Client-side implementation allows players to connect to the server and play the game.
- Communication between the server and clients is achieved using sockets and a simple messaging protocol.
- Threading is used to handle multiple client connections concurrently and enables simultaneous gameplay.

## How to Play

1. Navigate to the project directory from the command line.
>cd Desktop
>cd deneme

2. Start the server by executing the following command:
>python TicTacToeServer.py <port>

3. Open two separate terminals and run the client instances:
>python TicTacToeClient.py <port>

4. Follow the instructions displayed on the client consoles to play the game.

## Code Structure

TicTacToeServer.py: This file contains the server-side implementation that manages game logic and client connections.
TicTacToeClient.py: This file contains the client-side implementation that connects to the server and playing the game.

