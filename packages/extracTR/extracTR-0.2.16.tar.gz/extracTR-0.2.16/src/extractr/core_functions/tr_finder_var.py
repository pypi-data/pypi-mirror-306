from collections import deque
import math
from typing import Dict, List, Tuple, Optional
import numpy as np

class RepeatWithVariants:
    def __init__(self, core_sequence: str):
        self.core_sequence = core_sequence
        self.variants: Dict[int, List[Tuple[str, float]]] = {}
        self.consensus: Optional[str] = None
        self.entropy_profile: Dict[int, float] = {}
        
    def add_variant(self, position: int, nucleotide: str, frequency: float):
        if position not in self.variants:
            self.variants[position] = []
        self.variants[position].append((nucleotide, frequency))
        
    def calculate_position_entropy(self, position: int) -> float:
        variants = self.variants.get(position, [])
        if not variants:
            return 0.0
        total = sum(freq for _, freq in variants)
        probabilities = [freq/total for _, freq in variants]
        return -sum(p * math.log2(p) for p in probabilities if p > 0)
    
    def build_consensus(self):
        """Build consensus sequence considering all variants"""
        self.consensus = list(self.core_sequence)
        for pos, variants in self.variants.items():
            if variants:
                # Use the most frequent variant
                most_frequent = max(variants, key=lambda x: x[1])
                self.consensus[pos] = most_frequent[0]
        self.consensus = ''.join(self.consensus)
        
def tr_finder_with_variants(sdat: List[Tuple[str, int]], 
                          kmer2tf: Dict[str, int],
                          max_depth: int = 30_000,
                          coverage: int = 30,
                          variant_threshold: float = 0.3,
                          k: int = 23) -> List[RepeatWithVariants]:
    """
    Enhanced repeat finder that considers sequence variants.
    
    Args:
        sdat: List of tuples (kmer, tf) sorted by tf descending
        kmer2tf: Dictionary mapping k-mer to its tf value
        max_depth: Maximum extension length
        coverage: Minimum coverage threshold
        variant_threshold: Minimum fraction of max tf to consider as variant
        k: k-mer size
    
    Returns:
        List of RepeatWithVariants objects
    """
    MIN_TF = coverage * 100
    repeats: List[RepeatWithVariants] = []
    cache: Dict[str, Tuple[int, int, int]] = {}
    
    def get_valid_extensions(prefix_or_suffix: str, 
                           is_right: bool = True) -> List[Tuple[int, str, str]]:
        solutions = []
        for nucleotide in "ACTG":
            new_kmer = (prefix_or_suffix + nucleotide) if is_right else (nucleotide + prefix_or_suffix)
            tf = kmer2tf.get(new_kmer, 0)
            if tf >= MIN_TF:
                solutions.append((tf, nucleotide, new_kmer))
        
        if not solutions:
            return []
            
        solutions.sort(reverse=True)
        max_tf = solutions[0][0]
        return [s for s in solutions if s[0] >= max_tf * variant_threshold]
    
    def extend_repeat(start_kmer: str) -> Optional[RepeatWithVariants]:
        if start_kmer in cache:
            return None
            
        repeat = RepeatWithVariants(start_kmer)
        current_pos = len(start_kmer)
        
        # Right extension
        right_prefix = start_kmer[1:]
        while current_pos < max_depth:
            extensions = get_valid_extensions(right_prefix, is_right=True)
            if not extensions:
                break
                
            for tf, nucleotide, new_kmer in extensions:
                repeat.add_variant(current_pos, nucleotide, tf)
                cache[new_kmer] = (len(repeats), 0, current_pos)
                
            # Use most frequent variant for further extension
            _, nucleotide, new_kmer = extensions[0]
            right_prefix = new_kmer[1:]
            current_pos += 1
            
            if new_kmer == start_kmer:  # Tandem repeat detected
                repeat.is_tandem = True
                break
        
        # Left extension (similar logic)
        left_suffix = start_kmer[:-1]
        current_pos = -1
        
        while abs(current_pos) < max_depth:
            extensions = get_valid_extensions(left_suffix, is_right=False)
            if not extensions:
                break
                
            for tf, nucleotide, new_kmer in extensions:
                repeat.add_variant(current_pos, nucleotide, tf)
                cache[new_kmer] = (len(repeats), 0, current_pos)
                
            _, nucleotide, new_kmer = extensions[0]
            left_suffix = new_kmer[:-1]
            current_pos -= 1
            
            if new_kmer == start_kmer:
                repeat.is_tandem = True
                break
        
        repeat.build_consensus()
        return repeat
    
    # Main loop
    for start_kmer, tf in sdat:
        if tf < MIN_TF:
            break
            
        repeat = extend_repeat(start_kmer)
        if repeat:
            repeats.append(repeat)
            
    return repeats