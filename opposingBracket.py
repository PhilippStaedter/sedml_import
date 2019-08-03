# function to fin the index of correct closing bracket

from collections import deque


def getIndex(string, start_index):

    # If input is invalid.
    if string[start_index] != '(':
        return -1

    # Create a deque to use it as a stack.
    d = deque()

    # Traverse through all elements
    # starting from i.
    for iElement in range(start_index, len(string)):

        # Pop a starting bracket
        # for every closing bracket
        if string[iElement] == ')':
            d.popleft()

        # Push all starting brackets
        elif string[iElement] == '(':
            d.append(string[start_index])

        # If deque becomes empty
        if not d:
            return iElement

    return iElement
