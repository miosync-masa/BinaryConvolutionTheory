"""
Binary Convolution Theory - Theorem 8 Verification
===================================================

Theorem 8 (Even Perfect Number Structure):
    For even perfect numbers P = 2^{p-1} × (2^p - 1), where 2^p - 1 is Mersenne prime,
        H(P) = 1
    Furthermore, bin(P) = 1^p 0^{p-1}

Corollary: All even perfect numbers are BCT-perfect.

Corollary (Binary Generation):
    n is an even perfect number ⟺ bin(n) = 1^p 0^{p-1} for Mersenne prime 2^p - 1

Lemma (Power of Two Orthogonality):
    H(2^a, m) = 1 for any a ≥ 1 and m ≥ 1

Lemma (BCT-Perfectness Inheritance):
    n = 2^a · m is BCT-perfect ⟺ m is BCT-perfect

Paper verification: First 7 even perfect numbers

Known even perfect numbers (Euclid-Euler form):
    p=2:  6 = 2^1 × 3
    p=3:  28 = 2^2 × 7
    p=5:  496 = 2^4 × 31
    p=7:  8128 = 2^6 × 127
    p=13: 33550336 = 2^12 × 8191
    p=17: 8589869056 = 2^16 × 131071
    p=19: 137438691328 = 2^18 × 524287
"""

import sys
from pathlib import Path
from typing import Tuple, List, Optional

from core import (
    H, binary_convolution, popcount, bin_str, 
    is_bct_perfect, sigma, abundance_ratio, is_mersenne
)


# Mersenne prime exponents (known as of 2024)
# Only first 7 for practical computation
MERSENNE_PRIME_EXPONENTS = [2, 3, 5, 7, 13, 17, 19]

# Extended list (for reference, larger ones may be slow)
MERSENNE_PRIME_EXPONENTS_EXTENDED = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107]


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


def mersenne_prime(p: int) -> Tuple[int, bool]:
    """
    Compute M_p = 2^p - 1 and check if it's prime.
    
    Returns:
        (M_p, is_prime)
    """
    m_p = (1 << p) - 1
    return m_p, is_prime(m_p)


def even_perfect_number(p: int) -> Optional[int]:
    """
    Compute the even perfect number for Mersenne prime exponent p.
    
    P = 2^{p-1} × (2^p - 1) if 2^p - 1 is prime.
    
    Returns:
        The even perfect number, or None if 2^p - 1 is not prime
    """
    m_p, is_mp_prime = mersenne_prime(p)
    if not is_mp_prime:
        return None
    return (1 << (p - 1)) * m_p


def expected_binary_pattern(p: int) -> str:
    """
    Return the expected binary pattern for even perfect number with exponent p.
    
    Pattern: 1^p 0^{p-1} (p ones followed by p-1 zeros)
    """
    return '1' * p + '0' * (p - 1)


def verify_theorem8_single(p: int) -> Tuple[bool, dict]:
    """
    Verify Theorem 8 for a single Mersenne prime exponent p.
    
    Checks:
        1. H(P) = 1 (or equivalently, H(2^{p-1}, M_p) = 1)
        2. bin(P) = 1^p 0^{p-1}
        3. σ(P)/P = 2 (perfect)
        4. P is BCT-perfect
    
    Returns:
        (all_passed, details_dict)
    """
    m_p, is_mp_prime = mersenne_prime(p)
    
    if not is_mp_prime:
        return False, {
            'p': p,
            'M_p': m_p,
            'is_mersenne_prime': False,
            'error': f'2^{p} - 1 = {m_p} is not prime'
        }
    
    P = (1 << (p - 1)) * m_p
    power_of_2 = 1 << (p - 1)
    
    # Check 1: H(2^{p-1}, M_p) = 1
    h = H(power_of_2, m_p)
    h_is_1 = (h == 1)
    
    # Check 2: Binary pattern
    actual_binary = bin_str(P)
    expected_binary = expected_binary_pattern(p)
    binary_matches = (actual_binary == expected_binary)
    
    # Check 3: Perfect number (σ(P)/P = 2)
    ratio = abundance_ratio(P)
    is_perfect = abs(ratio - 2.0) < 1e-10
    
    # Check 4: BCT-perfect
    bct_perfect = is_bct_perfect(P)
    
    all_passed = h_is_1 and binary_matches and is_perfect and bct_perfect
    
    return all_passed, {
        'p': p,
        'M_p': m_p,
        'is_mersenne_prime': is_mp_prime,
        'P': P,
        '2^(p-1)': power_of_2,
        'H': h,
        'H_is_1': h_is_1,
        'binary': actual_binary,
        'expected_binary': expected_binary,
        'binary_matches': binary_matches,
        'sigma_ratio': ratio,
        'is_perfect': is_perfect,
        'is_bct_perfect': bct_perfect,
        'all_passed': all_passed
    }


