"""
Binary Convolution Theory - Binary Utilities
=============================================

Basic utilities for binary representation operations.

References:
    - Definition 2.1 (Binary Representation)
    - popcount (Hamming weight)
"""

from typing import List, Set, Tuple
import numpy as np


def bin_seq(n: int) -> np.ndarray:
    """
    Return binary representation as a coefficient sequence.
    
    For a positive integer n, returns (b_0, b_1, ..., b_k) where
    n = Σ b_i * 2^i and b_i ∈ {0, 1}.
    
    Args:
        n: Positive integer
        
    Returns:
        numpy array of binary coefficients, LSB first
        
    Example:
        >>> bin_seq(13)  # 13 = 1101 in binary
        array([1, 0, 1, 1])
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    bits = []
    while n > 0:
        bits.append(n & 1)
        n >>= 1
    return np.array(bits, dtype=np.int64)


def popcount(n: int) -> int:
    """
    Count the number of 1-bits (Hamming weight / digit sum in base 2).
    
    This is the function pop(n) = Σ b_i in the paper.
    
    Args:
        n: Non-negative integer
        
    Returns:
        Number of 1-bits in binary representation
        
    Example:
        >>> popcount(13)  # 1101 has three 1-bits
        3
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return bin(n).count('1')


def bit_positions(n: int) -> Set[int]:
    """
    Return the set of positions where 1-bits occur.
    
    For analyzing sumsets S_i + S_j in orthogonality proofs.
    
    Args:
        n: Positive integer
        
    Returns:
        Set of bit positions (0-indexed from LSB)
        
    Example:
        >>> bit_positions(13)  # 1101 = bits at 0, 2, 3
        {0, 2, 3}
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    positions = set()
    pos = 0
    while n > 0:
        if n & 1:
            positions.add(pos)
        n >>= 1
        pos += 1
    return positions


def bit_length(n: int) -> int:
    """
    Return the number of bits needed to represent n.
    
    Args:
        n: Positive integer
        
    Returns:
        Bit length (position of highest 1-bit + 1)
        
    Example:
        >>> bit_length(13)  # 1101 needs 4 bits
        4
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    return n.bit_length()


def is_power_of_two(n: int) -> bool:
    """
    Check if n is a power of 2.
    
    Used for Lemma 5 (Power of Two Orthogonality).
    
    Args:
        n: Positive integer
        
    Returns:
        True if n = 2^k for some k ≥ 0
    """
    if n <= 0:
        return False
    return (n & (n - 1)) == 0


def is_mersenne(n: int) -> Tuple[bool, int]:
    """
    Check if n is a Mersenne number M_k = 2^k - 1.
    
    Args:
        n: Positive integer
        
    Returns:
        (is_mersenne, k) where k is the exponent if Mersenne, else -1
        
    Example:
        >>> is_mersenne(31)  # 31 = 2^5 - 1
        (True, 5)
    """
    if n <= 0:
        return False, -1
    
    # M_k = 2^k - 1 means all bits are 1
    # Check if n+1 is a power of 2
    m = n + 1
    if is_power_of_two(m):
        k = m.bit_length() - 1
        return True, k
    return False, -1


def is_fermat(n: int) -> Tuple[bool, int]:
    """
    Check if n is a Fermat number F_k = 2^(2^k) + 1.
    
    Used for Theorem 6 (Fermat Minimum Resonance) and Lemma C.
    
    Args:
        n: Positive integer
        
    Returns:
        (is_fermat, k) where k is the index if Fermat number, else -1
        
    Example:
        >>> is_fermat(17)  # 17 = 2^4 + 1 = 2^(2^2) + 1 = F_2
        (True, 2)
    """
    if n <= 1:
        return False, -1
    
    # F_k = 2^(2^k) + 1, so n-1 must be 2^(2^k)
    m = n - 1
    if not is_power_of_two(m):
        return False, -1
    
    # m = 2^(2^k), so log2(m) must be a power of 2
    exp = m.bit_length() - 1  # log2(m)
    if exp == 0:
        # m = 1 = 2^0, so 2^k = 0, meaning k doesn't exist in usual sense
        # But F_0 = 2^1 + 1 = 3, so m = 2, exp = 1 = 2^0, k = 0
        return False, -1
    
    if is_power_of_two(exp):
        k = exp.bit_length() - 1  # log2(exp) = k
        return True, k
    
    # Special case: F_0 = 3 (2^(2^0) + 1 = 2^1 + 1 = 3)
    if n == 3:
        return True, 0
    
    return False, -1


