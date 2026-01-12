"""
Binary Convolution Theory - Theorem 4 & 5 Verification
=======================================================

Theorem 4 (Mersenne Equality):
    For Mersenne numbers M_k = 2^k - 1,
        H(M_k²) = k = pop(M_k)

Theorem 5 (Mersenne Carry Formula):
    For Mersenne numbers M_k = 2^k - 1,
        C(M_k²) = (k-1)²

Key insight:
    M_k = 111...1 (k ones) is maximally symmetric.
    Self-convolution forms the perfect triangle [1, 2, 3, ..., k, ..., 3, 2, 1].

Paper verification range: k ∈ [2, 15]
"""

import sys
from pathlib import Path
from typing import Tuple, List
import numpy as np

from ..core import H, C, binary_convolution, popcount, bin_str, is_mersenne


def mersenne(k: int) -> int:
    """
    Compute Mersenne number M_k = 2^k - 1.
    
    Args:
        k: Exponent (k >= 1)
        
    Returns:
        M_k = 2^k - 1
        
    Example:
        >>> mersenne(3)
        7
        >>> mersenne(5)
        31
    """
    if k < 1:
        raise ValueError("k must be >= 1")
    return (1 << k) - 1


def expected_mersenne_convolution(k: int) -> List[int]:
    """
    Return the expected convolution pattern for M_k self-convolution.
    
    The pattern is the perfect triangle: [1, 2, 3, ..., k, ..., 3, 2, 1]
    
    Args:
        k: Mersenne exponent
        
    Returns:
        List representing [1, 2, ..., k, ..., 2, 1]
    """
    # Ascending: 1, 2, ..., k
    ascending = list(range(1, k + 1))
    # Descending: k-1, k-2, ..., 1
    descending = list(range(k - 1, 0, -1))
    return ascending + descending


def expected_carry_count(k: int) -> int:
    """
    Compute the expected carry count C(M_k²) = (k-1)².
    
    Derivation from paper:
        Convolution [1, 2, ..., k, ..., 2, 1] has carry contributions (c-1) for c >= 2.
        Sum = 2 * Σ_{i=2}^{k-1} (i-1) + (k-1)
            = 2 * Σ_{j=1}^{k-2} j + (k-1)
            = 2 * (k-2)(k-1)/2 + (k-1)
            = (k-2)(k-1) + (k-1)
            = (k-1)(k-2+1)
            = (k-1)²
    
    Args:
        k: Mersenne exponent
        
    Returns:
        (k-1)²
    """
    return (k - 1) ** 2


def verify_theorem4_single(k: int) -> Tuple[bool, dict]:
    """
    Verify Theorem 4 for a single Mersenne number M_k.
    
    Check: H(M_k²) = k = pop(M_k)
    
    Returns:
        (passed, details_dict)
    """
    m_k = mersenne(k)
    h = H(m_k, m_k)
    pop_m = popcount(m_k)
    
    # All three should equal k
    h_equals_k = (h == k)
    pop_equals_k = (pop_m == k)
    passed = h_equals_k and pop_equals_k
    
    return passed, {
        'k': k,
        'M_k': m_k,
        'binary': bin_str(m_k),
        'H_Mk2': h,
        'pop_Mk': pop_m,
        'expected': k,
        'H_equals_k': h_equals_k,
        'pop_equals_k': pop_equals_k,
        'passed': passed
    }


def verify_theorem5_single(k: int) -> Tuple[bool, dict]:
    """
    Verify Theorem 5 for a single Mersenne number M_k.
    
    Check: C(M_k²) = (k-1)²
    
    Returns:
        (passed, details_dict)
    """
    m_k = mersenne(k)
    c = C(m_k, m_k)
    expected = expected_carry_count(k)
    
    passed = (c == expected)
    
    return passed, {
        'k': k,
        'M_k': m_k,
        'binary': bin_str(m_k),
        'C_Mk2': c,
        'expected': expected,
        'formula': f'({k}-1)² = {expected}',
        'passed': passed
    }


