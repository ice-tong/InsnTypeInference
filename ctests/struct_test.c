#include <stdlib.h>

struct A {
    int a;
    char c;
};

struct B
{
    float num;
    struct A* pre;
    struct A* next;
    struct B* father;
};

typedef struct A StructA;


void
main()
{
    struct A A1 = {1, 'a'};
    StructA A2;
    A2.a = 2;
    A2.c = 'b';
    struct B B1;
    B1.num = 1.0;
    B1.pre = &A1;
    B1.next = &A2;
    B1.father = NULL;
    struct B* B2; 
    B2 = (struct B*)malloc(sizeof(struct B));
    B2->num = 2.0;
    B2->pre = &A2;
    B2->next = &A1;
    B2->father = &B1;
}