def verify_power_of_two_orthogonality(max_a: int = 10, max_m: int = 100) -> dict:
    """
    Verify Lemma: H(2^a, m) = 1 for all a, m.
    
    The single 1-bit in 2^a just shifts m without overlap.
    
    Returns:
        Summary statistics
    """
    violations = []
    total = 0
    
    for a in range(1, max_a + 1):
        power = 1 << a
        for m in range(1, max_m + 1):
            total += 1
            h = H(power, m)
            if h != 1:
                violations.append({'a': a, '2^a': power, 'm': m, 'H': h})
    
    return {
        'lemma': 'Power of Two Orthogonality',
        'statement': 'H(2^a, m) = 1 for all a ≥ 1, m ≥ 1',
        'range': f'a ∈ [1, {max_a}], m ∈ [1, {max_m}]',
        'total_checked': total,
        'violations': len(violations),
        'verified': len(violations) == 0,
        'violation_examples': violations[:10]
    }


def verify_theorem8(exponents: List[int] = None) -> dict:
    """
    Verify Theorem 8 for a list of Mersenne prime exponents.
    
    Args:
        exponents: List of p values (default: first 7)
        
    Returns:
        Summary statistics
    """
    if exponents is None:
        exponents = MERSENNE_PRIME_EXPONENTS
    
    results = []
    violations = []
    
    for p in exponents:
        passed, details = verify_theorem8_single(p)
        results.append(details)
        if not passed:
            violations.append(details)
    
    return {
        'theorem': 'Theorem 8 (Even Perfect Number Structure)',
        'statement': 'H(P) = 1 and bin(P) = 1^p 0^{p-1} for even perfect P',
        'exponents_checked': exponents,
        'total_checked': len(results),
        'violations': len(violations),
        'verified': len(violations) == 0,
        'results': results,
        'violation_details': violations
    }


def verify_binary_generation(max_p: int = 20) -> dict:
    """
    Verify Corollary (Binary Generation) by checking both directions:
    
    1. Every even perfect number has pattern 1^p 0^{p-1}
    2. Pattern 1^p 0^{p-1} gives even perfect only when 2^p - 1 is prime
    
    Returns:
        Summary of forward and reverse checks
    """
    forward_results = []  # Known perfect → check pattern
    reverse_results = []  # All patterns → check which are perfect
    
    # Forward: Known Mersenne prime exponents
    for p in MERSENNE_PRIME_EXPONENTS:
        P = even_perfect_number(p)
        actual = bin_str(P)
        expected = expected_binary_pattern(p)
        forward_results.append({
            'p': p,
            'P': P,
            'binary': actual,
            'expected': expected,
            'matches': actual == expected
        })
    
    # Reverse: Check all p up to max_p
    for p in range(2, max_p + 1):
        pattern = expected_binary_pattern(p)
        n = int(pattern, 2)
        m_p, is_mp_prime = mersenne_prime(p)
        ratio = abundance_ratio(n)
        is_perfect = abs(ratio - 2.0) < 1e-10
        
        reverse_results.append({
            'p': p,
            'pattern': pattern,
            'n': n,
            'M_p': m_p,
            'is_mersenne_prime': is_mp_prime,
            'sigma_ratio': ratio,
            'is_perfect': is_perfect,
            'consistent': is_perfect == is_mp_prime  # Should match!
        })
    
    all_forward_match = all(r['matches'] for r in forward_results)
    all_reverse_consistent = all(r['consistent'] for r in reverse_results)
    
    return {
        'corollary': 'Binary Generation of Even Perfect Numbers',
        'forward_check': {
            'description': 'Every even perfect has pattern 1^p 0^{p-1}',
            'results': forward_results,
            'all_match': all_forward_match
        },
        'reverse_check': {
            'description': 'Pattern gives perfect iff 2^p-1 is prime',
            'results': reverse_results,
            'all_consistent': all_reverse_consistent
        },
        'verified': all_forward_match and all_reverse_consistent
    }


