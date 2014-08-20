void ShellSort(int *A, int N){
    int k, h = 1;
    while(h < N)
        h = 3 * h + 1;
    h /= 3;
#pragma omp parallel firstprivate(h)
    {
        while(h != 1){
#pragma omp for
            for(k = 0; k < h; k++){
                int i, j, v;
                for(i = k; i < N; i += h){
                    v = A[i];
                    j = i;
                    while(A[j-h] > v){
                        A[j] = A[j-h];
                        j -= h;
                        if(j <= h) break;
                    }
                    A[j] = v;
                }
            }
            h /= 3;
        }
    }
    InsertionSort(A, N);
}
