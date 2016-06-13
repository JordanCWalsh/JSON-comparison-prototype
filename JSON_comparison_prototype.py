'''
Started on May 24, 2016
@author: Jordan C Walsh
project repo:  https://github.com/JordanCWalsh/JSON-comparison-prototype

This prototype is designed to:
1. download fresh json data from a URL, into an OrderedDict object
2. _if_ an old json fil is present, load stale json data from '.hcl' file 
3. _else if_ old file does not exist, new json will be saved as the old json file (for next comparison run)
4. contrast json data in step 1 to json data in step 2
5. save any changes to csv file
6. save new json over old json 'hcl' file
7. catch a few common errors


...my file-nameing convention (MUST name files this way)
...STALE json file = 'json_old.hcl'   
----------------------------------
!!! _PLEASE NOTE_ !!!  
each time you run this script you
will OVERWRITE the 'json_old.hcl'
file PERMANENTLY, no undo here :)
----------------------------------

FUTURE FEATURES:
i)     add in 'output to xml file'
ii)    add in 'OPTIONAL output to new generated tweet, populated tweet after use signs in (Twitter API)'
iii)   look for deeper differences, such as anything changed inside each object's nested dictionaries
'''
# imports
import os, sys, time, glob, json, urllib.request, copy, csv, argparse
from collections import OrderedDict
from datetime import datetime
from deepdiff import DeepDiff
from urllib.error import URLError

#-- argparse function for command line --#
def get_args():
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Script prints csv of new supported hardware for VMware product')
    parser.add_argument(
        '-o', '--oldPath', type=str, help='OldPath file', required=False)
    parser.add_argument(
        '-u', '--urlAddress', type=str, help='UrlAddress json', required=False)
    parser.add_argument(
        '-c', '--CSVpath', type=str, help='CSVpath file', required=False)
    parser.add_argument(
        '-l', '--consoleLog', type=str, help='ConsoleLog log', required=False)
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    oldHCLpath = args.oldPath
    updatesUrl = args.urlAddress
    csvpath = args.CSVpath
    consolelog = args.consoleLog
    # Return all variable values
    return oldHCLpath, updatesUrl, csvpath, consolelog