def print_theorem8_results(result: dict):
    """Pretty print Theorem 8 results."""
    print(f"\n{'='*70}")
    print(f"  {result['theorem']}")
    print(f"{'='*70}")
    print(f"  Statement: {result['statement']}")
    print(f"  VERIFIED: {'✓ YES' if result['verified'] else '✗ NO'}")
    print()
    print("   p │ M_p = 2^p-1 │         P = 2^(p-1)×M_p │  H │ binary pattern            │ σ/P")
    print("  ───┼─────────────┼─────────────────────────┼────┼───────────────────────────┼──────")
    
    for r in result['results']:
        if r.get('error'):
            print(f"  {r['p']:2d} │ {r['M_p']:11d} │ {'N/A':>23s} │ -- │ {r['error']}")
        else:
            status = '✓' if r['all_passed'] else '✗'
            binary_display = r['binary']
            if len(binary_display) > 25:
                binary_display = binary_display[:11] + '...' + binary_display[-11:]
            print(f"  {r['p']:2d} │ {r['M_p']:11d} │ {r['P']:23d} │ {r['H']:2d} │ {binary_display:>25s} │ {r['sigma_ratio']:.2f} {status}")
    print()


def print_binary_generation_results(result: dict):
    """Pretty print Binary Generation corollary results."""
    print(f"\n{'='*70}")
    print(f"  {result['corollary']}")
    print(f"{'='*70}")
    
    print("\n  Forward check (perfect → pattern):")
    for r in result['forward_check']['results']:
        status = '✓' if r['matches'] else '✗'
        print(f"    p={r['p']}: P={r['P']}, bin={r['binary'][:20]}... {status}")
    
    print(f"\n  Reverse check (pattern → perfect iff M_p prime):")
    print("    p │      n = 1^p 0^{p-1} │ M_p prime │ perfect │ consistent")
    print("   ───┼──────────────────────┼───────────┼─────────┼────────────")
    for r in result['reverse_check']['results'][:15]:
        mp_str = '✓' if r['is_mersenne_prime'] else '✗'
        pf_str = '✓' if r['is_perfect'] else '✗'
        cons_str = '✓' if r['consistent'] else '✗'
        print(f"   {r['p']:2d} │ {r['n']:20d} │ {mp_str:^9s} │ {pf_str:^7s} │ {cons_str:^10s}")
    
    print(f"\n  All consistent: {'✓ YES' if result['verified'] else '✗ NO'}")
    print()


if __name__ == "__main__":
    print("="*70)
    print(" BCT Theorem 8 (Even Perfect Number Structure) Verification")
    print("="*70)
    
    # Main theorem verification
    result = verify_theorem8()
    print_theorem8_results(result)
    
    # Power of Two Orthogonality Lemma
    print("\n[Lemma: Power of Two Orthogonality]")
    lemma_result = verify_power_of_two_orthogonality(max_a=10, max_m=100)
    print(f"  Statement: {lemma_result['statement']}")
    print(f"  Range: {lemma_result['range']}")
    print(f"  Total checked: {lemma_result['total_checked']}")
    print(f"  VERIFIED: {'✓ YES' if lemma_result['verified'] else '✗ NO'}")
    
    # Binary Generation Corollary
    print("\n[Corollary: Binary Generation]")
    gen_result = verify_binary_generation(max_p=15)
    print_binary_generation_results(gen_result)
    
    # Show the beautiful pattern
    print("\n[The Beautiful Pattern: 1^p 0^{p-1}]")
    print("  Even perfect numbers have this elegant binary structure:")
    for p in [2, 3, 5, 7]:
        P = even_perfect_number(p)
        binary = bin_str(P)
        print(f"    p={p}: {P:8d} = {binary}")
    print()
    
    # Caution example from paper
    print("\n[Caution: Pattern alone doesn't guarantee perfection]")
    p = 11
    pattern = expected_binary_pattern(p)
    n = int(pattern, 2)
    m_p, is_prime_mp = mersenne_prime(p)
    ratio = abundance_ratio(n)
    print(f"  p = {p}:")
    print(f"    Pattern 1^{p} 0^{p-1} = {n}")
    print(f"    M_{p} = 2^{p} - 1 = {m_p}")
    print(f"    Is M_{p} prime? {'YES' if is_prime_mp else f'NO ({m_p} = 23 × 89)'}")
    print(f"    σ(n)/n = {ratio:.6f} ≠ 2")
    print(f"    → NOT a perfect number!")
    print()
    
    # Summary
    print("="*70)
    print(" Summary")
    print("="*70)
    print(f"  Theorem 8: {'✓ VERIFIED' if result['verified'] else '✗ FAILED'}")
    print(f"  Power of Two Lemma: {'✓ VERIFIED' if lemma_result['verified'] else '✗ FAILED'}")
    print(f"  Binary Generation: {'✓ VERIFIED' if gen_result['verified'] else '✗ FAILED'}")
    print()
    print("  Key insight: Even perfect numbers have the elegant form")
    print("               bin(P) = 1^p 0^{p-1} when 2^p - 1 is Mersenne prime")
    print()
