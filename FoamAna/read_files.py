def key_lines(lines, keys):
    for line in lines:
        if "Time = " in line and not "s" in line:
            yield 'time', line
        for key, key_w in keys.iteritems():
            if key_w in line:
                yield key, line


def find_start_of_log(log):
    for i, line in enumerate(log):
        if "Time = " in line and not "s" in line:
            return i


def extractFromLog(keys, path, logString):
    '''
        A function using grep to search for a string (ss) in a logfile

        Using regexep to extract only numbers
        converts to  floats and returns the data
    '''
    logs = get_ipython().getoutput("ls {0}{1}".format(path, logString))
    logInd = []
    old_it = 0
    df0 = DataFrame()
    for log_number, log_name in enumerate(logs):
        dataDict = defaultdict(list)
        try:
            with open(log_name) as log:
                f = log.readlines()
                start = find_start_of_log(f)
                for key, line in key_lines(f[start:-1], keys):
                    readAndCleanLinesDict(line, dataDict, key)
            print "finished log file {} of {} ".format(log_number+1, len(logs))

            for key, value in dataDict.iteritems():
                cur_it = old_it + len(value)
                dataDict[key] = Series(value, index=range(old_it, cur_it))

            df = DataFrame(dataDict)
            df['log'] = log_number
            df2 = DataFrame(df.describe())
            inner = int(max(df2.ix['count']))
            tot = inner + old_it
            logInd = logInd + [log_number] * inner
            df0 = df0.combine_first(df)
            old_it = tot
        except:
            pass
    return df0


def readAndCleanLinesDict(line, dic, key):
    '''
        Takes a string splits it and converts it to a number

    '''
    conv = []
    line = line.replace(',', '')             # move to caller
    for i, elem in enumerate(line.split()):
        try:
            conv.append(np.float32(elem))
        except:
            pass
    for i, elem in enumerate(conv):
        dic[key + str(i)].append(elem)


def begins_with_int(line):
    try:
        int(line)
        return True, int(line)
    except:
        return False, 0


def if_header_skip(content):
    first_line = content[0]
    if '#' in first_line:
        return 1,-2
    if '/*-' in first_line:
        for line_number, line in enumerate(content):
            is_int, entries = begins_with_int(line)
            if is_int:
                return line_number + 2, entries
    else:
        return 0, -1
