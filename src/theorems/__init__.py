"""
Binary Convolution Theory - Theorems Module
============================================

Verification code for all theorems in the BCT paper.

Modules:
    - thm1_2_upper_bound: Theorem 1 (Upper Bound) & Theorem 2 (Self-Conv Bound)
    - thm3_equality_condition: Theorem 3 (Central Symmetry ⟺ Equality)
    - thm4_5_mersenne: Theorem 4 (Mersenne Equality) & Theorem 5 (Carry Formula)
    - thm6_fermat_resonance: Theorem 6 (Fermat Minimum Resonance)
    - thm7_sweep: Theorem 7 (Single-sweep normalization)
    - thm8_even_perfect: Theorem 8 (Even Perfect Number Structure)
    - thm9_fermat_orthogonality: Theorem 9 (Fermat Prime Orthogonality)
    - thm10_structure: Theorem 10 (BCT-Perfect Structure)
    - thm11_abundance: Theorem 11 (Abundance Bounds)
    - thm12_obstruction: Theorem 12 (BCT Obstruction)
"""

from .thm1_2_upper_bound import (
    verify_theorem1,
    verify_theorem2,
    verify_theorem1_single,
    verify_theorem2_single,
    find_equality_cases,
)

from .thm3_equality_condition import (
    verify_theorem3,
    verify_theorem3_single,
    pigeonhole_bound,
    gap_upper_bound,
    verify_paper_example_807743,
    analyze_symmetry_patterns,
)

from .thm4_5_mersenne import (
    verify_theorem4,
    verify_theorem5,
    verify_theorem4_single,
    verify_theorem5_single,
    mersenne,
    expected_mersenne_convolution,
    expected_carry_count,
    verify_convolution_pattern,
)

from .thm6_fermat_resonance import (
    verify_theorem6,
    verify_theorem6_single,
    fermat,
    verify_fermat_convolution,
    FERMAT_PRIMES,
)

from .thm7_prop5_sweep import (
    verify_theorem7,
    verify_theorem7_single,
    verify_proposition5,
    verify_proposition5_single,
    proposition5_m,
    analyze_parallel_vs_sequential,
)

from .thm8_even_perfect import (
    verify_theorem8,
    verify_theorem8_single,
    verify_power_of_two_orthogonality,
    verify_binary_generation,
    even_perfect_number,
    expected_binary_pattern,
    MERSENNE_PRIME_EXPONENTS,
)

from .lemma4_thm9_fermat import (
    verify_lemma4,
    verify_lemma4_single,
    verify_theorem9,
    verify_theorem9_single,
    get_fermat_number,
    demonstrate_orthogonality_structure,
)

from .thm10_structure import (
    verify_theorem10,
    classify_structure,
    format_factorization,
)

from .thm11_conjecture1_abundance import (
    verify_theorem11b,
    verify_conjecture1,
    find_bct_perfect_odds,
    classify_structure,
    analyze_fermat_products,
)

from .remaining_lemmas_theorems import (
    verify_lemma1,
    verify_lemma2,
    verify_lemma3,
    verify_theorem11a,
    verify_theorem12,
    verify_theorem13,
    verify_table2,
    pigeonhole_lower_bound,
    get_odd_part,
)

__all__ = [
    # Theorem 1 & 2
    'verify_theorem1',
    'verify_theorem2',
    'verify_theorem1_single',
    'verify_theorem2_single',
    'find_equality_cases',
    # Theorem 3
    'verify_theorem3',
    'verify_theorem3_single',
    'pigeonhole_bound',
    'gap_upper_bound',
    'verify_paper_example_807743',
    'analyze_symmetry_patterns',
    # Theorem 4 & 5 (Mersenne)
    'verify_theorem4',
    'verify_theorem5',
    'verify_theorem4_single',
    'verify_theorem5_single',
    'mersenne',
    'expected_mersenne_convolution',
    'expected_carry_count',
    'verify_convolution_pattern',
    # Theorem 6 (Fermat)
    'verify_theorem6',
    'verify_theorem6_single',
    'fermat',
    'verify_fermat_convolution',
    'FERMAT_PRIMES',
    # Theorem 7 & Proposition 5 (Sweep)
    'verify_theorem7',
    'verify_theorem7_single',
    'verify_proposition5',
    'verify_proposition5_single',
    'proposition5_m',
    'analyze_parallel_vs_sequential',
    # Theorem 8 (Even Perfect)
    'verify_theorem8',
    'verify_theorem8_single',
    'verify_power_of_two_orthogonality',
    'verify_binary_generation',
    'even_perfect_number',
    'expected_binary_pattern',
    'MERSENNE_PRIME_EXPONENTS',
    # Lemma 4 & Theorem 9 (Fermat)
    'verify_lemma4',
    'verify_lemma4_single',
    'verify_theorem9',
    'verify_theorem9_single',
    'get_fermat_number',
    'demonstrate_orthogonality_structure',
    # Theorem 10 (Structure)
    'verify_theorem10',
    'classify_structure',
    'format_factorization',
    # Theorem 11(b) & Conjecture 1 (Abundance Bounds)
    'verify_theorem11b',
    'verify_conjecture1',
    'find_bct_perfect_odds',
    'classify_structure',
    'analyze_fermat_products',
    # Remaining Lemmas & Theorems
    'verify_lemma1',
    'verify_lemma2',
    'verify_lemma3',
    'verify_theorem11a',
    'verify_theorem12',
    'verify_theorem13',
    'verify_table2',
    'pigeonhole_lower_bound',
    'get_odd_part',
]
