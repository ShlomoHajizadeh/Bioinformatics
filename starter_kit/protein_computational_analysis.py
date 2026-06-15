#!/usr/bin/env python3
"""
Advanced Computational Structural Biology & Protein Biophysics Analyzer
Developed for Cambridge MPhil Portfolio Upgrades
Author: Suleyman Hajizadeh
Date: June 1, 2026

This script performs physical and thermodynamic analyses of protein structures,
including:
1. Hydrophobic Core Detection (Kyte-Doolittle scale and spatial packing density)
2. Contact Potential Scoring (Miyazawa-Jernigan statistical interaction matrix approximation)
3. B-factor (Thermal Displacement) profiling and structural rigidity correlation
4. Fractional Solvent Accessibility (SASA geometric approximation)
"""

import os
import sys
import math
import argparse
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
from Bio.PDB import PDBParser

# Kyte-Doolittle Hydrophobicity Scale
KYTE_DOOLITTLE = {
    'ALA': 1.8, 'ARG': -4.5, 'ASN': -3.5, 'ASP': -3.5, 'CYS': 2.5,
    'GLN': -3.5, 'GLU': -3.5, 'GLY': -0.4, 'HIS': -3.2, 'ILE': 4.5,
    'LEU': 3.8, 'LYS': -3.9, 'MET': 1.9, 'PHE': 2.8, 'PRO': -1.6,
    'SER': -0.8, 'THR': -0.7, 'TRP': -0.9, 'TYR': -1.3, 'VAL': 4.2
}

# Simplified Miyazawa-Jernigan (MJ) Statistical Potential Matrix
# Represents residue-residue contact energies (negative values are attractive/favorable)
RESIDUE_GROUPS = {
    'H': {'ALA', 'VAL', 'LEU', 'ILE', 'MET', 'PHE', 'TRP', 'PRO', 'CYS'}, # Hydrophobic
    'P': {'GLY', 'SER', 'THR', 'TYR', 'ASN', 'GLN'},                      # Polar
    'POS': {'LYS', 'ARG', 'HIS'},                                         # Positively Charged
    'NEG': {'ASP', 'GLU'}                                                 # Negatively Charged
}

def get_residue_group(res_name):
    for group, residues in RESIDUE_GROUPS.items():
        if res_name in residues:
            return group
    return 'P'  # Default fallback to Polar

def calculate_mj_energy(res1, res2):
    """Calculates interaction energy based on statistical preferences."""
    g1 = get_residue_group(res1)
    g2 = get_residue_group(res2)
    
    # Energy grid
    if g1 == 'H' and g2 == 'H':
        return -5.0  # Favorable hydrophobic collapse
    elif (g1 == 'POS' and g2 == 'NEG') or (g1 == 'NEG' and g2 == 'POS'):
        return -6.0  # Favorable ionic salt bridge
    elif (g1 == 'POS' and g2 == 'POS') or (g1 == 'NEG' and g2 == 'NEG'):
        return 3.0   # Unfavorable electrostatic repulsion
    elif g1 == 'P' and g2 == 'P':
        return -1.5  # Weak hydrogen bond/dipole interactions
    elif (g1 == 'H' and g2 == 'P') or (g1 == 'P' and g2 == 'H'):
        return 0.5   # Unfavorable hydrophobic-polar interface
    else:
        return 0.0   # Neutral/solvent exposed

def download_pdb(pdb_id, output_dir="sample_data"):
    """Downloads a PDB file from the RCSB Protein Data Bank."""
    pdb_id = pdb_id.lower()
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{pdb_id}.pdb")
    
    if os.path.exists(file_path):
        print(f" -> Found cached PDB file: {file_path}")
        return file_path
        
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    print(f" -> Fetching {pdb_id.upper()} from RCSB PDB...")
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f" -> File saved successfully: {file_path}")
        return file_path
    except Exception as e:
        print(f"[ERROR] Failed to download PDB: {e}")
        sys.exit(1)

