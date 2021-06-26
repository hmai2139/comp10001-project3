from previous import count_type

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

def phasedout_group_extra_cards(group, phase_type):
    
    types = count_type(group)
    card_dict, natural, wild, red, black = (types[0], types[1], types[2],
                                            types[3], types[4])
    
    # check group requirements
    if 2 <= natural:
        
        # check group 1 and group 3
        for value in VALUES:
            if card_dict[value] + wild == len(group):
                if phase_type == 1:
                    return 1
                elif phase_type == 3 or phase_type == 5:
                    return 3
                
        # check group 2
        for suit in SUITS:
            if card_dict[suit] + wild == len(group) >= 7:
                if phase_type == 2:
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
        
        if len(group) >= 8 and phase_type == 4:
            return 4
        # check group 5 and group 4, respectively
        if red + wild == len(group) or black + wild == len(group):
            if phase_type == 4:
                return 4
            elif phase_type == 5:
                return 5
         
