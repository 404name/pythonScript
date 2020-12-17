def ReadTxtName(rootdir):
    lines = []
    with open(rootdir, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)
    return lines

list_data = ReadTxtName("C:\\Users\\404name\\Desktop\\oj.txt")

file=open('data.txt','w') 
file.write(str(list_data))
file.close() 
