from collections import defaultdict as dd
from modified import phasedout_group_extra_cards as extra
# dictionary to map cards to integer values 
VAL_DICT = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 25}
WILDCARDS = 'A'

def sequence(unique_cards):
    '''This function takes a list of unique non-wildcards `unique_cards`
    with len >= 2 and returns True if it is in reverse sequence, and returns
    False otherwise.'''
    
    # value of first card
    val = VAL_DICT[unique_cards[0][0]]
    
    for card in unique_cards[1:]:
        val -= 1
        if val == 1:
            return False
        if VAL_DICT[card[0]] != val:
            return False
    return True    

def wildcards(hand):
    '''This function takes `hand` and return a list of wildcards on hand'''
    wildcards = [card for card in hand if card[0] in WILDCARDS]
    return wildcards

def unique(hand):
    '''This function takes `hand` and return a list of non-wildcards unique
    in values.'''
    
    # split hand into unique non-wildcards and wildcards
    card_dict = dd(int)
    for card in hand:
        card_dict[card[0]] += 1
    unique_cards = []
    for card in hand:
        if card_dict[card[0]] > 0 and card[0] not in WILDCARDS:
            unique_cards.append(card)
            if card[0] not in WILDCARDS:
                card_dict[card[0]] = 0
            
    return unique_cards


def needed_cards(hand):
    '''This function takes `hand` and returns a list of cards need to make a 
    straight of 8.'''
    hand = unique(hand)
    hand = sorted(hand, key=lambda x: VAL_DICT[x[0]], reverse=True)
    needed = []
    if hand:
        val = VAL_DICT[hand[0][0]]
        for card in hand[1:]:
        
            # difference between val and `card`
            diff = val - VAL_DICT[card[0]]
        
            # check for needed card value by appending value between `val` and 
            # `card` to `needed`
            if diff > 1:
                for i in range(VAL_DICT[card[0]], val):
                    if str(i) != card[0]:
                        needed.append(str(i))
            val = VAL_DICT[card[0]]
    have = []
    for card in hand:
        have.append(str(VAL_DICT[card[0]]))
    needed = [val for val in needed if val not in have]
    return needed
        
def straight(hand):
    '''This function takes `hand` and return a straight of 8 cards.'''
    
    # return hand if hand is already a valid run
    hand = sorted(hand, key=lambda x: VAL_DICT[x[0]])
    if extra(hand, 4) == 4:
        return hand
    
    # non_wildcards with unique values on hand
    unique_cards = unique(hand)  
        
    # wildcards on hand
    wilds = wildcards(hand)
      
    # sort hand and `unique_cards` in descending value order
    unique_cards = sorted(unique_cards, key=lambda x: VAL_DICT[x[0]],
                          reverse=True)
        
    while len(unique_cards) + len(wilds) >= 8:
        
        # check if unique cards can form a straight without wildcards by 
        # calling `sequence` function to check if `unique_cards` is a valid
        # run
        if sequence(unique_cards):
            
            # return `unique_cards` in ascending order if its length >= 8
            if len(unique_cards) >= 8:
                return(unique_cards[:8:-1])
            
            # else, add aces to unique_cards
            elif len(unique_cards) < 8:
                
                # value of first and last card of `unique_cards`
                first_val = VAL_DICT[unique_cards[0][0]]
                last_val =  VAL_DICT[unique_cards[-1][0]]
                
                # add to the start, if first card has a smaller value than 13
                if first_val < 13:
                    unique_cards = wilds[:13 - first_val] + unique_cards
                    wilds = wilds[13 - first_val:]
                    
                # append if last card has a greater value than 2
                if last_val > 2:
                    unique_cards += wilds[:last_val - 2]
                    wilds = wilds[last_val - 2:]
            
            # return if have a valid run
            phase = unique_cards[::-1]
            return phase
        
        # if `unique_cards` is not a valid run, try adding wildcards between
        # cards with difference > 1                
        run = [unique_cards[0]]
        val = VAL_DICT[unique_cards[0][0]]
        for card in unique_cards[1:]:
            # difference between val and `card`
            diff = val - VAL_DICT[card[0]]
            if diff > 1 and len(wilds) >= diff - 1:
                run += (wilds[:diff - 1]) + [card]
                wilds = wilds[diff - 1:]
            elif diff == 1:
                run += [card]
            val = VAL_DICT[card[0]]
        
        # call `extra` function to check if `run` is a valid run
        if extra(run[::-1], 4) == 4:
            return run[::-1]
        
        if len(run) + len(wilds) >= 8:
            
            # value of first and last card of `unique_cards`
            first_val = VAL_DICT[run[0][0]]
            last_val =  VAL_DICT[run[-1][0]]
                
            # add to the start, if first card has a smaller value than 13
            if first_val < 13:
                run = wilds[:13 - first_val] + run
                wilds = wilds[13 - first_val:]
                    
            # append if last card has a greater value than 2
            if last_val > 2:
                run += wilds[:last_val - 2]
                wilds = wilds[last_val - 2:]
                
            if extra(run[::-1], 4) == 4:
                return run[::-1]
            
        # if not, choose the next combination of `unique_cards` and repeat the
        # process
        wilds = wildcards(hand)
        unique_cards = unique_cards[1:]

                   
        
