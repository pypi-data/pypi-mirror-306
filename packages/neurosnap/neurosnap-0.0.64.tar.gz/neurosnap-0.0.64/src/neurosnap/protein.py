"""
Provides functions and classes related to processing protein data as well as
a feature rich wrapper around protein structures using BioPython.
"""

import io
import json
import os
import tempfile
import time
import xml.etree.ElementTree as ET
from typing import List, Union, Tuple, Optional

import matplotlib
import matplotlib.animation as animation
import matplotlib.patheffects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from Bio.PDB import PDBIO, SASA, PDBParser, PPBuilder
from Bio.PDB.mmcifio import MMCIFIO
from Bio.PDB.Polypeptide import is_aa
from Bio.PDB.Superimposer import Superimposer
from matplotlib import collections as mcoll
from rdkit import Chem
from requests_toolbelt.multipart.encoder import MultipartEncoder
from scipy.special import expit as sigmoid

import neurosnap.algos.lDDT as lDDT
from neurosnap.api import USER_AGENT
from neurosnap.log import logger

### CONSTANTS ###
# Names of atoms that are part of a protein's backbone structure
BACKBONE_ATOMS = {"N", "CA", "C"}
# Codes for both RNA and DNA
STANDARD_NUCLEOTIDES = {"A", "T", "C", "G", "U", "DA", "DT", "DC", "DG", "DU"}
## Standard amino acids excluding the unknown character ("X")
## Currently excludes
# O | pyl | pyrrolysine
# U | sec | selenocysteine
# B | asx | asparagine/aspartic acid
# Z | glx | glutamine/glutamic acid
# J | xle | leucine/isoleucine
# X | UNK | unknown codon
# * | TRM | termination codon
STANDARD_AAs = "ACDEFGHIKLMNPQRSTVWY"
# List of hydrophobic residues
HYDROPHOBIC_RESIDUES = {"ALA", "VAL", "LEU", "ILE", "MET", "PHE", "TRP", "PRO"}

## Full amino acids table
AAs_FULL_TABLE = [
  ["A", "ALA", "ALANINE"],
  ["R", "ARG", "ARGININE"],
  ["N", "ASN", "ASPARAGINE"],
  ["D", "ASP", "ASPARTIC ACID"],
  ["C", "CYS", "CYSTEINE"],
  ["Q", "GLN", "GLUTAMINE"],
  ["E", "GLU", "GLUTAMIC ACID"],
  ["G", "GLY", "GLYCINE"],
  ["H", "HIS", "HISTIDINE"],
  ["I", "ILE", "ISOLEUCINE"],
  ["L", "LEU", "LEUCINE"],
  ["K", "LYS", "LYSINE"],
  ["M", "MET", "METHIONINE"],
  ["F", "PHE", "PHENYLALANINE"],
  ["P", "PRO", "PROLINE"],
  ["S", "SER", "SERINE"],
  ["T", "THR", "THREONINE"],
  ["W", "TRP", "TRYPTOPHAN"],
  ["Y", "TYR", "TYROSINE"],
  ["V", "VAL", "VALINE"],
  ["O", "PYL", "PYRROLYSINE"],
  ["U", "SEC", "SELENOCYSTEINE"],
  ["B", "ASX", "ASPARAGINE/ASPARTIC ACID"],
  ["Z", "GLX", "GLUTAMINE/GLUTAMIC ACID"],
  ["J", "XLE", "LEUCINE/ISOLEUCINE"],
  ["X", "UNK", "UNKNOWN CODON"],
]
AA_CODE_TO_ABR = {}
AA_CODE_TO_NAME = {}
AA_ABR_TO_CODE = {}
AA_ABR_TO_NAME = {}
AA_NAME_TO_CODE = {}
AA_NAME_TO_ABR = {}
for code, abr, name in AAs_FULL_TABLE:
  AA_CODE_TO_ABR[code] = abr
  AA_CODE_TO_NAME[code] = name
  AA_ABR_TO_CODE[abr] = code
  AA_ABR_TO_NAME[abr] = name
  AA_NAME_TO_ABR[name] = abr
  AA_NAME_TO_CODE[name] = code


