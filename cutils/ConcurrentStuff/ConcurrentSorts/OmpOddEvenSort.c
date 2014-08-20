void OddEvenSort(int *A, int N){
    int exch0, exch1 = 1, trips = 0, i;
    int temp;

    while(exch1){
        exch0 = 0;
        exch1 = 0;

#pragma omp parallel
        {   int temp;
#pragma omp for
            for(i = 0; i < N-1; i += 2){
                if(A[i] > A[i+1]){
                    temp = A[i];
                    A[i] = A[i+1];
                    A[i+1] = temp;
                    exch0 = 1;
                }
            }
            if(exch0 || !trips){
#pragma omp for
                for(i = 1; i < N-1; i += 2){
                    if(A[i] > A[i+1]){
                        temp = A[i];
                        A[i] = A[i+1];
                        A[i+1] = temp;
                        exch1 = 1;
                    }
                }
            }
        }
        trips = 1;
    }
}
