stocks = [[96, 5, 1.5], [96, 3.5, 1.5]]
cuts = [[24, 4.5, 1.5], [72, 3, 1.5], [48, 4, 1.5], [12, 3.5, 1.5]]

while(1):
    kerf_inp = input()
    if(kerf_inp == 'thin' or kerf_inp == 'Thin'):
        kerf = 0.09375
        break
    elif(kerf_inp =='full' or kerf_inp == 'Full'):
        kerf = 0.125
        break

possible_matchings = []
cuts = sorted(cuts, reverse=True) #sort cuts largest first

for cut in cuts:
    curr_cut_len = cut[0] #cut len
    curr_cut_width = cut[1] #cut width
    
    for stock in stocks: #check each stock len + width
        if(curr_cut_len <= stock[0] and curr_cut_width <= stock[1]): #if cut len and width less than max stock len and width
            possible_matchings.append([cuts.index(cut), stocks.index(stock)])#candidate found, store it. has shape [[cut, stock],]

print(possible_matchings) #set of all cuts that match to all stocks
print()

only_possible_matching = []
index_to_remove = []

for index, item in enumerate(possible_matchings): #iterate over the enumeraton of matchings
    current_cut = item[0] #current cut
    match_counter = 0 
    for i in range(len(possible_matchings)): #iterate over all matches
        if(current_cut == possible_matchings[i][0]): #check for multiple matches
            match_counter += 1 #increment match counter
    if(match_counter == 1): #check if only a single matching
        only_possible_matching.append(item) #store to single matching list
        index_to_remove.append(index)


index_to_remove = sorted(index_to_remove, reverse=True) #reverse index list to not change position of desired deletion indicies.

for index in index_to_remove: #remove cuts with only one match from list
    del possible_matchings[index]
    
print(possible_matchings) #cuts with multiple matchings
print(only_possible_matching) #cuts that must come out of a given stock

remaining_stock = stocks.copy() #get copy of stock list
completed_cuts = []

#function takes two index arguments and a lists of lists remaining stock. subtracts cut length and kerf from the length of stock and checks if it needs to cut down width. Places leftover back into the remaining stock array. Returns the remaining stock and completed cut arrays.
def cut_stock_to_size(current_cut, required_stock, remaining_stock):
    remaining_stock[required_stock][0] -= (cuts[current_cut][0] + kerf) #reduce length of remaining stock
    
    if(cuts[current_cut][1] < remaining_stock[required_stock][1]): #checking if the width of cut needed is less than the width of the stock
        
        current_cut_len = cuts[current_cut][0] #get dimensions in easy to read format
        current_cut_width = cuts[current_cut][1]
        current_cut_height = cuts[current_cut][2]

        current_cut_width = remaining_stock[required_stock][1] - (current_cut_width + kerf) #cut down to final width by subtracting required cut width plus blade kerf from width of stock
        cut_piece = [current_cut_len, current_cut_width, current_cut_height] #remainder of stock from cutoff
        remaining_stock.append(cut_piece) #return remainder of cutoff to stock pile
        
    completed_cuts.append(cuts[current_cut]) #add completed cut to pile
    
    return completed_cuts, remaining_stock
        
for match in only_possible_matching:
    current_cut = match[0]
    required_stock = match[1]
    
    completed_cuts, remaining_stock = cut_stock_to_size(current_cut, required_stock, remaining_stock)

    
print("cuts completed:", completed_cuts)
print("remaining stock: ", remaining_stock)
    
