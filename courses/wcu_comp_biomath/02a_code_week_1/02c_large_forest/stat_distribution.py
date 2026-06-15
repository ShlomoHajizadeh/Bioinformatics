import numpy as np
from scipy.linalg import eig

def get_eigenvectors_for_eigenvalue_one(matrix):
    """
    Computes the eigenvectors corresponding to the eigenvalue 1 of a real nxn matrix.

    Parameters:
    matrix (np.ndarray): A real square matrix of shape (n, n).

    Returns:
    List[np.ndarray]: A list of eigenvectors corresponding to the eigenvalue 1.
    """

    # Step 1: Validate the input matrix
    if not isinstance(matrix, np.ndarray):
        raise ValueError("Input must be a numpy ndarray.")
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Input must be a square matrix.")

    # Step 2: Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = eig(matrix)

    # Step 3: Find indices where eigenvalue is 1
    indices = np.isclose(eigenvalues, 1)  # Use np.isclose for numerical stability

    # Step 4: Extract corresponding eigenvectors
    result = eigenvectors[:, indices]

    # Step 5: Check if there are any eigenvectors for eigenvalue 1
    if result.size == 0:
        print("No eigenvectors corresponding to the eigenvalue 1.")
        return []

    # Step 6: Return the list of eigenvectors
    return [result[:, i] for i in range(result.shape[1])]

# Example usage:
if __name__ == "__main__":
    # Define a larger sample nxn matrix
    A = np.array([[0.12, 0.14, 0.12, 0.12, 0.13], 
              [0.12, 0.05, 0.08, 0.28, 0.27], 
              [0.12, 0.10, 0.10, 0.05, 0.08],
              [0.42, 0.53, 0.32, 0.20, 0.19],
              [0.22, 0.18, 0.38, 0.35, 0.33]])
    
    # Get eigenvectors corresponding to the eigenvalue 1
    eigenvectors = get_eigenvectors_for_eigenvalue_one(A)
    
    # Print the results
    if eigenvectors:
        for idx, vec in enumerate(eigenvectors):
            print(f"Eigenvector {idx + 1}: {vec}")