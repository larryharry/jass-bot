import json
from typing import List

import numpy as np
from jass.game.const import NORTH, SOUTH, WEST, EAST
from jass.game.game_state import GameState
from jass.game.game_state_util import state_from_complete_game, observation_from_state
from jass.logs.game_log_entry import GameLogEntry


def load_game_log_entries(path: str) -> List[GameLogEntry]:
    data = []
    with open(path) as f:
        for line in f:
            data.append(GameLogEntry.from_json(json.loads(line)))
    return data


def extract_relevant_players(game_state: GameState) -> (int, int):
    # TEAM 0 is NORTH(0) and SOUTH(2)
    # TEAM 1 is EAST(1) and WEST(3)
    if game_state.points[0] > game_state.points[1]:
        return NORTH, SOUTH
    else:
        return EAST, WEST


def extract_relevant_observations_for_game_state(game_state: GameState) -> List[List[int]]:
    rows = []
    (playerIndex1, playerIndex2) = extract_relevant_players(game_state)
    for card_index in range(36):
        game_obs = observation_from_state(state_from_complete_game(game_log_entries[0].game, card_index))
        if playerIndex1 == game_obs.player or playerIndex2 == game_obs.player:
            # target value as hot encoded 36 cards
            y_card_index = game_obs.tricks[int(card_index / 4)][card_index % 4]
            y_card = np.zeros((36,), dtype=np.float32)
            y_card[y_card_index] = 1
            # trump, my_hand, trick1, trick2, trick3, trick4, trick5, trick7
            x_game_obs = [game_obs.trump / 10]
            x_game_obs.extend(game_obs.hand)
            for trick in game_obs.tricks:
                x_game_obs.extend((trick + 1) / 36)
            # x and y
            row = []
            row.extend(x_game_obs)
            row.extend(y_card)
            rows.append(row)
        else:
            continue
    return rows


def extract_relevant_observations_for_entries(game_log_entries: List[GameLogEntry]) -> List[List[int]]:
    rows = []
    counter = 1;

    for game_log_entry in game_log_entries:
        rows.extend(extract_relevant_observations_for_game_state(game_log_entry.game))
        print("Process: " + str(counter) + " von " + str(len(game_log_entries)))
        counter += 1
    return rows

from_file_names2 = ['jass_game_0001', 'jass_game_0002', 'jass_game_0003', 'jass_game_0004', 'jass_game_0005',
             'jass_game_0006', 'jass_game_0007', 'jass_game_0008', 'jass_game_0009', 'jass_game_0010',
             'jass_game_0011', 'jass_game_0012', 'jass_game_0013', 'jass_game_0014', 'jass_game_0015',
             'jass_game_0016', 'jass_game_0017', 'jass_game_0018', 'jass_game_0019']


from_file_names = ['jass_game_0001']

for from_file_name in from_file_names:
    game_log_entries = load_game_log_entries(f'D:\DL4G\jass-exercise\converter\\from\\' + from_file_name + '.txt')
    game_observations_and_resulting_cards = np.array(extract_relevant_observations_for_entries(game_log_entries))
    np.savez_compressed('D:\DL4G\jass-exercise\converter\\to\\' + from_file_name +'.npz', game_observations_and_resulting_cards)
