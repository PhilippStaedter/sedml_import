# fscript to colour a data frame elementwise based on boolean

def colour(value):
    if value == True:
        return['background-color: green' if v else '' for v in value]
    elif value == False:
        return ['background-color: red' if v else '' for v in value]