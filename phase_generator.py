from previous import count_type as count, phasedout_phase_type, \
                               phasedout_group_type
from itertools import permutations as p
from straight_generator import straight
from collections import defaultdict as dd

# dictionary to map cards to corresponding integer value (wild cards are map
# to zero so that they are at the end of hand after sorting in descending order
VALUE_DICT = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 0}    

# dictionary to map cards to integer values 
VAL_DICT = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 25}

# values and suits in deck, respectively
VALUES = 'KQJ098765432'
SUITS = 'SDHC'

# set aces to wild cards 
WILDCARDS = 'A'

# colors of suits
RED = 'DH'
BLACK = 'SC'

# Phase 1: Two sets of three cards of the same value
def phase_1_check(hand):
    
    # sort hand by descending value of cards (aces are at the end of hand)
    hand = sorted(hand, key=lambda x: VALUE_DICT[x[0]], reverse=True)
    
    # dictionaries to count the no. of copies of each cards on hand
    copies_count = dd(int)
    for card in hand:
            copies_count[card] += 1

    # check if have a valid phase 1 on hand
    phase = []
    for val in VALUES:
        card_dict = count(hand)[0]
        wild = count(hand)[2]    
        group = []
        if card_dict[val] >= 3 or (card_dict[val] == 2 and wild >= 1):
            for card in hand:
                if (card_dict[card[0]] == card_dict[val] and card[0] in val) \
                     or card[0] in WILDCARDS:
                        group.append(card)
                        copies_count[card] -= 1
                        if len(group) == 3:
                            break
            phase.append(group)
            
            # find the remaining cards remove the cards in `group` from hands
            hand = []
            for card in copies_count.keys():
                if copies_count[card] == 1:
                    hand.append(card)
                elif copies_count[card] == 2:
                    hand += [card, card]
            if len(phase) == 2:
                break

    return phase

# Phase 2: One set of 7 cards of the same suit
def phase_2_check(hand):
    
    # sort hand by descending value of cards (aces are at the end of hand)
    hand = sorted(hand, key=lambda x: VALUE_DICT[x[0]], reverse=True)
    
    # no. of wild cards on hand
    wild = count(hand)[2]
    
    # check if have a valid phase 2 on hand
    card_dict = count(hand)[0]
    phase = []
    group = []
    for suit in SUITS:
        if card_dict[suit] >= 7 or (card_dict[suit] >= 2 and
                                    card_dict[suit] + wild >= 7):
            for card in hand:
                if card[-1] == suit or card[0] in WILDCARDS:
                    group.append(card)
                    if len(group) == 7:
                        break
        phase = [group]

    return phase

# Phase 3: Two sets of four cards of the same value
def phase_3_check(hand):
    
    
    # sort hand by descending value of cards (aces are at the end of hand)
    hand = sorted(hand, key=lambda x: VALUE_DICT[x[0]], reverse=True)
    
    # dictionaries to count the no. of copies of each cards on hand
    copies_count = dd(int)
    for card in hand:
            copies_count[card] += 1

    # check if have a valid phase 3 on hand
    phase = []
    for val in VALUES:
        card_dict = count(hand)[0]
        wild = count(hand)[2]    
        group = []
        if card_dict[val] >= 4 or (card_dict[val] >= 2 and 
                                   card_dict[val] + wild >= 4):
            for card in hand:
                if (card_dict[card[0]] == card_dict[val] and card[0] in val) \
                     or card[0] in WILDCARDS:
                    group.append(card)
                    copies_count[card] -= 1
                    if len(group) == 4:
                        break
            phase.append(group)
            
            # remaining cards on hand
            hand = []
            for card in copies_count.keys():
                if copies_count[card] == 1:
                    hand.append(card)
                elif copies_count[card] == 2:
                    hand += [card, card]
            
            # break and return phase + hand if have 2 groups in phase
            if len(phase) == 2:
                break
    return phase
                
                

