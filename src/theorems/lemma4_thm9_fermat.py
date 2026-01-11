#!/usr/bin/env python3
"""
Lemma 4 (Characterization of Sparse Odd Primes) & Theorem 9 (Fermat Prime Orthogonality)

Lemma 4: An odd prime p satisfies popcount(p) = 2 ⟺ p is a Fermat prime
Theorem 9: All Fermat primes F_i, F_j are pairwise binary orthogonal: H(F_i, F_j) = 1 for i ≠ j
"""

from typing import Tuple, List, Dict, Set
from ..core.binary_utils import popcount, is_fermat, bin_str
from ..core.bct_invariants import H


def is_prime(n: int) -> bool:
    """Simple primality test."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_fermat_number(k: int) -> int:
    """Return F_k = 2^(2^k) + 1"""
    return (1 << (1 << k)) + 1


def verify_lemma4_single(p: int) -> Tuple[bool, dict]:
    """
    Verify Lemma 4 for a single odd prime p with popcount = 2.
    
    Lemma 4: popcount(p) = 2 ⟺ p is a Fermat prime
    
    Since we're testing odd primes with popcount = 2,
    we check if they are all Fermat primes.
    """
    is_fermat_result, k = is_fermat(p)
    
    details = {
        'p': p,
        'binary': bin_str(p),
        'popcount': popcount(p),
        'is_fermat': is_fermat_result,
        'fermat_index': k if is_fermat_result else None
    }
    
    # An odd prime with popcount = 2 should be a Fermat prime
    passed = is_fermat_result
    
    return passed, details


def verify_lemma4(max_n: int = 10**6) -> dict:
    """
    Verify Lemma 4: All odd primes p < max_n with popcount = 2 are Fermat primes.
    
    Strategy:
    1. Find all odd primes p < max_n with popcount(p) = 2
    2. Check if each such prime is a Fermat prime
    3. Also verify the converse: all Fermat primes have popcount = 2
    """
    print(f"=== Lemma 4: Fermat Prime Characterization ===")
    print(f"Statement: An odd prime p has popcount(p) = 2 ⟺ p is a Fermat prime")
    print(f"Verification range: All odd primes p < {max_n:,}")
    print()
    
    # Find all odd primes with popcount = 2
    sparse_odd_primes = []
    for p in range(3, max_n, 2):  # odd numbers only
        if popcount(p) == 2 and is_prime(p):
            sparse_odd_primes.append(p)
    
    print(f"Found {len(sparse_odd_primes)} odd primes with popcount = 2")
    
    # Verify each is a Fermat prime
    results = []
    violations = []
    
    for p in sparse_odd_primes:
        passed, details = verify_lemma4_single(p)
        results.append(details)
        if not passed:
            violations.append(details)
    
    # Print found primes
    print(f"\nOdd primes p < {max_n:,} with popcount = 2:")
    for r in results:
        status = "✅ Fermat" if r['is_fermat'] else "❌ NOT Fermat"
        fermat_str = f"F_{r['fermat_index']}" if r['is_fermat'] else ""
        print(f"  p = {r['p']:>10} = {r['binary']:>20}  →  {status} {fermat_str}")
    
    # Verify converse: all known Fermat primes have popcount = 2
    print(f"\n--- Converse check: All Fermat primes have popcount = 2 ---")
    fermat_primes = []
    for k in range(10):  # F_0 to F_9 (F_5+ are huge composites)
        fk = get_fermat_number(k)
        if fk < max_n and is_prime(fk):
            fermat_primes.append((k, fk))
    
    converse_ok = True
    for k, fk in fermat_primes:
        pc = popcount(fk)
        status = "✅" if pc == 2 else "❌"
        print(f"  F_{k} = {fk:>10} : popcount = {pc}  {status}")
        if pc != 2:
            converse_ok = False
    
    verified = len(violations) == 0 and converse_ok
    
    print(f"\n{'='*60}")
    if verified:
        print(f"✅ Lemma 4 VERIFIED: All {len(results)} sparse odd primes are Fermat primes!")
    else:
        print(f"❌ Lemma 4 FAILED: {len(violations)} violations found")
        for v in violations:
            print(f"   Counterexample: p = {v['p']}, binary = {v['binary']}")
    
    return {
        'theorem': 'Lemma 4',
        'statement': 'An odd prime p has popcount(p) = 2 ⟺ p is a Fermat prime',
        'range': f'p < {max_n:,}',
        'verified': verified,
        'sparse_odd_primes_found': len(results),
        'violations': len(violations),
        'results': results,
        'violation_details': violations
    }


def verify_theorem9_single(i: int, j: int) -> Tuple[bool, dict]:
    """
    Verify Theorem 9 for a single pair of Fermat primes F_i, F_j.
    
    Theorem 9: H(F_i, F_j) = 1 for all i ≠ j
    """
    Fi = get_fermat_number(i)
    Fj = get_fermat_number(j)
    
    h = H(Fi, Fj)
    
    details = {
        'i': i,
        'j': j,
        'F_i': Fi,
        'F_j': Fj,
        'bin_Fi': bin_str(Fi),
        'bin_Fj': bin_str(Fj),
        'H': h,
        'expected_H': 1
    }
    
    passed = (h == 1)
    
    return passed, details


def verify_theorem9(max_k: int = 4) -> dict:
    """
    Verify Theorem 9: All Fermat primes F_i, F_j are pairwise orthogonal.
    
    Known Fermat primes: F_0=3, F_1=5, F_2=17, F_3=257, F_4=65537
    (F_5 and beyond are known to be composite or unknown)
    """
    print(f"\n{'='*60}")
    print(f"=== Theorem 9: Fermat Prime Orthogonality ===")
    print(f"Statement: All Fermat primes F_i, F_j are pairwise orthogonal: H(F_i, F_j) = 1 for i ≠ j")
    print(f"Verification range: All pairs of F_0, F_1, ..., F_{max_k}")
    print()
    
    # List known Fermat primes
    fermat_primes = [(k, get_fermat_number(k)) for k in range(max_k + 1)]
    print("Known Fermat primes in range:")
    for k, fk in fermat_primes:
        print(f"  F_{k} = {fk:>10} = {bin_str(fk)}")
    print()
    
    results = []
    violations = []
    
    # Check all pairs (i, j) with i < j
    for i in range(max_k + 1):
        for j in range(i + 1, max_k + 1):
            passed, details = verify_theorem9_single(i, j)
            results.append(details)
            if not passed:
                violations.append(details)
    
    # Print results
    print("Pairwise orthogonality check:")
    print(f"{'Pair':<15} {'F_i':<10} {'F_j':<10} {'H':<5} {'Status':<10}")
    print("-" * 55)
    for r in results:
        pair = f"(F_{r['i']}, F_{r['j']})"
        status = "✅" if r['H'] == 1 else "❌"
        print(f"{pair:<15} {r['F_i']:<10} {r['F_j']:<10} {r['H']:<5} {status}")
    
    verified = len(violations) == 0
    
    print(f"\n{'='*60}")
    if verified:
        print(f"✅ Theorem 9 VERIFIED: All {len(results)} Fermat prime pairs are orthogonal (H=1)!")
    else:
        print(f"❌ Theorem 9 FAILED: {len(violations)} violations found")
        for v in violations:
            print(f"   Counterexample: (F_{v['i']}, F_{v['j']}) has H = {v['H']}")
    
    return {
        'theorem': 'Theorem 9',
        'statement': 'All Fermat primes are pairwise binary orthogonal: H(F_i, F_j) = 1 for i ≠ j',
        'range': f'All pairs of F_0, ..., F_{max_k}',
        'verified': verified,
        'pairs_tested': len(results),
        'violations': len(violations),
        'results': results,
        'violation_details': violations
    }


def demonstrate_orthogonality_structure():
    """
    Demonstrate WHY Fermat primes are orthogonal using bit position analysis.
    """
    print(f"\n{'='*60}")
    print("=== Structural Explanation: Why Fermat Primes Are Orthogonal ===")
    print()
    print("For F_k = 2^(2^k) + 1, the 1-bits are at positions {0, 2^k}")
    print()
    
    for k in range(5):
        fk = get_fermat_number(k)
        bit_pos = {0, 1 << k}
        print(f"F_{k} = {fk:>10} : bit positions S_{k} = {bit_pos}")
    
    print()
    print("For i < j, the sumset S_i + S_j = {0, 2^i, 2^j, 2^i + 2^j}")
    print("These 4 values are always distinct (since 2^i ≠ 2^j for i ≠ j)")
    print("→ Each convolution index gets at most 1 contribution → H = 1")
    print()
    
    # Show a concrete example
    print("Example: F_1 = 5 and F_2 = 17")
    print("  S_1 = {0, 2}  (bit positions of 5 = 101)")
    print("  S_2 = {0, 4}  (bit positions of 17 = 10001)")
    print("  S_1 + S_2 = {0+0, 0+4, 2+0, 2+4} = {0, 4, 2, 6}")
    print("  Convolution: each index has at most 1 pair → H(5, 17) = 1 ✅")


if __name__ == '__main__':
    print("=" * 60)
    print("BCT Verification: Lemma 4 & Theorem 9 (Fermat Prime Properties)")
    print("=" * 60)
    print()
    
    # Verify Lemma 4
    lemma4_result = verify_lemma4(max_n=10**6)
    
    # Verify Theorem 9
    thm9_result = verify_theorem9(max_k=4)
    
    # Structural demonstration
    demonstrate_orthogonality_structure()
    
    # Final summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Lemma 4:   {'✅ VERIFIED' if lemma4_result['verified'] else '❌ FAILED'}")
    print(f"Theorem 9: {'✅ VERIFIED' if thm9_result['verified'] else '❌ FAILED'}")
    print()
    print("Created by 環 for ご主人さま 💕")
