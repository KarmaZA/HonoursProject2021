# File for the data evaluation
# 

def Evaluate(Patterns_list):
    max_val = max(Patterns_list)
    patterns = ''
    for x in range(6):
        if Patterns_list[x] > int(0.75 * max_val):
            if x == 0:
                patterns += ', Square'
            if x == 1:
                patterns += ', Rectangle'
            if x == 2:
                patterns += ', Triangle'
            if x == 3:
                patterns += ', Hexagonal'
            if x == 4:
                patterns += ', Quincunx'
            if x == 5:
                patterns += ', Double Hedge Row'
    
    patterns = patterns[2:]

    return patterns

def scoreMatches(match_array, current_score):
    modifier = 1000
    point_score = 0
    for x in range(6):
        point_score += match_array[x] * modifier
    if point_score > current_score:
        return point_score
    else:
        return current_score