"""
Binary Convolution Theory - Theorem 7 & Proposition 5 Verification
===================================================================

Theorem 7 (Single-sweep normalization, LSB→MSB model):
    For any factorization n = a × b, a single sequential LSB→MSB sweep
    reduces the convolution sequence to binary form.
    Equivalently: L(a, b) = 1 for all a, b.

Proposition 5 (A family with arbitrarily long parallel carry chains):
    Let k ≥ 3 be odd and set m = (2^k + 1) / 3.
    Then H(3, m) = 2, while L_par(3, m) = k - 1.
    In particular, L_par can be arbitrarily large even when H = 2.

Key insight:
    - Sequential model: L = 1 ALWAYS (carries propagate immediately)
    - Parallel model: L_par can exceed H due to ripple-carry phenomena

Paper verification:
    - Theorem 7: n ∈ [4, 5000], all L = 1
    - Proposition 5: odd k ∈ [3, 21], all L_par(3, m) = k - 1
    - Statistics: max H = 8, max L_par = 14 for n ≤ 10^5
    - L_par = H holds only in 28.96% of cases with H > 1
"""

import sys
from pathlib import Path
from typing import Tuple, List, Dict
from collections import defaultdict
import time

from src.core import H, L, L_parallel, binary_convolution, popcount, get_factorizations


def sequential_sweep_detailed(conv: List[int]) -> Tuple[int, List[int]]:
    """
    Sequential LSB→MSB sweep with detailed tracking.
    
    Each position is processed in order, carries propagate immediately.
    
    Returns:
        (num_sweeps, final_sequence)
    """
    c = list(conv)
    sweeps = 0
    
    while max(c) > 1:
        sweeps += 1
        for k in range(len(c)):
            if c[k] >= 2:
                carry = c[k] // 2
                c[k] = c[k] % 2
                if k + 1 < len(c):
                    c[k + 1] += carry
                else:
                    c.append(carry)
        
        if sweeps > 100:  # Safety
            break
    
    return sweeps, c


def parallel_sweep_detailed(conv: List[int]) -> Tuple[int, List[int], List[List[int]]]:
    """
    Parallel sweep with detailed tracking of each round.
    
    All positions updated simultaneously using previous round's values.
    
    Returns:
        (num_rounds, final_sequence, history_of_each_round)
    """
    c = list(conv)
    rounds = 0
    history = [c.copy()]
    
    while max(c) > 1:
        rounds += 1
        new_c = [0] * (len(c) + 10)
        
        for k in range(len(c)):
            new_c[k] += c[k] % 2
            new_c[k + 1] += c[k] // 2
        
        # Trim trailing zeros
        while len(new_c) > 1 and new_c[-1] == 0:
            new_c.pop()
        
        c = new_c
        history.append(c.copy())
        
        if rounds > 100:  # Safety
            break
    
    return rounds, c, history


def verify_theorem7_single(a: int, b: int) -> Tuple[bool, dict]:
    """
    Verify Theorem 7 for a single factorization.
    
    Check: L(a, b) = 1 (sequential sweep always completes in 1 pass)
    
    Returns:
        (passed, details_dict)
    """
    conv = binary_convolution(a, b)
    l_seq = L(a, b)
    h = H(a, b)
    
    passed = (l_seq == 1) or (h == 1 and l_seq == 0)  # H=1 means no carries needed
    
    return passed, {
        'a': a,
        'b': b,
        'n': a * b,
        'H': h,
        'L_seq': l_seq,
        'expected': 1,
        'passed': passed
    }


def verify_theorem7(max_n: int = 5000, verbose: bool = True) -> dict:
    """
    Verify Theorem 7 for all factorizations up to max_n.
    
    Args:
        max_n: Maximum value of n = a × b
        verbose: Print progress
        
    Returns:
        Summary statistics
    """
    total = 0
    violations = []
    
    start_time = time.time()
    
    for n in range(4, max_n + 1):
        for a, b in get_factorizations(n, include_trivial=False):
            total += 1
            passed, details = verify_theorem7_single(a, b)
            
            if not passed:
                violations.append(details)
        
        if verbose and n % 1000 == 0:
            print(f"  Checked n ≤ {n}, factorizations: {total}")
    
    elapsed = time.time() - start_time
    
    return {
        'theorem': 'Theorem 7 (Single-sweep normalization)',
        'statement': 'L(a, b) = 1 for all factorizations',
        'range_checked': f'n ∈ [4, {max_n}]',
        'total_factorizations': total,
        'violations': len(violations),
        'verified': len(violations) == 0,
        'time_seconds': elapsed,
        'violation_examples': violations[:10] if violations else []
    }


def proposition5_m(k: int) -> int:
    """
    Compute m = (2^k + 1) / 3 for Proposition 5.
    
    Requires k to be odd for m to be an integer.
    """
    if k < 3 or k % 2 == 0:
        raise ValueError("k must be odd and >= 3")
    return ((1 << k) + 1) // 3


