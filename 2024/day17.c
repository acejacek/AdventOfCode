#include <stdio.h>

int prog[] = {2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0};
int out[16] = {0};

int comp1(size_t A)
{
    int outIdx = 0;
    size_t B = 0;
    size_t C = 0;

    for (int pointer = 0; pointer < 16; pointer += 2)
        switch(prog[pointer])
        {
            case 0:
                A >>= 3;
                break;

            case 1:  // bxl
                B ^= prog[pointer + 1];
                break;

            case 2:  // bst
                B = A & 7;
                break;

            case 3:  // jnz
                if (A) pointer = prog[pointer + 1] - 2;
                break;

            case 4:  // bxc
                B ^= C;
                break;

            case 5:  // out
                out[outIdx++] = B & 7;
                break;

            case 7:
                C = A >> B;
                break;
        }

    return 1;
}
int comp(size_t A)
{
    int outIdx = 0;
    size_t B = 0;
    size_t C = 0;

    for (int pointer = 0; pointer < 16; pointer += 2)
        switch(prog[pointer])
        {
            case 0:
                A >>= 3;
                break;

            case 1:  // bxl
                B ^= prog[pointer + 1];
                break;

            case 2:  // bst
                B = A & 7;
                break;

            case 3:  // jnz
                if (A) pointer = prog[pointer + 1] - 2;
                break;

            case 4:  // bxc
                B ^= C;
                break;

            case 5:  // out
                if ((B & 7) != prog[outIdx]) return 0;
                out[outIdx++] = B & 7;
                break;

            case 7:
                C = A >> B;
                break;
        }

    return 1;
}

int main()
{
    comp1(59590048);
    for (int i = 0; i < 16; ++i)
        printf("%d ", out[i]);

    putchar('\n');
    return 0;


    for (size_t a = 9000000000; a < 90000000000; ++a)
        if (comp(a))
        {
            int fail = 0;
            for (int i = 0; i < 16; ++i)
            {
                if (prog[i] != out[i]) fail = 1;
                out[i] = 0;
            }
            if (!fail)
            {
                printf("Part 2: %zu\n", a);
                break;
            }
        }

    return 0;
}
