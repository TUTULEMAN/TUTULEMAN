import numpy as np

class Solution:
    def checkRecord(self, n: int) -> int:

        T = np.array([[1, 1, 0, 1, 0, 0],
                      [1, 0, 1, 1, 0, 0],
                      [1, 0, 0, 1, 0, 0],
                      [0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 1, 0, 1],
                      [0, 0, 0, 1, 0, 0]])

        def matPow(A, p):
            result = np.eye(6, dtype=int)
            while p > 0:
                if p % 2 == 1:
                    result = (result @ A) % (10**9 + 7)
                A = (A @ A) % (10**9 + 7)
                p //= 2
            return result

        A = matPow(T, n)

        return int(sum(A[0]) % (10**9 + 7))
