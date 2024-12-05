#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define TEST
// change for part 2
#define PART 2

#ifdef TEST
#define INPUT_FILE "day21.test"
#else
#define INPUT_FILE "day21.txt"
#endif

#define HASH_SIZE 100000

typedef char Tile;

typedef struct hash_t {
    bool lock;
    int x;
    int y;
    struct hash_t* next;
} Hash;

size_t step_counter = 0;
size_t max_new_cache = 0;
size_t max_prev_cache = 0;

Hash* new_cache = NULL;
Hash* prev_cache = NULL;

size_t hash(int a, int b)
{
    size_t A = (size_t)(a >= 0 ? 2 * (long)a : -2 * (long)a - 1);
    size_t B = (size_t)(b >= 0 ? 2 * (long)b : -2 * (long)b - 1);
    return ((A >= B ? A * A + A + B : A + B * B) % HASH_SIZE);
}

bool no_obstacle(Tile* tile, const size_t h, const size_t w, int x, int y)
{
    int local_x = x % (int)w;
    int local_y = y % (int)h;
    
    if (local_x < 0) local_x += w; 
    if (local_y < 0) local_y += h; 
    return (tile[local_y * w + local_x] != '#');
}

void add_to_hash_bucket(size_t index, int x, int y)
{
    Hash* curr = new_cache + index;
    while (curr->next != NULL)
    {
        if (curr->x == x && curr->y == y) // this entry exists
            return;
        curr = curr->next;
    }

    Hash* new = malloc(sizeof(*new));
    if (!new) exit(1);

    new->x = x;
    new->y = y;
    new->next = NULL;
    curr->next = new;
    step_counter++;
}

void add_step_hash(int x, int y)
{
    size_t index = hash(x, y);
    if (max_new_cache < index) max_new_cache = index;

    if (new_cache[index].lock)
    {
        if (new_cache[index].x != x || new_cache[index].y != y)  // colision in hash table?
        {
//            fprintf(stderr, "cache collision %d %d with %d %d id: %zu\n",x, y, new_cache[index].x, new_cache[index].y, index);
            add_to_hash_bucket(index, x, y);
        }
        return;
    }
    //        printf("x: %d, y: %d, h: %zu\n", x, y, index);
    new_cache[index].x = x;
    new_cache[index].y = y;
    new_cache[index].lock = true;
    step_counter++;
}

void change_cache_generations(void)
{
    Hash* tmp = prev_cache;
    prev_cache = new_cache;
    new_cache = tmp;

    max_prev_cache = max_new_cache;
    max_new_cache = 0;
}

void walk_steps_hash_bucket(Tile* garden, const size_t h, const size_t w, Hash* curr)
{
    if (!curr) return;

    walk_steps_hash_bucket(garden, h, w, curr->next);

    if (no_obstacle(garden, h, w, curr->x-1, curr->y))
        add_step_hash(curr->x-1, curr->y);
    if (no_obstacle(garden, h, w, curr->x+1, curr->y))
        add_step_hash(curr->x+1, curr->y);
    if (no_obstacle(garden, h, w, curr->x, curr->y-1))
        add_step_hash(curr->x, curr->y-1);
    if (no_obstacle(garden, h, w, curr->x, curr->y+1))
        add_step_hash(curr->x, curr->y+1);

    free(curr);
}

void walk_steps_hash(Tile* garden, const size_t h, const size_t w)
{
    Hash* curr = prev_cache;
    for (size_t i = 0; i <= max_prev_cache; ++i, curr++)
    {
        if (!curr->lock) continue;

        if (no_obstacle(garden, h, w, curr->x-1, curr->y))
            add_step_hash(curr->x-1, curr->y);
        if (no_obstacle(garden, h, w, curr->x+1, curr->y))
            add_step_hash(curr->x+1, curr->y);
        if (no_obstacle(garden, h, w, curr->x, curr->y-1))
            add_step_hash(curr->x, curr->y-1);
        if (no_obstacle(garden, h, w, curr->x, curr->y+1))
            add_step_hash(curr->x, curr->y+1);

        walk_steps_hash_bucket(garden, h, w, curr->next);

        curr->lock = false;
        curr->next = false;
    }
}
void show_garden(Tile* tile, const size_t h, const size_t w)
{
    for (size_t y = 0; y < h; ++y)
    {
        for (size_t x = 0; x < w; ++x)
            putchar(tile[y * w + x]);
        putchar('\n');
    }
}

void add_start(Tile* tile, const size_t h, const size_t w)
{
    for (size_t y = 0; y < h; ++y)
        for (size_t x = 0; x < w; ++x)
            if(tile[y * w + x] == 'S')
            {
                add_step_hash(x, y);
                return;
            }
}

int main(void)
{

#if PART == 1
#ifdef TEST
    const size_t steps = 6;
#else
    const size_t steps = 64;
#endif

#else  // PART 2
#ifdef TEST
    const size_t steps = 5000;
#else
    const size_t steps = 26501365;
#endif
#endif

    Tile* garden = NULL;

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

    size_t height = 0;
    size_t width = 0;
    for (height = 0; (read = getline(&line, &len, input)) != -1; ++height)
    {
      if (width ==0) width = read - 1;
      garden = realloc(garden, (height + 1) * width * sizeof(*garden));
      if (garden == NULL)
      {
        fprintf(stderr, "Can't allocate memory");
        fclose(input);
        exit(EXIT_FAILURE);
      }
      //strncpy(garden + (height * width), line, width);
      for (size_t i = 0; i < width; ++i)
      {
          garden[height * width + i] = line[i];
      }
    }

    fclose(input);  

    prev_cache = calloc(HASH_SIZE, sizeof(*prev_cache));
    if (!prev_cache)
        exit(1);
    new_cache = calloc(HASH_SIZE, sizeof(*new_cache));
    if (!new_cache)
        exit(1);

#if PART == 1
    for (size_t s = 0; s < steps; ++s)
    {

    }
    
    printf("Garden plots in reach: %zu\n", count_garden(garden, height, width));
#else
    
//    show_garden(garden, height, width);
    add_start(garden, height, width);

    for (size_t s = 0; s < steps; ++s)
    {
        change_cache_generations();
        step_counter = 0;
        walk_steps_hash(garden, height, width);
//        printf("step:%zu tiles: %zu\n", s+1, step_counter);
//        exit(0);
    }
    printf("Tiles: %zu\n", step_counter);
//    printf("max hash: %zu\n", max_hash);
#endif
    free(prev_cache);
    free(new_cache);
    free(garden);
    free(line);
    return 0;
}

