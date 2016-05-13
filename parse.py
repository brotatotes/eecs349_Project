import csv, collections

# Note: nominal data are integers while numeric data consists of floats
def parse(filename):
    '''
    takes a filename and returns attribute information and all the data in array of arrays
    This function also rotates the data so that the 0 index is the winner attribute, and returns
    corresponding attribute metadata
    '''
    # initialize variables
    array = []
    file = open(filename, "r")
    file.readline()
    for i in range(0, 5800):
        line = file.readline()
        if " / " in line:
            line = line.split(" / ")
            line[1] = line[1][0:-1]
            array.extend(line)
        else:
            array.append(line[0:-1])
    return array




    # skip first line of data
    # iterate through rows of actual data
