import sys,os
import gzip
import lzma
import numpy as np
import argparse

myargs=argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), description="Instantiate an interactome with a list of genes expressed (in a tissue) above a given expression value.",add_help=True)
myargs.add_argument('interactome',help="Interactome file")
myargs.add_argument('tissue',help='A TSV file with two columns: Gene/Protein ID and expression value')
myargs.add_argument('-c','--cutoff',default=1,type=float,help="Genes with values below this won't be considered as expressed.")
myargs.add_argument('-o','--output_file',help="A file to save the instantiated interactome.")

args=myargs.parse_args()
#zcat ../interactomes/BIOGRID-ORGANISM-Homo_sapiens-4.3.196.tab3.txt.gz |cut -f8,9,10,11,13,16,17|grep -P "physical\t\9606\t9606"|grep -v "^-\t-"|cut -f1,2,3,4|sort -u |pxz >biogrid_hsa-oss_phys.tsv.xz
#args.interactome,tissuef,cutoff='biogrid_hsa-4.3.196_edges.xz','hpa_nx/adipose_tissue.tsv',5.0
tissue,reps={},{}
with open(args.tissue, "r") as fh:
 for line in fh:
  geneid,expr=line.strip().split()[:2]
  try:
   if float(expr)<args.cutoff:continue
  except ValueError:
   sys.exit("ERROR!! The second column of '{}' should contain the expression values of the genes in the tissue.".format(args.tissue))
  if geneid in tissue:
   tissue[geneid].append(float(expr))
   reps[geneid]=tissue[geneid]
  else:tissue[geneid]=[float(expr)]

#Dprint(len(tissue),file=sys.stderr)
#print repeated genes and expvalues
#Dif len(reps)>0: print(*map("\t".join,[(k," ".join(map(str,v))) for k,v in reps.items()]), sep='\n',file=sys.stderr)

if args.output_file is None:
 out_fh = sys.stdout
else: out_fh = open(args.output_file,'w')

if os.path.splitext(args.interactome)[-1]=='.xz':
 inpf=lzma.open(args.interactome,'rt')
elif os.path.splitext(args.interactome)[-1]=='.gz':
 inpf=gzip.open(args.interactome,'rt')
else:
 inpf=open(args.interactome,'rt')

f="\t".join(['{}','{}',"{:.4g}","{:.4g}","{:.4g}"])
tint=[]
for line in inpf:
 #print(line.strip())
 l=line.strip().split('\t')
 ori,dest=l[:2]
 #ori,dest,sori,sdest=line.strip().split('\t')
 #hago np.mean() porque algunos ENSEMBL genes apuntaban a un mismo gen...
 if not ori in tissue:
  ori=''
  if len(l)>2:
   ori=[sino for sino in l[2].split("|") if sino in tissue]
   ori=ori[0] if len(ori)>0 else ''
 if not dest in tissue:
  dest=''
  if len(l)>2:
   dest=[sino for sino in l[3].split("|") if sino in tissue]
   dest=dest[0] if len(dest)>0 else ''
 if ori=='' or dest=='':continue
  #print(ori,dest)
 oriexp,destexp= np.mean(tissue[ori]),np.mean(tissue[dest])
  #Xtint.append([ori,dest,str(np.mean(tissue[ori])),str(np.mean(tissue[dest])),"{:.4g}".format(oriexp*destexp)])
 print(f.format(*(ori,dest,np.mean(tissue[ori]),np.mean(tissue[dest]),oriexp*destexp)),file=out_fh)
inpf.close()
out_fh.close()
#Xprint(*map("\t".join,tint),sep='\n')
