from xlrd import open_workbook
from os import listdir
from os.path import isfile, join
from os import walk
import pandas
from pandas import ExcelWriter
from pandas import ExcelFile
#Pillow
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import time
from statistics import mean

dataFiles = []

def navDirectories (directory = "C:\\"):
    nad = 0
    type = 0
    prevDir = []
    prevDir.extend([directory])
    files = []
    while nad == 0:
        f = []
        h = []
        if directory == "C:\\":
            run = 0
        else:
            run = 1

        if type == 0:
            curDir = "\nCurrent Directory: \'" + directory + "\'"
            print (curDir)
            print ("Directories:")
            for (dirpath, dirnames, filenames) in walk(directory):
                f.extend(dirnames)
                break
        else:
            print ("Files:")
            for (dirpath, dirnames, filenames) in walk(directory):
                f.extend(filenames)
                break
        i = 1
        for file in f:
            print ("%(first)d : " % {"first": i} + file )
            i += 1

        #Gives option to backtrack through Directories
        if run > 0:
            if (len(prevDir) > 0):
                if (directory == prevDir[len(prevDir) - 1]):
                    print("\nPress '0' to return to \'" + prevDir[len(prevDir) - 2] + "\'")
                else:
                    print("\nPress '0' to return to \'" + prevDir[len(prevDir) - 1] + "\'")

        if type == 1:
            nad = 1
            continue

        a = input("\nSelect a Directory %(1st)d-%(2nd)d (or type 'f' to show files): " % {"1st": 1, "2nd": i-1})

        if run == 0:
            a = checkInput(a, 1, i - 1)
        else:
            a = checkInput(a, 0, i - 1)

        if (isInt(a)):
            a -= 1

        if (a == -1):

            #TODO this fails when directory != "C:\\"
            if directory == prevDir[len(prevDir) - 1]:
                del prevDir[-1]
            directory = prevDir[len(prevDir) - 1]
            continue
        elif (a == 'f'):
                f = navFiles(directory)
                if len(f) == 0:
                    print("There are no files in this directory.")
                    continue
                elif 'y' == input("Would you like to select a file(s)? "):
                    dataFiles.append(directory)
                    files = input("Input file #'s separated by commas NO SPACES (Example: 1,2,3,4,5): ")
                    # TODO Write a check-input for this
                    fileIndexs = files.split(",")
                    w = 0
                    for st in fileIndexs:
                        st = int(st)
                        dataFiles.append(f[st - 1])
                        w += 1
                    break
                else:
                    d = input("Would you like to start over?: ")
                    if(d == 'y'):
                        continue
                    else:
                        break
        if(len(prevDir) > 0):
            if directory == prevDir[len(prevDir) - 1] and run != 0:
                del prevDir[-1]
            else:
               prevDir.extend([directory]);
        else:
            prevDir.extend([directory]);
        directory += str(f[a]) + "\\"
    return;
def navFiles (directory = "C:\\"):

    h = []
    if directory == "C:\\":
        run = 1
    else:
        run = 0


    print("\nCurrent Directory: \'" + directory + "\'")
    for (dirpath, dirnames, filenames) in walk(directory):
        print('Files in directory: %s' % dirnames)
        h = filenames
        break
    i = 1
    print(len(h))
    for file in h:
        print("%(first)d : " % {"first": i} + file)
        i += 1
    return h;

def checkInput (num, param1, param2):
    newNum = num
    nad = 0
    while (nad < 10):
        if (isInt(newNum)):
            newNum = int(newNum)
            if (newNum < param1 or newNum > param2):
                print ("Index \"%d\" is out of Bounds" % newNum)

            else:
                return newNum
        elif (newNum == 'f'):
            return newNum
        else:
            print("Input \"" + str(newNum) + "\" is not a number and is not 'f'.")
        newNum = input("Please re-input a number between %(1st)d and %(2nd)d: " % {"1st": param1, "2nd": param2})
        nad += 1


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def checkFiles (fils):
    NA = ' ';

    skip = 0
    for fil in fils:
        if (skip == 0):
            skip += 1;
            continue;
        if (fil.rpartition('.')[-1] == "xlsx" and NA != 'i'):
            NA = 'x';
            continue;
        else:
            NA = 'n';
        if((fil.rpartition('.')[-1] == "jpg" or fil.rpartition('.')[-1]
                 == "png" or fil.rpartition('.')[-1] == "tif") and NA != 'x'):
            NA = 'i';
        else:
            NA = 'n';
            continue;
    return NA;

