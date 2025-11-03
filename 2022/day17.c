#include <stdio.h>
#include <stdlib.h>

#define WIDTH 7

typedef struct {
    int h;
    int w;
    int x;
    int y;
    char body[9];
} Block;

typedef struct {
    char** wellData;
    int levels; 
    int highestPoint;
} Well;

void printBlock(Block* b)
{
    int pos = 0;
    for (int y = 0; y < b->h; ++y)
    {
        for (int x = 0; x < b->w; ++x)
        {
            putchar(b->body[pos++]);
        }
        putchar('\n');
    }
}

// increase well size to new depth
Well* rescaleWell(Well* w, const int newLevels)
{
    printf("reallocating from %d to %d levels\n", w->levels, newLevels);
    w->wellData = realloc(w->wellData, newLevels * sizeof(char*));
    for (int l = w->levels; l < newLevels; ++l)
        w->wellData[l] = calloc(WIDTH, sizeof(char));

    w->levels = newLevels;

    return w;
}

// find highest point of well
int maxLevel(Well* w)
{
    for (int l = w->levels - 1; l >= 0; --l)
        for (int x = 0; x < WIDTH; ++x)
            if (w->wellData[l][x] == '#') return l;

    return 0;
}

void printWell(Well* w)
{
    for (int l = w->levels - 1; l >= 0; --l)
    {
        putchar('|');
        for (int x = 0; x < WIDTH; ++x)
            if (w->wellData[0][0] == '\0')
                putchar(' ');
            else
                putchar(w->wellData[l][x]);

        puts("|");
    }
    puts("+-------+");
}

int setBlock(Block* b, int bottom)
{
    b->x = 2;
    b->y = bottom + 3 + b->h;

    return b->y;
}

int main()
{
    Block block[5] = {{ 1, 4, 0, 0,  "####"},
        { 3, 3, 0, 0, ".#.###.#."},
        { 3, 3, 0, 0, "..#..####"},
        { 4, 1, 0, 0, "####"},
        { 2, 2, 0, 0, "####"}};

    Well well = { NULL, 0, 0 };


    //const char jet = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>";
    //int jetpos = 0; 
    
    for (int i = 0; i < 5; ++i)
    {
        printBlock(block + i);
        putchar('\n');
    }

    int bottom = 0;
    int lev = setBlock(block, bottom);
    rescaleWell(&well, lev);

    //printf("lev: %d, bott: %p\n", well.levels, (void*)well.wellData[1]);

    printWell(&well);

    return EXIT_SUCCESS;
}

