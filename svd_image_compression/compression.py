from functools import reduce
import numpy as np
import numpy.typing as npt
import numpy.linalg as LA


eps = 1e-6

def is_zero(x: float) -> bool:
    return abs(x) < eps

def formated_list(lst: list[float]) -> str:
    if(hasattr(lst[0], '__iter__')):
        return str([formated_list(l) for l in lst])
    else:
        return str([float("{:0.2f}".format(e)) for e in lst])

class SVDTerm:
    sing_value: np.float32                 # sigma
    left_vector: npt.NDArray[np.float32]   # u
    right_vector: npt.NDArray[np.float32]  # v
    
    def __init__(self, sigma: np.float32, u: npt.NDArray[np.float32], v: npt.NDArray[np.float32]):
        """A term in the SVD decomposition of an n x d matrix ('n' rows and 'd' columns).

        Args:
            sigma (np.float32): singular value
            u (npt.NDArray[np.float32]): n x 1 column matrix
            v (npt.NDArray[np.float32]): d x 1 column matrix
        """
        self.sing_value = sigma
        self.left_vector = u
        self.right_vector = v
    
    def expanded(self) -> npt.NDArray[np.float32]:
        """Return the expanded matrix associated with this term.
        The expanded matrix has the same dimensions as the original
        matrix.

        Returns:
            npt.NDArray: the n x d matrix associated with this term.
        """
        return self.sing_value * (self.left_vector @ self.right_vector.T)
    
    def __repr__(self):
        return "{:0.2f} ・ {} ・ {}".format(
            self.sing_value,
            formated_list(self.left_vector),
            formated_list(self.right_vector.T)
        )

def SVD(A: npt.NDArray[np.float32]) -> list[SVDTerm]:
    """Return the singular value decomposition of (n x d) matrix A as a
    list of the decomposition terms, σ・u・vᵀ

    Args:
        A (npt.NDArray[np.float32]): a (n x d) matrix ('n' rows and 'd' columns)

    Returns:
        list[SVDTerm]: A list of of the decomposition terms. When the terms are
        expanded() and summed, the result equals A.
    """
    # matrices must always have 2 dimensions, i.e., don't do np.array([1,2,3]), do np.array([[1,2,3]])
    ATA = A.T @ A
    # eigenvectors are already normalized
    eig_vals, V = LA.eig(ATA)
    sing_vals = eig_vals**(1/2)
    
    terms = [
        SVDTerm(
            sing_vals[j],
            (A @ V[:,j].reshape((-1, 1)))/sing_vals[j],
            V[:,j].reshape((-1, 1))
        )
        for j in range(len(sing_vals))
        if not is_zero(sing_vals[j])
    ]
    terms.sort(key=lambda term: term.sing_value, reverse=True)
    return terms

def sum_terms(term_list: list[SVDTerm], how_many: int = -1) -> npt.NDArray[np.float32]:
    if how_many == -1:
        how_many = len(term_list)
    assert how_many <= len(term_list), "There are not enough terms in the list to sum"
    a_term = term_list[0]
    m = a_term.left_vector.shape[0]
    n = a_term.right_vector.shape[0]
    return reduce(lambda Ak, term: Ak + term.expanded(), term_list[0:how_many], np.zeros((m, n)))

# test
if __name__ == "__main__":
    A = [
        [1, 0, -1, 4],
        [-2, 1, 4, 3],
        [-2, 1, 4, -3],
        [-2, 5, 4, 3]
    ]
    A = np.array(A, dtype=np.float32)
    terms = SVD(A, False)
    print(*terms, sep='\n\n')
    print('\n', sum_terms(terms), '\n')