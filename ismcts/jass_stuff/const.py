# number of cards in one trick
import numpy as np

NBR_OF_CARDS_IN_ONE_TRICK: int = 4

# value representing the absence of a card in a trick
MISSING_CARD_IN_TRICK: int = -1

# value representing the absence of a card in a hand
MISSING_CARD_IN_HAND: int = 0

# value representing the presence of a card in a trick or a hand
EXISTING_CARD: int = 1

# array representing a empty trick
EMPTY_TRICK: np.dnarray = [MISSING_CARD_IN_TRICK, MISSING_CARD_IN_TRICK, MISSING_CARD_IN_TRICK, MISSING_CARD_IN_TRICK]
