import subprocess
import logging


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def run_plink2(command: str):
    """
    Runs a PLINK2 command using the subprocess module.

    Args:
        command: The PLINK2 command to run.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logging.debug("Error: %s", result.stderr)
    else:
        logging.debug("Output: %s", result.stdout)


def generate_bed_bim_fam(
    plink2_path: str,
    ped_file: str,
    map_file: str,
    output_prefix: str,
    relax_mind_threshold: bool = False
):
    """
    Generates BED/BIM/FAM files from PED/MAP files using PLINK2.

    Args:
        plink2_path: Path to the PLINK2 executable.
        ped_file: Path to the PED file.
        map_file: Path to the MAP file.
        output_prefix: Prefix for the output files.
    """
    mind = "" if relax_mind_threshold else "--mind 0.1"
    command = f"{plink2_path} --ped {ped_file} --map {map_file} --make-bed --geno 0.1 {mind} --out {output_prefix}"
    run_plink2(command)


def calculate_kinship_matrix(
    plink2_path: str,
    input_prefix: str,
    output_prefix: str
):
    """
    Calculates the kinship matrix using PLINK2.

    Args:
        plink2_path: Path to the PLINK2 executable.
        input_prefix: Prefix for the input BED/BIM/FAM files.
        output_prefix: Prefix for the output kinship matrix files.
    """
    command = f"{plink2_path} --bfile {input_prefix} --make-rel square --out {output_prefix}"
    run_plink2(command)
