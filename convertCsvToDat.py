#!/usr/bin/env python3
# e.g.
# $ ./convertCsvToDat.py ./23-06-hack-yuma_20230702T224137-0700.csv > 23-06-hack-yuma_20230702T224137-0700.dat
#
# input data example:
# "Record number","Date and time","Number1","Number2","Date"
# "18358","09/05/2023 05:52","2388.45","","2023-09-05-05-52-21"
# "18357","09/05/2023 05:51","2388.54","","2023-09-05-05-51-18"
#

import sys, re, csv, pprint
import datetime

csvFile = sys.argv[1]

minOfData = 1550
maxOfData = 2450

with open(csvFile) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0].isdecimal() != True:
            continue
        dataCSV = re.split('/|\s+|:', row[1])
        # ['07', '02', '2023', '21', '36']
        dataDate = datetime.datetime(int(dataCSV[2]), int(dataCSV[0]), int(dataCSV[1]),
                                     int(dataCSV[3]), int(dataCSV[4]))
        dataEpoch = dataDate.timestamp()
        if float(row[2]) >=  minOfData and float(row[2]) <= maxOfData:
            print(str(dataEpoch) + " " + row[2])

