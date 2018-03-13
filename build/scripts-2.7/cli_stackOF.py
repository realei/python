import sys
sys.path.append("..")
import argparse
import time
from stackexchange import StackApi
import json
import json2html

def is_valid_date(strdate):
    """
    :param: (required)** strdate is a time str 
    valid str is a data format, such as:
    "2018-01-01 10:00:00" or "2018-01-01"
    """
    try:
        if ":" in strdate:
            time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(strdate, "%Y-%m-%d")
        return True
    except:
        raise ValueError("Please input a valid date")


def main(argv=None):
    
    if argv is None:
        argv = sys.argv
        
    #Iniliatize the CLI Parser 
    parser = argparse.ArgumentParser(description="StackOverFlow CLI")
    parser.add_argument("cmd", type=str, choices=["stats", "get"], help="comand for stats or get: stats: check status for a given data/time get:retrieve data for a givea data/time")
    parser.add_argument("-d", "--datatype", type=str, choices=["answers","badges","comments", "questions", "answers/ids/comments"], help="the retrive datatype for stackoverflow site")
    parser.add_argument("-s", "--since", help="starting data/time to retrieve")
    parser.add_argument("-u", "--until", help="ending data/time to retrieve")
    parser.add_argument("-i", "--ids", type=int, nargs='+', help="set of ids for retrieve")
    parser.add_argument("-o", "--output-format", choices=["json", "html", "tabular"], help="the output format of the result")
    parser.add_argument("-f", "--filter", help="the filter information to add to StackExchangeApi", default="default")
    args = parser.parse_args()

    #Initialize StackOverFlow Api
    site = StackApi()

    #valid time input format
    #"--since" and "--until" are designed to be required, because can't receive unlimited data
    if not args.since and not args.until:
        print("Start and until date/time is not specified yet!")
    else:
        if not args.since:
            raise ValueError("Please specify starting time!!!")
        else:
            is_valid_date(args.since)
            is_valid_date(args.until)

    #processing the CLI request  
    if args.cmd == "get":
 
        #pre process datatype and ids
        if not args.datatype:
            raise ValueError("Please specify get datatype!!!")
        elif args.datatype == "answers/ids/comments":
            if not args.ids:
                raise ValueError("Please specify ids to comments-on-data method!!!")
            args.datatype = "answers/ids/comments"
            args.datatype = args.datatype.replace("ids", ";".join(str(x) for x in args.ids))

        response = site.fetch(args.datatype, filter=args.filter, fromdate=args.since, todate=args.until)
    elif args.cmd == "stats":
        result = site.fetch("answers", filter="!9Z(-x)63B", fromdate=args.since, todate=args.until, ids=args.ids)
        response = site.calAnswers(result["items"])
        result = site.fetch("questions", fromdate=args.since, todate=args.until)
        ave_count= {"average_answers_comment_count": site.calAve(result["items"], "answer_count")}
        response.update(ave_count)

    response = json.dumps(response, sort_keys=True, indent=4, separators=(",",":"))
    #response = json2html.convert(json = response)    
    return response   

if __name__ == "__main__":
      sys.exit(main())
