stocks = [[96, 5, 1.5, True], [96, 3.5, 1.5, True]]
cuts = [[24, 4.5, 1.5], [72, 3, 1.5], [48, 4, 1.5], [12, 3.5, 1.5]]

while(1):
    print("Kerf size (thin or full): ")
    kerf_inp = input()
    if(kerf_inp == 'thin' or kerf_inp == 'Thin'):
        kerf = 0.09375
        break
    elif(kerf_inp =='full' or kerf_inp == 'Full'):
        kerf = 0.125
        break

cuts = sorted(cuts, reverse=True) #sort cuts largest first

def find_possible_matching(cuts_remaining, stocks):
    possible_matchings = []
    for cut in cuts_remaining:
        curr_cut_len = cut[0] #cut len
        curr_cut_width = cut[1] #cut width
        
        for stock in stocks: #check each stock len + width
            if(curr_cut_len <= stock[0] and curr_cut_width <= stock[1]): #if cut len and width less than max stock len and width
                possible_matchings.append([cuts.index(cut), stocks.index(stock)])#candidate found, store it. has shape [[cut, stock],]
    return possible_matchings

def find_single_matching_cuts(possible_matchings):
    single_matching = []
    index_to_remove = []

    for index, item in enumerate(possible_matchings): #iterate over the enumeraton of matchings
        current_cut = item[0] #current cut
        match_counter = 0 
        for i in range(len(possible_matchings)): #iterate over all matches
            if(current_cut == possible_matchings[i][0]): #check for multiple matches
                match_counter += 1 #increment match counter
        if(match_counter == 1): #check if only a single matching
            single_matching.append(item) #store to single matching list
            index_to_remove.append(index)

    return index_to_remove, single_matching

def remove_indicies(index_to_remove, possible_matchings):
    index_to_remove = sorted(index_to_remove, reverse=True) #reverse index list to not change position of desired deletion indicies.
    for index in index_to_remove: #remove cuts with only one match from list
        del possible_matchings[index]
    
    return possible_matchings

#function takes two index arguments and a lists of lists remaining stock. subtracts cut length and kerf from the length of stock and checks if it needs to cut down width. Places leftover back into the remaining stock array. Returns the remaining stock and completed cut arrays.
def single_matching_cut_stock_to_size(current_cut, cuts_remaining, required_stock, remaining_stock, kerf, completed_cuts):
    remaining_stock[required_stock][3] = False
    remaining_stock[required_stock][0] -= (cuts_remaining[current_cut][0] + kerf) #reduce length of remaining stock
    
    if(cuts[current_cut][1] < remaining_stock[required_stock][1]): #checking if the width of cut needed is less than the width of the stock
        
        current_cut_len = cuts_remaining[current_cut][0] #get dimensions in easy to read format
        current_cut_width = cuts_remaining[current_cut][1]
        current_cut_height = cuts_remaining[current_cut][2]
        parent_stock = required_stock #get index of parent stock piece
        current_cut_width = remaining_stock[required_stock][1] - (current_cut_width + kerf) #cut down to final width by subtracting required cut width plus blade kerf from width of stock
        child_cut_piece = [current_cut_len, current_cut_width, current_cut_height, False, parent_stock] #remainder of stock from cutoff #if fourth val in list, index of parent stock it came from
        remaining_stock.append(child_cut_piece) #return remainder of cutoff to stock pile
        
    completed_cuts.append(cuts_remaining[current_cut]) #add completed cut to pile
    
    return completed_cuts, remaining_stock


def remove_completd_from_remaining_cuts(cuts_completed, cuts_remaining):
    for cut in cuts_completed:
        if cut in cuts_remaining:
            completed_cut_index = cuts_remaining.index(cut)
            cuts_remaining.pop(completed_cut_index)
    
    return cuts_remaining

def initial_ranking_multiple_matchings(multiple_matching, stock_remaining):
    priority_matchings = []
    for match in multiple_matching:
        if(stock_remaining[match[1]][3] == False): #check if board has already been cut - this is most desirable to minimize waste
            priority_matchings.append(match)
    
    return priority_matchings

