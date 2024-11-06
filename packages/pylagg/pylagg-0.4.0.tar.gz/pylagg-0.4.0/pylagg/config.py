import os
import toml

from pylagg.cut_adapt import trim
from pylagg.cgr_step import config_count_file_to_image_file
import pylagg.ena_download as ena
import pylagg.kmer_counting as jellyfish


def load_toml_file(config_file: str) -> dict:
    """
    Reads a TOML file and returns a dictionary of the contents.
    """
    if not os.path.isfile(config_file):
        raise Exception(
            "Config file not detected. Please ensure you have given the correct path."
        )

    # read the TOML file
    try:
        config = toml.load(config_file)
    except Exception as e:
        if type(e) is toml.TomlDecodeError:
            raise Exception("Invalid TOML file. Please provide a valid TOML file.")
        else:
            raise Exception(
                "An error occurred while reading the config file. Please ensure it is a valid TOML file."
            )

    return config


def config_accession_to_cgr(config_file: str):
    config = load_toml_file(config_file)

    accession_list = ena.get_accessions_from_config(config)

    for accession_number in accession_list:
        fastq_files = ena.ena_download(accession_number)

        # Check if the 'cutadapt' section exists
        if "cutadapt" in config and bool(config["cutadapt"]):
            trimmed_file = trim(fastq_files, config)

            counts_path = jellyfish.handle_config_jellyfish(config, [trimmed_file])

            # will activate if trim key is missing or equals "False"
            if not config.get("Files", {}).get("trim", False):
                os.remove(trimmed_file)

        else:
            counts_path = jellyfish.handle_config_jellyfish(config, fastq_files)

        # Delete .jf file that jellyfish creates. This file has no use outside of jellyfish
        os.remove(counts_path.replace(".counts", ".jf"))

        with open(counts_path, "r") as f:
            config_count_file_to_image_file(
                f, counts_path.replace(".counts", ".png"), config
            )

        if not config.get("Files", {}).get("fastq", False):
            for files in fastq_files:
                os.remove(files)

        if not config.get("Files", {}).get("counts", False):
            os.remove(counts_path)
