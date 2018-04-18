from .base_agent import BaseAgent
from random import randint


class Agent(BaseAgent):
    '''Computer Agent'''

    def get_boards(self, cursor):
        '''Retrieves potential board states'''
        params = {'lookahead': self.lookahead, 'cursor': cursor}
        data = self.request('GET', '/v1.0/games/{}/states'.format(self.game_id), params=params)
        return {'boards': data['boards'], 'cursor': data['cursor']}

    def play_round(self):
        '''Play a game round'''
        cursor = True
        board_score = 0
        best_boards = []
        while cursor:
            board_options = self.get_boards(cursor)
            boards = board_options['boards']
            cursor = board_options['cursor']
            evaluation = self.evaluate_boards(boards)
            if evaluation['board_score'] > board_score:
                best_boards = [evaluation['best_board']]
            elif evaluation['board_score'] == board_score:
                if evaluation['best_board'] not in best_boards:
                    best_boards.append(evaluation['best_board'])

        return self.put_board(best_boards[randint(0,len(best_boards)-1)])

    def play_game(self):
        '''Play a game'''
        game_over = False
        while not game_over:
            game_over = self.play_round()
        return game_over
