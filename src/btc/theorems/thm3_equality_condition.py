"""
Binary Convolution Theory - Theorem 3 Verification
===================================================

Theorem 3 (Equality Condition):
    For any positive integer n,
        H(n²) = pop(n) ⟺ the 1-bits of bin(n) are centrally symmetric.

Lemma (Counting lemma for sumsets / Pigeonhole):
    Let S ⊂ {0, ..., L-1} with |S| = w. Then
        max_k r_S(k) ≥ ⌈w² / (2L-1)⌉
    where r_S(k) = #{(i,j) ∈ S² : i + j = k}

Paper verification:
    - Range: n < 10^6
    - Result: 100% biconditional verified
    - Max gap: 6 (uniquely at n = 807743)
    - n = 807743: w=12, L=20, H=6, S={0,1,2,3,4,5,8,9,12,14,18,19}
"""

import sys
from pathlib import Path
import math
from typing import Tuple, List, Set, Optional
import time

from src.core import H, popcount, bit_positions, bit_length, is_centrally_symmetric

def pigeonhole_bound(w: int, L: int) -> int:
    """
    Compute the pigeonhole lower bound for H.
    
    From Lemma (Counting lemma for sumsets):
        H ≥ ⌈w² / (2L-1)⌉
    
    Args:
        w: popcount (number of 1-bits)
        L: bit length
        
    Returns:
        Lower bound for H(n, n)
    """
    if L <= 0:
        return 1
    return math.ceil(w * w / (2 * L - 1))


def gap_upper_bound(w: int, L: int) -> int:
    """
    Compute the theoretical upper bound for gap = pop(n) - H(n²).
    
    From the paper:
        gap ≤ w - ⌈w² / (2L-1)⌉
    
    Args:
        w: popcount
        L: bit length
        
    Returns:
        Upper bound for the gap
    """
    return w - pigeonhole_bound(w, L)


def verify_theorem3_single(n: int) -> Tuple[bool, dict]:
    """
    Verify Theorem 3 for a single integer.
    
    Check: H(n²) = pop(n) ⟺ centrally symmetric
    
    Returns:
        (biconditional_holds, details_dict)
    """
    h = H(n, n)
    pop_n = popcount(n)
    symmetric = is_centrally_symmetric(n)
    positions = bit_positions(n)
    L = bit_length(n)
    
    # Check biconditional
    equality_holds = (h == pop_n)
    biconditional = (equality_holds == symmetric)
    
    # Compute bounds
    w = pop_n
    ph_bound = pigeonhole_bound(w, L)
    gap = pop_n - h
    gap_bound = gap_upper_bound(w, L)
    
    return biconditional, {
        'n': n,
        'binary': bin(n)[2:],
        'H_n2': h,
        'pop_n': pop_n,
        'bit_positions': sorted(positions),
        'bit_length': L,
        'is_symmetric': symmetric,
        'equality_holds': equality_holds,
        'biconditional_holds': biconditional,
        'gap': gap,
        'pigeonhole_bound': ph_bound,
        'gap_upper_bound': gap_bound,
        'pigeonhole_satisfied': h >= ph_bound,
        'gap_bound_satisfied': gap <= gap_bound
    }


