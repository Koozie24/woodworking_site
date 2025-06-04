stocks = [[96, 5, 1.5, True], [96, 3.5, 1.5, True]]
cuts = [[24, 4.5, 1.5], [72, 3, 1.5], [48, 4, 1.5], [12, 3.5, 1.5]]

#prompt user to get kerf size
while(1):
    print("Kerf size (thin or full): ", end=None)
    kerf_inp = input()
    if(kerf_inp == 'thin' or kerf_inp == 'Thin'):
        kerf = 0.09375
        break
    elif(kerf_inp =='full' or kerf_inp == 'Full'):
        kerf = 0.125
        break

cuts = sorted(cuts, reverse=True) #sort cuts largest first

def find_possible_matching(cuts_remaining, stocks):
    '''
        Function takes two lists and finds all possible matchings between some desired cuts and the stock on hand. Returns a list of all possible matchings
    '''
    possible_matchings = []
    for cut in cuts_remaining:
        curr_cut_len = cut[0] #cut len
        curr_cut_width = cut[1] #cut width
        
        for stock in stocks: #check each stock len + width
            if(curr_cut_len <= stock[0] and curr_cut_width <= stock[1]): #if cut len and width less than max stock len and width
                possible_matchings.append([cuts_remaining.index(cut), stocks.index(stock)])#candidate found, store it. has shape [[cut, stock],]
    return possible_matchings

def find_single_matching_cuts(possible_matchings):
    '''
        Function takes some list of matchings and checks for cuts that only have one matching stock within their dimensions. Returns a list of indicies to remove from possible_matchings and the list of single matchings
    '''
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
    '''
        Function sorts some indicies in a reverse order and then pops each index from start to finsih from a list. Returns the filtered list.
    '''
    index_to_remove = sorted(index_to_remove, reverse=True) #reverse index list to not change position of desired deletion indicies.
    for index in index_to_remove: #remove cuts with only one match from list
        del possible_matchings[index]
    
    return possible_matchings

#function takes two index arguments and a lists of lists remaining stock. subtracts cut length and kerf from the length of stock and checks if it needs to cut down width. Places leftover back into the remaining stock array. Returns the remaining stock and completed cut arrays.
def cut_stock_to_size(current_cut, cuts_remaining, required_stock, remaining_stock, kerf, completed_cuts):
    '''
        Function performs the cut operation for a board by removing the length. Appends completed cut to completed Also checks width of required stock compared to cut. If cut length is less than that of the stock, we cut away from the width of the leftover piece and store the
        remaining stock at in the stock list. Returns two lists: the completed cuts and the remaining stock. 
    '''
    remaining_stock[required_stock][3] = False
    remaining_stock[required_stock][0] -= (cuts_remaining[current_cut][0] + kerf) #reduce length of remaining stock

    #checking if the width of cut needed is less than the width of the stock
    if(cuts_remaining[current_cut][1] < remaining_stock[required_stock][1]):
        #get dimensions in easy to read format
        current_cut_len = cuts_remaining[current_cut][0] 
        current_cut_width = cuts_remaining[current_cut][1]
        current_cut_height = cuts_remaining[current_cut][2]
        #cut down to final width by subtracting required cut width plus blade kerf from width of stock
        current_cut_width = remaining_stock[required_stock][1] - (current_cut_width + kerf)
        #remainder of stock from cutoff #if fourth val in list, index of parent stock it came from
        child_cut_piece = [current_cut_len, current_cut_width, current_cut_height, False, required_stock] 
        remaining_stock.append(child_cut_piece)
    
    completed_cuts.append([cuts_remaining[current_cut], required_stock])
    return completed_cuts, remaining_stock

def remove_completed_from_remaining_cuts(cuts_completed, cuts_remaining):
    '''
        Removes cut pieces that have been successfully added to completed list from cuts remaining list and returns an updated remaining cut list
    '''
    for cut in cuts_completed:
        if cut[0] in cuts_remaining:
            completed_cut_index = cuts_remaining.index(cut[0])
            cuts_remaining.pop(completed_cut_index)
    
    return cuts_remaining

def  find_matches_to_already_cut_stock(multiple_matching, stock_remaining):
    '''
        goes through matchings and determines if a board has already been cut - if so, then marks it as a priority. returns a list of priority matches
    '''
    priority_matchings = []
    for match in multiple_matching:
        if(stock_remaining[match[1]][3] == False): #check if board has already been cut - this is most desirable to minimize waste
            priority_matchings.append(match)
    
    return priority_matchings

def get_list_of_multiple_matches_to_evaluate(multiple_matchings):
    '''
        Function iterates over set of matches to find the multiple matches of the first index. Returns a list of the set of pairs with the same index as the first match in list
    '''
    current_cut_to_evaluate_matchings = multiple_matchings[0][0] #first match in multiple matchings
    set_of_current_cut_matches = []
    for match in multiple_matchings:
        if(match[0] == current_cut_to_evaluate_matchings): #check if current match is for the same cut as current cut we are evaluating 
            set_of_current_cut_matches.append(match) #store the match
        else:
            break #otherwise no more matches to evaluate

    return set_of_current_cut_matches

