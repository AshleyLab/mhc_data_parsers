#assembles results generated by get_activity_fraction_and_duration_appv2.healthkit.sh and get_activity_fraction_and_duration_appv2.activity_only.sh
#into a single file including all subject data.
import argparse
import pdb
def parse_args():
    parser=argparse.ArgumentParser(description="assemble results")
    parser.add_argument("--prefix")
    parser.add_argument("--first",type=int)
    parser.add_argument("--last",type=int)
    parser.add_argument("--outf")
    parser.add_argument("--suffix",default="") 
    return parser.parse_args()

def main():
    args=parse_args()
    outf=open(args.outf,'w')
    is_first=True #only write header for first file
    first_index=args.first
    last_index=args.last
    for index in range(first_index,last_index+1):
        print(str(index))
        data=open(args.prefix+str(index)+args.suffix,'r').read().strip().split('\n')
        header=data[0]
        body=data[1::]
        if is_first==True:
            print(str(header))
            outf.write(header+'\n')
            is_first=False
        outf.write('\n'.join(body)+'\n')
    
if __name__=="__main__":
    main()
    
