#!/bin/python3

import sys
import math

t = int(input().strip())
for a0 in range(t):
    n, k = input().strip().split(' ')
    n, k = [int(n),int(k)]
    
    print(" ".join(list(map(str, max_permutation(n, k)))))
