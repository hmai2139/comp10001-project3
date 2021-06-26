from previous import (count_type as count, phasedout_is_valid_play as valid)
from modified import phasedout_group_extra_cards as extra
from phase_generator import (phase_check, remaining_cards, unicolor,
                             phase_5_first_group, phase_5_second_group)
from straight_generator import needed_cards

# dictionary to map cards to corresponding integer values
VALUE_DICT = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 25}

# values and suits in deck, respectively
VALUES = '234567890JQK'
SUITS = 'SDHC'

# wild cards in deck
WILDCARDS = 'A'

# colors of suits
RED = 'DH'
BLACK = 'SC'

def record(turn_history, player_id, next_player, phase_status):
    '''This function takes `turn_history`, `player_id`, next_player`,
    `phase_status` as arguments and return a record of next player (one who 
    can pick up current player's discarded cards)'s discarded and picked up
    card ranks/ suits, to be used as a part of strategy.'''
    
    # next player's picked cards
    picked = []
    
    # next player's discarded cards
    discarded = []
    
    # iterate through turn history to record
    for turn in turn_history:
        if turn[0] == next_player:
            for play in turn[-1]:
                
                # record picked/discarded card ranks when next player
                # is building phase 1/phase 3/phase 4
                if phase_status[next_player] == 0 or \
                   phase_status[next_player] == 2 or \
                   phase_status[next_player] == 3:
                    if play[0] == 2:
                        picked.append(play[1][0])
                    elif play[0] == 5:
                        discarded.append(play[1][0])
                
                # record picked/discarded suits when next player is building
                # phase 2
                elif phase_status[next_player] == 1:
                    if play[0] == 2:
                        picked.append(play[1][-1])
                    elif play[0] == 5:
                        discarded.append(play[1][-1])
                
                # record picked/discarded suits and ranks when next player is
                # building the last phase
                elif phase_status[next_player] == 4:
                    if play[0] == 2:
                        picked.append(play[1][0])
                        picked.append(play[1][-1])
                    elif play[0] == 5:
                        discarded.append(play[1][0])
                        discarded.append(play[1][-1])
    
    # return the recorded lists
    return picked, discarded


