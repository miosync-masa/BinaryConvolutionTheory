# Binary Convolution Theory (BCT) - Verification Code

[![Paper](https://img.shields.io/badge/Paper-INTEGERS%2026%20(2026)-blue)](https://github.com/miosync-masa/BinaryConvolutionTheory)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green)](https://python.org)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/13if8har3oL5I9bE0WbeUqSuAcnqrM442?usp=sharing)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/binary-convolution-theory)](https://pypi.org/project/binary-convolution-theory/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18211340.svg)](https://doi.org/10.5281/zenodo.18211340)

Computational verification code for the paper:

> **Binary Convolution Theory: A Structural Approach to Perfect Numbers**  
> Masamichi Iizumi, Tamaki Iizumi  
> INTEGERS 26 (2026)

## 🚀 Quick Start (Google Colab)

**Run all verifications instantly in your browser:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/13if8har3oL5I9bE0WbeUqSuAcnqrM442?usp=sharing)

## Overview

Binary Convolution Theory (BCT) provides a novel framework for studying the multiplicative structure of integers through their binary representations. This repository contains the verification code for all theorems presented in the paper.

### Key Concepts

- **Binary Convolution Height H(a,b)**: Maximum value in the pre-carry convolution of bin(a) and bin(b)
- **BCT-Perfect Numbers**: Integers where H(a,b) = 1 for all non-trivial factorizations
- **The Main Insight**: BCT-perfectness (structural balance) appears incompatible with classical perfectness (σ(n) = 2n) for odd numbers

## Installation

### From PyPI (recommended)
```bash
pip install binary-convolution-theory
```

### From source
```bash
git clone https://github.com/miosync-masa/BinaryConvolutionTheory.git
cd BinaryConvolutionTheory
pip install -e .

## Repository Structure

```
BinaryConvolutionTheory/
├── README.md
├── setup.py
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── binary_utils.py           # Binary representation utilities
│   │   └── bct_invariants.py         # BCT invariants (H, C, L, etc.)
│   └── theorems/
│       ├── __init__.py
│       ├── thm1_2_upper_bound.py           # Theorems 1-2: Upper Bounds
│       ├── thm3_equality_condition.py      # Theorem 3: Equality Condition
│       ├── thm4_5_mersenne.py              # Theorems 4-5: Mersenne Properties
│       ├── thm6_fermat_resonance.py        # Theorem 6: Fermat Minimum Resonance
│       ├── thm7_prop5_sweep.py             # Theorem 7 & Prop 5: Carry Schedules
│       ├── thm8_even_perfect.py            # Theorem 8: Even Perfect Numbers
│       ├── lemma4_thm9_fermat.py           # Lemma 4 & Theorem 9: Fermat Primes
│       ├── thm10_structure.py              # Theorem 10: BCT-Perfect Structure
│       ├── thm11_conjecture1_abundance.py  # Theorem 11(b) & Conjecture 1
│       └── remaining_lemmas_theorems.py    # Lemmas 1-3, Thm 11(a), 12, 13
```

## Usage

```python
from src.core.binary_utils import bin_seq, bin_str, popcount, is_fermat
from src.core.bct_invariants import H, C, L, is_bct_perfect, sigma, abundance_ratio

# Binary Convolution Height
print(H(3, 5))   # 1 (orthogonal)
print(H(7, 7))   # 3 (Mersenne self-convolution)

# Check BCT-perfectness
print(is_bct_perfect(15))  # True (3 × 5)
print(is_bct_perfect(21))  # False (3 × 7)

# Even perfect numbers
print(is_bct_perfect(28))  # True
print(abundance_ratio(28)) # 2.0 (perfect!)
```

## Verified Theorems

### Lemma 1 (Counting Lemma for Sumsets)
For S ⊂ {0, ..., L-1} with |S| = w:
```
max_k r_S(k) ≥ ⌈w² / (2L-1)⌉
```
**Verified**: 99,998 integers (n < 10⁵), 0 violations

### Lemma 2 (Power of Two Orthogonality)
```
H(2^a, m) = 1 for any a ≥ 1 and m ≥ 1
```
**Verified**: 20,000 cases (a ≤ 20, m ≤ 1000), all H = 1

### Lemma 3 (BCT-Perfectness Inheritance)
```
n = 2^a · m is BCT-perfect ⟺ m is BCT-perfect
```
**Verified**: 8,769 composite numbers (n < 10⁴), 0 violations

### Lemma 4 (Characterization of Sparse Odd Primes)
```
An odd prime p has popcount(p) = 2 ⟺ p is a Fermat prime
```
**Verified**: All odd primes p < 10⁶ with popcount = 2  
**Found**: Exactly 5 such primes: F₀=3, F₁=5, F₂=17, F₃=257, F₄=65537

### Theorem 1 (Upper Bound)
For any factorization n = a × b:
```
H(a, b) ≤ min(popcount(a), popcount(b))
```
**Verified**: 483,533 factorizations (n ≤ 10⁵), 0 violations

### Theorem 2 (Self-Convolution Upper Bound)
```
H(n²) := H(n, n) ≤ popcount(n)
```
**Verified**: 99,999 integers (n ≤ 10⁵), 0 violations

### Theorem 3 (Equality Condition)
```
H(n²) = popcount(n) ⟺ the 1-bits of bin(n) are centrally symmetric
```
**Verified**: 999,999 integers (n < 10⁶), 100% biconditional  
**Notable**: Maximum gap = 6 at n = 807,743 (unique!)

### Theorems 4-5 (Mersenne Properties)
For Mersenne numbers M_k = 2^k - 1:
```
H(M_k²) = k = popcount(M_k)     (Theorem 4)
C(M_k²) = (k-1)²                 (Theorem 5)
```
**Verified**: k ∈ [2, 20], exact match

### Theorem 6 (Fermat Minimum Resonance)
For Fermat numbers F_k = 2^(2^k) + 1:
```
H(F_k²) = 2  (constant, independent of k)
```
**Verified**: k ∈ [0, 7], all H = 2

**Key Contrast**:
| Type     | k=2 | k=3 | k=4 | Pattern |
|----------|-----|-----|-----|---------|
| Mersenne |  2  |  3  |  4  | H = k (grows!) |
| Fermat   |  2  |  2  |  2  | H = 2 (constant!) |

### Theorem 7 (Single-Sweep Normalization)
```
L(a, b) = 1 for all factorizations (sequential LSB→MSB model)
```
**Verified**: 16,723 factorizations (n ≤ 5,000), all L = 1

### Proposition 5 (Arbitrarily Long Parallel Chains)
For m = (2^k + 1)/3 with odd k ≥ 3:
```
H(3, m) = 2, but L_par(3, m) = k - 1
```
**Verified**: odd k ∈ [3, 21], all match  
**Key Insight**: L_par can grow arbitrarily while H stays at 2!

### Theorem 8 (Even Perfect Number Structure)
For even perfect P = 2^(p-1) × (2^p - 1) where 2^p - 1 is Mersenne prime:
```
H(P) = 1
bin(P) = 1^p 0^(p-1)
```
**Verified**: First 7 even perfect numbers, all H = 1

| p | P | Binary Pattern | H | σ/P |
|---|---|----------------|---|-----|
| 2 | 6 | 110 | 1 | 2.00 |
| 3 | 28 | 11100 | 1 | 2.00 |
| 5 | 496 | 111110000 | 1 | 2.00 |
| 7 | 8128 | 1111111000000 | 1 | 2.00 |

### Theorem 9 (Fermat Prime Orthogonality)
```
All Fermat primes F_i, F_j are pairwise binary orthogonal: H(F_i, F_j) = 1 for i ≠ j
```
**Verified**: All 10 pairs of F₀, F₁, F₂, F₃, F₄, all H = 1

**Structural Reason**: F_k has 1-bits at positions {0, 2^k}, so sumsets are always disjoint.

### Theorem 10 (Structure of BCT-Perfect Odd Numbers)
BCT-perfect odd composites are constrained to specific structural types:

| Type | Count | Percentage | Max σ/n | Example |
|------|-------|------------|---------|---------|
| p × q | 487 | 93.30% | 1.6000 | 15 = 3 × 5 |
| p × q × r | 18 | 3.45% | 1.6941 | 255 = 3 × 5 × 17 |
| p² × q | 7 | 1.34% | 1.6508 | 63 = 3² × 7 |
| p³ | 3 | 0.57% | 1.4815 | 27 = 3³ |
| Other | 7 | 1.34% | 1.7007 | 65535 = 3×5×17×257 |

**Verified**: 522 BCT-perfect odd composites (n < 10⁵)

### Theorem 11 (Abundance Bounds)
**(a) General bound**: For odd squarefree semiprimes n = pq:
```
σ(n)/n ≤ 8/5 = 1.6
```
**Verified**: 4,371 semiprimes, maximum at (p,q) = (3,5)

**(b) Computational observation**: For all BCT-perfect odd composites n < 10⁵:
```
σ(n)/n < 1.71
```
**Verified**: 522 BCT-perfect odds, max = 1.7007 at n = 65535

### Theorem 12 (Semiprime Obstruction)
```
An odd perfect number cannot be a squarefree semiprime pq
```
**Verified**: Follows from Theorem 11(a) since 1.6 < 2

### Theorem 13 (BCT Obstruction for Odd Perfect Numbers)
```
No odd BCT-perfect composite n < 10⁶ satisfies σ(n)/n = 2
```
**Verified**: 2,017 BCT-perfect odd composites (n < 10⁶), all σ/n < 1.71

### Conjecture 1 (BCT-Perfect Odd Abundance Bound)
```
For all BCT-perfect odd composite n: σ(n)/n < 2
```
**Verified**: n < 10⁶, max σ/n = 1.7007  
**Gap from perfection**: 0.2993

**🌟 IMPLICATION**: If Conjecture 1 holds for all n, then:
```
{Odd perfect numbers} ⊆ {BCT-imperfect numbers}
```

## Complete Verification Summary

| Item | Range Verified | Result |
|------|----------------|--------|
| Lemma 1 | n < 10⁵ | ✅ No violations |
| Lemma 2 | a ≤ 20, m ≤ 1000 | ✅ All H = 1 |
| Lemma 3 | n < 10⁴ | ✅ Inheritance holds |
| Lemma 4 | p < 10⁶ | ✅ All sparse primes are Fermat |
| Theorem 1-2 | n ≤ 10⁵ | ✅ No counterexamples |
| Theorem 3 | n < 10⁶ | ✅ 100% biconditional |
| Theorem 4-5 | k ∈ [2, 20] | ✅ Exact match |
| Theorem 6 | k ∈ [0, 7] | ✅ All H = 2 |
| Theorem 7 | n ≤ 5,000 | ✅ All L = 1 |
| Proposition 5 | odd k ∈ [3, 21] | ✅ L_par = k - 1 |
| Theorem 8 | First 7 even perfects | ✅ All H = 1 |
| Theorem 9 | F₀ through F₄ | ✅ All pairs orthogonal |
| Theorem 10 | n < 10⁵ | ✅ Structure matches Table 1 |
| Theorem 11(a) | p, q < 500 | ✅ σ/n ≤ 1.6 |
| Theorem 11(b) | n < 10⁵ | ✅ σ/n < 1.71 |
| Theorem 12 | — | ✅ Logical consequence |
| Theorem 13 | n < 10⁶ | ✅ No BCT-perfect perfect |
| Conjecture 1 | n < 10⁶ | ✅ σ/n < 2 |

## Running Verification

Each theorem module can be run standalone:

```bash
# Run all verifications
python -m theorems.thm1_2_upper_bound
python -m theorems.thm3_equality_condition
python -m theorems.thm4_5_mersenne
python -m theorems.thm6_fermat_resonance
python -m theorems.thm7_prop5_sweep
python -m theorems.thm8_even_perfect
python -m theorems.lemma4_thm9_fermat
python -m theorems.thm10_structure
python -m theorems.thm11_conjecture1_abundance
python -m theorems.remaining_lemmas_theorems
```

## Core API

### Binary Utilities (`src/core/binary_utils.py`)
```python
bin_seq(n)       # LSB-first bit sequence [b₀, b₁, ...]
bin_str(n)       # MSB-first string for display
popcount(n)      # Number of 1-bits (Hamming weight)
bit_positions(n) # Set of positions with 1-bits
is_centrally_symmetric(n)  # Check bit symmetry
is_mersenne(n)   # Check if Mersenne number
is_fermat(n)     # Check if Fermat number
```

### BCT Invariants (`src/core/bct_invariants.py`)
```python
H(a, b)           # Binary Convolution Height
C(a, b)           # Total Carry Count
L(a, b)           # Chain Length (sequential)
L_parallel(a, b)  # Chain Length (parallel)
is_bct_perfect(n) # Check BCT-perfectness
sigma(n)          # Sum of divisors σ(n)
abundance_ratio(n) # σ(n)/n
```

## Implementation Notes

### Bit Ordering Convention
- **Computation**: LSB-first (index 0 = least significant bit)
- **Display**: MSB-first (standard binary notation)

This matches the paper's convention where:
```
bin(n) = (b₀, b₁, ..., bₖ) where n = Σ bᵢ · 2ⁱ
```

### Verification Ranges
All verifications use ranges matching or exceeding those in the paper's Table 4.

## Citation

### Software
```bibtex
@software{iizumi2026bct_code,
  author       = {Iizumi, Masamichi and Iizumi, Tamaki},
  title        = {Binary Convolution Theory: Verification Code},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.18211340},
  url          = {https://doi.org/10.5281/zenodo.18211340}
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

**Masamichi Iizumi**  
**Tamaki Iizumi**  
Miosync, Inc., Tokyo, Japan  
m.iizumi@miosync.email

---