def get_width_and_length_difference_of_all_matches_being_evaluated(stock_remaining, cuts_remaining, set_of_current_cut_matches):
    '''
        Function iterates over all considered matches and calculates the difference of cut and stock width and length, then returns a list sorted by width shortest to longest
    '''
    possible_stock_widths = [] #initialize empty list to store widths, difference of lengths, and stock piece
    for match in set_of_current_cut_matches: #iterate over current matches we are evaluating
        width_of_current_stock = stock_remaining[match[1]][1] #get current width
        length_diff = stock_remaining[match[1]][0] - cuts_remaining[match[0]][0] #get length diff
        possible_stock_widths.append([width_of_current_stock, length_diff, match[0], match[1]]) #store in shape [width, difference of length, cut, stock]
    
    possible_stock_widths = sorted(possible_stock_widths)
    return possible_stock_widths

def recursive_greedy_cut_solver(cuts_remaining, stock_remaining, completed_cuts, kerf, depth=0):
    '''
        Recursive function that implements a greedy algorithm to find the most optimal way way perform all of the cuts in cuts_remaining by having a ranking system that primarily checks for cuts that only match to one possible stock (single matching).
        If no such single matching exists, the algorithm checks for cuts with multiple matchings and implements a priority system for determining the best cut to make by first looking to boards that have been cut once already > boards that are the closest width
        to our cut width > boards with the least leftover length.
        Returns three lists: completed cuts, leftover stock, and any incomplete remaining cuts to make
    '''

    cuts_remaining = sorted(cuts_remaining, reverse=True) #reverse the cuts remaining from largest to smallest
    possible_matchings = find_possible_matching(cuts_remaining, stock_remaining)

    if(len(cuts_remaining) == 0 or len(stock_remaining) == 0 or not possible_matchings): #base case, where either no cuts or no stock remain or no matches possible
        return completed_cuts, stock_remaining, cuts_remaining
    
    indicies_for_removal, single_matchings = find_single_matching_cuts(possible_matchings)

    #remove indicies of single matching from multiple
    if(indicies_for_removal):
        multiple_matchings = remove_indicies(indicies_for_removal, possible_matchings)
    else:
        multiple_matchings = possible_matchings #no single matching exists

    #checking if there are single matchings and performing cut
    if single_matchings:
        for match in single_matchings: 
            current_cut = match[0] 
            required_stock = match[1]
            completed_cuts, stock_remaining = cut_stock_to_size(current_cut, cuts_remaining, required_stock, stock_remaining, kerf, completed_cuts) 
        cuts_remaining = remove_completed_from_remaining_cuts(completed_cuts, cuts_remaining)
   
   #no single matchings - move on to multiple
    else: 
        #get list of matches that are the same cut as first index in multiple matchings
        set_of_current_cut_matches = get_list_of_multiple_matches_to_evaluate(multiple_matchings) 
        
        match_priority = find_matches_to_already_cut_stock(set_of_current_cut_matches, stock_remaining)

        if(match_priority):
            set_of_current_cut_matches = match_priority

        possible_stock_widths = get_width_and_length_difference_of_all_matches_being_evaluated(stock_remaining, cuts_remaining, set_of_current_cut_matches)
        smallest_width = possible_stock_widths[0][0]

        #check in possible_stock_widths if there are multiple stocks with the smallest width
        tie_count = 0
        ties = []
        ties.append(possible_stock_widths[0])
        for i in range (len(possible_stock_widths)):
            if(possible_stock_widths[i][0] <= smallest_width and i > 0):
                tie_count += 1 
                ties.append(possible_stock_widths[i])
        
        #multiple stocks with same smallest width - check for minimum leftover length
        if(tie_count > 0):
            min_length_of_ties = float('inf')
            best_stock = None
            for tie in ties:
                if tie[1] < min_length_of_ties:
                    best_stock = tie
            
            #perform cut operation for best stock
            current_cut = best_stock[2]
            required_stock = best_stock[3]

            completed_cuts, stock_remaining = cut_stock_to_size(current_cut, cuts_remaining, required_stock, stock_remaining, kerf, completed_cuts)
            cuts_remaining = remove_completed_from_remaining_cuts(completed_cuts, cuts_remaining) #remove completed cuts from cuts remaining

        #smallest width found
        else:
            #perform cut operation for current board
            current_cut = possible_stock_widths[0][2]
            required_stock = possible_stock_widths[0][3]

            completed_cuts, stock_remaining = cut_stock_to_size(current_cut, cuts_remaining, required_stock, stock_remaining, kerf, completed_cuts)
            cuts_remaining = remove_completed_from_remaining_cuts(completed_cuts, cuts_remaining) #remove completed cuts from cuts remaining
             
    depth += 1
    return recursive_greedy_cut_solver(cuts_remaining, stock_remaining, completed_cuts, kerf, depth)

print("Starting Cuts: ", cuts)
print("Starting Stocks: ", stocks)

my_finished_cuts, leftover_stock, cuts_remaining = recursive_greedy_cut_solver(cuts, stocks, [], kerf)

print()

print(" after recursive function completes")

print("finished: ", my_finished_cuts)
print("leftover stock: ", leftover_stock)
print("cuts to be completed: ", cuts_remaining)