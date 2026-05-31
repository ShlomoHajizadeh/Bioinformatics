#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 GENOMIC DATA ANALYZER & MUTATION DETECTOR (Hamming Distance & Translation)
==============================================================================
Bu alət bioloji FASTA verilənlərini analiz edən, transkripsiya/translasiya aparan
və DNT zəncirləri arasındakı mutasiyaları (SNPs) Hamming məsafəsi alqoritmi ilə
hesablayan və terminalda rəngli şəkildə vizuallaşdıran professional bioinformatika skriptidir.

Müəllif: Süleyman Hacızadə (Hybrid Portfolio)
Tarix: 2026-05-31
==============================================================================
"""

import os
import sys
import argparse

# Terminalda rəngli çıxışlar üçün ANSI kodları
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

# Standart Genetik Kodon Cədvəli (RNA -> Amino Acid)
CODON_TABLE = {
    'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
    'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',  # * = STOP kodonlar
    'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
    'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',  # M = START/Metionin
    'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
    'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
}

def parse_fasta(file_path):
    """
    FASTA formatlı faylı oxuyur və başlıqlar ilə ardıcıllıqları lüğət (dict) olaraq qaytarır.
    """
    if not os.path.exists(file_path):
        print(f"{COLOR_RED}[XƏTA] Sənəd tapılmadı: {file_path}{COLOR_RESET}")
        sys.exit(1)
        
    sequences = {}
    current_header = None
    current_seq = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_header:
                    sequences[current_header] = "".join(current_seq).upper()
                current_header = line[1:]  # '>' işarəsini silirik
                current_seq = []
            else:
                current_seq.append(line)
        if current_header:
            sequences[current_header] = "".join(current_seq).upper()
            
    return sequences

def transcribe_dna_to_rna(dna_sequence):
    """
    DNT zəncirini RNT-yə transkripsiya edir (T -> U).
    """
    return dna_sequence.replace('T', 'U')

def translate_rna_to_protein(rna_sequence):
    """
    RNT zəncirini Standart Genetik Kod cədvəli ilə Protein zəncirinə translasiya edir.
    START (AUG) kodonundan başlayır və STOP (*) kodonunda dayanır.
    """
    protein = []
    start_found = False
    
    # 3-lü oxuma çərçivəsində (Reading Frame) hərəkət edirik
    for i in range(0, len(rna_sequence) - 2, 3):
        codon = rna_sequence[i:i+3]
        if len(codon) < 3:
            break
            
        amino_acid = CODON_TABLE.get(codon, '?')
        
        if not start_found:
            if codon == 'AUG':  # START kodon (Metionin)
                start_found = True
                protein.append(amino_acid)
        else:
            if amino_acid == '*':  # STOP kodonuna rast gəldikdə translasiya dayanır
                protein.append('*')
                break
            protein.append(amino_acid)
            
    return "".join(protein) if start_found else "START (AUG) kodonu tapılmadı!"

def calculate_gc_content(sequence):
    """
    Ardıcıllığın GC faizini (G+C faizi) hesablayır.
    """
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    total = len(sequence)
    if total == 0:
        return 0.0
    return ((g_count + c_count) / total) * 100

def calculate_hamming_distance(seq1, seq2):
    """
    İki bərabər uzunluqlu ardıcıllıq arasındakı Hamming Məsafəsini (Mutasiya sayını) hesablayır
    və mutasiyaya uğramış mövqelərin siyahısını qaytarır.
    """
    if len(seq1) != len(seq2):
        raise ValueError("Hamming məsafəsini hesablamaq üçün zəncirlərin uzunluqları BƏRABƏR olmalıdır!")
        
    distance = 0
    mutations = []
    
    for idx, (n1, n2) in enumerate(zip(seq1, seq2)):
        if n1 != n2:
            distance += 1
            mutations.append((idx + 1, n1, n2))  # 1-indexed mövqe, normal, mutasiyalı
            
    return distance, mutations

def visualize_mutation_alignment(seq1, seq2):
    """
    İki zənciri terminalda rəngli şəkildə qarşılaşdırır.
    Mutasiya olan mövqelər qırmızı, sağlam mövqelər yaşıl rəngdə göstərilir.
    """
    visual1 = []
    visual2 = []
    match_line = []
    
    for n1, n2 in zip(seq1, seq2):
        if n1 == n2:
            visual1.append(f"{COLOR_GREEN}{n1}{COLOR_RESET}")
            visual2.append(f"{COLOR_GREEN}{n2}{COLOR_RESET}")
            match_line.append("|")
        else:
            visual1.append(f"{COLOR_RED}{COLOR_BOLD}{n1}{COLOR_RESET}")
            visual2.append(f"{COLOR_RED}{COLOR_BOLD}{n2}{COLOR_RESET}")
            match_line.append("*")
            
    print(f"\n{COLOR_BOLD}[CANLI MUTASİYA XƏRİTƏSİ (MUTATION ALIGNMENT)]{COLOR_RESET}")
    print("----------------------------------------------------------------------")
    print(f"Normal:   " + "".join(visual1))
    print(f"Uyğunluq: " + "".join(match_line))
    print(f"Tumor:    " + "".join(visual2))
    print("----------------------------------------------------------------------")
    print(f"(Qeyd: {COLOR_GREEN}Yaşıl{COLOR_RESET} = Sağlam, {COLOR_RED}{COLOR_BOLD}Qırmızı (*){COLOR_RESET} = Nöqtəvi Mutasiya/SNP)")

def main():
    parser = argparse.ArgumentParser(
        description="🧬 Genomic Data Analyzer & Mutation Detector — Kembric Qəbul Portfoliosu üçün bioloji alət.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--file', type=str, required=True, help="Analiz ediləcək FASTA (.fasta) faylının yolu")
    parser.add_argument('--transcribe', action='store_true', help="DNT-ni RNT-yə transkripsiya et")
    parser.add_argument('--translate', action='store_true', help="RNT-ni Protein (amin turşusu) zəncirinə translasiya et")
    parser.add_argument('--gc', action='store_true', help="Hər bir zəncirin GC faizini hesablayır")
    parser.add_argument('--compare', action='store_true', help="İki zənciri Hamming Məsafəsi alqoritmi ilə müqayisə et")
    
    args = parser.parse_args()
    
    # 1. FASTA faylını oxuyuruq
    print(f"{COLOR_BLUE}{COLOR_BOLD}[1/4] FASTA faylı yüklənir...{COLOR_RESET}")
    sequences = parse_fasta(args.file)
    print(f"   -> Uğurla yükləndi. Tapılan zəncir sayı: {len(sequences)}")
    
    for idx, (header, seq) in enumerate(sequences.items()):
        print(f"   -> Zəncir {idx+1}: '{COLOR_YELLOW}{header}{COLOR_RESET}' (Uzunluq: {len(seq)} bp)")
        
        # 2. GC faizinin hesablanması
        if args.gc:
            gc = calculate_gc_content(seq)
            print(f"      - GC faizi: {COLOR_BOLD}{gc:.2f}%{COLOR_RESET}")
            
        # 3. Transkripsiya (DNA -> RNA)
        if args.transcribe:
            rna = transcribe_dna_to_rna(seq)
            print(f"      - RNT Transkripsiyası (ilk 50 bp): {COLOR_GREEN}{rna[:50]}...{COLOR_RESET}")
            
            # 4. Translasiya (RNA -> Protein)
            if args.translate:
                protein = translate_rna_to_protein(rna)
                print(f"      - Protein Translasiyası (START -> STOP): {COLOR_BLUE}{protein}{COLOR_RESET}")
                
    # 5. İki zəncirin müqayisəsi (Hamming Distance)
    if args.compare:
        print(f"\n{COLOR_BLUE}{COLOR_BOLD}[2/4] Zəncirlərin Hamming Məsafəsi analizi başladılır...{COLOR_RESET}")
        headers = list(sequences.keys())
        if len(headers) < 2:
            print(f"{COLOR_RED}[XƏTA] Müqayisə etmək üçün FASTA faylında minimum 2 zəncir olmalıdır!{COLOR_RESET}")
            sys.exit(1)
            
        seq1 = sequences[headers[0]]
        seq2 = sequences[headers[1]]
        
        try:
            distance, mutations = calculate_hamming_distance(seq1, seq2)
            print(f"   -> Normal zəncir: {headers[0]}")
            print(f"   -> Mutasiyalı zəncir: {headers[1]}")
            print(f"   -> {COLOR_YELLOW}{COLOR_BOLD}Hamming Məsafəsi (Ümumi Mutasiya Sayı): {distance}{COLOR_RESET}")
            
            if distance > 0:
                print(f"\n   -> {COLOR_RED}{COLOR_BOLD}Aşkar edilən nöqtəvi mutasiyaların (SNPs) siyahısı:{COLOR_RESET}")
                for pos, normal, tumor in mutations:
                    print(f"      • Mövqe {pos:3d}: Normal [{COLOR_GREEN}{normal}{COLOR_RESET}] ---> Xərçəng [{COLOR_RED}{COLOR_BOLD}{tumor}{COLOR_RESET}]")
                
                # Vizual müqayisəni çəkirik
                visualize_mutation_alignment(seq1, seq2)
            else:
                print(f"   -> ✅ Zəncirlər tamamilə eynidir, heç bir mutasiya aşkar edilmədi.")
                
        except ValueError as e:
            print(f"{COLOR_RED}[XƏTA] {e}{COLOR_RESET}")

if __name__ == "__main__":
    main()
