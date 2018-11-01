import os

def getFolderSize(folder):
    print "*****RESULT: File Path: " + getFolderContentSize(folder,0)

def getFolderContentSize(folder, max_size):
    global max_size_total
    global result
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        print("so far max size total is =" + str(max_size_total) + " before checking file path "+itempath)
        if os.path.isfile(itempath):
            file_size=os.path.getsize(itempath)
            print("path ="+itempath+" file_size="+str(file_size))
            if (file_size > max_size_total):
                max_size_total=file_size
                print("max size total changed to =" + str(max_size_total))
                print("this is a larger path =" + itempath + " file_size=" + str(file_size))
                result= itempath
        elif os.path.isdir(itempath):
            result=getFolderContentSize(itempath, max_size)
    return result


max_size_total=0
result=""
getFolderSize("sampleFiles")