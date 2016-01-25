#include <stdio.h>
#define N getchar()
char m[320][386][3];
main(){puts("P6 386 320 255");
	int c=N,i=0;
	while(c--) {
		char r=N,g=N,b=N;
		
		int startx=N*2,endx=N*2,starty=N*2,endy=N*2;
		
		for (int x = startx; x<=endx; x++) {
			for (int y = starty; y<=endy; y++) {
				m[y][x][0]=r;
				m[y][x][1]=g;
				m[y][x][2]=b;
			}
		}
	}
	while(i<370560){
		putchar(*((**m)+i++));
	}
	return 0;
}
