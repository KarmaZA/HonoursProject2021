# File for the data evaluation
# 

"""Reads the scoring list and outputs a string of the patterns with the highest scores. 
Any pattern with a score greater than 75% of the high score is returned"""
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

"""Implements the basic scoring on the match count array. 
If the score is higher then returns the new score and true
else returns old score and false."""
def scoreMatches(match_array, current_score):
    modifier = 2000
    point_score = 0
    for x in range(6):
        point_score += match_array[x] * modifier
        modifier *=0.5
    if point_score > current_score:
        return point_score, True
    else:
        return current_score, False