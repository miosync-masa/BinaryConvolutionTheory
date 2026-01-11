"""
BCT-ζ Correspondence: Experimental Investigation
=================================================

This module explores the correspondence between Binary Convolution Theory
and the Riemann zeta function. This is EXPERIMENTAL research for future papers.

Key Findings (Preliminary):
---------------------------
1. Both BCT density gaps and zeta zero gaps show GUE statistics (var/mean < 1)
2. popcount/bits ratio may correspond to Re(s) on the critical strip
3. "Vanishing rate" in convolutions may correspond to ζ(s) = 0

Proposed Correspondence:
------------------------
    popcount/bits  ←→  Re(s)
    H(n) distribution  ←→  Zero distribution
    Vanishing rate  ←→  ζ(s) = 0
    GUE statistics  ←→  GUE statistics

WARNING: This is speculative research. Not peer-reviewed.

Authors: Masamichi Iizumi, Tamaki Iizumi
Date: 2026-01
"""

import numpy as np
from typing import List, Tuple, Optional


def popcount(n: int) -> int:
    """Count number of 1-bits in binary representation."""
    return bin(n).count('1')


def bit_length(n: int) -> int:
    """Return number of bits needed to represent n."""
    return len(bin(n)) - 2 if n > 0 else 1


def is_prime(n: int) -> bool:
    """Simple primality test."""
    if n < 2:
        return False
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            return False
    return True


def binary_convolution(a: int, b: int) -> List[int]:
    """
    Compute binary convolution before carry propagation.
    """
    bin_a = [int(x) for x in bin(a)[2:][::-1]]
    bin_b = [int(x) for x in bin(b)[2:][::-1]]
    conv_len = len(bin_a) + len(bin_b) - 1
    conv = [0] * conv_len
    for i, ai in enumerate(bin_a):
        for j, bj in enumerate(bin_b):
            conv[i + j] += ai * bj
    return conv


def H(a: int, b: int) -> int:
    """Binary Convolution Height."""
    return max(binary_convolution(a, b))


# =============================================================================
# BCT Density Analysis
# =============================================================================

def compute_density_ratios(primes: List[int]) -> List[float]:
    """
    Compute popcount/bits ratio for each prime.
    
    This ratio is conjectured to correspond to Re(s) in the critical strip.
    """
    return [popcount(p) / bit_length(p) for p in primes]


def compute_density_gaps(density_ratios: List[float]) -> List[float]:
    """
    Compute gaps between adjacent density ratios.
    """
    return [abs(density_ratios[i+1] - density_ratios[i]) 
            for i in range(len(density_ratios)-1)]


# =============================================================================
# GUE Statistics
# =============================================================================

def variance_mean_ratio(gaps: List[float]) -> float:
    """
    Compute variance/mean ratio.
    
    GUE (random matrix) → ratio < 1 (level repulsion)
    Poisson (random) → ratio ≈ 1
    """
    if len(gaps) == 0 or np.mean(gaps) == 0:
        return float('inf')
    return np.var(gaps) / np.mean(gaps)


def classify_statistics(ratio: float) -> str:
    """Classify gap statistics based on var/mean ratio."""
    if ratio < 0.5:
        return "Strongly GUE-like"
    elif ratio < 1.0:
        return "GUE-like (level repulsion)"
    elif ratio < 1.2:
        return "Near Poisson"
    else:
        return "Super-Poisson (clustering)"


# =============================================================================
# Vanishing Rate Analysis
# =============================================================================

def vanishing_rate(n: int) -> Optional[float]:
    """
    Compute vanishing rate = fraction of zeros in convolution.
    
    Higher vanishing rate → closer to "zero" of some function.
    Conjectured to correspond to ζ(s) approaching 0.
    """
    if is_prime(n) or n < 4:
        return None
    
    for a in range(2, int(n**0.5) + 1):
        if n % a == 0:
            b = n // a
            conv = binary_convolution(a, b)
            zeros = sum(1 for c in conv if c == 0)
            return zeros / len(conv)
    return 0.0


def interference_balance(n: int) -> Optional[float]:
    """
    Compute interference balance = (H - 1) / min_popcount.
    
    0 → perfect orthogonality (BCT-perfect)
    1 → maximum resonance
    """
    if is_prime(n) or n < 4:
        return None
    
    for a in range(2, int(n**0.5) + 1):
        if n % a == 0:
            b = n // a
            h = H(a, b)
            pop_min = min(popcount(a), popcount(b))
            if pop_min > 0:
                return (h - 1) / pop_min
    return 0.0


