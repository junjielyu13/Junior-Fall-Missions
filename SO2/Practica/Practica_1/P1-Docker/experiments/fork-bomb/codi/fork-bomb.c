#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main(void)
{
    while (1) { fork(); }

    return 0;
}


