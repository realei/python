# Python Assignment Stack Cli From Lei WANG --v0.1.1

Stack Cli use StackExchange Apr to retrive StackOverFlow's data by time and id and calculate the results:

  - Retrive the StackOverflow answer data for a given date/time range from the StackExchange Api
  - Retrive the comment data for a given set of answers 
  - For a given data/time range calculates 
  --the totalnumber of accpeted answers
  --the average score for all the accepted answers
  --the averange answer count per question 
  --the comment count for each of the 10 answers with the highest score

### Installation

Prerequest:
  - have "python 2.7" installed
  - have "setuptools" installed
  - linux root permission

```sh
$ cd ls
$ unzip lwang-python-assignment.zip
$ cd python-assignment
$ python ./setup.py install

```

### How to run the application

USAGE: 
       cli_stackOF.py [-h]
                      [-d {answers,badges,comments,questions,answers/ids/comments}]
                      [-s SINCE] [-u UNTIL] [-i IDS [IDS ...]]
                      [-o {json,html,tabular}] [-f FILTER]
                      {stats,get}

StackOverFlow CLI

positional arguments:
  {stats,get}           comand for stats or get: stats: check status for a
                        given data/time get:retrieve data for a givea
                        data/time

optional arguments:
  -h, --help            show this help message and exit
  -d {answers,badges,comments,questions,answers/ids/comments}, --datatype {answers,badges,comments,questions,answers/ids/comments}
                        the retrive datatype for stackoverflow site
  -s SINCE, --since SINCE
                        starting data/time to retrieve
  -u UNTIL, --until UNTIL
                        ending data/time to retrieve
  -i IDS [IDS ...], --ids IDS [IDS ...]
                        set of ids for retrieve
  -o {json,html,tabular}, --output-format {json,html,tabular}
                        the output format of the result
  -f FILTER, --filter FILTER
                        the filter information to add to StackExchangeApi

Examples:

Retrive the comment data for a given date/time range 
```sh
$ cli_stackOF.py get -d answers -s "2016-06-02 10:00:00" -u "2016-06-02 11:00:00" 
```

Retrive the comment data for a given set of answers

```sh
$ cli_stackOF.py get -d answers/ids/comments --ids 37584787 37584801 37584818 37584826
```

Retrive the stats for a given date/time range

```sh
$ cli_stackOF.py stats -s "2016-06-02 10:00:00" -u "2016-06-02 11:00:00" 
```

### New Features:
  - have json2html in egg
  - update some comments

### Known Issues & TBD: 
  - Issue: duplicated top_ten_answers_comment_count
  - TBD: HTML output
  - Add UT 
