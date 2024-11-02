from itertools import permutations

def flop_isomorphisms(flop, 
                     with_spaces=None, 
                     suits_order=['s', 'h', 'd', 'c'], 
                     rank_order=['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']):

    cards = [r+s for r in rank_order for s in suits_order]
    suits_s = ['h', 'd', 'c']
    suits_h = ['s', 'd', 'c']
    suits_d = ['s', 'h', 'c']
    suits_c = ['s', 'h', 'd']
    suits_sh = ['d', 'c']
    suits_sd = ['h', 'c']
    suits_sc = ['h', 'd']
    suits_hs = ['d', 'c']
    suits_hd = ['s', 'c']
    suits_hc = ['s', 'd']
    suits_ds = ['h', 'c']
    suits_dh = ['s', 'c']
    suits_dc = ['s', 'h']
    suits_cs = ['h', 'd']
    suits_ch = ['s', 'd']
    suits_cd = ['s', 'h']

    if with_spaces == True:
        spaces = ' '
    elif with_spaces == False:
        spaces = ''
    elif with_spaces == None:
        if flop.count(' ') > 1:
            spaces = ' '
        else:
            spaces = ''

    flop = flop.replace(' ','')
    sorted_cards = [flop[0:2], flop[2:4], flop[4:6]]
    sorted_cards.sort(key=lambda x:cards.index(x))
    r1, r2, r3 = sorted_cards[0][0], sorted_cards[1][0], sorted_cards[2][0]
    s1, s2, s3 = sorted_cards[0][1], sorted_cards[1][1], sorted_cards[2][1]

    if s1 == s2 == s3: #mono
        flops = [f'{r1}{suit}{r2}{suit}{r3}{suit}' for suit in suits_order]
    elif s1 == s2 or s1 == s3 or s2 == s3: #suited
        if r1 == r2 and s1 != s3:
            temp = s1
            s1 = s2
            s2 = temp
        if r2 == r3 and s1 != s2:
            temp = s2
            s2 = s3
            s3 = temp
        if s1 == s2:
            flops_s = [f'{r1}s{r2}s{r3}{suit}' for suit in suits_s]
            flops_h = [f'{r1}h{r2}h{r3}{suit}' for suit in suits_h]
            flops_d = [f'{r1}d{r2}d{r3}{suit}' for suit in suits_d]
            flops_c = [f'{r1}c{r2}c{r3}{suit}' for suit in suits_c]
        elif s1 == s3:
            flops_s = [f'{r1}s{r2}{suit}{r3}s' for suit in suits_s]
            flops_h = [f'{r1}h{r2}{suit}{r3}h' for suit in suits_h]
            flops_d = [f'{r1}d{r2}{suit}{r3}d' for suit in suits_d]
            flops_c = [f'{r1}c{r2}{suit}{r3}c' for suit in suits_c]
        elif s2 == s3:
            flops_s = [f'{r1}s{r2}{suit}{r3}{suit}' for suit in suits_s]
            flops_h = [f'{r1}h{r2}{suit}{r3}{suit}' for suit in suits_h]
            flops_d = [f'{r1}d{r2}{suit}{r3}{suit}' for suit in suits_d]
            flops_c = [f'{r1}c{r2}{suit}{r3}{suit}' for suit in suits_c]
        flops = flops_s + flops_h + flops_d + flops_c
    else: #rainbow
        flops_sh = [f'{r1}s{r2}h{r3}{suit}' for suit in suits_sh]
        flops_sd = [f'{r1}s{r2}d{r3}{suit}' for suit in suits_sd]
        flops_sc = [f'{r1}s{r2}c{r3}{suit}' for suit in suits_sc]
        flops_hs = [f'{r1}h{r2}s{r3}{suit}' for suit in suits_hs]
        flops_hd = [f'{r1}h{r2}d{r3}{suit}' for suit in suits_hd]
        flops_hc = [f'{r1}h{r2}c{r3}{suit}' for suit in suits_hc]
        flops_ds = [f'{r1}d{r2}s{r3}{suit}' for suit in suits_ds]
        flops_dh = [f'{r1}d{r2}h{r3}{suit}' for suit in suits_dh]
        flops_dc = [f'{r1}d{r2}c{r3}{suit}' for suit in suits_dc]
        flops_cs = [f'{r1}c{r2}s{r3}{suit}' for suit in suits_cs]
        flops_ch = [f'{r1}c{r2}h{r3}{suit}' for suit in suits_ch]
        flops_cd = [f'{r1}c{r2}d{r3}{suit}' for suit in suits_cd]
        flops = flops_sh + flops_sd + flops_sc + flops_hs + flops_hd + flops_hc + flops_ds + flops_dh + flops_dc + flops_cs + flops_ch + flops_cd

    flop_list = []
    for flop in flops:
        for card_list in list(permutations([flop[0:2], flop[2:4], flop[4:6]])):
            flop_list.append(f'{card_list[0]}{spaces}{card_list[1]}{spaces}{card_list[2]}')
    return list(dict.fromkeys(flop_list))

def flop_normalise(flop, 
                   with_spaces=None, 
                   suits_order=['s', 'h', 'd', 'c'], 
                   rank_order=['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']):

    if with_spaces == True:
        spaces = ' '
    elif with_spaces == False:
        spaces = ''
    elif with_spaces == None:
        if flop.count(' ') > 1:
            spaces = ' '
        else:
            spaces = ''

    cards = [r+s for r in rank_order for s in suits_order]
    flop = flop.replace(' ','')
    sorted_cards = [flop[0:2], flop[2:4], flop[4:6]]
    sorted_cards.sort(key=lambda x:cards.index(x))
    r1, r2, r3 = sorted_cards[0][0], sorted_cards[1][0], sorted_cards[2][0]
    s1, s2, s3 = sorted_cards[0][1], sorted_cards[1][1], sorted_cards[2][1]

    if s1 == s2 == s3: #mono
        suit = suits_order[0]
        return f'{r1}{suit}{spaces}{r2}{suit}{spaces}{r3}{suit}'
    elif s1 == s2 or s1 == s3 or s2 == s3: #suited
        if r1 == r2 and s1 != s3:
            temp = s1
            s1 = s2
            s2 = temp
        if r2 == r3 and s1 != s2:
            temp = s2
            s2 = s3
            s3 = temp
        suit_0 = suits_order[0]
        suit_1 = suits_order[1]
        if s1 == s2:
            return f'{r1}{suit_0}{spaces}{r2}{suit_0}{spaces}{r3}{suit_1}'
        elif s1 == s3:
            return f'{r1}{suit_0}{spaces}{r2}{suit_1}{spaces}{r3}{suit_0}'
        elif s2 == s3:
            return f'{r1}{suit_0}{spaces}{r2}{suit_1}{spaces}{r3}{suit_1}'
    else: #rainbow
        suit_0 = suits_order[0]
        suit_1 = suits_order[1]
        suit_2 = suits_order[2]
        return f'{r1}{suit_0}{spaces}{r2}{suit_1}{spaces}{r3}{suit_2}'