def play_1_or_2(player_id, table, turn_history, phase_status, hand, discard):    
    '''This function returns the play type 1 and type 2 the current player
    wishes to make.'''
    
    # play wish to make
    play = (None, None)
    
    if not turn_history:
        play = (1, None)
        return play
    
    # if `discard` is a wildcard, pick up
    if discard[0] in WILDCARDS:
        play = (2, discard)
        if valid(play, player_id, table, turn_history,
                 phase_status, hand, discard):
            return play
                
    # implement `count` to count type of cards
    card_dict = count(hand)[0]
    
    # no. of wildcards on hand
    wilds = count(hand)[2]
    
    # the phase the current player is working on
    current_phase = phase_status[player_id] + 1
    
    # strategy if haven't placed a phase
    if table[player_id][0] is None:
    
        # check if already have a valid phase on hand by implementing
        # imported `phase_check` function, which takes 
        # `(hand, player_id, phase_status)` as arguments and return a tuple
        # in the form of `(phase type, phase)` 
        phase_type = phase_check(hand, player_id, phase_status)[0]
            
        # check if `discard` can be placed on phases by calling `extra`
        # function which takes group(s) of a phase with extra cards and their
        # original types and return the original type if it still holds.
        
        if phase_type:
            phase = phase_check(hand, player_id, phase_status)[-1]
            group1 = phase[0]
            group2 = phase[-1]
            
            # check if `discard` can be placed on phase 5
            if phase_type == current_phase == 5:
                if extra(group1 + [discard], phase_type) == 5 or \
                   extra(group2 + [discard], phase_type) == 3:
                        play = (2, discard)
                        if valid(play, player_id, table, turn_history,
                                 phase_status, hand, discard):
                            return play
            
            # check if `discard` can be placed on phase 4
            elif phase_type == 4:
                if extra(group1 + [discard], phase_type) == current_phase or \
                   extra([discard] + group1, phase_type) == current_phase:
                    play = (2, discard)
                    if valid(play, player_id, table, turn_history,
                             phase_status, hand, discard):
                            return play
                    
            # check if `discard` can be placed on phase 1/2/3
            elif phase_type < 4:
                if extra(group1 + [discard], phase_type) == current_phase or \
                   extra(group2 + [discard], phase_type) == current_phase:
                    play = (2, discard)
                    if valid(play, player_id, table, turn_history,
                             phase_status, hand, discard):
                            return play
                        
            # check if `discard` can be placed on another phase on the table
            # by calling `play_4` function:
            if play_4(discard, player_id, table, turn_history, phase_status,
                      hand):
                play = (2, discard)
                if valid(play, player_id, table, turn_history,
                         phase_status, hand, discard):
                        return play
            
            # find the remaining cards on hand after completing phase by
            # calling the `remaining_cards` function which takes group(s)
            # of a phase and `hand` and returns the remaining cards on hand.
            
            if len(phase) == 1:
                remain = remaining_cards(group1, hand)
            elif len(phase) == 2:
                remain = remaining_cards(group1 + group2, hand)
            
            # remove wildcards and sort `remain` in ascending order
            remain = [card for card in remain if card[0] not in WILDCARDS]
            remain = sorted(remain, key=lambda x: VALUE_DICT[x[0]])
            
             
            # pick up `discard` if is smaller than or equal to the smallest
            # card on hand
            if hand:
                if VALUE_DICT[discard[0]] <= VALUE_DICT[remain[0][0]]:
                    play = (2, discard)
                    if valid(play, player_id, table, turn_history,
                             phase_status, hand, discard):
                            return play 
            
            # else, pick up from deck
            play = (1, None)
            return play
        
        # strategy if don't have a phase on hand
        elif phase_type is None:
        
            # check if `discard` helps complete phases
            if phase_check(hand + [discard], player_id, phase_status)[0] == \
               current_phase:
                        play = (2, discard)
                        if valid(play, player_id, table, turn_history,
                                 phase_status, hand, discard):
                            return play
         
            # if `discard` can't complete phase, check if `discard` helps build 
            # phase:
            
            # check if `discard` helps build phase 1
            if current_phase == 1:
                if card_dict[discard[0]] >= 2:
                    play = (2, discard)
                    if valid(play, player_id, table, turn_history,
                             phase_status, hand, discard):
                        return play
            
            # check if `discard` helps build phase 2
            elif current_phase == 2:
                
                # sort hand in ascending suit frequency
                hand = [card for card in hand if card[0] not in WILDCARDS]
                hand = sorted(hand, key=lambda x: card_dict[x[1]])
                
                # max suit frequency
                max_freq = card_dict[hand[-1][-1]]
                
                # check if discard is of the suit with max frequency
                if max_freq >= 3 and card_dict[discard[-1]] == max_freq:
                    play = (2, discard)
                    if valid(play, player_id, table, turn_history,
                             phase_status, hand, discard):
                        return play
                        
            # check if `discard` helps build phase 3
            elif current_phase == 3:
                if card_dict[discard[0]] >= 3: 
                    play = (2, discard)
                    return play
                elif (card_dict[discard[0]] >= 2 and card_dict[discard[0]] +
                      wilds >= 4):
                    play = (2, discard)
                    return play
                        
            # check if `discard` helps build phase 4 by calling `needed_cards`
            # function which takes `hand` and returns a list of card ranks
            # needed for a run
            elif current_phase == 4:
                needed = needed_cards(hand)
                if str(VALUE_DICT[discard[0]]) in needed:
                    play = (2, discard)
                    if valid(play, player_id, table, turn_history,
                             phase_status, hand, discard):
                        return play
               
            # check if `discard` helps build phase 5
            elif current_phase == 5:
                
                # check if have a valid group 2 of phase 5 on hand by 
                # calling `phase_5_first_group` function which takes
                # `hand` and returns group 2 of phase 5 if valid
                if phase_5_second_group(hand):
                    
                    # if have a valid group2, find the remaining cards
                    group2 = phase_5_second_group(hand)
                    remain = remaining_cards(group2, hand)
                                       
                    # check if `discard` can complete group 1
                    if phase_5_first_group(remain + [discard]):
                            play = (2, discard)
                            if valid(play, player_id, table, turn_history,
                                     phase_status, hand, discard):
                                return play
                    
                    # else, check if `discard` with `remain` can build a valid
                    # group 1 of phase 5 by finding cards rank needed for a run
                    
                    # remove wildcards from `remain`
                    remain = [card for card in remain if card[0] not in
                              WILDCARDS]
                    
                    # count the remaining no. of red cards and black cards
                    red_remain = unicolor(remain)[0]
                    black_remain = unicolor(remain)[-1]
                    
                    # find the cards needed for a red/ black run
                    needed_red = needed_cards(red_remain)
                    needed_black = needed_cards(black_remain)
                    
                    if ((discard[-1] in RED and str(VALUE_DICT[discard[0]]) in
                         needed_red) or (discard[-1] in BLACK and
                                         str(VALUE_DICT[discard[0]]) in 
                                         needed_black)):
                        play = (2, discard)
                        if valid(play, player_id, table, turn_history,
                                 phase_status, hand, discard):
                            return play
                    
                # if don't have a group 2 but have a group 1 on hand
                if phase_5_first_group(hand):
                    group1 = phase_5_first_group(hand)
                    
                    # remaining cards on hand
                    remain = remaining_cards(group1, hand)
                    
                    # check if `discard` can complete group 2
                    if phase_5_second_group(remain + [discard]):
                        play = (2, discard)
                        if valid(play, player_id, table, turn_history,
                                 phase_status, hand, discard):
                            return play
                    
                    # else, check if `discard` can help build group 2
                    # count types of cards in remain
                    remain_dict = count(remain)[0]
                    
                    # no of wildcards in `remain`
                    wilds_remain = count(remain)[2]
                    
                    # remove wildcards from `remain` so they won't count in
                    # frequency comparison
                    remain = [card for card in remain if card[0] not in
                              WILDCARDS]
                    
                    # check the maximum card rank frequency
                    remain = sorted(remain, key=lambda x: remain_dict[x[0]],
                                    reverse=True)
                    
                    max_freq = remain_dict[remain[0][0]]
                    if (remain_dict[discard[0]] == max_freq or 
                        (remain_dict[discard[0]] >= 2 and
                         remain_dict[discard[0]] + wilds_remain >= 4)):
                        play = (2, discard)
                        if valid(play, player_id, table, turn_history,
                                 phase_status, hand, discard):
                            return play
        
        # else, pick from deck
        play = (1, None)
        return play
        
    # if played a phase, check if `discard` can be placed on phases on table
    elif table[player_id][0] is not None:
        if play_4(discard, player_id, table, turn_history, phase_status,
                  hand):
            play = (2, discard)
            if valid(play, player_id, table, turn_history,
                     phase_status, hand, discard):
                return play
        else:
            play = (1, None)
            return play
        
        
