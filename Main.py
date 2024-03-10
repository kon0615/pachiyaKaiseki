import sys 
import scriptCode


def main():
    areaName =["宮城県"]
    test_startDay = "2023/01/01"
    test_endDay   = "2024/04/01"
    print(",".join(areaName))
    for area in areaName:
        
        scrayp = scriptCode.Scrayp(area)
        scrayp.Start_scrayping(test_startDay,test_endDay)
    
if __name__ =="__main__":
    main()