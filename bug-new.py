import getfile
import gethtml
import getre
import _thread
import socker
#import time

tempf = open("txts/URLs.txt","at")
socker.socker("192.168.0.100",1080)
URL = str(input("Input a URL,<e.g:https://taobao.com/>"))
threadNum = int(input("Input an threadNumber:"))

f = open("ThreadNumber.txt","w+")
f.write("0")
f.close()

def minThreadNumber():
    try:
        f = open("ThreadNumber.txt","r")
        temp = int(f.read()) - 1
        f.close()
        f = open("ThreadNumber.txt","w+")
        f.write(str(temp))
        f.close()
        print(temp)
    except:
        minThreadNumber()

def addThreadNumber():
    try:
        f = open("ThreadNumber.txt","r")
        temp = int(f.read()) + 1
        f.close()
        f = open("ThreadNumber.txt","w+")
        f.write(str(temp))
        f.close()
        print(temp)
    except:
        addThreadNumber()

    #Check the URL's hash.
def checkhash(URL):
    tempasd = str(hash(URL)) #Get the hash of URL.
    for f in open("./txts/%s/%s/%s.txt" % (tempasd[0],tempasd[1],tempasd[2]),"r"):
        [mmm] = getre.get(r'(.+)\n',f)
        if str(hash(URL)) in mmm:    #Check if hash in list.
            return("non")   #If it,return an error.
    #If not:                <<\/
    hashs = open("./txts/%s/%s/%s.txt" % (tempasd[0],tempasd[1],tempasd[2]),"at")
    hashs.write("%s\n" % hash(URL))   #Write the hash into list.
    hashs.close()
#e
    hashbak = open("./txts/hash.txt","at")
    hashbak.write("%s\n" % hash(URL))    #emmmmmm... Just a temp.
    hashbak.close()
    return("ok")

def addMore(a,URL):
    temp = a.split('/')
    if URL[-1] == "/":
        a = URL
    else:
        a = URL + "/"
    for i in range(len(temp) - 1):
        a += temp[i + 1]
        if i < len(temp) - 2:
            a += "/"
    return(a)

    #Check if URL is wrong.
def checka(a,URL):
    if a == "/" or a == "#":
        return("error1")
    if a[0] == a[1] == "/":
        a = "http:"+a
    if (a[0] != "h") and (a[1] != "/" ) or (a[0] == "/") and (a[1] != "/"):
        a = addMore(a,URL)    #s	
    if a[0] == "." and a[1] == "/":
        a = addMore(a,URL)
#    print(a)
    return(a)

    #Start a new thread of a URL.
def startt(trmp,URL,threadNum):
    minThreadNumber()
    for a in trmp:
        temp = 0
        def get(temp):
            f = open("ThreadNumber.txt","r")
            try:
                temp = int(f.read())
            except:
                get(temp)
            f.close()
            return(temp)
        temp = get(temp)
        while temp >= threadNum:
            pass
        try:
            addThreadNumber()
            _thread.start_new_thread(sp,(a,URL,threadNum))   #Start a new thread.
        except:
            minThreadNumber()
            print("can't start thread: %s" % a)

    while 1:
        pass

    #Main def,get the page and get URLs.
def sp(URL,TN,threadNum):
    #Check
    a = checka(URL,TN)
    if a == "error0":
        print("Url %s is not a xxx,Exiting thread..." % URL)
        minThreadNumber()
        exit()
    if a == "error1":
        print("Url %s was scanned,Exiting thread..." % URL)
        minThreadNumber()
        exit()
    else:                                       #IF ERROR
        URL = a
    temp2 = checkhash(URL)
    if temp2 == "non":
        print("Url %s was scanned,Exiting thread..." % URL)
        minThreadNumber()
        exit()
    else:
        try:
            print("Now start thread: %s" % URL)
            one = gethtml.get(URL)    #Get the page of URL.
            two = getre.get(r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')',one.decode("utf-8"))
        except:
            print("Some error in %s,exiting,," % a)
            minThreadNumber()
            exit()
        tempf = open("txts/URLs.txt","at")
        tempf.write("%s\n" % URL)    #Temp the URL.
        tempf.close()
        startt(two,URL,threadNum)

    #Start.

sp(URL,URL,threadNum)
