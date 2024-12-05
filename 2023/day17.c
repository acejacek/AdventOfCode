#include <stdio.h>
#include <stdlib.h>

#define INPUT_FILE "day17.test"

typedef struct
{
    char point;
    int prev;
    int val;
} Map;

int main(void)
{
    const char filename[] = INPUT_FILE;
    FILE* input = fopen(filename, "r");
    if (!input)
    {
        fprintf(stderr, "Can't load file %s.\n", filename);
        exit(EXIT_FAILURE);
    }

    char* line = NULL;
    size_t len = 0;
    ssize_t read = 0;

    Map* map = NULL;
    int h = 0;
    int w;

    while ((read = getline(&line, &len, input)) != -1)
    {
        w = read - 1;
        map = realloc(map, (h + 1) * w * sizeof(Map));
        if (! map)
        {
            fprintf(stderr, "Can't allocate memory.\n");
            fclose(input);
            exit(EXIT_FAILURE);
        }
        for (int i = 0; i < w; ++i)
        {
            char d[2] = { 0 };
            d[0] = line[i];

            map[h * w + i].point = atoi(d);
            map[h * w + i].prev = -1;
            map[h * w + i].val = -1;
        }
        h++;
    }
    fclose(input);

    for (int i = 0; i < w * h; ++i)
    {
        if (i % w == 0) putchar('\n');
        printf("%d", map[i].point);
    }

//    printf("Best configurtion:  %zu\n", best_energized);

    free(map);
    return 0;
}