def verify_convolution_pattern(k: int) -> Tuple[bool, dict]:
    """
    Verify that M_k self-convolution forms the perfect triangle.
    
    Expected: [1, 2, 3, ..., k, ..., 3, 2, 1]
    
    Returns:
        (matches, details_dict)
    """
    m_k = mersenne(k)
    conv = binary_convolution(m_k, m_k)
    conv_list = conv.tolist() 
    expected = expected_mersenne_convolution(k)

    matches = conv_list == expected 
    
    return matches, {
        'k': k,
        'M_k': m_k,
        'convolution': conv_list,
        'expected': expected,
        'matches': matches,
        'is_triangle': matches
    }


def verify_theorem4(k_range: Tuple[int, int] = (2, 15)) -> dict:
    """
    Verify Theorem 4 for a range of Mersenne exponents.
    
    Args:
        k_range: (k_min, k_max) inclusive
        
    Returns:
        Summary statistics
    """
    k_min, k_max = k_range
    results = []
    violations = []
    
    for k in range(k_min, k_max + 1):
        passed, details = verify_theorem4_single(k)
        results.append(details)
        if not passed:
            violations.append(details)
    
    return {
        'theorem': 'Theorem 4 (Mersenne Equality)',
        'statement': 'H(M_k²) = k = pop(M_k)',
        'range_checked': f'k ∈ [{k_min}, {k_max}]',
        'total_checked': len(results),
        'violations': len(violations),
        'verified': len(violations) == 0,
        'results': results,
        'violation_details': violations
    }


def verify_theorem5(k_range: Tuple[int, int] = (2, 15)) -> dict:
    """
    Verify Theorem 5 for a range of Mersenne exponents.
    
    Args:
        k_range: (k_min, k_max) inclusive
        
    Returns:
        Summary statistics
    """
    k_min, k_max = k_range
    results = []
    violations = []
    
    for k in range(k_min, k_max + 1):
        passed, details = verify_theorem5_single(k)
        results.append(details)
        if not passed:
            violations.append(details)
    
    return {
        'theorem': 'Theorem 5 (Mersenne Carry Formula)',
        'statement': 'C(M_k²) = (k-1)²',
        'range_checked': f'k ∈ [{k_min}, {k_max}]',
        'total_checked': len(results),
        'violations': len(violations),
        'verified': len(violations) == 0,
        'results': results,
        'violation_details': violations
    }


def verify_convolution_patterns(k_range: Tuple[int, int] = (2, 15)) -> dict:
    """
    Verify that all Mersenne self-convolutions form perfect triangles.
    
    Args:
        k_range: (k_min, k_max) inclusive
        
    Returns:
        Summary statistics
    """
    k_min, k_max = k_range
    results = []
    non_triangles = []
    
    for k in range(k_min, k_max + 1):
        matches, details = verify_convolution_pattern(k)
        results.append(details)
        if not matches:
            non_triangles.append(details)
    
    return {
        'property': 'Mersenne Triangle Pattern',
        'statement': 'conv(M_k, M_k) = [1, 2, ..., k, ..., 2, 1]',
        'range_checked': f'k ∈ [{k_min}, {k_max}]',
        'total_checked': len(results),
        'non_triangles': len(non_triangles),
        'all_triangles': len(non_triangles) == 0,
        'results': results
    }


def print_theorem4_results(result: dict):
    """Pretty print Theorem 4 results."""
    print(f"\n{'='*60}")
    print(f"  {result['theorem']}")
    print(f"{'='*60}")
    print(f"  Statement: {result['statement']}")
    print(f"  Range: {result['range_checked']}")
    print(f"  VERIFIED: {'✓ YES' if result['verified'] else '✗ NO'}")
    print()
    print("  k │   M_k │ binary          │ H(M_k²) │ pop(M_k) │ expected")
    print("  ──┼───────┼─────────────────┼─────────┼──────────┼─────────")
    for r in result['results']:
        status = '✓' if r['passed'] else '✗'
        print(f"  {r['k']:2d} │ {r['M_k']:5d} │ {r['binary']:>15s} │ {r['H_Mk2']:7d} │ {r['pop_Mk']:8d} │ {r['expected']:7d} {status}")
    print()


