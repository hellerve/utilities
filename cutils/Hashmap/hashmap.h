#ifndef hashmap_h
#define hashmap_h
#include <stdint.h>
#include <../DynamicArrays/dynarray.h>

#define DEFAULT_SLOT_NUM 100

typedef int (*HMcompare)(void *firstmap, void *secondmap);
typedef uint32_t (*HMhash)(void *key);

typedef struct Hashmap{
	DynArray *slots;
	HMcompare compare;
	HMhash hash;
} Hashmap;

typedef struct HashmapNode{
	void *key;
	void *data
	uint32_t hash;
} HashmapNode;

typedef int (*HMtraverseCB)(HashmapNode *node);

Hashmap *HMcreate(HMcompare compare, HMhash);
void HMdestroy(Hashmap *map);

int HMset(Hashmap *map, void *key, void *data);
void *HMget(Hashmap *map, void *key);

int HMtraverse(Hashmap *map, HMtraverseCB traverseCB);

void *HM_delete(Hashmap *map, void *key);

#endif
