"""
Binary Convolution Theory - BCT Invariants
===========================================

Core definitions of the three BCT invariants:
    - H(a, b): Binary Convolution Height
    - C(a, b): Carry Count  
    - L(a, b): Chain Length

And the central concept:
    - BCT-perfectness

References:
    - Definition 2.3 (Binary Convolution)
    - Definition 2.4 (Binary Convolution Height)
    - Definition 2.5 (Carry Count)
    - Definition 2.6 (Chain Length)
    - Definition 2.7 (BCT-Perfect)
"""

from typing import Tuple, List, Optional
import numpy as np
from .binary_utils import bin_seq, popcount, get_factorizations


def binary_convolution(a: int, b: int) -> np.ndarray:
    """
    Compute the binary convolution of two integers.
    
    This is the convolution BEFORE carry propagation:
        (bin(a) * bin(b))_k = Σ_{i+j=k} a_i · b_j
    
    The result may contain values greater than 1.
    
    Args:
        a, b: Positive integers
        
    Returns:
        numpy array of convolution coefficients
        
    Example:
        >>> binary_convolution(3, 5)  # 11 * 101
        array([1, 1, 1, 1])  # before carry: positions 0,1,2,3
    """
    if a <= 0 or b <= 0:
        raise ValueError("Both a and b must be positive integers")
    
    bits_a = bin_seq(a)
    bits_b = bin_seq(b)
    
    # Full convolution (no carry propagation)
    conv = np.convolve(bits_a, bits_b)
    
    return conv


def H(a: int, b: int) -> int:
    """
    Binary Convolution Height.
    
    H(a, b) := max_k (bin(a) * bin(b))_k
    
    This measures the maximum "overlap" in the convolution.
    H = 1 means binary orthogonality (no overlap).
    
    Args:
        a, b: Positive integers
        
    Returns:
        Maximum value in the pre-carry convolution
        
    Example:
        >>> H(3, 5)   # 11 * 101 → orthogonal
        1
        >>> H(7, 7)   # 111 * 111 → Mersenne self-conv
        3
    """
    conv = binary_convolution(a, b)
    return int(np.max(conv))


def H_n2(n: int) -> int:
    """
    Convenience function for self-convolution height H(n, n) = H(n²).
    
    Args:
        n: Positive integer
        
    Returns:
        H(n, n)
    """
    return H(n, n)


def C(a: int, b: int) -> int:
    """
    Carry Count (Total Carry).
    
    C(a, b) := Σ_{c_k ≥ 2} (c_k - 1)
    
    This counts the total "excess mass" above 1 in the pre-carry convolution.
    It is an invariant of the convolution sequence.
    
    Args:
        a, b: Positive integers
        
    Returns:
        Total carry count
        
    Example:
        >>> C(7, 7)   # Mersenne M_3, should be (3-1)² = 4
        4
    """
    conv = binary_convolution(a, b)
    # Sum of (c_k - 1) for all c_k >= 2
    return int(np.sum(np.maximum(conv - 1, 0)))


def L(a: int, b: int) -> int:
    """
    Chain Length (Sequential LSB→MSB sweep model).
    
    L(a, b) is the number of sequential sweeps required to reduce
    the convolution sequence to binary form (all values in {0, 1}).
    
    By Theorem 7 (Single-sweep normalization), L(a, b) = 1 for all a, b.
    This function verifies this property computationally.
    
    Args:
        a, b: Positive integers
        
    Returns:
        Number of sweeps (always 1 for sequential model)
    """
    conv = binary_convolution(a, b).tolist()
    
    sweeps = 0
    while any(c > 1 for c in conv):
        sweeps += 1
        # Single LSB→MSB sweep
        new_conv = []
        carry = 0
        for c in conv:
            total = c + carry
            new_conv.append(total % 2)
            carry = total // 2
        # Handle final carry
        while carry > 0:
            new_conv.append(carry % 2)
            carry //= 2
        conv = new_conv
    
    return max(sweeps, 1) if sweeps == 0 else sweeps


def L_parallel(a: int, b: int) -> int:
    """
    Chain Length under PARALLEL carry schedule.
    
    At each round, all positions are updated simultaneously:
        c'_k = (c_k mod 2) + floor(c_{k-1} / 2)
    
    This can exceed both 1 and H(a, b) due to ripple-carry phenomena.
    
    Args:
        a, b: Positive integers
        
    Returns:
        Number of parallel rounds needed
        
    Example:
        >>> L_parallel(7, 7)  # Mersenne M_3
        3
    """
    conv = binary_convolution(a, b).tolist()
    
    rounds = 0
    while any(c > 1 for c in conv):
        rounds += 1
        # Parallel update
        new_conv = []
        for k in range(len(conv)):
            remainder = conv[k] % 2
            carry_from_prev = conv[k-1] // 2 if k > 0 else 0
            new_conv.append(remainder + carry_from_prev)
        
        # Handle overflow beyond current length
        final_carry = conv[-1] // 2
        while final_carry > 0:
            new_conv.append(final_carry % 2)
            final_carry //= 2
        
        conv = new_conv
        
        # Safety: prevent infinite loops
        if rounds > 1000:
            raise RuntimeError("L_parallel exceeded 1000 rounds")
    
    return rounds


