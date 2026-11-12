#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define NB 4096
unsigned char ks[NB];
static void gen(uint32_t st,int len,const int*taps,int nt,unsigned char*out,int n){
  for(int i=0;i<n;i++){out[i]=st&1;int fb=0;for(int t=0;t<nt;t++)fb^=(st>>taps[t])&1;st=(st>>1)|((uint32_t)fb<<(len-1));}
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb");unsigned char b[512];fread(b,1,512,f);
  for(int i=0;i<NB;i++)ks[i]=(b[i/8]>>(7-i%8))&1;
  int t1[]={0,1,2,5},t2[]={0,2},t3[]={0,5};
  unsigned char a[NB],x[NB],c[NB];
  int best2=0;uint32_t s2=0,best3=0,s3=0;
  for(uint32_t s=1;s<(1u<<21);s++){gen(s,21,t2,2,x,NB);int m=0;for(int i=0;i<NB;i++)m+=(x[i]==ks[i]);if(m>best2){best2=m;s2=s;}}
  fprintf(stderr,"L2 %u %d\n",s2,best2);
  for(uint32_t s=1;s<(1u<<23);s++){gen(s,23,t3,2,c,NB);int m=0;for(int i=0;i<NB;i++)m+=(c[i]==ks[i]);if(m>(int)best3){best3=m;s3=s;}}
  fprintf(stderr,"L3 %u %u\n",s3,best3);
  gen(s2,21,t2,2,x,NB);gen(s3,23,t3,2,c,NB);
  for(uint32_t s=1;s<(1u<<19);s++){gen(s,19,t1,4,a,NB);int ok=1;for(int i=0;i<NB;i++){int o=(a[i]&x[i])^((a[i]^1)&c[i]);if(o!=ks[i]){ok=0;break;}}if(ok){printf("%u %u %u\n",s,s2,s3);}}
}