def verify_proposition5_single(k: int) -> Tuple[bool, dict]:
    """
    Verify Proposition 5 for a single odd k.
    
    Check: For m = (2^k + 1) / 3,
           H(3, m) = 2 and L_par(3, m) = k - 1
    
    Returns:
        (passed, details_dict)
    """
    if k % 2 == 0:
        return False, {'error': 'k must be odd'}
    
    m = proposition5_m(k)
    
    h = H(3, m)
    l_par = L_parallel(3, m)
    
    expected_h = 2
    expected_l_par = k - 1
    
    h_correct = (h == expected_h)
    l_par_correct = (l_par == expected_l_par)
    passed = h_correct and l_par_correct
    
    return passed, {
        'k': k,
        'm': m,
        'product': 3 * m,
        'binary_m': bin(m)[2:],
        'H': h,
        'expected_H': expected_h,
        'L_par': l_par,
        'expected_L_par': expected_l_par,
        'H_correct': h_correct,
        'L_par_correct': l_par_correct,
        'passed': passed
    }


def verify_proposition5(k_range: Tuple[int, int] = (3, 21)) -> dict:
    """
    Verify Proposition 5 for odd k in range.
    
    Args:
        k_range: (k_min, k_max) inclusive (only odd k tested)
        
    Returns:
        Summary statistics
    """
    k_min, k_max = k_range
    results = []
    violations = []
    
    for k in range(k_min, k_max + 1, 2):  # Step by 2 for odd only
        passed, details = verify_proposition5_single(k)
        results.append(details)
        if not passed:
            violations.append(details)
    
    return {
        'proposition': 'Proposition 5 (Arbitrarily long parallel chains)',
        'statement': 'For m = (2^k + 1)/3: H(3, m) = 2, L_par(3, m) = k - 1',
        'range_checked': f'odd k ∈ [{k_min}, {k_max}]',
        'total_checked': len(results),
        'violations': len(violations),
        'verified': len(violations) == 0,
        'results': results,
        'violation_details': violations
    }


