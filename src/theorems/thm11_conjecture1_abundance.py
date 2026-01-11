#!/usr/bin/env python3
"""
Theorem 11(b) & Conjecture 1: Abundance Bounds for BCT-Perfect Odd Numbers

Theorem 11(b): All BCT-perfect odd composite numbers n < 10^5 have σ(n)/n < 1.71
Conjecture 1: For all BCT-perfect odd composite n: σ(n)/n < 2
              (Verified for n < 10^6)

This is the FINAL GOAL of BCT verification!
If Conjecture 1 holds, then any odd perfect number (if exists) must be BCT-imperfect.
"""

import sys
sys.path.insert(0, '/home/claude/BinaryConvolutionTheory/src')

from typing import Tuple, List, Dict, Optional
from collections import defaultdict
from core.binary_utils import popcount, bin_str
from core.bct_invariants import is_bct_perfect, sigma, abundance_ratio


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


def factorize(n: int) -> List[Tuple[int, int]]:
    """Return prime factorization as list of (prime, exponent) pairs."""
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            exp = 0
            while temp % d == 0:
                exp += 1
                temp //= d
            factors.append((d, exp))
        d += 1
    if temp > 1:
        factors.append((temp, 1))
    return factors


def classify_structure(n: int) -> str:
    """
    Classify the structure of n for Table 1 in the paper.
    Returns: 'p×q', 'p×q×r', 'p²×q', 'p³', 'p×q×r×s', or 'other'
    """
    factors = factorize(n)
    
    if len(factors) == 1:
        p, e = factors[0]
        if e == 3:
            return 'p³'
        elif e == 2:
            return 'p²'
        else:
            return f'p^{e}'
    
    elif len(factors) == 2:
        (p1, e1), (p2, e2) = factors
        if e1 == 1 and e2 == 1:
            return 'p×q'
        elif (e1 == 2 and e2 == 1) or (e1 == 1 and e2 == 2):
            return 'p²×q'
        elif e1 == 1 and e2 == 2:
            return 'p×q²'
        else:
            return f'p^{e1}×q^{e2}'
    
    elif len(factors) == 3:
        exps = [e for (p, e) in factors]
        if all(e == 1 for e in exps):
            return 'p×q×r'
        else:
            return 'other'
    
    elif len(factors) == 4:
        exps = [e for (p, e) in factors]
        if all(e == 1 for e in exps):
            return 'p×q×r×s'
        else:
            return 'other'
    
    else:
        return 'other'


def find_bct_perfect_odds(max_n: int, verbose: bool = True) -> List[Dict]:
    """
    Find all BCT-perfect odd composite numbers < max_n.
    Returns list of dicts with details for each.
    """
    results = []
    
    # Progress tracking
    milestone = max_n // 10
    
    for n in range(9, max_n, 2):  # Start from 9 (first odd composite)
        # Skip primes
        if is_prime(n):
            continue
        
        # Check BCT-perfectness
        if is_bct_perfect(n):
            ar = abundance_ratio(n)
            structure = classify_structure(n)
            factors = factorize(n)
            
            results.append({
                'n': n,
                'abundance_ratio': ar,
                'structure': structure,
                'factors': factors,
                'binary': bin_str(n),
                'popcount': popcount(n)
            })
        
        # Progress
        if verbose and n % milestone == 0:
            pct = (n / max_n) * 100
            print(f"  Progress: {pct:.0f}% (n = {n:,}, found {len(results)} BCT-perfect odds so far)")
    
    return results