def parse_pdb_structure(pdb_path, chain_id="A"):
    """Parses PDB file and returns lists of coordinates, residue names, and B-factors."""
    parser = PDBParser(QUIET=True)
    pdb_id = os.path.basename(pdb_path).split('.')[0].upper()
    structure = parser.get_structure(pdb_id, pdb_path)
    model = structure[0]
    
    if chain_id not in model:
        print(f"[ERROR] Chain {chain_id} not found in model.")
        sys.exit(1)
        
    chain = model[chain_id]
    
    residues_data = []
    for residue in chain:
        # standard residues only
        if residue.id[0] == " " and "CA" in residue:
            res_name = residue.get_resname()
            res_seq = residue.id[1]
            ca_atom = residue["CA"]
            coord = ca_atom.get_coord()
            b_factor = ca_atom.get_bfactor()
            
            residues_data.append({
                'name': res_name,
                'seq': res_seq,
                'coord': coord,
                'bfactor': b_factor
            })
            
    if not residues_data:
        print(f"[ERROR] No valid standard residues parsed from Chain {chain_id}.")
        sys.exit(1)
        
    return residues_data

def run_computational_analysis(residues, dist_threshold=8.0, sasa_radius=10.0):
    """
    Performs core structural biology calculations.
    """
    n = len(residues)
    coords = np.array([r['coord'] for r in residues])
    
    # Precompute distance matrix
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    dist_matrix = np.sqrt(np.sum(diff**2, axis=-1))
    
    total_mj_energy = 0.0
    contacts_count = 0
    
    # 1. Hydrophobic Core & Local Density Calculation
    for i in range(n):
        res_i = residues[i]
        name_i = res_i['name']
        
        # Neighbor count within thresholds
        neighbors_packing = np.sum((dist_matrix[i] < dist_threshold) & (dist_matrix[i] > 0))
        neighbors_sasa = np.sum((dist_matrix[i] < sasa_radius) & (dist_matrix[i] > 0))
        
        # Kyte-Doolittle Hydrophobicity score
        kd_val = KYTE_DOOLITTLE.get(name_i, -0.4)
        
        # Core score = local packing density * hydrophobicity index
        core_score = neighbors_packing * kd_val
        
        # Approximate SASA: Higher packing means LOWER solvent exposure
        # Assuming maximum packing is ~24 residues inside a 10 Angstrom sphere
        max_packing = 22.0
        sasa_est = max(0.0, 1.0 - (neighbors_sasa / max_packing))
        
        residues[i]['packing_density'] = int(neighbors_packing)
        residues[i]['core_score'] = core_score
        residues[i]['sasa_est'] = sasa_est
        
        # 2. Miyazawa Jernigan potential summing
        # Sum non-covalent contacts (sequence separation > 2 residues)
        for j in range(i + 3, n):
            if dist_matrix[i, j] < dist_threshold:
                name_j = residues[j]['name']
                energy = calculate_mj_energy(name_i, name_j)
                total_mj_energy += energy
                contacts_count += 1
                
    # 3. Rigidity analysis (B-factor correlation with packing density)
    bfactors = np.array([r['bfactor'] for r in residues])
    packing_densities = np.array([r['packing_density'] for r in residues])
    
    # Calculate Pearson correlation coefficient
    mean_bf = np.mean(bfactors)
    mean_pk = np.mean(packing_densities)
    cov = np.mean((bfactors - mean_bf) * (packing_densities - mean_pk))
    std_bf = np.std(bfactors)
    std_pk = np.std(packing_densities)
    
    correlation = cov / (std_bf * std_pk) if (std_bf * std_pk) > 0 else 0.0
    
    return total_mj_energy, contacts_count, correlation