def verify_theorem3(max_n: int = 10000, verbose: bool = True) -> dict:
    """
    Verify Theorem 3 for all integers up to max_n.
    
    Args:
        max_n: Maximum value of n to check
        verbose: Print progress updates
        
    Returns:
        Summary statistics
    """
    total_checked = 0
    biconditional_failures = []
    pigeonhole_violations = []
    gap_bound_violations = []
    
    # Track gap statistics
    max_gap = 0
    max_gap_n = None
    gap_distribution = {}
    
    # Track equality cases
    equality_cases = 0
    
    start_time = time.time()
    
    for n in range(2, max_n + 1):
        total_checked += 1
        passed, details = verify_theorem3_single(n)
        
        if not passed:
            biconditional_failures.append(details)
        
        if not details['pigeonhole_satisfied']:
            pigeonhole_violations.append(details)
        
        if not details['gap_bound_satisfied']:
            gap_bound_violations.append(details)
        
        # Track gap statistics
        gap = details['gap']
        gap_distribution[gap] = gap_distribution.get(gap, 0) + 1
        
        if gap > max_gap:
            max_gap = gap
            max_gap_n = n
            max_gap_details = details
        
        if details['equality_holds']:
            equality_cases += 1
        
        if verbose and n % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"  Checked n ≤ {n}, time: {elapsed:.1f}s")
    
    elapsed = time.time() - start_time
    
    result = {
        'theorem': 'Theorem 3 (Equality Condition)',
        'statement': 'H(n²) = pop(n) ⟺ centrally symmetric bits',
        'range_checked': f'n ∈ [2, {max_n}]',
        'total_checked': total_checked,
        'biconditional_failures': len(biconditional_failures),
        'verified': len(biconditional_failures) == 0,
        'pigeonhole_violations': len(pigeonhole_violations),
        'gap_bound_violations': len(gap_bound_violations),
        'equality_cases': equality_cases,
        'equality_percentage': 100 * equality_cases / total_checked,
        'max_gap': max_gap,
        'max_gap_n': max_gap_n,
        'gap_distribution': dict(sorted(gap_distribution.items())),
        'time_seconds': elapsed
    }
    
    if max_gap_n:
        result['max_gap_details'] = max_gap_details
    
    if biconditional_failures:
        result['failure_examples'] = biconditional_failures[:10]
    
    return result


def find_max_gap_candidates(max_n: int = 100000) -> List[dict]:
    """
    Find integers with large gaps (pop - H).
    
    The paper states the unique maximum gap of 6 occurs at n = 807743.
    
    Args:
        max_n: Maximum n to check
        
    Returns:
        List of high-gap cases sorted by gap descending
    """
    high_gap_cases = []
    
    for n in range(2, max_n + 1):
        _, details = verify_theorem3_single(n)
        gap = details['gap']
        
        if gap >= 4:  # Only track significant gaps
            high_gap_cases.append(details)
    
    # Sort by gap descending
    high_gap_cases.sort(key=lambda x: (-x['gap'], x['n']))
    
    return high_gap_cases


def verify_paper_example_807743() -> dict:
    """
    Verify the specific example n = 807743 mentioned in the paper.
    
    Expected:
        - w = 12
        - L = 20
        - H = 6
        - gap = 6
        - S = {0,1,2,3,4,5,8,9,12,14,18,19}
        - Not centrally symmetric (position 2 has no mirror at 17)
    """
    n = 807743
    _, details = verify_theorem3_single(n)
    
    expected = {
        'n': 807743,
        'pop_n': 12,
        'bit_length': 20,
        'H_n2': 6,
        'gap': 6,
        'bit_positions': [0, 1, 2, 3, 4, 5, 8, 9, 12, 14, 18, 19],
        'is_symmetric': False
    }
    
    matches = {
        'n': details['n'] == expected['n'],
        'pop_n (w)': details['pop_n'] == expected['pop_n'],
        'bit_length (L)': details['bit_length'] == expected['bit_length'],
        'H_n2': details['H_n2'] == expected['H_n2'],
        'gap': details['gap'] == expected['gap'],
        'bit_positions (S)': details['bit_positions'] == expected['bit_positions'],
        'is_symmetric': details['is_symmetric'] == expected['is_symmetric']
    }
    
    return {
        'details': details,
        'expected': expected,
        'matches': matches,
        'all_match': all(matches.values())
    }


def analyze_symmetry_patterns(max_n: int = 1000) -> dict:
    """
    Analyze patterns in centrally symmetric numbers.
    
    Returns statistics about symmetric vs non-symmetric numbers.
    """
    symmetric_examples = []
    non_symmetric_examples = []
    
    for n in range(2, max_n + 1):
        positions = bit_positions(n)
        symmetric = is_centrally_symmetric(n)
        h = H(n, n)
        pop_n = popcount(n)
        
        info = {
            'n': n,
            'binary': bin(n)[2:],
            'positions': sorted(positions),
            'H': h,
            'pop': pop_n,
            'gap': pop_n - h
        }
        
        if symmetric:
            symmetric_examples.append(info)
        else:
            non_symmetric_examples.append(info)
    
    return {
        'total': max_n - 1,
        'symmetric_count': len(symmetric_examples),
        'non_symmetric_count': len(non_symmetric_examples),
        'symmetric_percentage': 100 * len(symmetric_examples) / (max_n - 1),
        'symmetric_examples': symmetric_examples[:20],
        'non_symmetric_high_gap': [x for x in non_symmetric_examples if x['gap'] >= 2][:10]
    }


