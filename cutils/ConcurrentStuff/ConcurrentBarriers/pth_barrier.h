typedef struct{
    pthread_mutex_t m;
    pthread_cond_t c;
    int count, go, numThreads;
} pth_barrier_t;

void pth_barrier_init(pth_barrier_t *b, int numT){
    pthread_mutex_init(&b->m, NULL);
    pthread_cond_init(&b->c, NULL);
    b->count = b->numThreads = numT;
    b->go = false;
}

void pth_barrier(pth_barrier_t *b){
    pthread_mutex_lock(&b->m);
    int i_go = b->go;
    if(--(b->count)){
        while(i_go == b->go)
            pthread_cond_wait(&b->c, &b->m);
    }else{
        pthread_cond_broadcast(&b->c);
        b->count = b->numThreads;
        b->go = !b->go;
    }
    pthread_mutex_unlock(&b->m);
}
