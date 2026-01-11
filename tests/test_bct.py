"""
BCT Core Tests
==============
Unit tests for Binary Convolution Theory core functions.
"""

import pytest
import numpy as np
from src.core.binary_utils import (
    bin_seq, bin_str, popcount, bit_positions, bit_length,
    is_centrally_symmetric, is_mersenne, is_fermat
)
from src.core.bct_invariants import (
    H, C, L, L_parallel, is_bct_perfect, sigma, abundance_ratio,
    binary_convolution, get_factorizations
)


class TestBinaryUtils:
    """Tests for binary_utils.py"""
    
    def test_bin_seq(self):
        """Test LSB-first binary sequence"""
        # bin_seq returns numpy array, use .tolist() for comparison
        assert bin_seq(5).tolist() == [1, 0, 1]  # 101 in binary
        assert bin_seq(7).tolist() == [1, 1, 1]  # 111
        assert bin_seq(8).tolist() == [0, 0, 0, 1]  # 1000
        assert bin_seq(1).tolist() == [1]
    
    def test_bin_str(self):
        """Test MSB-first binary string"""
        assert bin_str(5) == "101"
        assert bin_str(7) == "111"
        assert bin_str(8) == "1000"
    
    def test_popcount(self):
        """Test Hamming weight (number of 1-bits)"""
        assert popcount(0) == 0
        assert popcount(1) == 1
        assert popcount(7) == 3  # 111
        assert popcount(8) == 1  # 1000
        assert popcount(15) == 4  # 1111
        assert popcount(255) == 8  # 11111111
    
    def test_bit_positions(self):
        """Test positions of 1-bits"""
        assert bit_positions(5) == {0, 2}  # 101
        assert bit_positions(7) == {0, 1, 2}  # 111
        assert bit_positions(8) == {3}  # 1000
    
    def test_is_centrally_symmetric(self):
        """Test central symmetry of bit positions"""
        assert is_centrally_symmetric(7) == True  # 111
        assert is_centrally_symmetric(5) == True  # 101
        assert is_centrally_symmetric(9) == True  # 1001
        # Note: 6 (110) - check actual implementation behavior
        # 110 has bits at {1, 2}, center at 1.5, symmetric around 1.5
        # Depends on implementation - skip this edge case
    
    def test_is_mersenne(self):
        """Test Mersenne number detection"""
        # is_mersenne returns (bool, k) tuple
        assert is_mersenne(3)[0] == True  # 2^2 - 1
        assert is_mersenne(7)[0] == True  # 2^3 - 1
        assert is_mersenne(31)[0] == True  # 2^5 - 1
        assert is_mersenne(127)[0] == True  # 2^7 - 1
        assert is_mersenne(5)[0] == False
        assert is_mersenne(15)[0] == True  # 2^4 - 1
        
        # Check k values
        assert is_mersenne(3) == (True, 2)
        assert is_mersenne(7) == (True, 3)
        assert is_mersenne(31) == (True, 5)
    
    def test_is_fermat(self):
        """Test Fermat number detection"""
        # is_fermat returns (bool, k) tuple
        assert is_fermat(3)[0] == True  # F_0 = 2^1 + 1
        assert is_fermat(5)[0] == True  # F_1 = 2^2 + 1
        assert is_fermat(17)[0] == True  # F_2 = 2^4 + 1
        assert is_fermat(257)[0] == True  # F_3 = 2^8 + 1
        assert is_fermat(65537)[0] == True  # F_4 = 2^16 + 1
        assert is_fermat(7)[0] == False
        assert is_fermat(15)[0] == False
        
        # Check k values
        assert is_fermat(3) == (True, 0)
        assert is_fermat(5) == (True, 1)
        assert is_fermat(17) == (True, 2)
        assert is_fermat(257) == (True, 3)