### CLASSES ###
class Protein:
  def __init__(self, pdb: Union[str | io.IOBase]):
    """Class that wraps around a protein structure.

    Utilizes the biopython protein structure under the hood.
    Atoms that are not part of a chain will automatically be
    added to a new chain that does not overlap with any
    existing chains.

    Parameters:
      pdb: Can be either a file handle, PDB filepath, PDB ID, or UniProt ID

    """
    self.title = "Untitled Protein"
    if isinstance(pdb, io.IOBase):
      pass
    elif isinstance(pdb, str):
      if os.path.exists(pdb):
        self.title = pdb.split("/")[-1]
      else:
        self.title = pdb.upper()
        if len(pdb) == 4:  # check if a valid PDB ID
          r = requests.get(f"https://files.rcsb.org/download/{pdb.upper()}.pdb")
          r.raise_for_status()
          with tempfile.NamedTemporaryFile(delete=False, suffix=".pdb") as temp_file:
            temp_file.write(r.content)
            pdb = temp_file.name
            logger.info("Found matching structure in RCSB PDB, downloading and using that.")
        else:  # check if provided a uniprot ID and fetch from AF2
          r = requests.get(f"https://alphafold.ebi.ac.uk/api/prediction/{pdb.upper()}")
          if r.status_code != 200:
            raise ValueError("Invalid input type provided. Can be either a file handle, PDB filepath, PDB ID, or UniProt ID")
          r = requests.get(r.json()[0]["pdbUrl"])
          if r.status_code != 200:
            raise ValueError("Invalid input type provided. Can be either a file handle, PDB filepath, PDB ID, or UniProt ID")
          with tempfile.NamedTemporaryFile(delete=False, suffix=".pdb") as temp_file:
            temp_file.write(r.content)
            pdb = temp_file.name
            logger.info("Found matching structure in AF-DB, downloading and using that.")
    else:
      raise ValueError("Invalid input type provided. Can be either a file handle, PDB filepath, PDB ID, or UniProt ID")

    # load structure
    parser = PDBParser()
    self.structure = parser.get_structure("structure", pdb)
    assert len(self.structure), "No models found. Structure appears to be empty."

    # Adds any missing chains to the structure.
    # Ensures new chain IDs do not overlap with existing ones.
    existing_chains = self.chains()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numeric_suffix = 1
    new_chain_id = None

    # Find an available chain ID that does not overlap with existing ones
    for char in alphabet:
      if char not in existing_chains:
        new_chain_id = char
        break
    if new_chain_id is None:
      # If all single-letter chain IDs are used, append a numeric suffix
      while new_chain_id is None:
        for char in alphabet:
          candidate_id = f"{char}{numeric_suffix}"
          if candidate_id not in existing_chains:
            new_chain_id = candidate_id
            break
        numeric_suffix += 1

    if new_chain_id:
      # rename chain
      for model in self.structure:
        for chain in model:
          if chain.id is None or chain.id == " ":
            chain.id = new_chain_id
            logger.info(f"Assigned ID '{new_chain_id}' to chain with missing ID in model '{model.id}'.")
    else:
      logger.warning(f"No chain IDs available. Could not rename chain with missing ID in model '{model.id}'.")

    # generate the pandas dataframe similar to that of biopandas
    self.generate_df()

  def __repr__(self):
    return f"<Neurosnap Protein: Title={self.title} Models={self.models()}, Chains=[{', '.join(self.chains())}], Atoms={len(self.df)}>"

  def __call__(self, model: Optional[int] = None, chain: Optional[int] = None, res_type: Optional[int] = None) -> pd.DataFrame:
    """Returns a selection of a copy of the internal dataframe
    that matches the provided query. If no queries are
    provided, will return a copy of the internal dataframe.

    Parameters:
      model: If provided, returned atoms must match this model
      chain: If provided, returned atoms must match this chain
      res_type: If provided, returned atoms must match this res_type

    Returns:
      Copy of the internal dataframe that matches the input query

    """
    df = self.df.copy()
    if model is not None:
      df = df.loc[df.model == model]
    if chain is not None:
      df = df.loc[df.chain == chain]
    if res_type is not None:
      df = df.loc[df.res_type == res_type]
    return df

  def __sub__(self, other_protein: "Protein") -> pd.DataFrame:
    """Automatically calculate the RMSD of two proteins.
    Model used will naively be the first models that have
    identical backbone shapes.
    Essentially just wraps around :obj:`self.calculate_rmsd()`

    Parameters:
      other_protein: Another Protein object to compare against

    Returns:
      Copy of the internal dataframe that matches the input query

    """
    # Get models for each structure using backbone shape
    model1 = None
    model2 = None
    for m1 in self.structure:
      backbone1 = self.get_backbone(model=m1.id)
      for m2 in other_protein.structure:
        backbone2 = other_protein.get_backbone(model=m2.id)
        if backbone1.shape == backbone2.shape:
          model1 = m1.id
          model2 = m2.id
          break

    assert (
      model1 is not None
    ), "Could not find any matching matching models to calculate RMSD for. Please ensure at least two models with matching backbone shapes are provided."
    return self.calculate_rmsd(other_protein, model1=model1, model2=model2)

  def models(self) -> List[int]:
    """Returns a list of all the model names/IDs.

    Returns:
      models: Chain names/IDs found within the PDB file

    """
    return [model.id for model in self.structure]

  def chains(self, model: int = 0) -> List[str]:
    """Returns a list of all the chain names/IDs.

    Parameters:
      model: The ID of the model you want to fetch the chains of, defaults to 0

    Returns:
      Chain names/IDs found within the PDB file

    """
    return [chain.id for chain in self.structure[model] if chain.id.strip()]

  def generate_df(self):
    """Generate the biopandas-like dataframe and update the
    value of self.df to the new dataframe.
    This method should be called whenever the internal
    protein structure is modified or has a transformation
    applied to it.

    Inspired by: https://biopandas.github.io/biopandas

    """
    df = {
      "model": [],
      "chain": [],
      "res_id": [],
      "res_name": [],
      "res_type": [],
      "atom": [],
      "atom_name": [],
      "bfactor": [],
      "x": [],
      "y": [],
      "z": [],
      "mass": [],
    }
    for model in self.structure:
      for chain in model:
        for res in chain:
          for atom in res:
            # get residue type
            res_type = "HETEROGEN"
            if res.id[0] == " " and res.resname in AA_ABR_TO_CODE:
              res_type = "AMINO_ACID"
            elif res.id[0] == " " and res.resname in STANDARD_NUCLEOTIDES:
              res_type = "NUCLEOTIDE"
            df["model"].append(model.id)
            df["chain"].append(chain.id)
            df["res_id"].append(res.id[1])
            df["res_name"].append(res.resname)
            df["res_type"].append(res_type)
            df["atom"].append(atom.serial_number)
            df["atom_name"].append(atom.name)
            df["bfactor"].append(atom.bfactor)
            df["x"].append(atom.coord[0])
            df["y"].append(atom.coord[1])
            df["z"].append(atom.coord[2])
            df["mass"].append(atom.mass)
    self.df = pd.DataFrame(df)

  def get_aas(self, model: int, chain: str) -> str:
    """Returns the amino acid sequence of a target chain.
    Ligands, small molecules, and nucleotides are ignored.

    Parameters:
      model: The ID of the model containing the target chain
      chain: The ID of the chain you want to fetch the AA sequence of

    Returns:
      The amino acid sequence of the found chain

    """
    assert model in self.structure, f'Protein does not contain model "{model}"'
    assert chain in self.structure[model], f'Model {model} does not contain chain "{chain}"'

    ppb = PPBuilder()
    return str(ppb.build_peptides(self.structure[model][chain])[0].get_sequence())

  def renumber(self, model: Optional[int] = None, chain: Optional[int] = None, start: int = 1):
    """Renumbers all selected residues. If selection does not
    exist this function will do absolutely nothing.

    Parameters:
      model: The model ID to renumber. If ``None``, will use all models.
      chain: The chain ID to renumber. If ``None``, will use all models.
      start: Starting value to increment from, defaults to 1.

    """

    def aux(start):
      for m in self.structure:
        if model is None or m.id == model:
          for c in m:
            if chain is None or c.id == chain:
              for res in c:
                # Renumber residue
                res.id = (res.id[0], start, res.id[2])
                start += 1

    # perform initial renumbering to avoid collisions
    aux(-100000)
    # perform actual renumbering
    aux(start)
    # update the pandas dataframe
    self.generate_df()

  def remove_waters(self):
    """Removes all water molecules (residues named 'WAT' or 'HOH')
    from the structure. It is suggested to call :obj:`.renumber()`
    afterwards as well.

    """
    for model in self.structure:
      for chain in model:
        # Identify water molecules and mark them for removal
        residues_to_remove = [res for res in chain if res.get_resname() in ["WAT", "HOH"]]

        # Remove water molecules
        for res in residues_to_remove:
          chain.detach_child(res.id)
    # update the pandas dataframe
    self.generate_df()

  def remove_non_biopolymers(self, model: Optional[int] = None, chain: Optional[str] = None):
    """Removes all ligands, heteroatoms, and non-biopolymer
    residues from the selected structure. Non-biopolymer
    residues are considered to be any residues that are not
    standard amino acids or standard nucleotides (DNA/RNA).
    If no model or chain is provided, it will remove from
    the entire structure.

    Parameters:
      model: The model ID to process. If ``None``, will use all models.
      chain: The chain ID to process. If ``None``, will use all chains.

    """
    # List of standard amino acids and nucleotides (biopolymer residues)
    biopolymer_residues = set(AA_ABR_TO_CODE.keys()).union(STANDARD_NUCLEOTIDES)

    for m in self.structure:
      if model is None or m.id == model:
        for c in m:
          if chain is None or c.id == chain:
            # Identify non-biopolymer residues (ligands, heteroatoms, etc.)
            residues_to_remove = [res for res in c if res.get_resname() not in biopolymer_residues]

            # Remove non-biopolymer residues
            for res in residues_to_remove:
              c.detach_child(res.id)
    # update the pandas dataframe
    self.generate_df()

  def remove_nucleotides(self, model: Optional[int] = None, chain: Optional[str] = None):
    """Removes all nucleotides (DNA and RNA) from the structure.
    If no model or chain is provided, it will remove nucleotides
    from the entire structure.

    Parameters:
      model: The model ID to process. If ``None``, will use all models.
      chain: The chain ID to process. If ``None``, will use all chains.

    """
    for m in self.structure:
      if model is None or m.id == model:
        for c in m:
          if chain is None or c.id == chain:
            # Identify nucleotide residues (both RNA and DNA)
            residues_to_remove = [res for res in c if res.get_resname() in STANDARD_NUCLEOTIDES]

            # Remove nucleotide residues
            for res in residues_to_remove:
              c.detach_child(res.id)

    # update the pandas dataframe
    self.generate_df()

  def get_backbone(self, model: Optional[int] = None, chain: Optional[str] = None) -> np.ndarray:
    """Extract backbone atoms (N, CA, C) from the structure.
    If model or chain is not provided, extracts from all models/chains.

    Parameters:
      model: Model ID to extract from. If ``None``, all models are included.
      chain: Chain ID to extract from. If ``None``, all chains are included.

    Returns:
      A numpy array of backbone coordinates (Nx3)

    """
    backbone_coords = []

    for m in self.structure:
      if model is None or m.id == model:
        for c in m:
          if chain is None or c.id == chain:
            for res in c:
              for atom in res:
                if atom.name in BACKBONE_ATOMS:
                  backbone_coords.append(atom.coord)

    return np.array(backbone_coords)

  def find_disulfide_bonds(self, threshold: float = 2.05) -> List[Tuple]:
    """Find disulfide bonds between Cysteine residues in the structure.
    Looks for SG-SG bonds within a threshold distance.

    Parameters:
      threshold: Maximum distance to consider a bond between SG atoms, in angstroms.
        Default is 2.05 Å.

    Returns:
      List of tuples of residue pairs forming disulfide bonds

    """
    disulfide_pairs = []

    for model in self.structure:
      for chain in model:
        cysteines = [res for res in chain if res.get_resname() == "CYS"]
        for i, res1 in enumerate(cysteines):
          for res2 in cysteines[i + 1 :]:
            try:
              sg1 = res1["SG"]
              sg2 = res2["SG"]
              distance = sg1 - sg2
              if distance < threshold:
                disulfide_pairs.append((res1, res2))
            except KeyError:
              pass  # Skip if no SG atom found
    return disulfide_pairs

  def find_salt_bridges(self, model: Optional[int] = None, chain: Optional[str] = None, cutoff: float = 4.0) -> List[Tuple]:
    """Identify salt bridges between oppositely charged residues.
    A salt bridge is defined as an interaction between
    a positively charged residue (Lys, Arg) and a negatively
    charged residue (Asp, Glu) within a given cutoff distance.

    Parameters:
      model: Model ID to search. If ``None``, all models are searched.
      chain: Chain ID to search. If ``None``, all chains are searched.
      cutoff: Maximum distance for a salt bridge (float)

    Returns:
      List of residue pairs forming salt bridges

    """
    positive_residues = {"LYS", "ARG"}
    negative_residues = {"ASP", "GLU"}
    salt_bridges = []

    for m in self.structure:
      if model is None or m.id == model:
        for c in m:
          if chain is None or c.id == chain:
            pos_residues = [res for res in c if res.get_resname() in positive_residues]
            neg_residues = [res for res in c if res.get_resname() in negative_residues]
            for pos_res in pos_residues:
              for neg_res in neg_residues:
                dist = pos_res["CA"] - neg_res["CA"]  # Use alpha-carbon distance as a proxy
                if dist < cutoff:
                  salt_bridges.append((pos_res, neg_res))
    return salt_bridges

  def find_hydrophobic_residues(self, model: Optional[int] = None, chain: Optional[str] = None) -> List[Tuple]:
    """Identify hydrophobic residues in the structure.

    Parameters:
      model: Model ID to extract from. If ``None``, all models are checked.
      chain: Chain ID to extract from. If ``None``, all chains are checked.

    Returns:
      List of tuples ``(model_id, chain_id, residue)`` for hydrophobic residues

    """
    hydrophobic_residues = []

    for m in self.structure:
      if model is None or m.id == model:
        for c in m:
          if chain is None or c.id == chain:
            for res in c:
              if res.get_resname() in HYDROPHOBIC_RESIDUES:
                hydrophobic_residues.append((m.id, c.id, res))

    return hydrophobic_residues

  def find_missing_residues(self, chain: Optional[str] = None) -> List[int]:
    """Identify missing residues in the structure based on residue numbering.
    Useful for identifying gaps in the structure.

    Parameters:
      chain: Chain ID to inspect. If ``None``, all chains are inspected.

    Returns:
      missing_residues: List of missing residue positions

    """
    missing_residues = []

    for model in self.structure:
      for chain in model:
        residues = sorted(res.id[1] for res in chain)
        for i in range(len(residues) - 1):
          if residues[i + 1] != residues[i] + 1:
            missing_residues.extend(range(residues[i] + 1, residues[i + 1]))

    return missing_residues

  def align(self, other_protein: "Protein", model1: int = 0, model2: int = 0):
    """Align another Protein object's structure to the self.structure
    of the current object. The other Protein will be transformed
    and aligned. Only compares backbone atoms (N, CA, C).

    Parameters:
      other_protein: Another Protein object to compare against
      model1: Model ID of reference protein to align to
      model2: Model ID of other protein to transform and align to reference

    """
    assert model1 in self.models(), "Specified model needs to be present in the reference structure."
    assert model2 in other_protein.models(), "Specified model needs to be present in the other structure."

    # Use the Superimposer to align the structures
    def aux(sample_model):
      atoms = []
      for sample_chain in sample_model:
        for res in sample_chain:
          for atom in res:
            if atom.name in BACKBONE_ATOMS:
              atoms.append(atom)
      return atoms

    sup = Superimposer()
    sup.set_atoms(aux(self.structure[model1]), aux(other_protein.structure[model2]))
    sup.apply(other_protein.structure[model2])  # Apply the transformation to the other protein
    # update the pandas dataframe
    other_protein.generate_df()

  def calculate_rmsd(
    self, other_protein: "Protein", model1: int = 0, model2: int = 0, chain1: Optional[str] = None, chain2: Optional[str] = None, align: bool = True
  ) -> float:
    """Calculate RMSD between the current structure and another protein.
    Only compares backbone atoms (N, CA, C). RMSD is in angstroms (Å).

    Parameters:
      other_protein: Another Protein object to compare against
      model1: Model ID of original protein to compare
      model2: Model ID of other protein to compare
      chain1: Chain ID of original protein, if not provided compares all chains
      chain2: Chain ID of other protein, if not provided compares all chains
      align: Whether to align the structures first using Superimposer

    Returns:
      The root-mean-square deviation between the two structures

    """
    # ensure models are present
    assert model1 in self.models(), f"Model {model1} was not found in current protein."
    assert model2 in other_protein.models(), f"Model {model2} was not found in other protein."

    # Get backbone coordinates of both structures
    backbone1 = self.get_backbone(model=model1, chain=chain1)
    backbone2 = other_protein.get_backbone(model=model2, chain=chain2)
    assert backbone1.shape == backbone2.shape, "Structures must have the same number of backbone atoms for RMSD calculation."

    if align:
      self.align(other_protein, model1=model1, model2=model2)

    # Get new backbone coordinates of both structures
    backbone1 = self.get_backbone(model=model1, chain=chain1)
    backbone2 = other_protein.get_backbone(model=model2, chain=chain2)

    diff = backbone1 - backbone2
    rmsd = np.sqrt(np.sum(diff**2) / backbone1.shape[0])
    return rmsd

  def calculate_distance_matrix(self, model: Optional[int] = None, chain: Optional[str] = None) -> np.ndarray:
    """Calculate the distance matrix for all alpha-carbon (CA) atoms in the chain.
    Useful for creating contact maps or proximity analyses.

    Parameters:
      model: The model ID to calculate the distance matrix for, if not provided will use first model found
      chain: The chain ID to calculate, if not provided calculates for all chains

    Returns:
      A 2D numpy array representing the distance matrix

    """
    model = self.models()[0]
    ca_atoms = []

    for m in self.structure:
      if m.id == model:
        for c in m:
          if chain is None or c.id == chain:
            for res in c:
              if "CA" in res:
                ca_atoms.append(res["CA"].coord)

    ca_atoms = np.array(ca_atoms)
    dist_matrix = np.sqrt(np.sum((ca_atoms[:, np.newaxis] - ca_atoms[np.newaxis, :]) ** 2, axis=-1))
    return dist_matrix

  def calculate_center_of_mass(self, model: Optional[int] = None, chain: Optional[str] = None) -> np.ndarray:
    """Calculate the center of mass of the protein.
    Considers only atoms with defined masses.

    Parameters:
      model: Model ID to calculate for, if not provided calculates for all models
      chain: Chain ID to calculate for, if not provided calculates for all chains

    Returns:
      center_of_mass: A 3D numpy array representing the center of mass

    """
    total_mass = 0
    weighted_coords = np.zeros(3)

    for m in self.structure:
      if model is None or m.id == model:
        for c in m:
          if chain is None or c.id == chain:
            for res in c:
              for atom in res:
                if atom.mass is not None:
                  total_mass += atom.mass
                  weighted_coords += atom.mass * atom.coord

    if total_mass == 0:
      raise ValueError("No atoms with mass found in the selected structure.")

    return weighted_coords / total_mass

  def distances_from_com(self, model: Optional[int] = None, chain: Optional[str] = None):
    """Calculate the distances of all atoms from the center of mass (COM) of the protein.

    This method computes the Euclidean distance between the coordinates of each atom
    and the center of mass of the structure. The center of mass is calculated for the
    specified model and chain, or for all models and chains if none are provided.

    Parameters:
      model: The model ID to calculate for. If not provided, calculates for all models.
      chain: The chain ID to calculate for. If not provided, calculates for all chains.

    Returns:
      A 1D NumPy array containing the distances (in Ångströms) between each atom and the center of mass.

    """
    com = self.calculate_center_of_mass(model=model, chain=chain)
    distances = []

    for m in self.structure:
      if model is None or m.id == model:
        for c in m:
          if chain is None or c.id == chain:
            for res in c:
              for atom in res:
                distance = np.linalg.norm(atom.coord - com)
                distances.append(distance)

    return np.array(distances)  # Convert the list of distances to a NumPy array

  def calculate_surface_area(self, model: int = 0, level: str = "R") -> float:
    """Calculate the solvent-accessible surface area (SASA) of the protein.
    Utilizes Biopython's SASA module.

    Parameters:
      model: The model ID to calculate SASA for, defaults to 0.
      level: The level at which ASA values are assigned, which can be one of "A" (Atom), "R" (Residue), "C" (Chain), "M" (Model), or "S" (Structure). The ASA value of an entity is the sum of all ASA values of its children.

    Returns:
      Solvent-accessible surface area in Å²

    """
    assert model in self.models(), f"Model {model} is not currently present."
    structure_model = self.structure[model]
    sasa_calculator = SASA.ShrakeRupley()
    sasa_calculator.compute(structure_model, level=level)
    total_sasa = sum([residue.sasa for residue in structure_model.get_residues() if residue.sasa])
    return total_sasa

  def calculate_protein_volume(self, model: int = 0, chain: Optional[str] = None) -> float:
    """Compute an estimate of the protein volume using the van der Waals radii.
    Uses the sum of atom radii to compute the volume.

    Parameters:
      model: Model ID to compute volume for, defaults to 0
      chain: Chain ID to compute, if not provided computes for all chains

    Returns:
      Estimated volume in Å³

    """
    assert model in self.models(), f"Model {model} is not currently present."
    vdw_radii = {"H": 1.2, "C": 1.7, "N": 1.55, "O": 1.52, "P": 1.8, "S": 1.8}  # Example radii in Å
    volume = 0

    for m in self.structure:
      for c in m:
        if chain is None or c.id == chain:
          for res in c:
            if is_aa(res):
              for atom in res:
                element = atom.element
                if element in vdw_radii:
                  radius = vdw_radii[element]
                  volume += (4 / 3) * np.pi * (radius**3)
    return volume

  def to_sdf(self, fpath: str):
    """Save the current protein structure as an SDF file.
    Will export all models and chains. Use :obj:`.remove()`
    method to get rid of undesired regions.

    Parameters:
      fpath: Path to the output SDF file

    """
    # Write the current protein structure to a temporary PDB file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdb") as temp_pdb:
      self.save(temp_pdb.name, format="pdb")
      pdb_fpath = temp_pdb.name

      # Read the PDB file
      mol = Chem.MolFromPDBFile(pdb_fpath, sanitize=False)

      if mol is None:
        raise ValueError("Unable to parse the PDB file.")

      # Write the molecule to SDF
      writer = Chem.SDWriter(fpath)
      writer.write(mol)
      writer.close()
      logger.info(f"Successfully wrote SDF file to {fpath}.")

  def remove(self, model: int, chain: Optional[str] = None, resi_start: Optional[int] = None, resi_end: Optional[int] = None):
    """Completely removes all parts of a selection from
    self.structure. If a residue range is provided then all
    residues between resi_start and resi_end will be removed
    from the structure (inclusively). If a residue range is
    not provided then all residues in a chain will be removed.

    Parameters:
      model: ID of model to remove from
      chain: ID of chain to remove from, if not provided will remove all chains in the model
      resi_start: Index of first residue in the range you want to remove
      resi_end: Index of last residues in the range you want to remove

    """
    # validate input query
    assert model in self.models(), f"Model ID {model} does not exist in your structure. Found models include {self.models()}."
    if chain is not None:
      assert chain in self.chains(model), f"Chain ID {chain} does not exist in your structure. Found chains include {self.chains(model)}."
    if resi_start is not None or resi_end is not None:
      assert chain is not None, "Chain needs to specified if you want to remove residues"
      assert resi_start is not None and resi_end is not None, "Both resi_start and resi_end must be provided"
      assert isinstance(resi_start, int) and isinstance(resi_end, int), "Both resi_start and resi_end must be valid integers"
      assert resi_end >= resi_start, "resi_start start must be less than resi_end"
      assert resi_start in self.structure[model][chain], f"Residue {resi_start} does not exist in the specified part of your structure."
      assert resi_end in self.structure[model][chain], f"Residue {resi_end} does not exist in the specified part of your structure."

    # Perform the removal
    if resi_start is not None and resi_end is not None:
      # Remove residues in the specified range
      chain_obj = self.structure[model][chain]
      residues_to_remove = [res for res in chain_obj if resi_start <= res.id[1] <= resi_end]
      for res in residues_to_remove:
        chain_obj.detach_child(res.id)
    elif chain is not None:
      # Remove the entire chain
      self.structure[model].detach_child(chain)
    else:
      # Remove the entire model
      self.structure.detach_child(model)

    # Update the pandas dataframe to reflect the changes
    self.generate_df()

  def save(self, fpath: str, format: str = "pdb"):
    """Save the structure as a PDB or mmCIF file.
    Will overwrite any existing files.

    Parameters:
      fpath: File path where you want to save the structure
      format: File format to save in, either 'pdb' or 'mmcif'

    """
    format = format.lower()
    if format == "pdb":
      io = PDBIO()
      io.set_structure(self.structure)
      io.save(fpath, preserve_atom_numbering=True)
    elif format == "mmcif":
      mmcif_io = MMCIFIO()
      mmcif_io.set_structure(self.structure)
      mmcif_io.save(fpath)
    else:
      raise ValueError("Format must be 'pdb' or 'mmcif'.")


