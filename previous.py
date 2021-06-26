from collections import defaultdict

# dictionary to map cards to corresponding integer values
VALUE_DICT = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              '0': 10, 'J': 11, 'Q': 12, 'K': 13}

# values and suits in deck, respectively
VALUES = '234567890JQK'
SUITS = 'SDHC'

# set aces to wild cards 
WILDCARDS = 'A'

# colors of suits
RED = 'DH'
BLACK = 'SC'

def count_type(group):
        
    # create dictionary `card_dict` to count types of cards
    card_dict = defaultdict(int)
    wild = 0
    natural = 0
    red = 0
    black = 0
    for card in group:
        # no. of wild cards
        if card[0] in WILDCARDS:
            wild += 1
            card_dict[card[0]] += 1
        # no. of natural cards of the same color/value/suit, respectively
        else:
            natural += 1
            if card[1] in RED:
                red += 1
            elif card[1] in BLACK:
                black += 1
            card_dict[card[0]] += 1
            card_dict[card[1]] += 1
            
    return card_dict, natural, wild, red, black


def phasedout_group_type(group):
    
    
    # implement `count_type` to count types of cards
    types = count_type(group)
    card_dict, natural, wild, red, black = (types[0], types[1], types[2],
                                            types[3], types[4])
    
    # check group requirements
    if 2 <= natural:
        
        # check group 1 and group 3
        for value in VALUES:
            if card_dict[value] + wild == len(group):
                if len(group) == 3:
                    return 1
                elif len(group) == 4:
                    return 3
                
        # check group 2
        for suit in SUITS:
            if card_dict[suit] + wild == len(group) == 7:
                return 2
            
        # no. of wild cards at the start of the run
        wild_start = 0
        
        # count and remove wild cards at the start of the run
        run = group
        while run[0][0] in WILDCARDS:
            wild_start += 1
            run = run[1:]
        
        # value of the first non-wild card of the run    
        val = VALUE_DICT[run[0][0]]
        
        # check if the first wild card takes value of 1, which is invalid
        if wild_start == val - 1:
            return None
        
        # check if there is wild card before card with value of 2
        if wild_start > 0 and val == 2:
            return None
        
        for card in run[1:]:
            val += 1
            
            # check if there is any card after a King, which is invalid
            if val == 14:
                return None
            
            # check if `run` is in sequence
            if card[0] not in WILDCARDS and VALUE_DICT[card[0]] != val:
                return None
        
        # check group 4 and group 5, respectively
        if len(group) == 8:
                return 4
        elif len(group) == 4:
            if red + wild == len(group) or black + wild == len(group):
                return 5
                
def group_with_extra_cards(group, play, phase_status):
    
    # id of player who played the phase
    phase_player = play[1][1][0]
    
    # implement `count_type` to count types of cards
    types = count_type(group)
    card_dict, natural, wild, red, black = (types[0], types[1], types[2],
                                            types[3], types[4])
    
    # check group requirements
    if 2 <= natural:
        
        # check group 1 and group 3
        for value in VALUES:
            if card_dict[value] + wild == len(group):
                return phase_status[phase_player]
                
        # check group 2
        for suit in SUITS:
            if card_dict[suit] + wild == len(group):
                return 2
            
        # no. of wild cards at the start of the run
        wild_start = 0
        
        # count and remove wild cards at the start of the run
        run = group
        while run[0][0] in WILDCARDS:
            wild_start += 1
            run = run[1:]
        
        # value of the first non-wild card of the run
        val = VALUE_DICT[run[0][0]]
        
        # check if the first wild card takes value of 1, which is invalid
        if wild_start == val - 1:
            return False
        
        # check if there is wild card before card with value of 2
        if wild_start > 0 and val == 2:
            return None
        
        for card in run[1:]:
            val += 1
            
            # check if there is any card after a King, which is invalid
            if val == 14:
                return False
            
            # check if `run` is in sequence
            if card[0] not in WILDCARDS and VALUE_DICT[card[0]] != val:
                return False
        
        # check group 5 and group 4, respectively
        if red + wild == len(group) or black + wild == len(group):
            if phase_status[phase_player] == 4:
                return 4
            elif phase_status[phase_player] == 5:
                return 5
        return 4  