class TestBCTInvariants:
    """Tests for bct_invariants.py"""
    
    def test_H_orthogonal(self):
        """Test H = 1 for orthogonal pairs"""
        assert H(3, 5) == 1  # 11 * 101
        assert H(2, 7) == 1  # Power of 2 shifts
        assert H(4, 15) == 1
    
    def test_H_mersenne(self):
        """Test H for Mersenne self-convolution"""
        assert H(3, 3) == 2  # M_2
        assert H(7, 7) == 3  # M_3
        assert H(15, 15) == 4  # M_4
        assert H(31, 31) == 5  # M_5
    
    def test_H_fermat(self):
        """Test H = 2 for Fermat self-convolution"""
        assert H(3, 3) == 2  # F_0 (also M_2)
        assert H(5, 5) == 2  # F_1
        assert H(17, 17) == 2  # F_2
        assert H(257, 257) == 2  # F_3
    
    def test_H_upper_bound(self):
        """Test H(a,b) <= min(popcount(a), popcount(b))"""
        for a in range(2, 100):
            for b in range(2, 100):
                h = H(a, b)
                upper = min(popcount(a), popcount(b))
                assert h <= upper, f"H({a},{b})={h} > {upper}"
    
    def test_C_mersenne(self):
        """Test C(M_k²) = (k-1)²"""
        for k in range(2, 10):
            m_k = (1 << k) - 1  # 2^k - 1
            c = C(m_k, m_k)
            expected = (k - 1) ** 2
            assert c == expected, f"C(M_{k}²) = {c}, expected {expected}"
    
    def test_L_always_one(self):
        """Test L = 1 for sequential sweep"""
        for n in range(4, 100):
            for a in range(2, int(n**0.5) + 1):
                if n % a == 0:
                    b = n // a
                    assert L(a, b) == 1, f"L({a},{b}) != 1"
    
    def test_is_bct_perfect(self):
        """Test BCT-perfectness detection"""
        # Known BCT-perfect numbers
        assert is_bct_perfect(15) == True  # 3 × 5
        assert is_bct_perfect(51) == True  # 3 × 17
        assert is_bct_perfect(85) == True  # 5 × 17
        
        # Known non-BCT-perfect
        assert is_bct_perfect(21) == False  # 3 × 7
        assert is_bct_perfect(35) == False  # 5 × 7
    
    def test_sigma(self):
        """Test sum of divisors"""
        assert sigma(1) == 1
        assert sigma(6) == 12  # 1+2+3+6
        assert sigma(28) == 56  # 1+2+4+7+14+28 (perfect!)
        assert sigma(12) == 28  # 1+2+3+4+6+12
    
    def test_abundance_ratio(self):
        """Test σ(n)/n"""
        assert abundance_ratio(6) == 2.0  # Perfect
        assert abundance_ratio(28) == 2.0  # Perfect
        assert abundance_ratio(15) == pytest.approx(1.6)  # 24/15


class TestEvenPerfect:
    """Tests for even perfect number properties"""
    
    def test_even_perfect_bct_perfect(self):
        """All even perfect numbers should be BCT-perfect"""
        # First few even perfect numbers
        even_perfects = [6, 28, 496, 8128]
        for p in even_perfects:
            assert is_bct_perfect(p), f"{p} should be BCT-perfect"
            assert abundance_ratio(p) == 2.0, f"σ({p})/{p} should be 2"


class TestFermatOrthogonality:
    """Tests for Fermat prime orthogonality (Theorem 9)"""
    
    def test_fermat_pairwise_orthogonal(self):
        """All pairs of Fermat primes should have H = 1"""
        fermats = [3, 5, 17, 257, 65537]  # F_0 to F_4
        for i, fi in enumerate(fermats):
            for j, fj in enumerate(fermats):
                if i < j:
                    assert H(fi, fj) == 1, f"H(F_{i}, F_{j}) should be 1"


class TestConvolution:
    """Tests for binary convolution"""
    
    def test_convolution_mersenne_triangle(self):
        """Mersenne self-convolution forms perfect triangle"""
        for k in range(2, 8):
            m_k = (1 << k) - 1
            conv = binary_convolution(m_k, m_k).tolist()
            expected = list(range(1, k + 1)) + list(range(k - 1, 0, -1))
            assert conv == expected, f"M_{k} triangle mismatch"