### FUNCTIONS ###
def getAA(query: str) -> Tuple[str, str, str]:
  """Efficiently get any amino acid using either their 1 letter code,
  3 letter abbreviation, or full name. See AAs_FULL_TABLE
  for a list of all supported amino acids and codes.

  Parameters:
    query: Amino acid code, abbreviation, or name

  Returns:
    A triple of the form ``(code, abr, name)``.

    - ``code`` is the amino acid 1 letter abbreviation / code
    - ``abr`` is the amino acid 3 letter abbreviation / code
    - ``name`` is the amino acid full name

  """
  query = query.upper()
  try:
    if len(query) == 1:
      return query, AA_CODE_TO_ABR[query], AA_CODE_TO_NAME[query]
    elif len(query) == 3:
      return AA_ABR_TO_CODE[query], query, AA_ABR_TO_NAME[query]
    else:
      return AA_NAME_TO_CODE[query], AA_NAME_TO_ABR[query], query
  except KeyError:
    raise ValueError(f"Unknown amino acid for {query}")


def calc_lDDT(ref_pdb: str, sample_pdb: str) -> float:
  """Calculates the lDDT (Local Distance Difference Test) between two proteins.

  Parameters:
    ref_pdb: Filepath for reference protein
    sample_pdb: Filepath for sample protein

  Returns:
    The lDDT score of the two proteins which ranges between 0-1

  """
  ref_L, ref_dmap, ref_rnames = lDDT.pdb2dmap(ref_pdb)
  mod_L, mod_dmap, mod_rnames = lDDT.pdb2dmap(sample_pdb)
  return lDDT.get_LDDT(ref_dmap, mod_dmap)


