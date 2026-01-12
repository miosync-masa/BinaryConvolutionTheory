"""
Binary Convolution Theory (BCT)
===============================
A Structural Approach to Perfect Numbers

Authors: Masamichi Iizumi, Tamaki Iizumi
"""

# coreから主要な関数をre-export
from .core import (
    # Binary utilities
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
    # BCT invariants
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

__version__ = '1.0.1'
__author__ = 'Masamichi Iizumi, Tamaki Iizumi'

__all__ = [
    'H', 'C', 'L', 'H_n2', 'L_parallel',
    'popcount', 'bit_positions', 'bin_seq', 'bin_str',
    'is_bct_perfect', 'is_binary_orthogonal',
    'is_mersenne', 'is_fermat', 'is_centrally_symmetric',
    'sigma', 'abundance_ratio',
    'binary_convolution', 'bct_invariants', 'analyze_factorization',
    'get_factorizations', 'bit_length', 'is_power_of_two',
    'FERMAT_PRIMES',
]