def analyze_parallel_vs_sequential(max_n: int = 10000, verbose: bool = True) -> dict:
    """
    Compare sequential and parallel models across all factorizations.
    
    Reproduces paper's statistics:
        - max H = 8 (for n ≤ 10^5)
        - max L_par = 14
        - L_par = H in 28.96% of cases with H > 1
    
    Returns:
        Comprehensive statistics
    """
    stats = {
        'total': 0,
        'total_H_gt_1': 0,
        'L_seq_always_1': True,
        'L_par_eq_H_count': 0,
        'max_H': 0,
        'max_L_par': 0,
        'H_distribution': defaultdict(int),
        'L_par_distribution': defaultdict(int),
    }
    
    exceptions = []  # Cases where L_par ≠ H
    
    start_time = time.time()
    progress_step = max(1, max_n // 10)
    
    for n in range(4, max_n + 1):
        if verbose and n % progress_step == 0:
            print(f"  Progress: {n}/{max_n} ({100*n/max_n:.0f}%)")
        
        for a, b in get_factorizations(n, include_trivial=False):
            stats['total'] += 1
            
            h = H(a, b)
            l_seq = L(a, b)
            l_par = L_parallel(a, b)
            
            stats['H_distribution'][h] += 1
            stats['L_par_distribution'][l_par] += 1
            stats['max_H'] = max(stats['max_H'], h)
            stats['max_L_par'] = max(stats['max_L_par'], l_par)
            
            if l_seq != 1 and h > 1:
                stats['L_seq_always_1'] = False
            
            if h > 1:
                stats['total_H_gt_1'] += 1
                if l_par == h:
                    stats['L_par_eq_H_count'] += 1
                else:
                    if len(exceptions) < 100:
                        exceptions.append({
                            'n': n, 'a': a, 'b': b,
                            'H': h, 'L_par': l_par, 'diff': l_par - h
                        })
    
    elapsed = time.time() - start_time
    
    # Calculate percentage
    pct_L_par_eq_H = (100 * stats['L_par_eq_H_count'] / stats['total_H_gt_1'] 
                     if stats['total_H_gt_1'] > 0 else 0)
    
    return {
        'range_checked': f'n ∈ [4, {max_n}]',
        'total_factorizations': stats['total'],
        'total_H_gt_1': stats['total_H_gt_1'],
        'L_seq_always_1': stats['L_seq_always_1'],
        'L_par_eq_H_when_H_gt_1': stats['L_par_eq_H_count'],
        'L_par_eq_H_percentage': pct_L_par_eq_H,
        'max_H': stats['max_H'],
        'max_L_par': stats['max_L_par'],
        'H_distribution': dict(sorted(stats['H_distribution'].items())),
        'L_par_distribution': dict(sorted(stats['L_par_distribution'].items())),
        'exceptions_sample': exceptions[:20],
        'time_seconds': elapsed
    }


def print_theorem7_results(result: dict):
    """Pretty print Theorem 7 results."""
    print(f"\n{'='*60}")
    print(f"  {result['theorem']}")
    print(f"{'='*60}")
    print(f"  Statement: {result['statement']}")
    print(f"  Range: {result['range_checked']}")
    print(f"  Total factorizations: {result['total_factorizations']}")
    print(f"  Violations: {result['violations']}")
    print(f"  VERIFIED: {'✓ YES' if result['verified'] else '✗ NO'}")
    print(f"  Time: {result['time_seconds']:.2f}s")
    print()


def print_proposition5_results(result: dict):
    """Pretty print Proposition 5 results."""
    print(f"\n{'='*60}")
    print(f"  {result['proposition']}")
    print(f"{'='*60}")
    print(f"  Statement: {result['statement']}")
    print(f"  Range: {result['range_checked']}")
    print(f"  VERIFIED: {'✓ YES' if result['verified'] else '✗ NO'}")
    print()
    print("  k │       m │ product (3m) │  H │ L_par │ expected L_par")
    print("  ──┼─────────┼──────────────┼────┼───────┼────────────────")
    for r in result['results']:
        status = '✓' if r['passed'] else '✗'
        print(f"  {r['k']:2d} │ {r['m']:7d} │ {r['product']:12d} │ {r['H']:2d} │ {r['L_par']:5d} │ {r['expected_L_par']:14d} {status}")
    print()


def print_comparison_stats(stats: dict):
    """Pretty print sequential vs parallel comparison."""
    print(f"\n{'='*60}")
    print("  Sequential vs Parallel Model Statistics")
    print(f"{'='*60}")
    print(f"  Range: {stats['range_checked']}")
    print(f"  Total factorizations: {stats['total_factorizations']}")
    print(f"  Cases with H > 1: {stats['total_H_gt_1']}")
    print()
    print(f"  L_seq always = 1 (Theorem 7): {'✓ YES' if stats['L_seq_always_1'] else '✗ NO'}")
    print(f"  max H observed: {stats['max_H']}")
    print(f"  max L_par observed: {stats['max_L_par']}")
    print()
    print(f"  L_par = H (when H > 1): {stats['L_par_eq_H_when_H_gt_1']} / {stats['total_H_gt_1']}")
    print(f"                          ({stats['L_par_eq_H_percentage']:.2f}%)")
    print()
    print("  H distribution:")
    for h, count in stats['H_distribution'].items():
        pct = 100 * count / stats['total_factorizations']
        print(f"    H = {h}: {count} ({pct:.2f}%)")
    print()
    print("  L_par distribution:")
    for l, count in stats['L_par_distribution'].items():
        pct = 100 * count / stats['total_factorizations']
        print(f"    L_par = {l}: {count} ({pct:.2f}%)")
    print()
    if stats['exceptions_sample']:
        print("  Sample exceptions (L_par ≠ H when H > 1):")
        for e in stats['exceptions_sample'][:10]:
            sign = '+' if e['diff'] > 0 else ''
            print(f"    {e['n']} = {e['a']} × {e['b']}: H={e['H']}, L_par={e['L_par']} ({sign}{e['diff']})")
    print()


if __name__ == "__main__":
    print("="*60)
    print(" BCT Theorem 7 & Proposition 5 Verification")
    print("="*60)
    
    # Theorem 7: L(a, b) = 1 always
    print("\n[Theorem 7: Sequential sweep L = 1]")
    result7 = verify_theorem7(max_n=5000, verbose=False)
    print_theorem7_results(result7)
    
    # Proposition 5: L_par can be arbitrarily large
    print("\n[Proposition 5: Long parallel chains]")
    result_prop5 = verify_proposition5(k_range=(3, 21))
    print_proposition5_results(result_prop5)
    
    # Show the key insight: L_par grows while H stays at 2
    print("\n[Key Insight: L_par grows, H constant]")
    print("  For m = (2^k + 1)/3:")
    print("    H(3, m) = 2 always (constant)")
    print("    L_par(3, m) = k - 1 (grows without bound!)")
    print()
    
    # Full comparison statistics
    print("\n[Full Statistics: n ≤ 10,000]")
    stats = analyze_parallel_vs_sequential(max_n=10000, verbose=True)
    print_comparison_stats(stats)
    
    # Summary
    print("="*60)
    print(" Summary")
    print("="*60)
    print(f"  Theorem 7: {'✓ VERIFIED' if result7['verified'] else '✗ FAILED'}")
    print(f"  Proposition 5: {'✓ VERIFIED' if result_prop5['verified'] else '✗ FAILED'}")
    print()
    print("  Key findings:")
    print("    - Sequential model: L = 1 ALWAYS (immediate propagation)")
    print("    - Parallel model: L_par can grow arbitrarily large")
    print(f"    - L_par = H only ~{stats['L_par_eq_H_percentage']:.0f}% of the time (H > 1)")
    print()