def is_centrally_symmetric(n: int) -> bool:
    """
    Check if the 1-bit positions of n are centrally symmetric.
    
    Used for Theorem 3 (Equality Condition): H(n²) = pop(n) iff symmetric.
    
    The bit positions form a symmetric set with respect to some center k/2.
    
    Args:
        n: Positive integer
        
    Returns:
        True if bit positions are centrally symmetric
        
    Example:
        >>> is_centrally_symmetric(7)   # 111: symmetric around center
        True
        >>> is_centrally_symmetric(5)   # 101: symmetric around position 1
        True
        >>> is_centrally_symmetric(11)  # 1011: not symmetric
        False
    """
    positions = bit_positions(n)
    if len(positions) <= 1:
        return True
    
    pos_list = sorted(positions)
    center = (pos_list[0] + pos_list[-1]) / 2
    
    for p in pos_list:
        mirror = 2 * center - p
        if mirror != int(mirror) or int(mirror) not in positions:
            return False
    
    return True


# Known Fermat primes (only 5 known)
FERMAT_PRIMES = [3, 5, 17, 257, 65537]  # F_0 to F_4


def get_factorizations(n: int, include_trivial: bool = False) -> List[Tuple[int, int]]:
    """
    Return all factorizations of n as (a, b) with a ≤ b.
    
    Args:
        n: Positive integer
        include_trivial: If True, include (1, n)
        
    Returns:
        List of (a, b) pairs where a * b = n and a ≤ b
        
    Example:
        >>> get_factorizations(12)
        [(2, 6), (3, 4)]
        >>> get_factorizations(12, include_trivial=True)
        [(1, 12), (2, 6), (3, 4)]
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    factors = []
    start = 1 if include_trivial else 2
    
    for a in range(start, int(n**0.5) + 1):
        if n % a == 0:
            b = n // a
            if a <= b and (include_trivial or b < n):
                factors.append((a, b))
    
    return factors


if __name__ == "__main__":
    # Quick tests
    print("=== Binary Utils Tests ===")
    
    # bin_seq
    print(f"bin_seq(13) = {bin_seq(13)}")  # [1, 0, 1, 1]
    
    # popcount
    print(f"popcount(13) = {popcount(13)}")  # 3
    
    # bit_positions
    print(f"bit_positions(13) = {bit_positions(13)}")  # {0, 2, 3}
    
    # Mersenne check
    print(f"is_mersenne(31) = {is_mersenne(31)}")  # (True, 5)
    print(f"is_mersenne(30) = {is_mersenne(30)}")  # (False, -1)
    
    # Fermat check
    print(f"is_fermat(3) = {is_fermat(3)}")    # (True, 0)
    print(f"is_fermat(5) = {is_fermat(5)}")    # (True, 1)
    print(f"is_fermat(17) = {is_fermat(17)}")  # (True, 2)
    print(f"is_fermat(7) = {is_fermat(7)}")    # (False, -1)
    
    # Central symmetry
    print(f"is_centrally_symmetric(7) = {is_centrally_symmetric(7)}")    # True (111)
    print(f"is_centrally_symmetric(5) = {is_centrally_symmetric(5)}")    # True (101)
    print(f"is_centrally_symmetric(11) = {is_centrally_symmetric(11)}")  # False (1011)
    
    # Factorizations
    print(f"get_factorizations(12) = {get_factorizations(12)}")
    print(f"get_factorizations(15) = {get_factorizations(15)}")
