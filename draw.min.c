#define N getchar()
char m[320][386][3];main(){puts("P6 386 320 255");int c=N,i=0;while(c--){
		int r=N,g=N,b=N,x=N*2,v=N*2,u=N*2,w=N*2,y;
		for(;x<=v;x++){
			for(y=u;y<=w;y++){
				m[y][x][0]=r;
				m[y][x][1]=g;
				m[y][x][2]=b;
			}
		}
	}
	while(i<370560){putchar(*((**m)+i++));}
}
