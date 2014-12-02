#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include "../ConcurrentBarriers/pth_barrier.h"

#define NUM_THREADS 4
#define N 400000

unsigned int *A;
unsigned int gSum[NUM_THREADS];
pth_barrier_t B;

void *SumByReduction(void *pArg){
    int tNum = *((int *) pArg);
    int lSum = 0;
    int start, end, i;

    start = ((float)N/NUM_THREADS) * tNum;
    end = ((float)N/NUM_THREADS) * (tNum + 1);
    if(tNum == (NUM_THREADS-1)) end = N;
    for(i = start; i < end; i++){
        lSum += A[i];
    }
    gSum[tNum] = lSum;

    pth_barrier(&B);
    int p2 = 2;
    for(i = 1; i <= NUM_THREADS; i *= 2){
        if((tNum % p2) == 0)
            if(tNum+i < NUM_THREADS) gSum[tNum] += gSum[tNum+i];
        p2 *= 2;
        pth_barrier(&B);
    }
    free(pArg);
}

int main(int argc, char* argv[]){
    pthread_t tHandles[NUM_THREADS];

    A = new unsigned int[N];
    for(i = 0; i < N; i++)
        A[i] = i;
    pth_barrier_init(&B, NUM_THREADS);
    for(j = 0; j < NUM_THREADS; j++){
        int *threadNum = new(int);
        *threadNum = j;
        pthread_create(&tHandles[j], NULL, SumByReduction, (void *) threadNum);
    }
    pthread_join(tHandles[0], NULL);
    printf("The sum of all elements is %u.\n", gSum[0]);
    return 0;
}
