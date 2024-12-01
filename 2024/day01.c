#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

typedef struct {
    size_t size;
    int* list_a;
    int* list_b;
} Lists;

Lists load_data(const char* filename)
{
    FILE* input = fopen(filename, "r");
    if (!input)
    {
        fprintf(stderr, "Can't load file %s.\n", filename);
        exit(EXIT_FAILURE);
    }

    Lists l = {0, NULL, NULL};

    char* line = NULL;
    size_t len = 0;
    ssize_t read = 0;
    
    while ((read = getline(&line, &len, input)) != -1)
    {
        l.list_a = realloc(l.list_a, (l.size + 1) * sizeof(*l.list_a));
        if (!l.list_a)
            exit(EXIT_FAILURE);
        l.list_b = realloc(l.list_b, (l.size + 1) * sizeof(*l.list_b));
        if (!l.list_b)
            exit(EXIT_FAILURE);

        char* digit = strtok(line, " \n");
        l.list_a[l.size] = atoi(digit);
        digit = strtok(NULL, "\n");
        l.list_b[l.size] = atoi(digit);
        ++l.size;
    }

    free(line); 
    fclose(input);
    return l;
}

int compare (const void* a, const void* b)
{
    int arg1 = *(const int*)a;
    int arg2 = *(const int*)b;

    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

void sort_list(Lists l)
{
    qsort(l.list_a, l.size, sizeof(*l.list_a), compare);
    qsort(l.list_b, l.size, sizeof(*l.list_b), compare);
}

int sum_distances(Lists l)
{
    int sum = 0;
    for (size_t i = 0; i < l.size; ++i)
        sum += abs(l.list_a[i] - l.list_b[i]);

    return sum;
}

int find_a(Lists l, int a)
{
    int count_a = 0;
    for (size_t i = 0; i < l.size; ++i)
        if (l.list_b[i] == a) ++count_a;

    return count_a;
}

int calculate_similarity_score(Lists l)
{
    int sum = 0;
    for (size_t i = 0; i < l.size; ++i)
        sum += l.list_a[i] * find_a(l, l.list_a[i]);

    return sum;
}

int main(void)
{
    Lists l;
    int sum;

    l = load_data("day01.test");
    sort_list(l);
    sum = sum_distances(l);
    assert(sum == 11);

    sum = calculate_similarity_score(l);
    assert(sum == 31);

    free(l.list_a);
    free(l.list_b);

    l = load_data("day01.txt");
    sort_list(l);
    sum = sum_distances(l);
    printf("Part 1: sum of distances is %d\n", sum);

    sum = calculate_similarity_score(l);
    printf("Part 2: similarity score is %d\n", sum);

    free(l.list_a);
    free(l.list_b);
    return 0;
}

