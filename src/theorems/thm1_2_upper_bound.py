"""
Binary Convolution Theory - Theorem 1 & 2 Verification
=======================================================

Theorem 1 (Upper Bound):
    For any factorization n = a × b,
        H(a, b) ≤ min(pop(a), pop(b))

Theorem 2 (Self-Convolution Upper Bound):
    For any positive integer n,
        H(n²) := H(n, n) ≤ pop(n)

Paper verification range: n ∈ [2, 10^6]
"""

import sys
from pathlib import Path

from core import H, popcount, get_factorizations
from typing import Tuple, List, Optional
import time


def verify_theorem1_single(a: int, b: int) -> Tuple[bool, dict]:
    """
    Verify Theorem 1 for a single factorization.
    
    H(a, b) ≤ min(pop(a), pop(b))
    
    Returns:
        (passed, details_dict)
    """
    h = H(a, b)
    pop_a = popcount(a)
    pop_b = popcount(b)
    bound = min(pop_a, pop_b)
    
    passed = h <= bound
    
    return passed, {
        'a': a,
        'b': b,
        'n': a * b,
        'H': h,
        'pop_a': pop_a,
        'pop_b': pop_b,
        'bound': bound,
        'passed': passed
    }


def verify_theorem2_single(n: int) -> Tuple[bool, dict]:
    """
    Verify Theorem 2 for a single integer.
    
    H(n, n) ≤ pop(n)
    
    Returns:
        (passed, details_dict)
    """
    h = H(n, n)
    pop_n = popcount(n)
    
    passed = h <= pop_n
    
    return passed, {
        'n': n,
        'n_squared': n * n,
        'H_n2': h,
        'pop_n': pop_n,
        'passed': passed,
        'gap': pop_n - h  # How far below the bound
    }


def verify_theorem1(max_n: int = 10000, verbose: bool = True) -> dict:
    """
    Verify Theorem 1 for all factorizations up to max_n.
    
    Args:
        max_n: Maximum value of n = a × b to check
        verbose: Print progress updates
        
    Returns:
        Summary statistics
    """
    total_factorizations = 0
    violations = []
    max_h_seen = 0
    tightest_case = None  # Case where H = bound (equality)
    
    start_time = time.time()
    
    for n in range(4, max_n + 1):
        factorizations = get_factorizations(n, include_trivial=False)
        
        for a, b in factorizations:
            total_factorizations += 1
            passed, details = verify_theorem1_single(a, b)
            
            if not passed:
                violations.append(details)
            
            if details['H'] > max_h_seen:
                max_h_seen = details['H']
            
            # Track tightest case (H = bound)
            if details['H'] == details['bound']:
                if tightest_case is None or details['H'] > tightest_case['H']:
                    tightest_case = details
        
        if verbose and n % 10000 == 0:
            elapsed = time.time() - start_time
            print(f"  Checked n ≤ {n}, factorizations: {total_factorizations}, "
                  f"time: {elapsed:.1f}s")
    
    elapsed = time.time() - start_time
    
    result = {
        'theorem': 'Theorem 1 (Upper Bound)',
        'statement': 'H(a, b) ≤ min(pop(a), pop(b))',
        'range_checked': f'n ∈ [4, {max_n}]',
        'total_factorizations': total_factorizations,
        'violations': len(violations),
        'verified': len(violations) == 0,
        'max_H_observed': max_h_seen,
        'tightest_case': tightest_case,
        'time_seconds': elapsed
    }
    
    if violations:
        result['violation_examples'] = violations[:10]
    
    return result


