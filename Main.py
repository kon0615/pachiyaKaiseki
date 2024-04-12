import sys 
import scriptCode


def main():
    areaName =["岡山県","宮城県"]
    test_startDay = '2024/03/11'#sys.argv[0]
    test_endDay   = '2024/04/10' #sys.argv[1]
    print(",".join(areaName))
    for area in areaName:
        
        scrayp = scriptCode.Scrayp(area)
        scrayp.Start_scrayping(test_startDay,test_endDay)
    
if __name__ =="__main__":
    main()