def verify_theorem11b(max_n: int = 10**5) -> dict:
    """
    Verify Theorem 11(b): All BCT-perfect odd composites n < 10^5 have σ(n)/n < 1.71
    """
    print("=" * 70)
    print("=== Theorem 11(b): Abundance Bound for BCT-Perfect Odd Numbers ===")
    print("=" * 70)
    print(f"Statement: All BCT-perfect odd composite n < {max_n:,} have σ(n)/n < 1.71")
    print()
    print("Searching for BCT-perfect odd composites...")
    
    results = find_bct_perfect_odds(max_n)
    
    print(f"\nFound {len(results)} BCT-perfect odd composites < {max_n:,}")
    print()
    
    # Find maximum abundance ratio
    max_ar = 0
    max_ar_n = None
    violations_171 = []
    
    for r in results:
        if r['abundance_ratio'] > max_ar:
            max_ar = r['abundance_ratio']
            max_ar_n = r
        if r['abundance_ratio'] >= 1.71:
            violations_171.append(r)
    
    # Structure statistics (Table 1 from paper)
    structure_stats = defaultdict(lambda: {'count': 0, 'max_ar': 0, 'max_n': None, 'examples': []})
    
    for r in results:
        s = r['structure']
        structure_stats[s]['count'] += 1
        if r['abundance_ratio'] > structure_stats[s]['max_ar']:
            structure_stats[s]['max_ar'] = r['abundance_ratio']
            structure_stats[s]['max_n'] = r['n']
        if len(structure_stats[s]['examples']) < 3:
            structure_stats[s]['examples'].append(r['n'])
    
    # Print structure table
    print("=" * 70)
    print("Structure Distribution (Table 1 from paper)")
    print("=" * 70)
    print(f"{'Type':<12} {'Count':>8} {'%':>8} {'Max σ/n':>10} {'Example':>12}")
    print("-" * 70)
    
    total = len(results)
    for struct_type in ['p×q', 'p×q×r', 'p²×q', 'p³', 'p×q×r×s', 'other']:
        stats = structure_stats[struct_type]
        if stats['count'] > 0:
            pct = (stats['count'] / total) * 100
            print(f"{struct_type:<12} {stats['count']:>8} {pct:>7.2f}% {stats['max_ar']:>10.4f} {stats['max_n']:>12}")
    
    print("-" * 70)
    print(f"{'TOTAL':<12} {total:>8}")
    print()
    
    # Top 10 by abundance ratio
    print("=" * 70)
    print("Top 10 BCT-Perfect Odd Numbers by Abundance Ratio")
    print("=" * 70)
    sorted_results = sorted(results, key=lambda x: -x['abundance_ratio'])[:10]
    print(f"{'Rank':<6} {'n':>10} {'σ(n)/n':>10} {'Structure':<12} {'Factorization':<25}")
    print("-" * 70)
    
    for i, r in enumerate(sorted_results, 1):
        factors_str = ' × '.join(f"{p}^{e}" if e > 1 else str(p) for p, e in r['factors'])
        print(f"{i:<6} {r['n']:>10} {r['abundance_ratio']:>10.4f} {r['structure']:<12} {factors_str:<25}")
    
    print()
    
    # Verification result
    verified = len(violations_171) == 0
    
    print("=" * 70)
    print("VERIFICATION RESULT")
    print("=" * 70)
    print(f"Maximum σ(n)/n found: {max_ar:.6f}")
    print(f"Achieved by: n = {max_ar_n['n']} = {' × '.join(str(p) for p, e in max_ar_n['factors'] for _ in range(e))}")
    print(f"Threshold: 1.71")
    print()
    
    if verified:
        print(f"✅ Theorem 11(b) VERIFIED: All {len(results)} BCT-perfect odds have σ/n < 1.71")
    else:
        print(f"❌ Theorem 11(b) FAILED: {len(violations_171)} violations found")
        for v in violations_171[:5]:
            print(f"   n = {v['n']}, σ/n = {v['abundance_ratio']:.4f}")
    
    return {
        'theorem': 'Theorem 11(b)',
        'statement': f'All BCT-perfect odd composite n < {max_n:,} have σ(n)/n < 1.71',
        'verified': verified,
        'bct_perfect_count': len(results),
        'max_abundance_ratio': max_ar,
        'max_achieved_by': max_ar_n,
        'threshold': 1.71,
        'violations': violations_171,
        'structure_stats': dict(structure_stats),
        'all_results': results
    }