def effective_sigma(n: int) -> float:
    """
    Compute effective sigma based on popcount/bits.
    
    This is conjectured to correspond to Re(s).
    When popcount/bits = 0.5, we are on the "critical line".
    """
    if n < 2:
        return 0.5
    
    pop = popcount(n)
    bits = bit_length(n)
    
    # Deviation from 0.5
    deviation = abs(pop/bits - 0.5)
    
    # Re(s) analog: 0.5 + deviation
    return 0.5 + deviation


# =============================================================================
# Zeta Zero Data (for comparison)
# =============================================================================

# First 20 non-trivial zeros of ζ(s) on critical line (imaginary parts)
ZETA_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840
]


def compute_zeta_gaps() -> Tuple[List[float], float]:
    """
    Compute normalized gaps between zeta zeros.
    
    Returns:
        (gaps, var_mean_ratio)
    """
    gaps = [ZETA_ZEROS[i+1] - ZETA_ZEROS[i] for i in range(len(ZETA_ZEROS)-1)]
    mean_gap = np.mean(gaps)
    normalized = [g / mean_gap for g in gaps]
    ratio = np.var(normalized) / np.mean(normalized)
    return gaps, ratio


# =============================================================================
# Main Verification
# =============================================================================

def run_bct_zeta_comparison(max_prime: int = 2000, verbose: bool = True):
    """
    Run full BCT-ζ correspondence analysis.
    
    Args:
        max_prime: Upper limit for prime search
        verbose: Print detailed output
        
    Returns:
        Dictionary of results
    """
    primes = [p for p in range(2, max_prime) if is_prime(p)]
    
    # BCT density analysis
    density_ratios = compute_density_ratios(primes)
    density_gaps = compute_density_gaps(density_ratios)
    bct_ratio = variance_mean_ratio(density_gaps)
    
    # Zeta zero analysis
    zeta_gaps, zeta_ratio = compute_zeta_gaps()
    
    # H(n) analysis
    composites = [n for n in range(4, 500) if not is_prime(n)]
    H_values = []
    for n in composites:
        for a in range(2, int(n**0.5) + 1):
            if n % a == 0:
                H_values.append(H(a, n // a))
                break
    
    H_gaps = [abs(H_values[i+1] - H_values[i]) for i in range(len(H_values)-1)]
    H_ratio = variance_mean_ratio(H_gaps)
    
    results = {
        'bct_density_var_mean': bct_ratio,
        'zeta_gaps_var_mean': zeta_ratio,
        'H_gaps_var_mean': H_ratio,
        'bct_classification': classify_statistics(bct_ratio),
        'zeta_classification': classify_statistics(zeta_ratio),
        'H_classification': classify_statistics(H_ratio),
        'density_mean': np.mean(density_ratios),
        'density_std': np.std(density_ratios),
    }
    
    if verbose:
        print("=" * 70)
        print("BCT-ζ CORRESPONDENCE ANALYSIS")
        print("=" * 70)
        print()
        print("【Variance/Mean Ratios】 (GUE → < 1, Poisson → ≈ 1)")
        print(f"  BCT density gaps:  {bct_ratio:.4f} → {results['bct_classification']}")
        print(f"  Zeta zero gaps:    {zeta_ratio:.4f} → {results['zeta_classification']}")
        print(f"  H(n) gaps:         {H_ratio:.4f} → {results['H_classification']}")
        print()
        print("【Conjectured Correspondence】")
        print("  popcount/bits  ←→  Re(s)")
        print("  H(n) spectrum  ←→  Zero spectrum")  
        print("  Vanishing rate ←→  ζ(s) = 0")
        print("  GUE statistics ←→  GUE statistics")
        print()
        print("【Critical Line Conjecture】")
        print("  popcount/bits = 0.5 corresponds to Re(s) = 1/2")
        print(f"  Mean popcount/bits for primes: {results['density_mean']:.4f}")
        print()
    
    return results


if __name__ == "__main__":
    results = run_bct_zeta_comparison()
    
    print("=" * 70)
    print("【Sample Vanishing Rates】")
    print("=" * 70)
    print()
    print(f"{'n':>6} | {'Vanishing':>10} | {'Interference':>12} | {'Eff. σ':>8}")
    print("-" * 45)
    
    test_numbers = [6, 15, 21, 28, 35, 51, 85, 105, 255, 496]
    for n in test_numbers:
        vr = vanishing_rate(n)
        ib = interference_balance(n)
        es = effective_sigma(n)
        if vr is not None:
            print(f"{n:>6} | {vr:>10.3f} | {ib:>12.3f} | {es:>8.3f}")
