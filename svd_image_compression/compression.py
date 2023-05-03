import numpy as np
import numpy.typing as npt


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
    
    def expanded(self) -> npt.NDArray:
        """Return the expanded matrix associated with this term.
        The expanded matrix has the same dimensions as the original
        matrix.

        Returns:
            npt.NDArray: the n x d matrix associated with this term.
        """


def SVD(A: npt.NDArray[np.float32]) -> list[SVDTerm]:
    """Return the singular value decomposition of (n x d) matrix A as a
    list of the decomposition terms, σ・u・vᵀ

    Args:
        A (npt.NDArray[np.float32]): A (n x d) matrix ('n' rows and 'd' columns)

    Returns:
        list[SVDTerm]: A list of of the decomposition terms. When the terms are
        expanded() and summed, the result equals A.
    """