# Phase 4: One run of eight cards
def phase_4_check(hand):
    
    if straight(hand):
        run = straight(hand)
        # implement `straight` function to check if have valid phase 4
        if run:
            while len(run) >= 8:
                if phasedout_phase_type([run[-1::-1][::-1]]) == 4:
                    phase = [run[:8]]
                    return phase
                run = run[-2::-1]
                
                
          
# Phase 5: A run of four cards of the same colour and
# a set of four cards of the same value
def phase_5_first_group(hand):
    '''This function takes `hand` and return the first group in phase 5:
    a run of four cards of the same colour'''
    
    # a run of four cards of the same colour
    for permutation in p(sorted(hand, key=lambda x: VAL_DICT[x[0]], 
                                reverse=True), 4):
        if phasedout_group_type(permutation[::-1]) == 5:
            group1 = list(permutation[::-1])
            return group1

def phase_5_second_group(hand):
    '''This function takes `hand` and return the second group of phase 5:
    a set of fours card of the same value'''
    
    # a set of four cards with the same value
    for val in VALUES:
        card_dict = count(hand)[0]
        wild = count(hand)[1]    
        group2 = []
        if card_dict[val] >= 4 or (card_dict[val] >= 2 and 
                                   card_dict[val] + wild >= 4):
            hand = sorted(hand, key=lambda x: VALUE_DICT[x[0]], reverse=True)
            for card in hand:
                if card_dict[card[0]] == card_dict[val] and card[0] in val or\
                   card[0] in WILDCARDS:
                    group2.append(card)
                    if len(group2) == 4:
                        
                        # check and return if group2 is valid type 3
                        if phasedout_group_type(group2) == 3:
                            return group2
            
            
def remaining_cards(group, hand):
    '''this function take `group` and `hand` as arguments and return the
    remaining cards on hand after completing `group`'''
    
    # dictionaries to count the no. of copies of each cards on hand
    copies_count = dd(int)
    for card in hand:
        copies_count[card] += 1
    
    # no. of copies of each card remaining after completing group1
    if group:
        for card in group:
            copies_count[card] -= 1
    
    # remaining cards on hand
    hand = []
    for card in copies_count.keys():
        while copies_count[card] > 0:
            hand.append(card)
            copies_count[card] -= 1
    
    # return remaining cards on hand
    return hand

def unicolor(hand):
    ''' This function takes `hand` as an argument and return two lists: one
    of red cards and one of black cards on hand.'''
    
    # split hand into red and black cards
    red_cards = [card for card in hand if card[-1] in RED]
    black_cards = [card for card in hand if card[-1] in BLACK]
    
    return red_cards, black_cards

def phase_5_check(hand):
 
    if phase_5_first_group(hand):
        group1 = phase_5_first_group(hand)
        remain = remaining_cards(group1, hand)
        if phase_5_second_group(remain):
            group2 = phase_5_second_group(remain)
            phase = [group1, group2]
            if phasedout_phase_type(phase) == 5:
                return phase
    
    if phase_5_second_group(hand):
        group2 = phase_5_second_group(hand)
        remain = remaining_cards(group2, hand)
        if phase_5_first_group(remain):
            group1 = phase_5_first_group(remain)
            phase = [group1, group2]
            if phasedout_phase_type(phase) == 5:
                return phase

def phase_check(hand, player_id, phase_status):

    if phase_status[player_id] == 0:
        if phasedout_phase_type(phase_1_check(hand)) == 1:
            return 1, phase_1_check(hand)
    elif phase_status[player_id] == 1:
        if phasedout_phase_type(phase_2_check(hand)) == 2:
            return 2, phase_2_check(hand)
    elif phase_status[player_id] == 2:
        if phasedout_phase_type(phase_3_check(hand)) == 3:
            return 3, phase_3_check(hand)    
    elif phase_status[player_id] == 3:
        if phasedout_phase_type(phase_4_check(hand)) == 4:
            return 4, phase_4_check(hand)
    elif phase_status[player_id] == 4:
        if phasedout_phase_type(phase_5_check(hand)) == 5:
            return 5, phase_5_check(hand)
    
    return None, None
