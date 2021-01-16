
void
main()
{
    int i = 1;
    int* pti = &i;
    for(; i < 5; i++) {
        *pti = i;
    }
}