def foldseek_search(
  protein: Union["Protein", str],
  mode: str = "3diaa",
  databases: List[str] = None,
  max_retries: int = 10,
  retry_interval: int = 5,
  output_format: str = "json",
) -> Union[str, pd.DataFrame]:
  """Perform a protein structure search using the Foldseek API.

  Parameters:
      protein: Either a Protein object or a path to a PDB file.
      mode: Search mode. Must be on of "3diaa" or "tm-align".
      databases: List of databases to search. Defaults to a predefined list if not provided.
      max_retries: Maximum number of retries to check the job status.
      retry_interval: Time in seconds between retries for checking job status.
      output_format: Format of the output, either "json" or "dataframe".

  Returns:
      Search results in the specified format (JSON string or pandas DataFrame).

  Raises:
      RuntimeError: If the job fails.
      TimeoutError: If the job does not complete within the allotted retries.
      ValueError: If an invalid output_format is specified.

  """

  BASE_URL = "https://search.foldseek.com/api"

  # Default databases to search
  if databases is None:
    databases = ["afdb50", "afdb-swissprot", "afdb-proteome", "bfmd", "cath50", "mgnify_esm30", "pdb100", "gmgcl_id", "bfvd"]

  # Handle file input (Protein object or file path)
  if isinstance(protein, Protein):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdb") as temp_file:
      protein.save(temp_file.name)
      file_path = temp_file.name
  else:
    file_path = protein

  # Submit the job to the Foldseek API
  data = {"mode": mode, "database[]": databases}
  try:
    with open(file_path, "rb") as file:
      files = {"q": file}
      response = requests.post(f"{BASE_URL}/ticket", data=data, files=files)
    response.raise_for_status()
    job_id = response.json()["id"]
  except requests.RequestException as e:
    raise RuntimeError(f"Failed to submit job: {e}")

  # Poll for job status until complete or max retries are reached
  for attempt in range(max_retries):
    try:
      status_response = requests.get(f"{BASE_URL}/ticket/{job_id}")
      status_response.raise_for_status()
      status = status_response.json().get("status", "ERROR")
    except requests.RequestException as e:
      raise RuntimeError(f"Failed to retrieve job status: {e}")

    if status == "COMPLETE":
      break
    elif status == "ERROR":
      raise RuntimeError("Job failed")

    time.sleep(retry_interval)
  else:
    raise TimeoutError(f"Job did not complete within {max_retries * retry_interval} seconds")

  # Retrieve and accumulate results
  results = []
  entry = 0
  while True:
    try:
      result_response = requests.get(f"{BASE_URL}/result/{job_id}/{entry}")
      result_response.raise_for_status()
      result = result_response.json()
    except requests.RequestException as e:
      raise RuntimeError(f"Failed to retrieve results: {e}")

    if not result or all(len(db_result["alignments"]) == 0 for db_result in result["results"]):
      break

    results.append(result)
    entry += 1

  # Clean up temporary file if it was created
  if isinstance(protein, Protein):
    os.remove(file_path)

  # Return results based on the output format
  if output_format == "json":
    return json.dumps(results, indent=2)
  elif output_format == "dataframe":
    rows = []
    for result in results:
      for db_result in result["results"]:
        alignments = db_result["alignments"]
        for alignment in alignments[0]:
          rows.append(
            {
              "target": alignment["target"],
              "db": db_result["db"],
              "seqId": alignment.get("seqId", ""),
              "alnLength": alignment.get("alnLength", ""),
              "missmatches": alignment.get("missmatches", ""),
              "gapsopened": alignment.get("gapsopened", ""),
              "qStartPos": alignment.get("qStartPos", ""),
              "qEndPos": alignment.get("qEndPos", ""),
              "dbStartPos": alignment.get("dbStartPos", ""),
              "dbEndPos": alignment.get("dbEndPos", ""),
              "eval": alignment.get("eval", ""),
              "score": alignment.get("score", ""),
              "qLen": alignment.get("qLen", ""),
              "dbLen": alignment.get("dbLen", ""),
              "seq": alignment.get("tSeq", ""),
            }
          )
    return pd.DataFrame(rows)
  else:
    raise ValueError("Invalid output_format. Choose 'json' or 'dataframe'.")