def play_4(card, player_id, table, turn_history, phase_status, hand):
    ''' This function returns the play type 4 that current player wishes to
    make.'''
    
    # phase and its type that player 0 placed on table
    player_0_phase = table[0][-1]
    player_0_phase_type = table[0][0]
    
    # check if `card` can be placed on player 0's phase
    for group in player_0_phase:
                    
        # id of the player who placed the phase
        phase_player = 0
                    
        # index of the group to be placed on
        index = player_0_phase.index(group)
                    
        if extra(group + [card], player_0_phase_type) == \
           extra(group, player_0_phase_type):
                        
            # position within group the card is being played to
            pos = len(group)
                        
            # check and return play if valid
            play = (4, (card, (phase_player, index, pos)))
            return play
                        
        elif (extra([card] + group, player_0_phase_type) ==
              extra(group, player_0_phase_type)):
                
                # position within group the card is being played to
                pos = 0
                        
                # check and return play if valid
                play = (4, (card, (phase_player, index, pos)))
                return play
        
    # phase and its type that player 1 placed on table
    player_1_phase = table[1][-1]
    player_1_phase_type = table[1][0]
    
    # check if `card` can be placed on player 1's phase
    for group in player_1_phase:
        
        # id of the player who placed the phase
        phase_player = 1
                    
        # index of the group to be placed on
        index = player_1_phase.index(group)
        if extra(group + [card], player_1_phase_type) == \
           extra(group, player_1_phase_type):
                        
            # position within group the card is being played to
            pos = len(group)
                        
            # check and return play if valid
            play = (4, (card, (phase_player, index, pos)))
            return play
                        
        elif (extra([card] + group, player_1_phase_type) ==
              extra(group, player_1_phase_type)):
            
            # position within group the card is being played to
            pos = 0
                        
            # check and return play if valid
            play = (4, (card, (phase_player, index, pos)))
            return play

    # phase and its type that player 2 placed on table
    player_2_phase = table[2][-1]
    player_2_phase_type = table[2][0]
    
    # check if `card` can be placed on player 2's phase
    for group in player_2_phase:
        
        # id of the player who placed the phase
        phase_player = 2
                    
        # index of the group to be placed on
        index = player_2_phase.index(group)
                    
        if extra(group + [card], player_2_phase_type) == \
           extra(group, player_2_phase_type):
                        
            # position within group the card is being played to
            pos = len(group)
                        
            # check and return play if valid
            play = (4, (card, (phase_player, index, pos)))
            return play
                        
        elif (extra([card] + group, player_2_phase_type) ==
              extra(group, player_2_phase_type)):
                
                # position within group the card is being played to
                pos = 0
                        
                # check and return play if valid
                play = (4, (card, (phase_player, index, pos)))
                return play
                
    # phase and its type that player 3 placed on table
    player_3_phase = table[3][-1]
    player_3_phase_type = table[3][0]
    
    # check if `card` can be placed on player 3's phase
    for group in player_3_phase:
        
        # id of the player who placed the phase
        phase_player = 3
                    
        # index of the group to be placed on
        index = player_3_phase.index(group)
                    
        if extra(group + [card], player_3_phase_type) == \
           extra(group, player_3_phase_type):
                
                # position within group the card is being played to
                pos = len(group)
                        
                # check and return play if valid
                play = (4, (card, (phase_player, index, pos)))
                return play
                        
        elif (extra([card] + group, player_3_phase_type) ==
              extra(group, player_3_phase_type)):
                        
                # position within group the card is being played to
                pos = 0
                        
                # check and return play if valid
                play = (4, (card, (phase_player, index, pos)))
                return play                            

                
