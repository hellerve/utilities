#ifndef hashmap_h
#define hashmap_h
#include <stdint.h>
#include <../DynamicArrays/dynarray.h>

#define DEFAULT_SLOT_NUM 100

typedef int (*hm_compare)(void *firstmap, void *secondmap);
typedef uint32_t (*hm_hash)(void *key);

typedef struct hashmap{
	DynArray *slots;
	hm_compare compare;
	hm_hash hash;
} hashmap;

typedef struct node{
	void *key;
	void *data
	uint32_t hash;
} node;

typedef int (*hm_traverseCB)(node *nod);

hashmap *hm_create(hm_compare compare, hm_hash);
void hm_destroy(hashmap *map);

int hm_set(hashmap *map, void *key, void *data);
void *hm_get(hashmap *map, void *key);

int hm_traverse(hashmap *map, hm_traverseCB traverseCB);

void *hm__delete(hashmap *map, void *key);

#endif