def run_blast(
  sequence: Union[str, "Protein"],
  email: str,
  matrix: str = "BLOSUM62",
  alignments: int = 250,
  scores: int = 250,
  evalue: float = 10.0,
  filter: bool = False,
  gapalign: bool = True,
  database: str = "uniprotkb_refprotswissprot",
  output_format: Optional[str] = None,
  output_path: Optional[str] = None,
  return_df: bool = True,
) -> Optional[pd.DataFrame]:
  """Submits a BLAST job to the EBI NCBI BLAST web service, checks the status periodically, and retrieves the result.
  The result can be saved either as an XML or FASTA file. Optionally, a DataFrame with alignment details can be returned.

  Parameters:
    sequence: The input amino acid sequence as a string or a Protein object.

      If a Protein object is provided with multiple chains, an error will be raised, and the user will be prompted to provide a single chain sequence using the :obj:`Protein.get_aas` method.
    email: The email address to use for communication if there is a problem.
    matrix: The scoring matrix to use, default is ``"BLOSUM62"``.

      Must be one of::

      ["BLOSUM45", "BLOSUM62", "BLOSUM80", "PAM30", "PAM70"].
    alignments: The number of alignments to display in the result (default is 250). the number alignments must be one of the following::

      [50, 100, 250, 500, 750, 1000]
    scores: The number of scores to display in the result, default is ``250``.
    evalue: The E threshold for alignments (default is 10.0). Must be one of::

      [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
    filter: Whether to filter low complexity regions (default is False).
    gapalign: Whether to allow gap alignments (default is True).
    database: The database to search in, default is ``"uniprotkb_refprotswissprot"``.

      Must be one of::

      ["uniprotkb_refprotswissprot", "uniprotkb_pdb", "uniprotkb", "afdb", "uniprotkb_reference_proteomes", "uniprotkb_swissprot", "uniref100", "uniref90", "uniref50", "uniparc"]
    output_format: The format in which to save the result, either ``"xml"`` or ``"fasta"``. If ``None``, which is the default, no file will be saved.
    output_path: The file path to save the output. This is required if `output_format` is specified.
    return_df: Whether to return a DataFrame with alignment details, default is ``True``.

  Returns:
    A pandas DataFrame with BLAST hit and alignment information, if `return_df` is True.

    The DataFrame contains the following columns:
    - "Hit ID": The identifier of the hit sequence.
    - "Accession": The accession number of the hit sequence.
    - "Description": The description of the hit sequence.
    - "Length": The length of the hit sequence.
    - "Score": The score of the alignment.
    - "Bits": The bit score of the alignment.
    - "Expectation": The E-value of the alignment.
    - "Identity (%)": The percentage identity of the alignment.
    - "Gaps": The number of gaps in the alignment.
    - "Query Sequence": The query sequence in the alignment.
    - "Match Sequence": The matched sequence in the alignment.

  Raises:
    AssertionError: If ``sequence`` is provided as a Protein object with multiple chains.
  """

  def parse_xml_to_fasta_and_dataframe(xml_content, job_id, output_format=None, output_path=None, return_df=True):
    """Parses the XML content, saves it as a FASTA file, or returns a DataFrame if requested."""
    root = ET.fromstring(xml_content)
    hits = []
    fasta_content = ""

    for hit in root.findall(".//{http://www.ebi.ac.uk/schema}hit"):
      hit_id = hit.attrib["id"]
      hit_ac = hit.attrib["ac"]
      hit_description = hit.attrib["description"]
      hit_length = hit.attrib["length"]

      for alignment in hit.findall(".//{http://www.ebi.ac.uk/schema}alignment"):
        score = alignment.find("{http://www.ebi.ac.uk/schema}score").text
        bits = alignment.find("{http://www.ebi.ac.uk/schema}bits").text
        expectation = alignment.find("{http://www.ebi.ac.uk/schema}expectation").text
        identity = alignment.find("{http://www.ebi.ac.uk/schema}identity").text
        gaps = alignment.find("{http://www.ebi.ac.uk/schema}gaps").text
        query_seq = alignment.find("{http://www.ebi.ac.uk/schema}querySeq").text
        match_seq = alignment.find("{http://www.ebi.ac.uk/schema}matchSeq").text

        fasta_content += (
          f">{hit_id} | Accession: {hit_ac} | Description: {hit_description} | "
          f"Length: {hit_length} | Score: {score} | Bits: {bits} | "
          f"Expectation: {expectation} | Identity: {identity}% | Gaps: {gaps}\n"
          f"{match_seq}\n\n"
        )

        hits.append(
          {
            "Hit ID": hit_id,
            "Accession": hit_ac,
            "Description": hit_description,
            "Length": hit_length,
            "Score": score,
            "Bits": bits,
            "Expectation": expectation,
            "Identity (%)": identity,
            "Gaps": gaps,
            "Query Sequence": query_seq,
            "Match Sequence": match_seq,
          }
        )

    # Step 4: Save or return results
    if output_format == "fasta" and output_path:
      with open(output_path, "w") as fasta_file:
        fasta_file.write(fasta_content)
      print(f"FASTA result saved as {output_path}")

    if return_df:
      df = pd.DataFrame(hits)
      return df

  valid_databases = [
    "uniprotkb_refprotswissprot",
    "uniprotkb_pdb",
    "uniprotkb",
    "afdb",
    "uniprotkb_reference_proteomes",
    "uniprotkb_swissprot",
    "uniref100",
    "uniref90",
    "uniref50",
    "uniparc",
  ]
  if database not in valid_databases:
    raise ValueError(f"Database must be one of the following {valid_databases}")

  valid_matrices = ["BLOSUM45", "BLOSUM62", "BLOSUM80", "PAM30", "PAM70"]
  if matrix not in valid_matrices:
    raise ValueError(f"Matrix must be one of the following {valid_matrices}")

  valid_evalues = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
  if evalue not in valid_evalues:
    raise ValueError(f"E-threshold must be one of the following {valid_evalues}")

  # the api is very delicate, we need specific parameters
  if evalue > 1:
    evalue = int(evalue)

  valid_alignments = [50, 100, 250, 500, 750, 1000]
  if alignments not in valid_alignments:
    raise ValueError(f"Alignments must be one of the following {valid_alignments}")

  valid_output_formats = ["xml", "fasta", None]
  if output_format not in valid_output_formats:
    raise ValueError(f"Output format must be one of the following {valid_output_formats}")

  # Handle Protein object input
  if isinstance(sequence, Protein):
    if len(sequence.chains()) > 1:
      raise AssertionError("The protein has multiple chains. Use '.get_aas(model, chain)' to obtain the sequence for a specific chain.")

    model = sequence.models()[0]
    chain = sequence.chains()[0]
    sequence = sequence.get_aas(model, chain)

  # Step 1: Submit the BLAST job
  url = "https://www.ebi.ac.uk/Tools/services/rest/ncbiblast/run"

  multipart_data = MultipartEncoder(
    fields={
      "email": email,
      "program": "blastp",
      "matrix": matrix,
      "alignments": str(alignments),
      "scores": str(scores),
      "exp": str(evalue),
      "filter": "T" if filter else "F",
      "gapalign": str(gapalign).lower(),
      "stype": "protein",
      "sequence": sequence,
      "database": database,
    }
  )

  headers = {
    "User-Agent": USER_AGENT,
    "Accept": "text/plain,application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": multipart_data.content_type,
  }

  response = requests.post(url, headers=headers, data=multipart_data)

  if response.status_code == 200:
    job_id = response.text.strip()
    print(f"Job submitted successfully. Job ID: {job_id}")
  else:
    response.raise_for_status()

  # Step 2: Check job status
  status_url = f"https://www.ebi.ac.uk/Tools/services/rest/ncbiblast/status/{job_id}"

  while True:
    status_response = requests.get(status_url)
    status = status_response.text.strip()

    if status_response.status_code == 200:
      print(f"Job status: {status}")
      if status == "FINISHED":
        break
      elif status in ["RUNNING", "PENDING", "QUEUED"]:
        time.sleep(20)
      else:
        raise Exception(f"Job failed with status: {status}")
    else:
      status_response.raise_for_status()

  # Step 3: Retrieve XML result
  xml_url = f"https://www.ebi.ac.uk/Tools/services/rest/ncbiblast/result/{job_id}/xml"
  xml_response = requests.get(xml_url)

  if xml_response.status_code == 200:
    xml_content = xml_response.text
    # Save XML if output format is XML
    if output_format == "xml" and output_path:
      with open(output_path, "w") as xml_file:
        xml_file.write(xml_content)
      print(f"XML result saved as {output_path}")
    elif output_format == "fasta" and output_path:
      return parse_xml_to_fasta_and_dataframe(xml_content, job_id, output_format, output_path, return_df)
    elif return_df:
      return parse_xml_to_fasta_and_dataframe(xml_content, job_id, output_format, output_path, return_df)
  else:
    xml_response.raise_for_status()


