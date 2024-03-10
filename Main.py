import sys 
import scriptCode


def main():
    areaName =["宮城県","岡山県"]
    test_startDay = '2023/02/28' #sys.argv[0]
    test_endDay   = '2024/03/09' #sys.argv[1]
    print(",".join(areaName))
    for area in areaName:
        
        scrayp = scriptCode.Scrayp(area)
        scrayp.Start_scrayping(test_startDay,test_endDay)
    
if __name__ =="__main__":
    main()