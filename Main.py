import sys 
from scriptCode import Scrayp


def main():
    areaName =["宮城県"]
    test_startDay = "20230101"
    test_endDay   = "20240101"
    print(",".join(areaName))
    for area in areaName:
        
        scrayp = Scrayp(area)
        scrayp.Start_scrayping(test_startDay,test_endDay)
    
if __name__ =="__main__":
    main()