def plot_pseudo_3D(
  xyz: Union[np.ndarray, pd.DataFrame],
  c: np.ndarray = None,
  ax: matplotlib.axes.Axes = None,
  chainbreak: int = 5,
  Ls: Optional[List] = None,
  cmap: str = "gist_rainbow",
  line_w: float = 2.0,
  cmin: Optional[float] = None,
  cmax: Optional[float] = None,
  zmin: Optional[float] = None,
  zmax: Optional[float] = None,
  shadow: float = 0.95,
) -> matplotlib.collections.LineCollection:
  """Plot the famous Pseudo 3D projection of a protein.

  Algorithm originally written By Dr. Sergey Ovchinnikov.
  Adapted from https://github.com/sokrypton/ColabDesign/blob/16e03c23f2a30a3dcb1775ac25e107424f9f7352/colabdesign/shared/plot.py

  Parameters:
    xyz: XYZ coordinates of the protein
    c: 1D array of all the values to use to color the protein, defaults to residue index
    ax: Matplotlib axes object to add the figure to
    chainbreak: Minimum distance in angstroms between chains / segments before being considered a chain break (int)
    Ls: Allows handling multiple chains or segments by providing the lengths of each chain, ensuring that chains are visualized separately without unwanted connections
    cmap: Matplotlib color map to use for coloring the protein
    line_w: Line width
    cmin: Minimum value for coloring, automatically calculated if None
    cmax: Maximum value for coloring, automatically calculated if None
    zmin: Minimum z coordinate values, automatically calculated if None
    zmax: Maximum z coordinate values, automatically calculated if None
    shadow: Shadow intensity between 0 and 1 inclusive, lower numbers mean darker more intense shadows

  Returns:
    LineCollection object of what's been drawn

  """

  def rescale(a, amin=None, amax=None):
    a = np.copy(a)
    if amin is None:
      amin = a.min()
    if amax is None:
      amax = a.max()
    a[a < amin] = amin
    a[a > amax] = amax
    return (a - amin) / (amax - amin)

  # clip color values and produce warning if necesarry
  if c is not None and cmin is not None and cmax is not None:
    if np.any(c < cmin):
      logger.warn(f"The provided c colors array contains values that are less than cmin ({cmin}). Out of range values will be clipped into range.")
    if np.any(c > cmax):
      logger.warn(f"The provided c colors array contains values that are greater than cmax ({cmax}). Out of range values will be clipped into range.")
    c = np.clip(c, a_min=cmin, a_max=cmax)

  # make segments and colors for each segment
  xyz = np.asarray(xyz)
  if Ls is None:
    seg = np.concatenate([xyz[:, None], np.roll(xyz, 1, 0)[:, None]], axis=1)
    c_seg = np.arange(len(seg))[::-1] if c is None else (c + np.roll(c, 1, 0)) / 2
  else:
    Ln = 0
    seg = []
    c_seg = []
    for L in Ls:
      sub_xyz = xyz[Ln : Ln + L]
      seg.append(np.concatenate([sub_xyz[:, None], np.roll(sub_xyz, 1, 0)[:, None]], axis=1))
      if c is not None:
        sub_c = c[Ln : Ln + L]
        c_seg.append((sub_c + np.roll(sub_c, 1, 0)) / 2)
      Ln += L
    seg = np.concatenate(seg, 0)
    c_seg = np.arange(len(seg))[::-1] if c is None else np.concatenate(c_seg, 0)

  # set colors
  c_seg = rescale(c_seg, cmin, cmax)
  if isinstance(cmap, str):
    if cmap == "gist_rainbow":
      c_seg *= 0.75
    colors = matplotlib.colormaps[cmap](c_seg)
  else:
    colors = cmap(c_seg)

  # remove segments that aren't connected
  seg_len = np.sqrt(np.square(seg[:, 0] - seg[:, 1]).sum(-1))
  if chainbreak is not None:
    idx = seg_len < chainbreak
    seg = seg[idx]
    seg_len = seg_len[idx]
    colors = colors[idx]

  seg_mid = seg.mean(1)
  seg_xy = seg[..., :2]
  seg_z = seg[..., 2].mean(-1)
  order = seg_z.argsort()

  # add shade/tint based on z-dimension
  z = rescale(seg_z, zmin, zmax)[:, None]

  # add shadow (make lines darker if they are behind other lines)
  seg_len_cutoff = (seg_len[:, None] + seg_len[None, :]) / 2
  seg_mid_z = seg_mid[:, 2]
  seg_mid_dist = np.sqrt(np.square(seg_mid[:, None] - seg_mid[None, :]).sum(-1))
  shadow_mask = sigmoid(seg_len_cutoff * 2.0 - seg_mid_dist) * (seg_mid_z[:, None] < seg_mid_z[None, :])
  np.fill_diagonal(shadow_mask, 0.0)
  shadow_mask = shadow ** shadow_mask.sum(-1, keepdims=True)

  seg_mid_xz = seg_mid[:, :2]
  seg_mid_xydist = np.sqrt(np.square(seg_mid_xz[:, None] - seg_mid_xz[None, :]).sum(-1))
  tint_mask = sigmoid(seg_len_cutoff / 2 - seg_mid_xydist) * (seg_mid_z[:, None] < seg_mid_z[None, :])
  np.fill_diagonal(tint_mask, 0.0)
  tint_mask = 1 - tint_mask.max(-1, keepdims=True)

  colors[:, :3] = colors[:, :3] + (1 - colors[:, :3]) * (0.50 * z + 0.50 * tint_mask) / 3
  colors[:, :3] = colors[:, :3] * (0.20 + 0.25 * z + 0.55 * shadow_mask)

  set_lim = False
  if ax is None:
    fig, ax = plt.subplots()
    fig.set_figwidth(5)
    fig.set_figheight(5)
    set_lim = True
  else:
    fig = ax.get_figure()
    if ax.get_xlim() == (0, 1):
      set_lim = True

  if set_lim:
    xy_min = xyz[:, :2].min() - line_w
    xy_max = xyz[:, :2].max() + line_w
    ax.set_xlim(xy_min, xy_max)
    ax.set_ylim(xy_min, xy_max)

  ax.set_aspect("equal")
  ax.set_xlabel("Distance (Å)", fontsize=12)
  ax.set_ylabel("Distance (Å)", fontsize=12)

  # determine linewidths
  width = fig.bbox_inches.width * ax.get_position().width
  linewidths = line_w * 72 * width / np.diff(ax.get_xlim())

  lines = mcoll.LineCollection(
    seg_xy[order], colors=colors[order], linewidths=linewidths, path_effects=[matplotlib.patheffects.Stroke(capstyle="round")]
  )
  return ax.add_collection(lines)


