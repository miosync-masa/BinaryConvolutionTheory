"""
Binary Convolution Theory - Theorem 6 Verification
===================================================

Theorem 6 (Fermat Minimum Resonance):
    For Fermat numbers F_k = 2^(2^k) + 1,
        H(F_k²) = 2   (constant, independent of k)

Key insight:
    F_k = 1_00...0_1 (2^k - 1 zeros between the two 1s)
    - pop(F_k) = 2 (always!)
    - Centrally symmetric (the two 1-bits are equidistant from center)
    - By Theorem 3: H(F_k²) = pop(F_k) = 2

This is in stark contrast to Mersenne numbers where H(M_k²) = k grows!

Paper verification range: k ∈ [0, 4]

Known Fermat primes:
    F_0 = 3
    F_1 = 5
    F_2 = 17
    F_3 = 257
    F_4 = 65537
    (No other Fermat primes are known!)
"""

import sys
from pathlib import Path
from typing import Tuple, List

from src.core import (
    H, C, L_parallel, binary_convolution, popcount, 
    bin_str, is_fermat, is_centrally_symmetric, bit_positions
)


def fermat(k: int) -> int:
    """
    Compute Fermat number F_k = 2^(2^k) + 1.
    
    Args:
        k: Index (k >= 0)
        
    Returns:
        F_k = 2^(2^k) + 1
        
    Example:
        >>> fermat(0)
        3
        >>> fermat(2)
        17
    """
    if k < 0:
        raise ValueError("k must be >= 0")
    return (1 << (1 << k)) + 1


# Known Fermat primes (only 5 known as of 2024)
FERMAT_PRIMES = {
    0: 3,      # F_0 = 2^1 + 1
    1: 5,      # F_1 = 2^2 + 1
    2: 17,     # F_2 = 2^4 + 1
    3: 257,    # F_3 = 2^8 + 1
    4: 65537,  # F_4 = 2^16 + 1
}


def is_fermat_prime(n: int) -> Tuple[bool, int]:
    """
    Check if n is a known Fermat prime.
    
    Returns:
        (is_fermat_prime, k) where k is the index if it's a Fermat prime
    """
    for k, f_k in FERMAT_PRIMES.items():
        if n == f_k:
            return True, k
    return False, -1


def verify_theorem6_single(k: int) -> Tuple[bool, dict]:
    """
    Verify Theorem 6 for a single Fermat number F_k.
    
    Check: H(F_k²) = 2 (constant)
    
    Returns:
        (passed, details_dict)
    """
    f_k = fermat(k)
    h = H(f_k, f_k)
    pop_f = popcount(f_k)
    symmetric = is_centrally_symmetric(f_k)
    positions = bit_positions(f_k)
    
    # The claim: H = 2 always
    passed = (h == 2)
    
    # Also verify pop = 2 and symmetry (the reasons why H = 2)
    pop_is_2 = (pop_f == 2)
    
    return passed, {
        'k': k,
        'F_k': f_k,
        'binary': bin_str(f_k),
        'bit_length': f_k.bit_length(),
        'bit_positions': sorted(positions),
        'H_Fk2': h,
        'pop_Fk': pop_f,
        'expected_H': 2,
        'is_symmetric': symmetric,
        'pop_is_2': pop_is_2,
        'passed': passed
    }


def verify_fermat_convolution(k: int) -> dict:
    """
    Analyze the convolution pattern for F_k self-convolution.
    
    Expected pattern: [1, 0, 0, ..., 0, 2, 0, ..., 0, 0, 1]
    (The middle coefficient is 2, rest are 0 or 1)
    
    Returns:
        Details about the convolution
    """
    f_k = fermat(k)
    conv = binary_convolution(f_k, f_k)
    
    # Find non-zero positions
    nonzero_positions = [(i, int(v)) for i, v in enumerate(conv) if v > 0]
    max_val = int(max(conv))
    
    return {
        'k': k,
        'F_k': f_k,
        'convolution_length': len(conv),
        'nonzero_count': len(nonzero_positions),
        'nonzero_positions': nonzero_positions,
        'max_value': max_val,
        'H': max_val,
        # The pattern should be sparse: only 3 non-zero values
        'is_sparse': len(nonzero_positions) == 3
    }


def verify_theorem6(k_range: Tuple[int, int] = (0, 4)) -> dict:
    """
    Verify Theorem 6 for a range of Fermat numbers.
    
    Args:
        k_range: (k_min, k_max) inclusive
        
    Returns:
        Summary statistics
    """
    k_min, k_max = k_range
    results = []
    violations = []
    
    for k in range(k_min, k_max + 1):
        passed, details = verify_theorem6_single(k)
        results.append(details)
        if not passed:
            violations.append(details)
    
    return {
        'theorem': 'Theorem 6 (Fermat Minimum Resonance)',
        'statement': 'H(F_k²) = 2 (constant, independent of k)',
        'range_checked': f'k ∈ [{k_min}, {k_max}]',
        'total_checked': len(results),
        'violations': len(violations),
        'verified': len(violations) == 0,
        'results': results,
        'violation_details': violations
    }


