#include <stdio.h>

void 
main()
{
    int A[10];
    float B[10];
    char C[10];
    int i;
    for (i=0; i<10; i++) {
        A[i] = i;
        B[i] = i*1.0;
        C[i] = 65+i;
    }
    for (i=0; i<10; i++) {
        printf("%d\t", A[i]);
        printf("%f\t", B[i]);
        printf("%c\n", C[i]);
    }
}
