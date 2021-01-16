#include <stdio.h>
#include <stdlib.h>

struct st {
    int a;
    float b;
    char c;
};

void
main()
{
    int i = 1;
    short shorti = 2;
    long int longi = 3;
    unsigned int unsignedi = 4;
    signed int signedi = -5;

    float f = 6.0;
    double d = 7.0;

    char c = 'a';

    char s[10] = "hello!";
    int A[3] = {1, 1, 0};
    struct st ST = {10, 9.0, 'a'};

    int* pti;
    pti = &i;
    float* ptf;
    ptf = (float*) malloc(sizeof(float));

    for (; i < 10; i++) {
        shorti += i;
        longi += shorti;
        unsignedi += signedi;
        c += 1;
        s[i] = c;
        f += d;
        *pti = i;
        *ptf = f;
        printf("%d\t",  shorti);
        printf("%d\t", longi);
        printf("%d\t", unsignedi);
        printf("%c\t", c);
        printf("%f\t", f);
        printf("\n");
    }

    printf("%s\n", s);

}