def is_binary_orthogonal(a: int, b: int) -> bool:
    """
    Check if two integers are binary orthogonal.
    
    a ⊥ b iff H(a, b) = 1
    
    Binary orthogonality means no bit overlap in convolution.
    
    Args:
        a, b: Positive integers
        
    Returns:
        True if H(a, b) = 1
    """
    return H(a, b) == 1


def is_bct_perfect(n: int) -> bool:
    """
    Check if n is BCT-perfect.
    
    An integer n is BCT-perfect if for every non-trivial factorization
    n = a × b (with 1 < a ≤ b < n), we have H(a, b) = 1.
    
    This means all factorizations are binary orthogonal.
    
    Args:
        n: Positive integer > 1
        
    Returns:
        True if n is BCT-perfect
        
    Example:
        >>> is_bct_perfect(15)  # 3 × 5, both sparse
        True
        >>> is_bct_perfect(21)  # 3 × 7 = 11 × 111
        False
    """
    if n <= 1:
        raise ValueError("n must be greater than 1")
    
    factorizations = get_factorizations(n, include_trivial=False)
    
    # Prime numbers have no non-trivial factorizations
    if not factorizations:
        return True  # Convention: primes are trivially BCT-perfect
    
    for a, b in factorizations:
        if H(a, b) != 1:
            return False
    
    return True


def bct_invariants(a: int, b: int) -> Tuple[int, int, int]:
    """
    Compute all three BCT invariants at once.
    
    Args:
        a, b: Positive integers
        
    Returns:
        (H, C, L) tuple
    """
    conv = binary_convolution(a, b)
    
    h = int(np.max(conv))
    c = int(np.sum(np.maximum(conv - 1, 0)))
    l = L(a, b)
    
    return h, c, l


def analyze_factorization(n: int) -> List[dict]:
    """
    Analyze all factorizations of n with BCT invariants.
    
    Args:
        n: Positive integer
        
    Returns:
        List of dicts with factorization info and invariants
    """
    results = []
    
    for a, b in get_factorizations(n, include_trivial=True):
        conv = binary_convolution(a, b)
        h, c, l = bct_invariants(a, b)
        
        results.append({
            'n': n,
            'a': a,
            'b': b,
            'bin_a': bin(a)[2:],
            'bin_b': bin(b)[2:],
            'convolution': conv.tolist(),
            'H': h,
            'C': c,
            'L': l,
            'orthogonal': h == 1
        })
    
    return results


def sigma(n: int) -> int:
    """
    Sum of divisors function σ(n).
    
    Used for perfect number analysis.
    
    Args:
        n: Positive integer
        
    Returns:
        Sum of all divisors of n
    """
    if n <= 0:
        raise ValueError("n must be positive")
    
    total = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total


def abundance_ratio(n: int) -> float:
    """
    Compute σ(n)/n (abundance ratio).
    
    Perfect numbers have σ(n)/n = 2.
    
    Args:
        n: Positive integer
        
    Returns:
        σ(n)/n
    """
    return sigma(n) / n


if __name__ == "__main__":
    print("=== BCT Invariants Tests ===\n")
    
    # Basic convolution
    print("Binary Convolution Tests:")
    print(f"  conv(3, 5) = {binary_convolution(3, 5)}")  # 11 * 101
    print(f"  conv(7, 7) = {binary_convolution(7, 7)}")  # 111 * 111 = [1,2,3,2,1]
    
    # H tests
    print("\nHeight H Tests:")
    print(f"  H(3, 5) = {H(3, 5)}")    # Should be 1 (orthogonal)
    print(f"  H(7, 7) = {H(7, 7)}")    # Should be 3 (Mersenne M_3)
    print(f"  H(15, 15) = {H(15, 15)}")  # Should be 4 (Mersenne M_4)
    
    # C tests (Mersenne carry formula)
    print("\nCarry Count C Tests:")
    print(f"  C(7, 7) = {C(7, 7)}")      # Should be (3-1)² = 4
    print(f"  C(15, 15) = {C(15, 15)}")  # Should be (4-1)² = 9
    print(f"  C(31, 31) = {C(31, 31)}")  # Should be (5-1)² = 16
    
    # L tests
    print("\nChain Length L Tests:")
    print(f"  L(7, 7) = {L(7, 7)}")            # Should be 1 (sequential)
    print(f"  L_parallel(7, 7) = {L_parallel(7, 7)}")  # Should be 3
    
    # BCT-perfect tests
    print("\nBCT-Perfect Tests:")
    print(f"  is_bct_perfect(15) = {is_bct_perfect(15)}")  # True (3×5)
    print(f"  is_bct_perfect(21) = {is_bct_perfect(21)}")  # False (3×7)
    print(f"  is_bct_perfect(51) = {is_bct_perfect(51)}")  # True (3×17)
    
    # Analyze a number
    print("\nFactorization Analysis for n=15:")
    for info in analyze_factorization(15):
        print(f"  {info['a']} × {info['b']}: H={info['H']}, "
              f"bin: {info['bin_a']} × {info['bin_b']}, orth={info['orthogonal']}")
    
    # Perfect number test
    print("\nPerfect Number Tests:")
    for n in [6, 28, 496]:
        print(f"  σ({n})/{n} = {abundance_ratio(n):.4f}")
