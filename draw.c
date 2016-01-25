#include <stdio.h>
#define NEXT getchar()
#define NEXTPOS NEXT*2
//      y    x   c
char m[320][386][3];
int main(){
	puts("P6 386 320 255");
	int c=NEXT;
	while(c--) {
		char r = NEXT;
		char g = NEXT;
		char b = NEXT;
		
		int startx = NEXTPOS;
		int endx = NEXTPOS;
		int starty = NEXTPOS;
		int endy = NEXTPOS;
		
		for (int x = startx; x<=endx; x++) {
			for (int y = starty; y<=endy; y++) {
				m[y][x][0]=r;
				m[y][x][1]=g;
				m[y][x][2]=b;
			}
		}
	}
	// Dump the file
	int i=0;
	while(i<386*320*3){
		putchar(*((**m)+i++));
	}
	return 0;
}