def verify_theorem2(max_n: int = 10000, verbose: bool = True) -> dict:
    """
    Verify Theorem 2 for all integers up to max_n.
    
    Args:
        max_n: Maximum value of n to check
        verbose: Print progress updates
        
    Returns:
        Summary statistics
    """
    total_checked = 0
    violations = []
    max_h_seen = 0
    max_gap = 0
    gap_distribution = {}
    tightest_case = None
    
    start_time = time.time()
    
    for n in range(2, max_n + 1):
        total_checked += 1
        passed, details = verify_theorem2_single(n)
        
        if not passed:
            violations.append(details)
        
        # Track statistics
        h = details['H_n2']
        gap = details['gap']
        
        if h > max_h_seen:
            max_h_seen = h
        
        if gap > max_gap:
            max_gap = gap
        
        gap_distribution[gap] = gap_distribution.get(gap, 0) + 1
        
        # Track tightest case (H = pop, gap = 0)
        if gap == 0:
            if tightest_case is None or h > tightest_case['H_n2']:
                tightest_case = details
        
        if verbose and n % 50000 == 0:
            elapsed = time.time() - start_time
            print(f"  Checked n ≤ {n}, time: {elapsed:.1f}s")
    
    elapsed = time.time() - start_time
    
    result = {
        'theorem': 'Theorem 2 (Self-Convolution Upper Bound)',
        'statement': 'H(n, n) ≤ pop(n)',
        'range_checked': f'n ∈ [2, {max_n}]',
        'total_checked': total_checked,
        'violations': len(violations),
        'verified': len(violations) == 0,
        'max_H_observed': max_h_seen,
        'max_gap_observed': max_gap,
        'tightest_case': tightest_case,
        'gap_distribution': dict(sorted(gap_distribution.items())),
        'time_seconds': elapsed
    }
    
    if violations:
        result['violation_examples'] = violations[:10]
    
    return result


def find_equality_cases(max_n: int = 1000) -> List[dict]:
    """
    Find cases where H(n, n) = pop(n) (equality in Theorem 2).
    
    These correspond to centrally symmetric bit patterns (Theorem 3).
    
    Args:
        max_n: Maximum n to check
        
    Returns:
        List of equality cases with details
    """
    equality_cases = []
    
    for n in range(2, max_n + 1):
        h = H(n, n)
        pop_n = popcount(n)
        
        if h == pop_n:
            equality_cases.append({
                'n': n,
                'binary': bin(n)[2:],
                'H_n2': h,
                'pop_n': pop_n
            })
    
    return equality_cases


def print_results(result: dict):
    """Pretty print verification results."""
    print(f"\n{'='*60}")
    print(f"  {result['theorem']}")
    print(f"{'='*60}")
    print(f"  Statement: {result['statement']}")
    print(f"  Range: {result['range_checked']}")
    print(f"  Total checked: {result.get('total_checked', result.get('total_factorizations', 'N/A'))}")
    print(f"  Violations: {result['violations']}")
    print(f"  VERIFIED: {'✓ YES' if result['verified'] else '✗ NO'}")
    print(f"  Max H observed: {result['max_H_observed']}")
    
    if 'max_gap_observed' in result:
        print(f"  Max gap (pop - H): {result['max_gap_observed']}")
    
    if result.get('tightest_case'):
        tc = result['tightest_case']
        if 'a' in tc:
            print(f"  Tightest case: {tc['a']} × {tc['b']} = {tc['n']}, H = {tc['H']}")
        else:
            print(f"  Tightest case: n = {tc['n']}, H(n²) = {tc['H_n2']} = pop(n)")
    
    print(f"  Time: {result['time_seconds']:.2f}s")
    print()


if __name__ == "__main__":
    print("="*60)
    print(" BCT Theorem 1 & 2 Verification")
    print("="*60)
    
    # Quick test first
    print("\n[Quick test: n ≤ 1000]")
    
    result1 = verify_theorem1(max_n=1000, verbose=False)
    print_results(result1)
    
    result2 = verify_theorem2(max_n=1000, verbose=False)
    print_results(result2)
    
    # Show some equality cases for Theorem 2
    print("\n[Equality cases H(n,n) = pop(n) for n ≤ 100]")
    eq_cases = find_equality_cases(100)
    for case in eq_cases[:15]:
        print(f"  n = {case['n']:3d} = {case['binary']:>8s}₂, "
              f"H = pop = {case['H_n2']}")
    if len(eq_cases) > 15:
        print(f"  ... and {len(eq_cases) - 15} more")
    
    # Larger verification if requested
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action='store_true', 
                       help='Run full verification up to 10^5')
    args, _ = parser.parse_known_args()
    
    if args.full:
        print("\n" + "="*60)
        print(" Full Verification (n ≤ 100,000)")
        print("="*60)
        
        result1_full = verify_theorem1(max_n=100000, verbose=True)
        print_results(result1_full)
        
        result2_full = verify_theorem2(max_n=100000, verbose=True)
        print_results(result2_full)