def play_5(player_id, table, turn_history, phase_status, hand, discard):
    '''This function return the play type 5 the current player wishes to
    make.'''
    
    # call `count` to count types of cards
    card_dict = count(hand)[0]
    
    # discard logic when working on phases
    if table[player_id][0] is None:
      
        # when working on phase 1 or phase 3
        if phase_status[player_id] == 0 or phase_status[player_id] == 2:
            
            # remove wildcards from hand before discarding
            hand = [card for card in hand if card[0] not in WILDCARDS]
            
            # sort hand in ascending rank frequency and descending value
            hand = sorted(hand, key=lambda x: VALUE_DICT[x[0]],
                          reverse=True)
            hand = sorted(hand, key=lambda x: card_dict[x[0]])
           
            # discard card with highest value and lowest rank frequency                   
            to_be_discarded = hand[0]
            play = (5, to_be_discarded)
            if valid(play, player_id, table, turn_history, phase_status,
                     hand, discard):
                        return play
        
        # when working on phase 2
        elif phase_status[player_id] == 1:
          
            # remove wildcards from hand before discarding
            hand = [card for card in hand if card[0] not in WILDCARDS]
            
            # sort hand in ascending suit frequency and descending value
            hand = sorted(hand, key=lambda x: VALUE_DICT[x[0]], reverse=True)
            hand = sorted(hand, key=lambda x: x[1])
            hand = sorted(hand, key=lambda x: card_dict[x[1]])
                
            # discard card with highest value and lowest suit frequency                   
            to_be_discarded = hand[0]
            play = (5, to_be_discarded)
            if valid(play, player_id, table, turn_history, phase_status, 
                     hand, discard):
                return play
      
        # when working on phase 4
        elif phase_status[player_id] == 3:
            
            # remove wildcards from hand before discarding
            hand = [card for card in hand if card[0] not in WILDCARDS]
            
            # sort hand in descending rank frequency and descending value
            hand = sorted(hand, key=lambda x: VALUE_DICT[x[0]], reverse=True)
            hand = sorted(hand, key=lambda x: card_dict[x[0]], reverse=True)
                
 
            # discard card with the highest rank frequency and highest rank
            to_be_discarded = hand[0]                  
            play = (5, to_be_discarded)
            if valid(play, player_id, table, turn_history,
                     phase_status, hand, discard):
                return play            
      
        # when working on phase 5                  
        elif phase_status[player_id] == 4:
            
            # if have a valid group1, find the remaining cards
            if phase_5_first_group(hand):
                group1 = phase_5_first_group(hand)
                remain = remaining_cards(group1, hand)
                    
                # remove wildcards from `remain`
                remain = [card for card in remain if card[0] not in
                          WILDCARDS]
                
                # sort remaining cards on hand in descending value and 
                # ascending rank frequency
                remain = sorted(remain, key=lambda x: VALUE_DICT[x[0]],
                                reverse=True)
                remain = sorted(remain, key=lambda x: card_dict[x[0]])
                
                # discard the card with highest value and lowest rank
                # frequency               
                to_be_discarded = remain[0]
                play = (5, to_be_discarded)
                if valid(play, player_id, table, turn_history,
                         phase_status, hand, discard):
                    return play
                
            # if don't have valid group 1 but have a valid group 2, find 
            # remaining cards
            if phase_5_second_group(hand):
                group2 = phase_5_second_group(hand)
                remain = remaining_cards(group2, hand)
                    
                # remove wildcards from `remain`
                remain = [card for card in remain if card[0] not in
                          WILDCARDS]
                    
                # sort remaining cards in descending rank frequency and
                # descending value
                remain = sorted(remain, key=lambda x: VALUE_DICT[x[0]],
                                reverse=True)
                remain = sorted(remain, key=lambda x: card_dict[x[0]],
                                reverse=True) 
                    
                # count the remaining no. of red cards and black cards
                red_remain = unicolor(remain)[0]
                black_remain = unicolor(remain)[-1]
                    
                # find the cards needed for a red/ black run
                needed_red = needed_cards(red_remain)
                needed_black = needed_cards(black_remain)
               
                    
                # pick from the color which needs more cards to discard
                if len(needed_red) < len(needed_black):
                    to_be_discarded = black_remain[0]
                    play = (5, to_be_discarded)
                    if valid(play, player_id, table, turn_history,
                             phase_status, hand, discard):
                        return play
                    
                elif len(needed_red) > len(needed_black):
                    to_be_discarded = red_remain[0]
                    play = (5, to_be_discarded)
                    if valid(play, player_id, table, turn_history,
                             phase_status, hand, discard):
                        return play
                                
                # if tied, discard the card with highest value                 
                to_be_discarded = remain[0]
                play = (5, to_be_discarded)
                if valid(play, player_id, table, turn_history,
                         phase_status, hand, discard):
                    return play

            # if have neither valid group 1 nor group 2, discard the card
            # with highest value, lowest rank frequency and lowest
            # color frequency
            
            # remove wildcards from hand
            hand = [card for card in hand if card[0] not in WILDCARDS]
                
            # sort hand in descending value and ascending rank frequency
            hand = sorted(hand, key=lambda x: VALUE_DICT[x[0]],
                          reverse=True)
            hand = sorted(hand, key=lambda x: card_dict[x[0]])
                
            # split card into 2 list of red and black cards by calling
            # `unicolor` function
            reds = unicolor(hand)[0]
            blacks = unicolor(hand)[-1]

            # pass `reds` and `blacks` to `needed` function to find the card
            # necessary for a run
            needed_red = needed_cards(reds)
            needed_black = needed_cards(blacks)
            
            if len(needed_red) > len(needed_black):
                for card in hand:
                    if card[-1] in RED:
                        to_be_discarded = card
                        play = (5, to_be_discarded)
                        if valid(play, player_id, table, turn_history,
                                 phase_status, hand, discard):
                            return play
            
            elif len(needed_red) < len(needed_black):
                for card in hand:
                    if card[-1] in BLACK:
                        to_be_discarded = card
                        play = (5, to_be_discarded)
                        if valid(play, player_id, table, turn_history,
                                 phase_status, hand, discard):
                            return play
                
            # if tied, discard card with highest value
            to_be_discarded = hand[0]
            play = (5, to_be_discarded)
            if valid(play, player_id, table, turn_history,
                     phase_status, hand, discard):
                return play      
                
    
                                
