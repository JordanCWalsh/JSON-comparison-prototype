# JSON-comparison-prototype
Internship Project: JSON comparison prograon in Python 3, still in development stage, not set up for public use yet

<!-- ![Downloads](https://img.shields.io/pypi/dm/deepdiff.svg?style=flat) -->
![Python Versions](https://img.shields.io/badge/Python-3.2%2C%203.3%2C%203.4%2C%203.5-brightgreen.svg?style=flat)
![DeepDiff](https://img.shields.io/badge/DeepDiff-1.2.0-blue.svg?style=flat)

##Use Cases
###This Prototype is designed to:
1. download fresh json data from a URL into an OrderedDict object
2. _if_ an old json fil is present, load yesterday's json data from '.hcl' file 
3. _else if_ old file does not exist, new json will be saved as the old json file (for next time you run the script)
4. contrast json data in step 1 to json data in step 2
5. print the list of newly added hardware to csv file
6. save new json over old json 'hcl' file
7. catch a few common errors

!!! _PLEASE NOTE_ !!!  
each time you run this script you will OVERWRITE the 'json_old.hcl' file PERMANENTLY, no undo here :)

##Changelog

- v Beta-1-0-2: Initial commit for development testing and user feedback

##Author
Jordan C Walsh

- Github:  <https://github.com/jordancwalsh>
- Linkedin:  <http://www.linkedin.com/in/jordancwalshsoftwaredeveloper>
- Twitter:   <https://twitter.com/jcwsoftwaredev>