def compare_mersenne_fermat(k_max: int = 10) -> dict:
    """
    Compare Mersenne and Fermat self-convolution heights.
    
    Shows the stark contrast:
        - Mersenne: H(M_k²) = k (grows linearly)
        - Fermat: H(F_k²) = 2 (constant)
    
    Args:
        k_max: Maximum k for Mersenne (Fermat limited to k=4)
        
    Returns:
        Comparison data
    """
    from .thm4_5_mersenne import mersenne
    
    comparison = []
    
    for k in range(2, min(k_max + 1, 5)):  # Fermat only known up to k=4
        m_k = mersenne(k)
        f_k = fermat(k) if k <= 4 else None
        
        h_mersenne = H(m_k, m_k)
        h_fermat = H(f_k, f_k) if f_k else None
        
        comparison.append({
            'k': k,
            'M_k': m_k,
            'F_k': f_k,
            'H_Mersenne': h_mersenne,
            'H_Fermat': h_fermat,
            'Mersenne_grows': h_mersenne == k,
            'Fermat_constant': h_fermat == 2 if h_fermat else None
        })
    
    return {
        'comparison': comparison,
        'insight': 'Mersenne: H grows as k. Fermat: H = 2 always.'
    }


def print_results(result: dict):
    """Pretty print verification results."""
    print(f"\n{'='*70}")
    print(f"  {result['theorem']}")
    print(f"{'='*70}")
    print(f"  Statement: {result['statement']}")
    print(f"  Range: {result['range_checked']}")
    print(f"  VERIFIED: {'✓ YES' if result['verified'] else '✗ NO'}")
    print()
    print("  k │      F_k │ binary                            │ H(F_k²) │ pop │ symmetric")
    print("  ──┼──────────┼───────────────────────────────────┼─────────┼─────┼──────────")
    for r in result['results']:
        status = '✓' if r['passed'] else '✗'
        binary_display = r['binary']
        if len(binary_display) > 33:
            binary_display = binary_display[:15] + '...' + binary_display[-15:]
        print(f"  {r['k']:2d} │ {r['F_k']:8d} │ {binary_display:>33s} │ {r['H_Fk2']:7d} │ {r['pop_Fk']:3d} │ {str(r['is_symmetric']):>5s} {status}")
    print()


def print_convolution_analysis(k_max: int = 4):
    """Print detailed convolution analysis for Fermat numbers."""
    print(f"\n{'='*70}")
    print("  Fermat Convolution Patterns (Sparsity Analysis)")
    print(f"{'='*70}")
    
    for k in range(0, k_max + 1):
        info = verify_fermat_convolution(k)
        print(f"\n  F_{k} = {info['F_k']}")
        print(f"    Convolution length: {info['convolution_length']}")
        print(f"    Non-zero positions: {info['nonzero_positions']}")
        print(f"    H = max = {info['H']}")
        print(f"    Sparse (only 3 non-zero): {'✓' if info['is_sparse'] else '✗'}")


if __name__ == "__main__":
    print("="*70)
    print(" BCT Theorem 6 (Fermat Minimum Resonance) Verification")
    print("="*70)
    
    # Main verification: k ∈ [0, 4]
    result = verify_theorem6((0, 4))
    print_results(result)
    
    # Convolution pattern analysis
    print_convolution_analysis(4)
    
    # Comparison with Mersenne
    print(f"\n{'='*70}")
    print("  Mersenne vs Fermat: The Contrast")
    print(f"{'='*70}")
    print()
    print("  Type     │ k=2 │ k=3 │ k=4 │ Pattern")
    print("  ─────────┼─────┼─────┼─────┼─────────────────")
    
    # Define mersenne locally for standalone execution
    def mersenne(k):
        return (1 << k) - 1
    
    h_m = [H(mersenne(k), mersenne(k)) for k in [2, 3, 4]]
    h_f = [H(fermat(k), fermat(k)) for k in [2, 3, 4]]
    
    print(f"  Mersenne │ {h_m[0]:3d} │ {h_m[1]:3d} │ {h_m[2]:3d} │ H = k (grows!)")
    print(f"  Fermat   │ {h_f[0]:3d} │ {h_f[1]:3d} │ {h_f[2]:3d} │ H = 2 (constant!)")
    print()
    
    # Extended test (larger k for Fermat, but numbers get huge!)
    print(f"\n{'='*70}")
    print("  Extended Test: Fermat numbers with larger k")
    print(f"{'='*70}")
    
    for k in range(5, 8):
        f_k = fermat(k)
        h = H(f_k, f_k)
        pop_f = popcount(f_k)
        bit_len = f_k.bit_length()
        print(f"  F_{k}: bit_length = {bit_len:6d}, pop = {pop_f}, H = {h} {'✓' if h == 2 else '✗'}")
    
    print("\n  Note: F_k for k > 4 are composite (not prime), but H = 2 still holds!")
    
    # Summary
    print(f"\n{'='*70}")
    print(" Summary")
    print(f"{'='*70}")
    print(f"  Theorem 6: {'✓ VERIFIED' if result['verified'] else '✗ FAILED'}")
    print(f"  Key insight: Fermat numbers have MINIMUM resonance (H = 2)")
    print(f"               while Mersenne numbers have MAXIMUM resonance (H = k)")
    print()