def recursive_greedy_cut_solver(cuts_remaining, stock_remaining, completed_cuts, kerf, depth=0):

    cuts_remaining = sorted(cuts_remaining, reverse=True) #reverse the cuts remaining from largest to smallest
    possible_matchings = find_possible_matching(cuts_remaining, stock_remaining) #get list of possible matching of cuts

    if(len(cuts_remaining) == 0 or len(stock_remaining) == 0 or not possible_matchings): #base case, where either no cuts or no stock remain or no matches possible
        return completed_cuts, stock_remaining, cuts_remaining
    
    print()
    print("depth: ", depth)
    print("cuts remaining:", cuts_remaining)
    print("possible matchings:", possible_matchings)
    print("Stock remaining:", stock_remaining)
    print("completed cuts: ", completed_cuts)
    print()
    
    indicies_for_removal, single_matchings = find_single_matching_cuts(possible_matchings) #get any matches that only match to one stock piece and their index

    if(indicies_for_removal): #if there are indicies identified for removal
        multiple_matchings = remove_indicies(indicies_for_removal, possible_matchings) # - remove them  from multiple matchings list and return a list of possible multiple matching list
    else:
        multiple_matchings = possible_matchings #set mutliple matchings to entire list of possible matchings (no single matching exists)

    if single_matchings: #check non zero single matches
        for match in single_matchings: #iterate over cuts with one matching
            current_cut = match[0] 
            required_stock = match[1]
            completed_cuts, stock_remaining = single_matching_cut_stock_to_size(current_cut, cuts_remaining, required_stock, stock_remaining, kerf, completed_cuts) #calculate/handle cuts and return leftover to stock
        cuts_remaining = remove_completd_from_remaining_cuts(completed_cuts, cuts_remaining) #remove completed cuts from cuts remaining
   
    else: #otherwise, zero single matches evaluate multiple matchings
        current_cut_to_evaluate_matchings = multiple_matchings[0][0] #get the index of the first cut in multiple matchings
        set_of_current_cut_matches = []
        for match in multiple_matchings: #iterate over multiple matchings list
            if(match[0] == current_cut_to_evaluate_matchings): #check if current match is for the same cut as current cut we are evaluating 
                set_of_current_cut_matches.append(match) #store the match
            else:
                break #otherwise no more matches to evaluate
        
        print("set of current matches 129", set_of_current_cut_matches)
        match_priority = initial_ranking_multiple_matchings(set_of_current_cut_matches, stock_remaining) #get any boards that match that are already cut (preserve whole boards)

        print("priority:", match_priority)
        if(match_priority): #if there is a priority of matches
            set_of_current_cut_matches = match_priority #set equal to current priority evaluation set (remove any uncut stock from evaluation set)
        
        print("set of priority:", set_of_current_cut_matches)
        
        possible_stock_widths = [] #initialize empty list to store widths, difference of lengths, and stock piece
        for match in set_of_current_cut_matches: #iterate over current matches we are evaluating
            print(match)
            print("Current Match in set of current cut matches:", match[0], " Stock is: ", stock_remaining[match[1]])
            width_of_current_stock = stock_remaining[match[1]][1] #get current width
            print(cuts_remaining)
            length_diff = stock_remaining[match[1]][0] - cuts_remaining[match[0]][0] #get length diff
            possible_stock_widths.append([width_of_current_stock, length_diff, match[0], match[1]]) #store in shape [width, difference of length, cut, stock]

        possible_stock_widths = sorted(possible_stock_widths) #sort by width, smallest to largest

        print("sorted by width:" , possible_stock_widths)

        smallest_width = possible_stock_widths[0][0]
        print("min width", smallest_width)
        tie_count = 0
        for i in range (len(possible_stock_widths)): #iterate over possible stock widths
            if(possible_stock_widths[i][0] <= smallest_width and i > 0): #checking if current width is the same as the smallest
                tie_count += 1 #tie found
        
        if(tie_count > 0): #if we found a tie
            print("we need to check leftover lengths") 
        
        else: #no ties found
            #perform cut operation for current board
            current_cut = possible_stock_widths[0][2]
            required_stock = possible_stock_widths[0][3]
            
            print("Current cut on line 160:", current_cut)
            print("req stock:", required_stock)
            
            print("stock before cut: ", stock_remaining)
            completed_cuts, stock_remaining = single_matching_cut_stock_to_size(current_cut, cuts_remaining, required_stock, stock_remaining, kerf, completed_cuts)
            cuts_remaining = remove_completd_from_remaining_cuts(completed_cuts, cuts_remaining) #remove completed cuts from cuts remaining
            print("completed cuts:", completed_cuts)
            print("stock remaining:", stock_remaining)
            print("cuts remaining:", cuts_remaining)
            #evaluate the best match - what is the best match? minimizing leftover from remaining stock?
            fart = input()
             
    depth += 1
    return recursive_greedy_cut_solver(cuts_remaining, stock_remaining, completed_cuts, kerf, depth)

print("cuts: ", cuts)
print("stocks: ", stocks)
my_finished_cuts, leftover_stock, cuts_remaining = recursive_greedy_cut_solver(cuts, stocks, [], kerf)

print()
print(my_finished_cuts)
print(leftover_stock)
print(cuts_remaining)

