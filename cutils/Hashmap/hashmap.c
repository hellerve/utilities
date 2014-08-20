#undef NDEBUG
#include <stdint.h>
#include <hashmap.h>
#include <../BStringLibrary/bstrlib.h>
#include <Debug/debugheader.h>

static int default_compare(void *a, void *b){
	return bstrcmp((bstring)a, (bstring)b);
}

/**
 *
 * Implementation of Bob Jenkin's hash algorithm stolen from Wikipedia.
 *
 */
static uint32_t default_hash(void *a){
	size_t len = blength((bstring)a);
	char *key = bdata((bstring) a);
	uint32_t hash = 0;
	uint32_t i;
	
	for(i = 0; i < len; i++){
		hash += key[i];
		hash += (hash << 10);
		hash ^= (hash >> 6);
	}

	hash += (hash << 3);
	hash ^= (hash >> 11);
	hash += (hash << 15);

	return hash;
}

Hashmap *HMcreate(HMcompare compare, HMhash hash){
	Hashmap *map = calloc(1, sizeof(Hashmap));
	check_mem(map);

	map->compare = (compare == NULL ? default_compare : compare);
	map->hash = (hash == NULL ? default_hash : hash);
	map->slots = DynArray_create(sizeof(DynArray *), DEFAULT_SLOT_NUM);
	map->slots->end = map->slots->max;
	check_mem(map->slots);

	return map;

error:
	if(map)
		HMdestroy(map);

	return NULL;
}

void HMdestroy(Hashmap *map){
	int i, j;

	if(map){
		if(map->slots){
			for(i = 0; i < DynArray_count(map->slots); i++){
				DynArray *slot = DynArray_get(map->slots, i);
				if(bucket){
					for(j = 0; j < DynArray_count(slot); j++){
						free(DynArray_get(slot, j));
					}
					DynArray_destroy(slot);
				}
			}
			DynArray_destroy(map->buckets);
		}
	
		free(map);
	}
}