def readImage(imgs):
    num = 1;
    iar = []
    fig = plt.figure()
    ax = []
    ax.append(plt.subplot2grid((8, 6), (0, 0), rowspan=4, colspan=3))
    ax.append(plt.subplot2grid((8, 6), (4, 0), rowspan=4, colspan=3))
    for img in imgs:
        i = Image.open(img)
        iar.append(np.asarray(i))
        #iar.append(threshold(np.asarray(i)))

    axI = 0
    for iA in iar:
        ax[axI].imshow(iA)
        print("\nImage %d:" % num)
        print(iA)
        num += 1;
        axI += 1
    plt.show()

def threshold(imageArray):
    balanceAr = []
    newAr = []
    newAr = imageArray

    wtf = 1

    #Finding the average color for the image
    for row in imageArray:
        cnt = 0
        pix = []
        for pixel in row:
            if (cnt < 3):
                pix.append(pixel)
                cnt += 1;
            else:
                avgNum = mean(pix[:3])
                balanceAr.append(avgNum)
                cnt = 0
                pix = []
    balance = mean(balanceAr)

    #Using average color to make the image black/white
    for eachRow in newAr:
        cnt = 0
        permaCnt = 0
        pix = []
        for eachPix in eachRow:
            if (cnt < 3):
                pix.append(pixel)
                cnt += 1;
            else:
                if mean(pix[:3]) > balance:
                    eachRow[permaCnt - 3] = 255
                    eachRow[permaCnt - 2] = 255
                    eachRow[permaCnt - 1] = 255
                else:
                    eachRow[permaCnt - 3] = 0
                    eachRow[permaCnt - 2] = 0
                    eachRow[permaCnt - 1] = 0
                cnt = 0
                pix = []
            permaCnt += 1
    return newAr

def breakImage(imgs):
    num = 1;
    iar = []
    iarBroke = []
    fig = plt.figure()
    ax = []
    ax.append(plt.subplot2grid((2048, 2048), (0, 0), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (512, 0), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (1024, 0), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (1536, 0), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (0, 512), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (512, 512), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (1024, 512), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (1536, 512), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (0, 1024), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (512, 1024), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (1024, 1024), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (1536, 1024), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (0, 1536), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (512, 1536), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (1024, 1536), rowspan=512, colspan=512))
    ax.append(plt.subplot2grid((2048, 2048), (1536, 1536), rowspan=512, colspan=512))
    for img in imgs:
        i = Image.open(img)
        iar.append(np.asarray(i))
    nrows = 512
    ncols = 512
    for ar in iar:
        h, w = ar.shape
        iarBroke.append(ar.reshape(h // nrows, nrows, -1, ncols).swapaxes(1, 2).reshape(-1, nrows, ncols))

    axI = 0
    for iA in iarBroke:
        ax[axI].imshow(iA)
        print("\nImage %d:" % num)
        print(iA)
        num += 1;
        axI += 1
    plt.show()

##############################################################

navDirectories(directory="C:\\")
xl = []
#  TODO write something to filter out non-'.xlsx' file formats
fil = checkFiles(dataFiles);
strg = [];
for file in dataFiles:
    if (dataFiles[0] != file):
        if (fil == 'x'):
            sts = dataFiles[0] + file
            xl.append(pandas.read_excel(sts))
        elif  (fil == 'i'):
            strg.append(dataFiles[0] + file)
        else:
            print ("\nInvalid File type(s).\n")

if(fil == 'x'):
    o = 1
    for xll in xl:
        print("\n" + dataFiles[o].rpartition('\\')[2] + "\nHead: ")
        print(xll.head())
        o += 1
elif(fil == 'i'):
    readImage(strg)
   # breakImage(strg)