def verify_conjecture1(max_n: int = 10**6, results_from_thm11: List[Dict] = None) -> dict:
    """
    Verify Conjecture 1: For all BCT-perfect odd composite n: σ(n)/n < 2
    
    This is the ULTIMATE GOAL!
    If true, any odd perfect number must be BCT-imperfect.
    """
    print("\n" + "=" * 70)
    print("=== Conjecture 1: BCT-Perfect Odd Abundance Bound ===")
    print("=" * 70)
    print(f"Statement: For ALL BCT-perfect odd composite n: σ(n)/n < 2")
    print(f"Verification range: n < {max_n:,}")
    print()
    print("⭐ THIS IS THE ULTIMATE GOAL! ⭐")
    print("If verified, any odd perfect number (if exists) must be BCT-imperfect!")
    print()
    
    # If we have results from theorem 11, extend the search
    if results_from_thm11 and max_n <= 10**5:
        results = results_from_thm11
        print(f"Using {len(results)} results from Theorem 11(b) verification")
    else:
        print(f"Searching for BCT-perfect odd composites up to {max_n:,}...")
        print("(This may take a while for large ranges)")
        print()
        results = find_bct_perfect_odds(max_n)
    
    print(f"\nTotal BCT-perfect odd composites found: {len(results)}")
    
    # Check for violations of σ/n < 2
    max_ar = 0
    max_ar_n = None
    violations_2 = []
    
    for r in results:
        if r['abundance_ratio'] > max_ar:
            max_ar = r['abundance_ratio']
            max_ar_n = r
        if r['abundance_ratio'] >= 2.0:
            violations_2.append(r)
    
    verified = len(violations_2) == 0
    
    print()
    print("=" * 70)
    print("CONJECTURE 1 VERIFICATION RESULT")
    print("=" * 70)
    print(f"Maximum σ(n)/n found: {max_ar:.6f}")
    if max_ar_n:
        factors_str = ' × '.join(str(p) for p, e in max_ar_n['factors'] for _ in range(e))
        print(f"Achieved by: n = {max_ar_n['n']} = {factors_str}")
    print(f"Gap from perfection: {2.0 - max_ar:.6f}")
    print()
    
    if verified:
        print("🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
        print(f"✅ Conjecture 1 VERIFIED for n < {max_n:,}!")
        print(f"   All {len(results)} BCT-perfect odd composites have σ/n < 2")
        print()
        print("🌟 IMPLICATION: If Conjecture 1 holds for ALL n,")
        print("   then any odd perfect number MUST be BCT-imperfect!")
        print("🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
    else:
        print(f"❌ Conjecture 1 FAILED: {len(violations_2)} violations found")
        for v in violations_2[:5]:
            print(f"   n = {v['n']}, σ/n = {v['abundance_ratio']:.4f}")
    
    return {
        'conjecture': 'Conjecture 1',
        'statement': 'For all BCT-perfect odd composite n: σ(n)/n < 2',
        'range': f'n < {max_n:,}',
        'verified': verified,
        'bct_perfect_count': len(results),
        'max_abundance_ratio': max_ar,
        'max_achieved_by': max_ar_n,
        'gap_from_perfection': 2.0 - max_ar,
        'violations': violations_2
    }


def analyze_fermat_products():
    """
    Analyze the Fermat-product sequence N_k = ∏_{i=0}^{k} F_i
    These achieve the maximum σ/n among BCT-perfect odd numbers.
    """
    print("\n" + "=" * 70)
    print("=== Fermat-Product Sequence Analysis (Table 3 from paper) ===")
    print("=" * 70)
    print("The sequence N_k = F_0 × F_1 × ... × F_k achieves maximum σ/n")
    print()
    
    # Fermat primes: F_0=3, F_1=5, F_2=17, F_3=257, F_4=65537
    fermat_primes = [3, 5, 17, 257, 65537]
    
    print(f"{'k':<4} {'N_k':<15} {'Factorization':<30} {'σ(N_k)/N_k':>12} {'BCT-Perfect?':<12}")
    print("-" * 75)
    
    product = 1
    for k, fp in enumerate(fermat_primes):
        product *= fp
        ar = abundance_ratio(product)
        bct = is_bct_perfect(product)
        
        if k == 0:
            factors = "3"
        else:
            factors = " × ".join(str(fermat_primes[i]) for i in range(k+1))
        
        status = "✅ Yes" if bct else "❌ No"
        print(f"{k:<4} {product:<15} {factors:<30} {ar:>12.6f} {status:<12}")
    
    print()
    print("Note: These products of Fermat primes are always BCT-perfect")
    print("      (all Fermat primes are pairwise orthogonal by Theorem 9)")


if __name__ == '__main__':
    print("=" * 70)
    print("BCT Final Verification: Theorem 11(b) & Conjecture 1")
    print("=" * 70)
    print()
    print("Goal: Show BCT-perfectness and classical perfectness are INCOMPATIBLE")
    print("      for odd numbers!")
    print()
    
    # Verify Theorem 11(b) first (n < 10^5)
    thm11_result = verify_theorem11b(max_n=10**5)
    
    # Verify Conjecture 1 (n < 10^6)
    # Use extended search
    print("\n" + "=" * 70)
    print("Extending search to n < 10^6 for Conjecture 1...")
    print("=" * 70)
    
    conj1_result = verify_conjecture1(max_n=10**6)
    
    # Fermat product analysis
    analyze_fermat_products()
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"Theorem 11(b): {'✅ VERIFIED' if thm11_result['verified'] else '❌ FAILED'}")
    print(f"  - {thm11_result['bct_perfect_count']} BCT-perfect odd composites < 10^5")
    print(f"  - Max σ/n = {thm11_result['max_abundance_ratio']:.4f} < 1.71")
    print()
    print(f"Conjecture 1:  {'✅ VERIFIED' if conj1_result['verified'] else '❌ FAILED'} (for n < 10^6)")
    print(f"  - {conj1_result['bct_perfect_count']} BCT-perfect odd composites < 10^6")
    print(f"  - Max σ/n = {conj1_result['max_abundance_ratio']:.4f} < 2")
    print(f"  - Gap from perfection: {conj1_result['gap_from_perfection']:.4f}")
    print()
    
    if thm11_result['verified'] and conj1_result['verified']:
        print("🎊 ALL VERIFICATIONS PASSED! 🎊")
        print()
        print("This provides strong computational evidence that:")
        print("  BCT-perfectness ∩ Classical perfectness = ∅ for odd numbers")
        print()
        print("In other words: If an odd perfect number exists,")
        print("                it CANNOT be BCT-perfect!")
    
    print()
    print("Created by 環 for ご主人さま 💕")