def generate_report_plots(residues, pdb_id, output_path):
    """Generates analytical plots summarizing the biophysical findings."""
    plt.style.use('dark_background')
    fig, axs = plt.subplots(3, 1, figsize=(11, 12), dpi=300)
    
    seq_nums = [r['seq'] for r in residues]
    bfactors = [r['bfactor'] for r in residues]
    core_scores = [r['core_score'] for r in residues]
    sasa_est = [r['sasa_est'] for r in residues]
    
    # Plot 1: B-factor Profiling (Fluctuations & Rigidity)
    axs[0].plot(seq_nums, bfactors, color='#ef4444', linewidth=1.5, label='B-factor (Å²)')
    axs[0].fill_between(seq_nums, bfactors, color='#ef4444', alpha=0.15)
    axs[0].set_title(f"Protein B-factor Profile (Chain Flexibility) - PDB: {pdb_id}", color='#fbbf24', fontweight='bold')
    axs[0].set_xlabel("Residue Sequence Position", color='#9ca3af')
    axs[0].set_ylabel("B-factor Value (Å²)", color='#9ca3af')
    axs[0].grid(color='#333333', linestyle='--')
    axs[0].legend()
    
    # Plot 2: Kyte-Doolittle Hydrophobic Core Scores
    color_map = ['#10b981' if score > 0 else '#3b82f6' for score in core_scores]
    axs[1].bar(seq_nums, core_scores, color=color_map, alpha=0.8, width=0.8, label='Core Score (Density x KD)')
    axs[1].axhline(0, color='gray', linestyle='-', linewidth=0.5)
    axs[1].set_title("Hydrophobic Core Score (Positive indicates packed hydrophobic core)", color='#fbbf24', fontweight='bold')
    axs[1].set_xlabel("Residue Sequence Position", color='#9ca3af')
    axs[1].set_ylabel("Core Score Index", color='#9ca3af')
    axs[1].grid(color='#333333', linestyle='--')
    axs[1].legend()
    
    # Plot 3: Fractional Solvent Accessibility (SASA approximation)
    axs[2].plot(seq_nums, sasa_est, color='#0ea5e9', linewidth=1.5, label='Estimated SASA')
    axs[2].fill_between(seq_nums, sasa_est, color='#0ea5e9', alpha=0.1)
    axs[2].set_title("Solvent Accessible Surface Area (SASA) Approximation", color='#fbbf24', fontweight='bold')
    axs[2].set_xlabel("Residue Sequence Position", color='#9ca3af')
    axs[2].set_ylabel("SASA Fraction (0=Buried, 1=Exposed)", color='#9ca3af')
    axs[2].grid(color='#333333', linestyle='--')
    axs[2].legend()
    
    plt.tight_layout()
    plt.savefig(output_path, facecolor='#030712', edgecolor='none')
    plt.close()
    print(f" -> Biophysical analysis plots saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="🔬 Biophysical Structural Chemistry & Protein Folding Analyzer.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--pdb', type=str, help="Path to local PDB file")
    parser.add_argument('--download', type=str, default="1coh", help="4-character PDB ID to fetch (default: 1coh)")
    parser.add_argument('--chain', type=str, default="A", help="PDB Chain ID (default: A)")
    parser.add_argument('--output_img', type=str, default="sample_data/biophysical_profile.png", help="Path to save visual plots")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("        Protein Structural Biophysics & Folding Analyzer")
    print("=" * 70)
    
    # 1. PDB Fetching
    if args.pdb:
        pdb_path = args.pdb
    else:
        pdb_path = download_pdb(args.download)
        
    # 2. Parsing structure
    pdb_id = os.path.basename(pdb_path).split('.')[0].upper()
    print(f"\n[1/3] Parsing Chain {args.chain} from PDB: {pdb_id}...")
    residues = parse_pdb_structure(pdb_path, args.chain)
    print(f" -> Parsed {len(residues)} amino acid residues.")
    
    # 3. Running physical and statistical calculations
    print("\n[2/3] Performing thermodynamic and geometric calculations...")
    mj_energy, contacts, corr = run_computational_analysis(residues)
    
    # Identify hydrophobic core residues
    core_residues = [r for r in residues if r['core_score'] > 20]
    core_residues.sort(key=lambda x: x['core_score'], reverse=True)
    
    print("\nBiophysical Analysis Results:")
    print("-" * 50)
    print(f"Total Non-Covalent Contacts (<8.0 Å): {contacts}")
    print(f"MJ Statistical Potential Energy:       {mj_energy:.2f} kcal/mol")
    print(f"Rigidity Correlation (B-factor vs PK): {corr:.4f}")
    print("-" * 50)
    
    # Describe rigidity correlation
    if corr < -0.3:
        print("Note: Strong negative correlation detected. Tight residue packing")
        print("      strongly correlates with lower thermal B-factor variations,")
        print("      validating structural core stability.")
    else:
        print("Note: Weak correlation between packing and B-factor, common in")
        print("      flexible or disordered protein conformations.")
        
    print("\nTop 5 Hydrophobic Core Residues:")
    for idx, r in enumerate(core_residues[:5]):
        print(f" {idx+1}. Residue {r['name']} at index {r['seq']} | Core Score: {r['core_score']:.2f} (SASA: {r['sasa_est']:.2f})")
        
    # 4. Save plots
    print("\n[3/3] Generating visual biophysical reports...")
    os.makedirs(os.path.dirname(args.output_img), exist_ok=True)
    generate_report_plots(residues, pdb_id, args.output_img)
    
    print("\nBiophysical computational analysis completed successfully.")
    print("=" * 70)

if __name__ == "__main__":
    main()