try:
    # match argparse return values to variables
    oldpath, url, pathToCSV, logsPath = get_args()
    
    
    # strings we need from our JSON object to be searched
    PARENT_KEY = "data"         
    CHILD_KEY_0 = "controller"  
    CHILD_KEY_1 = "hdd"         
    CHILD_KEY_2 = "ssd"         
    TARGET_KEY_A = "id"         # target keys should be present in all objects of the 'child_key_# : value-array'
    
    # count of child keys for loops
    CHILD_LIST = [CHILD_KEY_0, CHILD_KEY_1, CHILD_KEY_2]
    CHILD_COUNT = len(CHILD_LIST)
    
    #url string and file path syntax (a Python headache)
    if(url==None): 
        url = "http://partnerweb.vmware.com/service/vsan/all.json"
    
    # windows specific file paths
    if(oldpath==None): 
        oldpath = 'C:\\Users\\jrdnc\\workspace\\testingPrototypes_2016_summerInternship\\'+'json_old.hcl'
    if(pathToCSV==None): 
        pathToCSV = 'C:\\Users\\jrdnc\\workspace\\testingPrototypes_2016_summerInternship\\'+'JSON_comparison_Output_Beta_1.0.2.csv'
    if(logsPath==None): 
        logsPath = 'C:\\Users\\jrdnc\\workspace\\testingPrototypes_2016_summerInternship\\'+'logs.txt'
    oldjsonfilepath = glob.glob(oldpath)
    
    
    #calendar time-stamp
    formatedTimestamp = datetime.utcfromtimestamp(time.time())
    #print to log
    logFile = open(logsPath, 'w')
    logFile.write(str(sys.version)+'\n')
    logFile.write(str(time.time())+'\n')
    logFile.write("UTC time-stamp = " + str(formatedTimestamp)+'\n' )
    #print to console
    print(sys.version)
    print(time.time())
    print("UTC time-stamp = " + str(formatedTimestamp) )
    #csvTimestampRow = ["UTC time at :", str(formatedTimestamp) ]


    # download fresh JSON
    urlresponse = urllib.request.urlopen(url).read().decode('UTF-8')
    todaysJSON = json.loads(urlresponse, object_pairs_hook=OrderedDict)

    # check for valid ols hcl file
    if ( os.path.isfile(oldpath) ):
        
        #load old file into OrderedDict
        with open(oldjsonfilepath[0]) as json_file:
            staleJSON = json.load( json_file, object_pairs_hook=OrderedDict)
    
            #pull all id-VALUES into a list, one for today, another for stale    
            todaysIDlist = []       #int arrays for id's
            staleIDlist = []
            
            childArrayIndex = 0     #in all.json.. 0->controller, 1->hdd, 2->ssd
            objIndex = 0            #this will be index of object in each above list
            
            # build todays id list
            while( childArrayIndex != CHILD_COUNT ):    
                for jsonObject in todaysJSON[PARENT_KEY][CHILD_LIST[childArrayIndex]]:
                    todaysIDlist.append(jsonObject[TARGET_KEY_A])
                childArrayIndex += 1
            
            childArrayIndex = 0     # reset indices
            objIndex = 0            
            
            # build stale id list
            while( childArrayIndex != CHILD_COUNT ):    
                for jsonObject in staleJSON[PARENT_KEY][CHILD_LIST[childArrayIndex]]:
                    staleIDlist.append(jsonObject[TARGET_KEY_A])   
                childArrayIndex += 1
            
            #-- GET NEWLY ADDED ID's IN TODAYS LIST --# 
            todaysIDlist.sort()
            staleIDlist.sort()
            
            changes = DeepDiff(staleIDlist, todaysIDlist)
            #print(json.dumps(changes, indent=2))
            #logFile.write("DeepDiff changes found:\n"+str(json.dumps(changes, indent=2)))
            
            if( len(changes)<1 ):
                logFile.write("sys.exit... no new json data at that url yet, check back later.\n")
                sys.exit("no new json data at that url yet, check back later.")
                
            
            listOfNewIDs = copy.deepcopy( list( changes["iterable_item_added"].values() ) )
            listOfNewIDs.sort()
            print(listOfNewIDs)
            logFile.write("list of new IDs found:\n"+str(listOfNewIDs)+"\n")
            
            #close old json file from above
            json_file.close()
        
        #---- print new id's object to a csv file ----#
        childArrayIndex = 0             # reset indices
        count = 0
        allNewValuesList = []           # a list of 'KVpairList' objects to print to csv from
        KVpairList = OrderedDict([])    # temp list of [key,value] objects for each new device printed to csv files
        keysListMaster = []             # master keys list to be headers for all columns in csv files
        keysList = []                   # temp keys list to compare
        
        with open(pathToCSV, 'w', newline='') as outputfile:
            outputWriter = csv.writer(outputfile)
            
            # initialize keys list to first set of keys 
            keysListMaster = list(todaysJSON[PARENT_KEY][CHILD_LIST[0]][0].keys())
            
            #---- find and record only new objects ----#
            while( childArrayIndex != CHILD_COUNT ):
                for jsonObject in todaysJSON[PARENT_KEY][CHILD_LIST[childArrayIndex]]:
                    if( jsonObject[TARGET_KEY_A]  in  listOfNewIDs ):
                        
                        #-- save all object data --#
                        KVpairList = OrderedDict(jsonObject.items())
                        
                        #-- save keys to a list to compare to master --#
                        for k,v in jsonObject.items():
                            #KVpairList
                            keysList.append(k)
                        
                        #-- update master key list if new list is longer --#
                        if( len(keysList) > len(keysListMaster) ):
                            del keysListMaster[:]
                            keysListMaster += keysList
                             
                        #-- add each new values list to an 'allNewValuesList' to print to csv after looping --#
                        allNewValuesList.append(KVpairList.copy())
                        
                        #-- erase values list to reuse in looping statement --#
                        del KVpairList
                        KVpairList = OrderedDict([])
                        del keysList[:]
    
                childArrayIndex += 1
                
            #---- print to csv file ----#
            # column headers
            outputWriter.writerow( keysListMaster ) #-- row 1 in csv sheet --#
            
            # values in matching columns
            csvrow = ['n/a']*(len(keysListMaster))  # temp to build each row of csv output according to headers list 
            klmIndex = 0                            # key list master index int for csv print loops
            csvNewRowsCount = 0                     # count of csv rows (other that col headers) printed to check successful printing
            
            #DevNotes# allNewValuesList[current object made of 'k,v' lists [current KV tuple in this list object]]
            for newDevice in allNewValuesList:         #-- rows 2 thru end of csv sheet --#
                for key in newDevice.keys():
                    header = key
                    value = newDevice[key]
                    if( str(header) in keysListMaster ):        # append values for matching headers
                        klmIndex = keysListMaster.index(str(header))
                        csvrow[klmIndex] = value
                    else: 
                        print("no match _ object's key was not in list of column headers")
                        logFile.write("while printing new csv rows, encouterned following error...\n"
                                      +"no match _ object's key was not in list of column headers\n")
                    
                # now print this device's csvrow to the csv file
                if(len(csvrow) > 0):
                    outputWriter.writerow(csvrow)
                    csvNewRowsCount += 1
                else:
                    print("error in adding values to the csvrow list")
                    logFile.write("while printing new csv rows, encouterned following error...\n"+
                                  "error in adding values to the csvrow list before printing \n")
                    
                del csvrow[:]   # reset csvrow for next device
                csvrow = ['n/a']*(len(keysListMaster)) # re-populate temp list with 'n/a' strings
                klmIndex = 0    # reset index for next device
                
            
            #-- upon csv print success, replace old_json.hcl data with new json from url --#
            print("new device csv rows printed: "+str(csvNewRowsCount))
            print("new device list length: "+str(len(allNewValuesList)))
            logFile.write("new device csv rows printed: "+str(csvNewRowsCount)+"\n")
            logFile.write("new device list length: "+str(len(allNewValuesList))+"\n")
            
            # check for success
            if( csvNewRowsCount == len(allNewValuesList) ):
                print("these numbers matched, successful csv printed!")
                logFile.write("these numbers matched, successful csv printed!\n")
                with open(oldpath, 'w') as replacingOldHCL:
                    json.dump(todaysJSON, replacingOldHCL, ensure_ascii=False)
                    replacingOldHCL.close()
                print("old json has been overwritten with newest json for next comparison.")
                logFile.write("old json has been overwritten with newest json for next comparison.\n")
            # print error msg if unsuccessful 
            else:
                print("these numbers must match for successful printing...")
                print("there was an error in the 'print to csv file' section of the program.")
                logFile.write("these numbers must match for successful printing...\n")
                logFile.write("there was an error in the 'print to csv file' section of the program.\n")
                
            # close csv file when no longer needed
            outputfile.close()
    
    # else for if hcl file is not found  
    # save todays as the 'old_json.hcl' to use as comparison tmrw      
    else:
        print("file >json_old.hcl< does not exist at specified path, nothing to compare")
        print("creating a new hcl file ..\\json_old.hcl.. with new json from the given url")
        logFile.write("file >json_old.hcl< does not exist at specified path, nothing to compare\n")
        logFile.write("creating a new hcl file ..\\json_old.hcl.. with new json from the given url\n")
        
        with open(oldpath, 'w') as newHCLfile:
            json.dump(todaysJSON, newHCLfile, ensure_ascii=False)
        newHCLfile.close()
        
    
# exceptions for common errors
except URLError:
    print(str(URLError) + "... HCL DIFF operation ended. Check URL string for correctness.")
    logFile.write(str(URLError) + "... HCL DIFF operation ended. Check URL string for correctness.\n")
except PermissionError:
    print(str(PermissionError) + "... Make sure csv file is closed, and that you have access to it on your system.")
    logFile.write(str(PermissionError) + "... Make sure csv file is closed, and that you have access to it on your system.\n")
    
#close the log file
logFile.close()

