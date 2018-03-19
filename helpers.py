def dictionarize(cursor):
    """ converts sqlite3 cursor query output to python dictionary format """

    # extract field names and nr of solution
    ncols = len(cursor.description)
    colnames = [cursor.description[i][0] for i in range(ncols)]
    results = []



    # convert to dictionary
    row = cursor.fetchall()

    for element in row:

        res = {}
        for i in range(ncols):
            res[colnames[i]] = element[i]

        results.append(res)

    return results