def phasedout_play(player_id, table, turn_history, phase_status, hand,
                   discard):
    '''This function returns the plays that the current player wishes to
    make.'''
    
    # play wish to make
    play = (None, None)
    
    # if starting the current hand, make play 1 or 2
    if not turn_history:
        return play_1_or_2(player_id, table, turn_history, phase_status,
                           hand, discard)
    
    # player who made the last play so far
    last_player = turn_history[-1][0]
    
    # the last play of the game so far
    last_play = turn_history[-1][-1][-1][0]
    
    # discard the last card of hand
    if len(hand) == 1 and last_player == player_id:
        return (5, hand[0])
    
    # make play 1 or 2 when turn starts
    if last_player != player_id:
        return play_1_or_2(player_id, table, turn_history, phase_status,
                           hand, discard)
    
    if table[player_id][0] is None:
        if last_player == player_id and (last_play == 1 or last_play == 2):
        
            # the phase the player is working on
            current_phase = phase_status[player_id] + 1
        
            # place phase if have a valid phase
            if table[player_id][0] is None:
                phase_type = phase_check(hand, player_id, phase_status)[0]
                if phase_type == current_phase:
                    phase = phase_check(hand, player_id, phase_status)[-1]
                    play = (3, phase)
                    if valid(play, player_id, table, turn_history,
                             phase_status, hand, discard):
                        return play
             
            # else, discard and end turn
            return play_5(player_id, table, turn_history, phase_status, hand,
                          discard)
    
    # make play 4 if played a phase within the current hand
    if table[player_id][0] is not None:
        for card in hand:
            play = play_4(card, player_id, table, turn_history, 
                          phase_status, hand)
            if play:
                return play 
    
        # discard logic if have played a phase within the current hand        
        # call `record` function to get a list of picked up and discarded
        # ranks/suits of the next player
        if player_id == 3:
            next_player = 0
        else:
            next_player = player_id + 1
            
        # sort hand in descending value after removing wildcards
        hand = [card for card in hand if card[0] not in WILDCARDS]
        hand = sorted(hand, key=lambda x: VALUE_DICT[x[0]], reverse=True)
        
        # if the next player hasn't played a phase
        if table[next_player][0] is None:
        
            # list of picked up and discarded ranks/suits of the next
            # player, respectively
            picked = record(turn_history, player_id, next_player,
                            phase_status)[0]
            discarded = record(turn_history, player_id, next_player,
                               phase_status)[-1]
        
            # predict what the next player needs and discard the largest
            # possible
            for card in hand:
            
                # discard when next player is working on phase 1 or 3
                if phase_status[next_player] == 0 or \
                   phase_status[next_player] == 2:
                        if card[0] in discarded and card[0] not in picked:
                            to_be_discarded = card
                            play = (5, to_be_discarded)
                            if valid(play, player_id, table, turn_history,
                                     phase_status, hand, discard):
                                return play
                        
                        # if no card meets the criteria, discard the one with
                        # highest rank
                        to_be_discarded = hand[0]
                        play = (5, to_be_discarded)
                        if valid(play, player_id, table, turn_history,
                                 phase_status, hand, discard):
                            return play
                    
                # discard when next player is working on phase 2
                elif phase_status[next_player] == 1:
                    if card[-1] in discarded and card[-1] not in picked:
                        to_be_discarded = card
                        play = (5, to_be_discarded)
                        if valid(play, player_id, table, turn_history,
                                 phase_status, hand, discard):
                            return play
                        
                    # if no card meets the criteria, discard the one with
                    # highest rank
                to_be_discarded = hand[0]
                play = (5, to_be_discarded)
                if valid(play, player_id, table, turn_history,
                         phase_status, hand, discard):
                    return play
                        
        elif table[next_player][0] is not None:
            
            # if the next player has played a phase, discard the largest 
            to_be_discarded = hand[0]
            play = (5, to_be_discarded)
            if valid(play, player_id, table, turn_history,
                     phase_status, hand, discard):
                return play