def print_theorem5_results(result: dict):
    """Pretty print Theorem 5 results."""
    print(f"\n{'='*60}")
    print(f"  {result['theorem']}")
    print(f"{'='*60}")
    print(f"  Statement: {result['statement']}")
    print(f"  Range: {result['range_checked']}")
    print(f"  VERIFIED: {'✓ YES' if result['verified'] else '✗ NO'}")
    print()
    print("  k │   M_k │ C(M_k²) │ (k-1)² │ formula")
    print("  ──┼───────┼─────────┼────────┼─────────────")
    for r in result['results']:
        status = '✓' if r['passed'] else '✗'
        print(f"  {r['k']:2d} │ {r['M_k']:5d} │ {r['C_Mk2']:7d} │ {r['expected']:6d} │ {r['formula']} {status}")
    print()


def print_convolution_patterns(result: dict, show_all: bool = False):
    """Pretty print convolution pattern results."""
    print(f"\n{'='*60}")
    print(f"  {result['property']}")
    print(f"{'='*60}")
    print(f"  Statement: {result['statement']}")
    print(f"  Range: {result['range_checked']}")
    print(f"  All triangles: {'✓ YES' if result['all_triangles'] else '✗ NO'}")
    print()
    
    if show_all:
        for r in result['results']:
            status = '✓' if r['matches'] else '✗'
            print(f"  k={r['k']}: {r['convolution']} {status}")
    else:
        # Show just first few
        for r in result['results'][:5]:
            status = '✓' if r['matches'] else '✗'
            print(f"  k={r['k']}: {r['convolution']} {status}")
        if len(result['results']) > 5:
            print(f"  ... ({len(result['results']) - 5} more)")
    print()


if __name__ == "__main__":
    print("="*60)
    print(" BCT Theorem 4 & 5 (Mersenne) Verification")
    print("="*60)
    
    # Paper range: k ∈ [2, 15]
    k_range = (2, 15)
    
    # Theorem 4: H(M_k²) = k = pop(M_k)
    result4 = verify_theorem4(k_range)
    print_theorem4_results(result4)
    
    # Theorem 5: C(M_k²) = (k-1)²
    result5 = verify_theorem5(k_range)
    print_theorem5_results(result5)
    
    # Bonus: Verify convolution patterns
    print("\n[Bonus: Convolution Triangle Patterns]")
    conv_result = verify_convolution_patterns(k_range)
    print_convolution_patterns(conv_result, show_all=True)
    
    # Summary
    print("="*60)
    print(" Summary")
    print("="*60)
    print(f"  Theorem 4 (H = k = pop): {'✓ VERIFIED' if result4['verified'] else '✗ FAILED'}")
    print(f"  Theorem 5 (C = (k-1)²): {'✓ VERIFIED' if result5['verified'] else '✗ FAILED'}")
    print(f"  Triangle patterns: {'✓ ALL MATCH' if conv_result['all_triangles'] else '✗ SOME MISMATCH'}")
    print()
    
    # Extended range test
    print("\n[Extended range: k ∈ [2, 20]]")
    ext_result4 = verify_theorem4((2, 20))
    ext_result5 = verify_theorem5((2, 20))
    print(f"  Theorem 4 (k ≤ 20): {'✓ VERIFIED' if ext_result4['verified'] else '✗ FAILED'}")
    print(f"  Theorem 5 (k ≤ 20): {'✓ VERIFIED' if ext_result5['verified'] else '✗ FAILED'}")
    
    # Show largest Mersenne tested
    largest = ext_result4['results'][-1]
    print(f"\n  Largest tested: M_20 = {largest['M_k']}")
    print(f"    H(M_20²) = {largest['H_Mk2']}")
    print(f"    C(M_20²) = {ext_result5['results'][-1]['C_Mk2']}")