def phasedout_phase_type(phase):
    # Implement this function
    
    if phase:
        # check phase type 1, 3:
        if len(phase) == 2:
            if phasedout_group_type(phase[0]) == \
               phasedout_group_type(phase[-1]):
                return phasedout_group_type(phase[0])
    
        # check phase type 5
            elif phasedout_group_type(phase[0]) == 5:
                if phasedout_group_type(phase[-1]) == 3:
                    return 5
        
        # check phase type 2,4
        elif len(phase) == 1:
            if phasedout_group_type(phase[0]) == 2:
                return 2
            elif phasedout_group_type(phase[0]) == 4:
                return 4
   
      
def play_1_is_valid(play, player_id, turn_history):
    # check if the current player has previously made any play within this turn
    if play[1]:
        if turn_history[-1][0] != player_id:
            return True
    return False    


def play_2_is_valid(play, player_id, turn_history, discard):
    
    # check if the current player has previously made any play within this turn
    if play[1] and discard:
        if turn_history[-1][0] != player_id:
            if play[1] == discard:
                return True
    return False


def play_3_is_valid(play, player_id, table, turn_history, phase_status, hand):
    
    # phase to be played
    phase = play[1]
    
    # check if all cards of `phase` are in hand
    if phase and turn_history[-1][0] == player_id:
        for group in phase:
                for card in group:
                    if card not in hand:
                        return False
                    
    # check if phase is valid
    if phasedout_phase_type(phase) == phase_status[player_id] + 1:
        return True
    return False        


def play_4_is_valid(play, player_id, table, turn_history, phase_status, hand):

    # card to be played
    card = play[1][0]
    
    # player id of the phase the card is to be placed on
    phase_player = play[1][1][0]
    
    # card to be played
    card = play[1][0]
    
    # player id of the phase the card is to be placed on
    phase_player = play[1][1][0]
    
    if card in hand and phase_status[phase_player] != 0 and \
       phase_status[player_id] != 0:
        
        # the group the card is to be placed in
        group_id = play[1][1][1]

        # the phase the card is to be placed on
        phase = table[phase_player][1]
        
        # check if `group_id` is valid
        try:
            group = phase[group_id]
        except:
            return False
        
        # check for invalid index
        index = play[1][1][2]
        if index > len(group):
            return False
        
        # group after the card is added
        added_group = group[:index] + [card] + group[index:]
        if group_with_extra_cards(group, play, phase_status) == \
           group_with_extra_cards(added_group, play, phase_status):
            return True
    return False
           
def play_5_is_valid(play, player_id, turn_history, hand):
    
    # card to be discarded
    card = play[1]
    
    if card in hand and turn_history[-1][0] == player_id:
        return True           
    return False
        
                
def phasedout_is_valid_play(play, player_id, table, turn_history, phase_status,
                            hand, discard):
    # the last play of the game so far
    last_play = turn_history[-1][-1][-1][0]
    
    # the player that made `last_play`
    last_player = turn_history[-1][0]

    if last_player == player_id:
        if last_play == 5 and (play[0] != 1 or play[0] != 2):
            return False
        
    # check if play type 1, 2, 3, 4, 5 is valid, respectively
    if play[0] == 1:
        return play_1_is_valid(play, player_id, turn_history)
    elif play[0] == 2:
        return play_2_is_valid(play, player_id, turn_history, discard)
    elif play[0] == 3:
        return play_3_is_valid(play, player_id, table, turn_history,
                               phase_status, hand)
    elif play[0] == 4:
        return play_4_is_valid(play, player_id, table, turn_history,
                               phase_status, hand)
    elif play[0] == 5:
        return play_5_is_valid(play, player_id, turn_history, hand)

