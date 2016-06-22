# JSON-comparison-prototype
Internship Project: JSON comparison prograon in Python 3, still in development stage, not set up for public use yet

<!-- ![Downloads](https://img.shields.io/pypi/dm/deepdiff.svg?style=flat) -->
![Python Versions](https://img.shields.io/badge/Python-3.2%2C%203.3%2C%203.4%2C%203.5-brightgreen.svg?style=flat)
![DeepDiff](https://img.shields.io/badge/DeepDiff-1.2.0-blue.svg?style=flat)

##Use Cases
###This Prototype is designed to:
1. use parameters set by command-line arguments OR default to variables initialized in the code
2. download fresh json data from a URL into an OrderedDict object
3. _if_ an old json fil is present, load yesterday's json data from '.hcl' file 
4. _else if_ old file does not exist, new json will be saved as the old json file (for next time you run the script)
5. contrast json data in step 1 to json data in step 2
6. print the list of newly added hardware to csv file
7. save new json over old json 'hcl' file
8. catch a few common errors

!!! _PLEASE NOTE_ !!!  
each time you run this script you will OVERWRITE the 'json_old.hcl' file PERMANENTLY, no undo here :)

##Command Line Arguments
###Calling the script with Required args
```
$ python JSON_comparison_prototype.py -oldPath OLDFILEPATH -urlAddress URLofJSON -csvpath CSVFILEPATH
```
###Required args and Optional args explained
```python
#Required
'-o' or '--oldPath'     #type string, goes first in command line call
'-u' or '--urlAddress'  #type string, goes second in command line call
'-c' or '--CSVpath'     #type string, goes third in command line call

#Optional
'-l' or '--consoleLog'  #file path where logs.txt will output if desired, 
                        #type string, goes fourth in command line call
```

##Changelog

- v Beta-1-0-2: Initial commit for development testing and user feedback

##Author
Jordan C Walsh

- Github:  <https://github.com/jordancwalsh>
- Linkedin:  <http://www.linkedin.com/in/jordancwalshsoftwaredeveloper>
- Twitter:   <https://twitter.com/jcwsoftwaredev>
