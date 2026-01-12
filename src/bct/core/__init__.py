"""
Binary Convolution Theory - Core Module
=======================================

This module provides the foundational definitions for BCT:

Binary Utilities (binary_utils):
    - bin_seq: Binary representation as sequence
    - popcount: Hamming weight
    - bit_positions: Set of 1-bit positions
    - is_mersenne, is_fermat: Special number detection
    - is_centrally_symmetric: For Theorem 3

BCT Invariants (bct_invariants):
    - H(a, b): Binary Convolution Height
    - C(a, b): Carry Count
    - L(a, b): Chain Length
    - is_bct_perfect: BCT-perfectness test
    - is_binary_orthogonal: Orthogonality test
"""

from .binary_utils import (
    bin_seq,
    bin_str,
    popcount,
    bit_positions,
    bit_length,
    is_power_of_two,
    is_mersenne,
    is_fermat,
    is_centrally_symmetric,
    get_factorizations,
    FERMAT_PRIMES,
)

from .bct_invariants import (
    binary_convolution,
    H,
    H_n2,
    C,
    L,
    L_parallel,
    is_binary_orthogonal,
    is_bct_perfect,
    bct_invariants,
    analyze_factorization,
    sigma,
    abundance_ratio,
)

__all__ = [
    # Binary utilities
    'bin_seq',
    'bin_str',
    'popcount',
    'bit_positions',
    'bit_length',
    'is_power_of_two',
    'is_mersenne',
    'is_fermat',
    'is_centrally_symmetric',
    'get_factorizations',
    'FERMAT_PRIMES',
    # BCT invariants
    'binary_convolution',
    'H',
    'H_n2',
    'C',
    'L',
    'L_parallel',
    'is_binary_orthogonal',
    'is_bct_perfect',
    'bct_invariants',
    'analyze_factorization',
    'sigma',
    'abundance_ratio',
]

__version__ = '0.1.0'
