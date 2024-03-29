board = [
    [0, 9, 0, 1, 4, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 0, 0, 2, 0],
    [0, 3, 0, 0, 0, 0, 0, 6, 0],
    [0, 4, 6, 0, 0, 0, 0, 0, 0],
    [1, 2, 0, 9, 3, 0, 0, 4, 5],
    [0, 0, 3, 0, 0, 4, 0, 0, 6],
    [4, 0, 0, 0, 0, 1, 2, 0, 0],
    [0, 8, 0, 4, 0, 0, 0, 0, 3],
    [3, 5, 0, 7, 0, 0, 9, 0, 0]
]

def solve(board):
	empty = find_empty(board)
	if not empty:
		return True
	else:
		row, col = empty

	for number in range(1, 10):
		if valid(board, number, (row, col)):
			board[row][col] = number

			if solve(board):
				return True

			board[row][col] = 0

	return False


def valid(board, num, pos):
	# Check row
	for i in range(len(board[0])):
		if board[pos[0]][i] == num and pos[1] != i: 
			return False

	# Check column
	for i in range(len(board[0])):
		if board[i][pos[1]] == num and pos[0] != i: 
			return False

	# Check box
	box_x = pos[1] // 3
	box_y = pos[0] // 3
	for i in range(box_y*3, box_y*3 + 3):
		for j in range(box_x*3, box_x*3 + 3):
			if board[i][j] == num and (i,j) != pos:
				return False

	return True

def print_board(board):
	for i in range(len(board)):
		if i % 3 == 0and i != 0:
			print('- ' * 11)

		for j in range(len(board[0])):
			if j % 3 == 0 and j != 0:
				print('| ', end='')

			if j == 8:
				print(board[i][j])
			else:
				print(str(board[i][j]) + ' ', end='')

def find_empty(board):
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 0:
				return (i, j) # row, col
	return None

if __name__ == '__main__':
	print('[+] Starting board')
	print_board(board)
	print('[+] Solving board')
	solve(board)
	print('[+] Board solved')
	print_board(board)
	print('[+] Finished')