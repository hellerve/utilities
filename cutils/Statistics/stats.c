#include "stats.h"

stats *stats_recreate(double sum, 
                      double sumsq, 
                      unsigned long n, 
                      double min, 
                      double max){
    
    stats *s = malloc(sizeof(stats));
    
    if(!s) return NULL;

    s->sum = sum;
    s->sumsq = sumsq;
    s->n = n;
    s->min = min;
    s->max = max;

    return s;
}

stats *stats_create(){
    return stats_recreate(0.0, 0.0, 0L, 0.0, 0.0);
}

void stats_sample(stats *s, double sum){
    s->sum += sum;
    s->sumsq += sum * sum;

    if(s->n == 0) {
        s->min = sum;
        s->max = sum;
    } else {
        if(s->min > sum) s->min = sum;
        if(s->max < sum) s->max = sum;
    }

    s->n += 1;
}

void stats_dump(stats *s){
    fprintf(stderr, "sum: %f, sumsq: %f, n: %ld, min: %f, max: %f, mean: %f, stddev: %f",
            s->sum, s->sumsq, s->n, s->min, s->max,
            stats_mean(s), stats_stddev(s));
}
