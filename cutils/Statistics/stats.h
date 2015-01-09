#ifndef STATS_H
#define STATS_H

#include <math.h>
#include <stdlib.h>

typedef struct stats {
    double sum;
    double sumsq;
    unsigned long n;
    double min;
    double max;
} stats;

tats *stats_recreate(double sum, double sumsq, unsigned long n, 
                     double min, double max);

tats *stats_create();

static inline double stats_mean(stats *s){
    return s->sum / s->n;
}

static inline double stats_stddev(stats *s){
   return sqrt((s->sumsq - (s->sum * s->sum / s->n)) / (s->n - 1));
}

void stats_sample(stats *s, double s);

void stats_dump(stats *s);

#endif