def animate_pseudo_3D(
  fig: matplotlib.figure.Figure,
  ax: matplotlib.axes.Axes,
  frames: matplotlib.collections.LineCollection,
  titles: Union[str, List[str]] = "Protein Animation",
  interval: int = 200,
  repeat_delay: int = 0,
  repeat: bool = True,
) -> matplotlib.animation.ArtistAnimation:
  """Animate multiple Pseudo 3D LineCollection objects.

  Parameters:
    fig: Matplotlib figure that contains all the frames
    ax: Matplotlib axes for the figure that contains all the frames
    frames: List of LineCollection objects
    titles: Single title or list of titles corresponding to each frame
    interval: Delay between frames in milliseconds
    repeat_delay: The delay in milliseconds between consecutive animation runs, if repeat is True
    repeat: Whether the animation repeats when the sequence of frames is completed

  Returns:
    Animation of all the different frames

  """
  # check titles
  if isinstance(titles, str):
    titles = [f"{titles} ({i+1}/{len(frames)})" for i in range(len(frames))]
  elif len(titles) == len(frames):
    ValueError(f"The number of titles ({len(titles)}) does not match the number of frames ({len(frames)}).")

  if isinstance(titles, str):
    titles = [f"{titles} ({i+1}/{len(frames)})" for i in range(len(frames))]
  elif len(titles) == len(frames):
    ValueError(f"The number of titles ({len(titles)}) does not match the number of frames ({len(frames)}).")

  # Gather all vertices safely across multiple paths per frame
  all_x = np.concatenate([path.vertices[:, 0] for frame in frames for path in frame.get_paths()])
  all_y = np.concatenate([path.vertices[:, 1] for frame in frames for path in frame.get_paths()])
  # Calculate limits with optional padding
  x_min, x_max = all_x.min(), all_x.max()
  y_min, y_max = all_y.min(), all_y.max()
  # Apply padding to the limits
  padding = 4
  ax.set_xlim(x_min - padding, x_max + padding)
  ax.set_ylim(y_min - padding, y_max + padding)
  # disable axes
  ax.axis("off")

  def init():
    # hide all frames
    for frame in frames:
      frame.set_visible(False)
    # Initialize the plot with the first frame
    collection = frames[0]
    ax.add_collection(collection)
    ax.set_title(titles[0])
    return (collection,)

  def animate(i):
    frames[i - 1].set_visible(False)
    frames[i].set_visible(True)
    ax.add_collection(frames[i])
    ax.set_title(titles[i])
    return (frames[i],)

  ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(frames), interval=interval, repeat_delay=repeat_delay, repeat=repeat)
  return ani