def print_results(result: dict):
    """Pretty print verification results."""
    print(f"\n{'='*60}")
    print(f"  {result['theorem']}")
    print(f"{'='*60}")
    print(f"  Statement: {result['statement']}")
    print(f"  Range: {result['range_checked']}")
    print(f"  Total checked: {result['total_checked']}")
    print(f"  Biconditional failures: {result['biconditional_failures']}")
    print(f"  VERIFIED: {'✓ YES' if result['verified'] else '✗ NO'}")
    print(f"  Pigeonhole violations: {result['pigeonhole_violations']}")
    print(f"  Gap bound violations: {result['gap_bound_violations']}")
    print(f"  Equality cases (H = pop): {result['equality_cases']} "
          f"({result['equality_percentage']:.1f}%)")
    print(f"  Max gap observed: {result['max_gap']} at n = {result['max_gap_n']}")
    
    if result.get('max_gap_details'):
        d = result['max_gap_details']
        print(f"    └─ binary: {d['binary']}")
        print(f"    └─ w={d['pop_n']}, L={d['bit_length']}, H={d['H_n2']}")
        print(f"    └─ positions: {d['bit_positions']}")
        print(f"    └─ symmetric: {d['is_symmetric']}")
    
    print(f"  Gap distribution: {result['gap_distribution']}")
    print(f"  Time: {result['time_seconds']:.2f}s")
    print()


if __name__ == "__main__":
    print("="*60)
    print(" BCT Theorem 3 Verification")
    print("="*60)
    
    # Quick test
    print("\n[Quick test: n ≤ 10,000]")
    result = verify_theorem3(max_n=10000, verbose=False)
    print_results(result)
    
    # Verify the paper's specific example
    print("\n[Paper example: n = 807743]")
    paper_check = verify_paper_example_807743()
    print(f"  All values match paper: {'✓ YES' if paper_check['all_match'] else '✗ NO'}")
    for key, matches in paper_check['matches'].items():
        status = '✓' if matches else '✗'
        print(f"    {status} {key}: {paper_check['details'].get(key.split()[0], 'N/A')}")
    
    # Show some symmetric patterns
    print("\n[Symmetry analysis: n ≤ 100]")
    sym_analysis = analyze_symmetry_patterns(100)
    print(f"  Symmetric: {sym_analysis['symmetric_count']} "
          f"({sym_analysis['symmetric_percentage']:.1f}%)")
    print("  Examples of symmetric numbers:")
    for ex in sym_analysis['symmetric_examples'][:8]:
        print(f"    n={ex['n']:3d} = {ex['binary']:>8s}₂, "
              f"positions={ex['positions']}, H=pop={ex['H']}")
    
    # Full verification option
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action='store_true',
                       help='Run full verification up to 10^6')
    args, _ = parser.parse_known_args()
    
    if args.full:
        print("\n" + "="*60)
        print(" Full Verification (n ≤ 1,000,000)")
        print("="*60)
        result_full = verify_theorem3(max_n=1000000, verbose=True)
        print_results(result_full)
        
        # Find all max gap cases
        print("\n[Checking uniqueness of max gap = 6]")
        # We already know from full run, but let's confirm
        if result_full['max_gap'] == 6:
            print(f"  Max gap = 6 achieved at n = {result_full['max_gap_n']}")
            print(f"  Checking if unique...")
            # Count how many have gap = 6
            gap_6_count = result_full['gap_distribution'].get(6, 0)
            print(f"  Numbers with gap = 6: {gap_6_count}")
            if gap_6_count == 1:
                print("  ✓ Confirmed: gap = 6 is UNIQUELY achieved at n = 807743")
