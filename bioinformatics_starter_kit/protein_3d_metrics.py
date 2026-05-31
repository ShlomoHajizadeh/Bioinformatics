#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔬 PROTEIN 3D STRUCTURE METRICS & BACKBONE VISUALIZER (PDB Parser & Euclidean Distance)
==============================================================================
Bu alət RCSB PDB bazasından protein strukturlarını avtomatik yükləyən, Bio.PDB
ilə atom koordinatlarını oxuyan, iki amin turşusu arasındakı 3D Evklid məsafəsini
hesablayan və protein zəncirini (backbone) 3D olaraq Matplotlib ilə vizuallaşdıran
professional bioinformatika skriptidir.

Müəllif: Süleyman Hacızadə (Hybrid Portfolio)
Tarix: 2026-05-31
==============================================================================
"""

import os
import sys
import math
import argparse
import urllib.request

# Terminalda rəngli çıxışlar üçün ANSI kodları
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

# Kitabxanaların yoxlanılması
try:
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from Bio.PDB import PDBParser
except ImportError:
    print(f"{COLOR_RED}[XƏTA] Lazım olan kitabxanalar tapılmadı!{COLOR_RESET}")
    print(f"Zəhmət olmasa asılılıqları quraşdırın: {COLOR_BOLD}pip install -r requirements.txt{COLOR_RESET}")
    sys.exit(1)

def download_pdb(pdb_id, output_dir="sample_data"):
    """
    RCSB Protein Data Bank bazasından verilən PDB ID-yə uyğun .pdb faylını yükləyir.
    """
    pdb_id = pdb_id.lower()
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{pdb_id}.pdb")
    
    if os.path.exists(file_path):
        print(f"   -> [OK] Protein faylı lokalda mövcuddur: {file_path}")
        return file_path
        
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    print(f"   -> {COLOR_YELLOW}[YÜKLƏNİR]{COLOR_RESET} PDB faylı yüklənir: {url}")
    
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"   -> {COLOR_GREEN}✓ Uğurla yükləndi və yaddaşa yazıldı:{COLOR_RESET} {file_path}")
        return file_path
    except Exception as e:
        print(f"{COLOR_RED}[XƏTA] RCSB PDB faylını yükləmək mümkün olmadı: {e}{COLOR_RESET}")
        sys.exit(1)

def calculate_euclidean_distance(coords1, coords2):
    """
    İki atomun 3D koordinatları (x, y, z) arasındakı Evklid məsafəsini hesablayır.
    """
    return math.sqrt(
        (coords1[0] - coords2[0])**2 +
        (coords1[1] - coords2[1])**2 +
        (coords1[2] - coords2[2])**2
    )

def analyze_pdb_structure(pdb_path, res_num1, res_num2, chain_id="A"):
    """
    Biopython PDBParser ilə faylı təhlil edir, amin turşularını və atom koordinatlarını tapır,
    iki atom arasındakı 3D məsafəni hesablayır.
    """
    parser = PDBParser(QUIET=True)
    pdb_id = os.path.basename(pdb_path).split('.')[0].upper()
    structure = parser.get_structure(pdb_id, pdb_path)
    
    # PDB iyerarxiyasını oxuyuruq: Structure -> Model (0) -> Chain -> Residue -> Atom
    model = structure[0]
    
    if chain_id not in model:
        print(f"{COLOR_RED}[XƏTA] Zülalda '{chain_id}' zənciri (chain) tapılmadı!{COLOR_RESET}")
        available_chains = [c.id for c in model]
        print(f"Mövcud zəncirlər: {available_chains}")
        sys.exit(1)
        
    chain = model[chain_id]
    
    # Hədəf amin turşularını (residues) axtarırıq
    residue1 = None
    residue2 = None
    
    for residue in chain:
        # Standard residues axtarırıq (hetero-atomları yox sayırıq)
        if residue.id[0] == " ":
            res_seq_num = residue.id[1]
            if res_seq_num == res_num1:
                residue1 = residue
            if res_seq_num == res_num2:
                residue2 = residue
                
    if not residue1:
        print(f"{COLOR_RED}[XƏTA] Mövqe {res_num1} üzrə amin turşusu tapılmadı!{COLOR_RESET}")
        sys.exit(1)
    if not residue2:
        print(f"{COLOR_RED}[XƏTA] Mövqe {res_num2} üzrə amin turşusu tapılmadı!{COLOR_RESET}")
        sys.exit(1)
        
    # C-Alpha (CA) atomlarını alırıq (3D Backbone məsafələri üçün standart olaraq CA atomları götürülür)
    if "CA" not in residue1:
        print(f"{COLOR_RED}[XƏTA] Amin turşusu {res_num1} daxilində C-Alpha (CA) atomu tapılmadı!{COLOR_RESET}")
        sys.exit(1)
    if "CA" not in residue2:
        print(f"{COLOR_RED}[XƏTA] Amin turşusu {res_num2} daxilində C-Alpha (CA) atomu tapılmadı!{COLOR_RESET}")
        sys.exit(1)
        
    atom1 = residue1["CA"]
    atom2 = residue2["CA"]
    
    coords1 = atom1.get_coord()
    coords2 = atom2.get_coord()
    
    distance = calculate_euclidean_distance(coords1, coords2)
    
    print(f"\n{COLOR_GREEN}{COLOR_BOLD}[3D STRUKTUR ANALİZİNİN NƏTİCƏLƏRİ]{COLOR_RESET}")
    print("----------------------------------------------------------------------")
    print(f"Protein PDB ID:      {COLOR_BOLD}{pdb_id}{COLOR_RESET}")
    print(f"Zəncir (Chain):      {chain_id}")
    print(f"Amin Turşusu 1:      Residue [{COLOR_YELLOW}{residue1.get_resname()}{COLOR_RESET}] (Mövqe: {res_num1})")
    print(f"   -> CA Atom 3D Coords:  X: {coords1[0]:.3f}, Y: {coords1[1]:.3f}, Z: {coords1[2]:.3f}")
    print(f"Amin Turşusu 2:      Residue [{COLOR_YELLOW}{residue2.get_resname()}{COLOR_RESET}] (Mövqe: {res_num2})")
    print(f"   -> CA Atom 3D Coords:  X: {coords2[0]:.3f}, Y: {coords2[1]:.3f}, Z: {coords2[2]:.3f}")
    print("----------------------------------------------------------------------")
    print(f"🧬 {COLOR_GREEN}{COLOR_BOLD}3D Evklid Məsafəsi (CA-CA): {distance:.4f} Angstrom (Å){COLOR_RESET}")
    print("----------------------------------------------------------------------")
    
    return chain, residue1, residue2, distance

def visualize_protein_backbone_3d(chain, residue1, residue2, output_img="protein_backbone_3d.png"):
    """
    Zülalın polipeptid zəncirinin (C-Alpha karbon skeletini) 3D fəzada Matplotlib ilə çəkir
    və fərqli amin turşularını və onların arasındakı məsafəni 3D-də vizuallaşdırır.
    """
    x_coords = []
    y_coords = []
    z_coords = []
    res_names = []
    res_nums = []
    
    # Bütün CA atomlarının koordinatlarını yığırıq
    for residue in chain:
        if residue.id[0] == " " and "CA" in residue:
            coord = residue["CA"].get_coord()
            x_coords.append(coord[0])
            y_coords.append(coord[1])
            z_coords.append(coord[2])
            res_names.append(residue.get_resname())
            res_nums.append(residue.id[1])
            
    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)
    z_coords = np.array(z_coords)
    
    # 3D Matplotlib Plot qurulması
    fig = plt.figure(figsize=(10, 8), facecolor='#060b14')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#060b14')
    
    # Zülalın 3D skeletini çəkirik (Cyan ribbon)
    ax.plot(x_coords, y_coords, z_coords, color='#1de9b6', linewidth=2.5, alpha=0.8, label="Protein Backbone (CA)")
    ax.scatter(x_coords, y_coords, z_coords, color='#0ea5e9', s=15, alpha=0.5)
    
    # Hesabladığımız iki hədəf nöqtəni qeyd edirik (Gold və Red)
    c1 = residue1["CA"].get_coord()
    c2 = residue2["CA"].get_coord()
    
    ax.scatter([c1[0]], [c1[1]], [c1[2]], color='#fbbf24', s=150, edgecolors='white', depthshade=False,
               label=f"Res {residue1.id[1]} ({residue1.get_resname()})")
    ax.scatter([c2[0]], [c2[1]], [c2[2]], color='#ef4444', s=150, edgecolors='white', depthshade=False,
               label=f"Res {residue2.id[1]} ({residue2.get_resname()})")
    
    # İki atom arasındakı Evklid məsafəsini göstərən qırıq-qırıq xətt çəkirik
    ax.plot([c1[0], c2[0]], [c1[1], c2[1]], [c1[2], c2[2]], color='#fbbf24', linestyle='--', linewidth=2,
            label="3D Distance (Euclidean)")
            
    # Qrafik bəzəkləri
    ax.set_title(f"Protein 3D Backbone Visualizer (CA Carbon Chain)\nTarget Residues: {residue1.id[1]} vs {residue2.id[1]}",
                 color='white', fontsize=12, fontweight='bold', pad=15)
    
    # Oxların bəzədilməsi
    ax.set_xlabel("X Koordinat (Å)", color='#9ca3af')
    ax.set_ylabel("Y Koordinat (Å)", color='#9ca3af')
    ax.set_zlabel("Z Koordinat (Å)", color='#9ca3af')
    ax.tick_params(colors='#6b7280')
    
    # Grid və panellərin rəngləri (Dark mode estetika)
    ax.w_xaxis.set_pane_color((0.03, 0.05, 0.1, 1.0))
    ax.w_yaxis.set_pane_color((0.03, 0.05, 0.1, 1.0))
    ax.w_zaxis.set_pane_color((0.03, 0.05, 0.1, 1.0))
    
    # Legend
    legend = ax.legend(facecolor='#0d1628', edgecolor='#1e293b', loc="upper left")
    plt.setp(legend.get_texts(), color='white')
    
    # Qrafiki yaddaşda saxlayırıq
    plt.savefig(output_img, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    
    print(f"📸 {COLOR_GREEN}3D Struktur Vizuallaşdırması saxlanıldı:{COLOR_RESET} {output_img}")

def main():
    parser = argparse.ArgumentParser(
        description="🔬 Protein 3D Structure Metrics Analyzer & Visualizer — Kembric Qəbul Portfoliosu üçün bioloji alət.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--pdb', type=str, help="Lokal PDB (.pdb) faylının yolu")
    parser.add_argument('--download', type=str, help="RCSB PDB-dən yüklənəcək 4-hərfli PDB ID (məsələn, 1coh)")
    parser.add_argument('--residues', type=int, nargs=2, required=True, help="Məsafəsi hesablanacaq iki amin turşusunun mövqe indeksləri (məsələn: 10 50)")
    parser.add_argument('--chain', type=str, default="A", help="Zülal zənciri ID-si (Chain ID, standart: A)")
    parser.add_argument('--output', type=str, default="protein_backbone_3d.png", help="Yaranacaq 3D vizuallaşdırma şəklinin yolu")
    
    args = parser.parse_args()
    
    print(f"{COLOR_BLUE}{COLOR_BOLD}[1/4] PDB faylı hazırlanır...{COLOR_RESET}")
    
    if args.pdb:
        pdb_path = args.pdb
        if not os.path.exists(pdb_path):
            print(f"{COLOR_RED}[XƏTA] Lokal PDB faylı tapılmadı: {pdb_path}{COLOR_RESET}")
            sys.exit(1)
    elif args.download:
        pdb_path = download_pdb(args.download)
    else:
        # Standart olaraq Hemoqlobin zülalını yükləyirik (Əgər heç bir arqument verilməyibsə)
        print("   -> [Məlumat] PDB faylı təyin edilmədiyi üçün standart olaraq '1coh' (İnsulin) yüklənir.")
        pdb_path = download_pdb("1coh")
        
    # 2. Struktur analizi və Evklid Məsafəsi
    print(f"\n{COLOR_BLUE}{COLOR_BOLD}[2/4] Zülalın 3D atom strukturu Bio.PDB ilə oxunur...{COLOR_RESET}")
    chain, res1, res2, distance = analyze_pdb_structure(pdb_path, args.residues[0], args.residues[1], args.chain)
    
    # 3. 3D Vizuallaşdırma
    print(f"\n{COLOR_BLUE}{COLOR_BOLD}[3/4] Karbon skeleti (CA Backbone) 3D-də vizuallaşdırılır...{COLOR_RESET}")
    visualize_protein_backbone_3d(chain, res1, res2, args.output)
    
    print(f"\n{COLOR_BLUE}{COLOR_BOLD}[4/4] Analiz uğurla tamamlandı!{COLOR_RESET}")

if __name__ == "__main__":
    main()
