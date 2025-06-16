stocks = {0 : {'length': 96, 
               'width': 5, 
               'height': 1.5, 
               }, 
          1 : {'length': 96,
               'width': 3.5,
               'height': 1.5,
               }
        }
cuts = {0 : {'length': 24, 
            'width': 4.5, 
            'height': 1.5, 
            }, 
        1 : {'length': 72,
            'width': 3,
            'height': 1.5,
            },
        2 : {'length': 48, 
            'width': 4, 
            'height': 1.5, 
            }, 
        3 : {'length': 12,
            'width': 3.5,
            'height': 1.5,
            }
    }

def get_kerf_input_from_user():
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
        return kerf
    
#cuts = [[24, 4.5, 1.5], [72, 3, 1.5], [48, 4, 1.5], [12, 3.5, 1.5]]

class Stock_Wood:
    _stock_id = 0

    def __init__(self, length, width, height):
        self.id = Stock_Wood._stock_id
        Stock_Wood._stock_id += 1

        self.length = length
        self.width = width
        self.height = height 
        self.is_original_stock = True
        self.parent_stock_index = None
        self.cuts_made_from_this_stock = {}

    def check_if_required_cut_fits_stock(self, cut):
        if(cut.length <= self.length and cut.width <= self.width and cut.height <= self.height):
            return (cut, self)
        else:
            return (False, False)
        
    def cut_stock_to_size(self, cut):
        '''
            Function takes two arguments self, cut and shortens the length of self stock. Also checks if the
            width of the cut is less than that of the stock. If so, we cut away from the width and create a new stock wood
            object using the cutoff piece. 
        '''
        self.length -= (cut.length + KERF)
        self.is_original_stock = False
        self.cuts_made_from_this_stock[cut.id] = cut
        cutoff_piece = None
        
        if(cut.width < self.width):
            remaining_width = self.width - (cut.width + KERF)
            cutoff_piece = Stock_Wood(cut.length, remaining_width, self.height)

        return cutoff_piece
    
class Desired_Cut:
    _cut_id = 0
    def __init__(self, length, width, height):
        self.id = Desired_Cut._cut_id
        Desired_Cut._cut_id += 1

        self.length = length
        self.width = width
        self.height = height
        self.is_completed_cut = False
        self.no_possible_matching = False

class Cut_Optimizer:
    def __init__(self, cuts, stocks):
        self.cuts = cuts
        self.stocks = stocks
        self.matches = {}
        self.single_matching = {}
        self.multiple_matching = {}
        self.completed_cuts = {}
        self.depth = 0
        
    def find_all_possible_matchings(self):
        match_count = 0
        for stock in self.stocks.values():
            for cut in self.cuts.values():
                matching_pair = stock.check_if_required_cut_fits_stock(cut)
                if(False not in matching_pair):
                    self.matches[match_count] = [cut.id, stock.id]
                    match_count += 1

        self.check_for_unmatchable_cuts()
        return self.matches

    def check_for_unmatchable_cuts(self):
        matched_value_ids = [match[0] for match in self.matches.values()] #comprehension to get id of each cut in matching

        for cut in self.cuts.values():
            if(cut.id not in matched_value_ids):
                cut.no_possible_matching = True

    def seperate_single_and_multiple_matching_cuts(self):
        for key, value in self.matches.items():
            match_counter = 0
            for item in self.matches.values():
                if item[0] == value[0]:
                    match_counter += 1

            if match_counter == 1:
                self.single_matching[key] = value
            else:
                self.multiple_matching[key] = value
    
    def find_matches_to_already_cut_stock(self):
        priority_matching = {}
        
        for key, match in self.matches.items():
            if(self.stocks[match[1]].is_original_stock == False):
                priority_matching[key] = match
        
        return priority_matching
    
    def recursive_cut_solver(self):
        
        self.matches = self.find_all_possible_matchings()
        
        print(self.matches)

        if(len(self.cuts) == 0 or len(self.stocks) == 0 or not self.matches):
            return self.completed_cuts, self.stocks, self.cuts
            
        self.seperate_single_and_multiple_matching_cuts()
        
        if self.single_matching:
            print("single matchhing:", self.single_matching)
            for key, matching in self.single_matching.items():
                print(self.stocks[matching[1]].length)
                cutoff = self.stocks[matching[1]].cut_stock_to_size(self.cuts[matching[0]])
                self.stocks[cutoff.id] = cutoff
                self.cuts.is_completed_cut = True
                self.matches.pop(key)
        else:
            matchings_to_cut_stocks = self.find_matches_to_already_cut_stock()
            print(matchings_to_cut_stocks)
                
            #find matches that match to already cut stocks
            #check if match priority - if yes then use this set of matches
            #calculate widths and length differences then take the smallest width if no ties - cut
            #otherwise if there are multiple minimum widths, then go to minimum length
        fart = input()
        self.depth += 1
        #clean up cuts after making them
        self.recursive_cut_solver()
            

def initialize_and_store_objects_from_dictionary(dict, class_to_call):
    object_storage = {}
    for key, item in dict.items():
        object_storage[key] = class_to_call(item['length'], item['width'], item['height'])
    return object_storage


if __name__ == "__main__":
    KERF = get_kerf_input_from_user()

    stock_objects = initialize_and_store_objects_from_dictionary(stocks, Stock_Wood)
    cut_objects = initialize_and_store_objects_from_dictionary(cuts, Desired_Cut)

    
    cut_optimizer = Cut_Optimizer(cut_objects, stock_objects)
    #call recursive function here
    completed_cut_list, remaining_stock_after_cuts, incomplete_cuts = cut_optimizer.recursive_cut_solver()
    
