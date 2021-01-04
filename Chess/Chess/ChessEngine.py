"""
В этом классе мы храним все данные, поэтому этот класс отвечает за хранение всей
информации связанной с текущем состоянием шахматной ппартией. Также будет возможность
остановить ход в текущем сосотянии игры. Будет вести журнал ходов, поэтому мы сможем
отменить ходы и посмотреть как развивалась партия.
"""


class GameState():
    def __init__(self):
        """ Доска состоит из списка 8*8, где каждый элемент имеет 2 характеристики.
            Первая характеристика отвечает за цвет w-белый, b-черный.
            Вторя характеристика отвечает за тип фигуры.
            Queen - королева, King - король, Bishop - слон, K(n)ight- конь, Rook - ладья, pawn - пешка.
            "--" пустое пространство """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "bp", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"], ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # меняем местами

    # отмена хода
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.EndRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    ''' Все возможные ходы с учето проверок'''

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    ''' Все возможные ходы без учета проверок'''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):  # Номер колонки в полученной строке
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # вызывает соответсвующие функции перемещения в зависимоти от типа фигуры
                    self.moveFunctions[piece](r, c, moves)
        return moves

    # получить все возможные ходы для пешки и добавить эти действие в список
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # если белые ходят
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: # захват слева
                if self.board[r-1][c-1][0] == 'b': # враг захвачен
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: # захват справа
                if self.board[r-1][c+1][0] == 'b': # враг захвачен
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: # если черные ходят
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))

            if c-1 >= 0: # захват слева
                if self.board[r+1][c-1][0] == 'w': # враг захвачен
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: # захват справа
                if self.board[r+1][c+1][0] == 'w': # враг захвачен
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    # получить все возможные ходы для ладьи и добавить эти действие в список
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # на доске
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else: # off board
                    break


    # получить все возможные ходы для коня и добавить эти действие в список
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # не союзник ( пустой кусок )
                    moves.append(Move((r, c), (endRow, endCol), self.board ))

    # получить все возможные ходы для слона и добавить эти действие в список
    def getBishopMoves(self, r, c, moves):
        pass
        # получить все возможные ходы для королевы и добавить эти действие в список

    def getQueenMoves(self, r, c, moves):
        pass
        # получить все возможные ходы для короля и добавить эти действие в список

    def getKingMoves(self, r, c, moves):
        pass


class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    '''Переопределяем метод equals '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
