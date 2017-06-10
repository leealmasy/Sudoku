
assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
def cross(a, b):
    return [s+t for s in a for t in b]

def diag_boxes(rows,cols):
    d1 = [rows[i]+cols[i] for i in range(9)]
    d2 = [rows[i]+cols[8-i] for i in range(9)] 
    #print('diag type',type(d1))
    d3=[]
    d3.append(d1)
    d3.append(d2)
    return d3

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def update_naked_twins(values,peers,twins,box,cat):
    non_twins= [x for x in peers if x not in twins]
    #for x in twins:
    #    print('twin, value',x,values[x],cat)
    if not twins:
        return values
    #print('non-twins',non_twins)
    #display(values)
    for nt in non_twins:
        if len(values[nt])==1:
            continue
        digits = values[box]
        #print('=========>TWIN %r  value=%r'%(nt,values[nt]))
        #print('old digits',values[nt])
        new_digits = [ x for x in values[nt] if x not in digits]
        #print('new digits::',new_digits)
        new_digits_str = ''.join(str(e) for e in new_digits)                 
        #print('new-digit =',new_digits_str)
        if len(new_digits_str)>1:
            values[nt]=new_digits_str   
            #print('naked update<<<')
    return values
  
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    boxes = cross(rows, cols)
    diags1 = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']
    diags2 = ['A9','B8','C7','D6','E5','F4','G3','H2','I1']
    
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    diags = diag_boxes(rows,cols)
    
    unitCols =    dict((s,[u for u in column_units if s in u]) for s in boxes)
    unitRows =    dict((s,[u for u in row_units    if s in u]) for s in boxes)    
    unitSquares = dict((s,[u for u in square_units if s in u]) for s in boxes)
    unitsDiags = dict((s, [u for u in diags        if s in u]) for s in boxes)
 
    #PEER for individual unit categories
    peersDiags =  dict((s, set(sum(unitsDiags[s],[]))-set([s])) for s in boxes)
    peersCols =    dict((s, set(sum(unitCols[s]   ,[]))-set([s]))   for s in boxes)
    peersRows =    dict((s, set(sum(unitRows[s]   ,[]))-set([s]))   for s in boxes)
    peersSquares = dict((s, set(sum(unitSquares[s],[]))-set([s]))   for s in boxes)
    # Find all instances of naked twins
    #print('xxxxxxxxxxxxxxxxxxxxxxxxxxx TWINS IN  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  #################   in.')    
  
    set1=set(values.items())

    twinActivity =True
    while twinActivity:
        twinActivity = False
        ##print('- - - -  - - -  * * * * * * * * * * *  * ** * * *  -------------------------- - - - - - - - ')
        twoDigitBoxes = [x for x  in values if len(values[x])==2 ]


        #print('2-digit bx:',twoDigitBoxes)
        v1= values.copy()
        for box in twoDigitBoxes:  
            # COLUMN TWIN
            peersCol=[x for x in peersCols[box]]
            peers2=[x for x in peersCol if len(x)>1]
            twins_col=[x for x in peers2 if values[x] == values[box]]  
            if peers2:
                #print('col target %r=%r'%(box,values[box]))
                #display(values)
                values=update_naked_twins(values,peers2,twins_col,box,"Column")
                #twinActivity = True
            
            peersRow=[x for x in peersRows[box]]
            peers2=[x for x in peersRow if len(x)>1]
            twins_row = [x for x in peers2 if values[x]==values[box]] 
            if peers2:
                #print('row target %r=%r'%(box,values[box]))
                values=update_naked_twins(values,peers2,twins_row,box,"Row") 
                #twinActivity = True  
                
            peersSqr=[x for x in peersSquares[box]]
            peers2=[x for x in peersSqr if len(x)>1]
            twins_sqr = [x for x in peers2 if values[x]==values[box]]
            if peers2:
                #print('sqr target %r=%r'%(box,values[box]))
                values=update_naked_twins(values,peers2,twins_sqr,box,"SQUARE") 
                #twinActivity= True
                
            diag1_peers=[x for x in values if x in peersDiags[box] and x in diags1 and x != box]
            peers2=[x for x in diag1_peers if len(x)>1] 
            twins_diag1 = [x for x in peers2 if values[x]==values[box]]  
            if peers:
                #print('diag1 target %r=%r'%(box,values[box]))
                values=update_naked_twins(values,peers2,twins_diag1,box,"DIAG1")   
                #twinActivity= True
                
            diag2_peers=[x for x in values if x in peersDiags[box] and x in diags2  and x != box]
            peers2=[x for x in diag2_peers if len(x)>1]            
            twins_diag2 = [x for x in diag2_peers if values[x]==values[box]]  
            if peers2:
                #print('diag2 target %r=%r'%(box,values[box]))
                values=update_naked_twins(values,peers2,twins_diag2,box,"DIAG1")   
                #twinActivity= True  
        set1=set(v1.items())
        set2=set(values.items())
        diff=dict(set1^set2)
        if len(diff)>0:
            twinActivity = True

    return values
    # Eliminate the naked twins as possibilities for their peers



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values=naked_twins(values)
    
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
     
        #lwa insert naked twins        
        values = only_choice(values)

        #values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

diag_units = diag_boxes(rows,cols)

#print('diagonal units type ',diag_units)

unitlist = row_units + column_units + square_units + diag_units

#print(unitlist)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)




if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')



