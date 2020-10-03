import logging

from jass.agents.agent_random_schieber import AgentRandomSchieber
from jass.arena.arena import Arena

from minimax.agent_minimax_schieber import AgentMinimaxSchieber


def main():
    # Set the global logging level (Set to debug or info to see more messages)
    logging.basicConfig(level=logging.DEBUG)
    arena = Arena(1)

    player_1 = AgentRandomSchieber()
    player_2 = AgentMinimaxSchieber(arena._game._state)
    player_3 = AgentRandomSchieber()
    player_4 = AgentMinimaxSchieber(arena._game._state)

    arena.set_players(player_1, player_2, player_3, player_4)
    print('Playing {} games'.format(arena.nr_games_to_play))
    arena.play_all_games()
    print('Average Points Team 0: {:.2f})'.format(arena.points_team_0.mean()))
    print('Average Points Team 1: {:.2f})'.format(arena.points_team_1.mean()))


if __name__ == '__main__':
    main()
