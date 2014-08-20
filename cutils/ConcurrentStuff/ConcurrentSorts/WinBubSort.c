unsigned __stdcall BubbleSort(LPVOID pArg){
    int i, j, k, releasePoint, temp, rpInc;
    BOOL exch;

    rpInc = N/NUM_LOCKS;
    rpInc++;

    while(!Done){
        k = 0;
        exch = FALSE;
        EnterCriticalSection(&BLock[k]);
        i = iCounter--;
        releasePoint = rpInc;
        if(i <= 0){
            Done = TRUE;
            LeaveCriticalSection(&BLock[k]);
            break;
        }

        for(j = 0; j < i; j++){
            if(A[j] > A[j+1]){
                temp = A[j];
                A[j] = A[j+1];
                A[j+1] = temp;
                exch = TRUE;
            }
            if(j == releasePoint){
                LeaveCriticalSection(&BLock[k++]);
                EnterCriticalSection(&BLock[k]);
                releasePoint += rpInc;
            }
        }
        LeaveCriticalSection(&BLock[k]);
        if(!exch) Done = TRUE;
    }
    return 0;
}
