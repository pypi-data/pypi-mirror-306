import os
import subprocess
from typing import List

import rich.progress as prog
from rich.progress import Progress

PROGBAR_COLUMNS = (
    prog.SpinnerColumn(),
    prog.TextColumn("[progress.description]{task.description}"),
    prog.BarColumn(),
    prog.TimeElapsedColumn()
)

def get_zcat_command() -> str:
    '''
    Checks if zcat or gzcat exist on the machine, returns whichever is functional!
    '''
    try:
        subprocess.run("zcat --help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        try:
            subprocess.run("gzcat --help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            raise Exception("Error when attempting to run zcat or gzcat command for k-mer counting.")
        else:
            return "gzcat"
    else:
        return "zcat"


def check_jellyfish():
    '''
    Checks if jellyfish is installed. Raises an exception if not.
    '''
    try:
        subprocess.check_output("jellyfish --help", shell=True)
    except subprocess.CalledProcessError:
        raise Exception("Jellyfish not found. Please install Jellyfish to count kmers.")


def try_command(command: str, err_msg: str):
    '''
    Runs and command and if there's an error, raises an exception with the provided error message.
    '''
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"{err_msg}{e}")

def handle_config_jellyfish(config: dict, list_of_input_file_paths: List[str] = []):
    '''
    Reads a TOML file and returns a list of the counts_files for the given list of input paths.

    Runs fastq_to_kmer_counts with custom parameters based on content of config file.

    If parsing the config file fails, exits the program.
    '''

    config_keys_valid_options = ["kmer_length", "hash_size", "threads"]

    args = {}
    # check if the 'jellyfish_args' section exists

    if 'jellyfish_args' in config:
        jellyfish_args = config['jellyfish_args']

        # iterate through the jellyfish_args section of the config file
        for key, value in jellyfish_args.items():

            if key not in config_keys_valid_options:
                # ignore invalid keys but let the user know there was one in the file
                raise Exception(f"Invalid key: '{key}' was found in the 'jellyfish_args' section of the config file.")
            elif value != "" and value is not None:
                # key and value are valid, add to args dictionary
                args[key] = value
        if args == {}:
            raise Exception("The 'jellyfish_args' section of the config file is empty.")
        
        # if the required args are not present in the config file and valid, exit the program
        if 'kmer_length' not in args:
            raise Exception("Kmer length is required. Please provide a value for this key in your config file.")

        if (type(args['kmer_length']) is not int) or args['kmer_length'] < 1:
            raise Exception("Kmer length value in config file must be a positive integer.")

    else:
        raise Exception("No 'jellyfish_args' section found in the config file.")

    
    parameters = set_up_parameters(args)
        
    # NOTE: output path is always ""
    return fastq_to_kmer_counts(list_of_input_file_paths, parameters['k'], "", parameters['threads'], parameters['hash_size'])


def set_up_parameters(args: dict):
    '''
    Sets up the arguments for the jellyfish command.
    '''
    arguments = {}

    k = args['kmer_length']
    arguments['k'] = k

    # check if the other values are present in the config file, if not use default values
    if args.get('threads') is not None:
        if (type(args['threads']) is not int) or args['threads'] < 1:
            raise Exception("Threads value in config file must be a positive integer.")
        else:
            threads = args['threads']
    else:
        print("Threads not found in config file. Using default value of 10.")
        threads = 10
    arguments['threads'] = threads

    if args.get("hash_size") is not None:
        if (type(args['hash_size']) is not int) or args['hash_size'] < 1:
            raise Exception("Hash size value in config file must be a positive integer.")
        else:
            hash_size = args['hash_size']
    else:
        print("Hash size not found in config file. Using default value of 100,000,000.")
        hash_size = 100_000_000

    arguments['hash_size'] = hash_size

    return arguments


def fastq_to_kmer_counts(
    file_paths: List[str],
    k: int,
    output_dir: str = "",
    threads: int = 10,
    hash_size: int = 100_000_000,
) -> str:
    """
    Takes a path to a 'fastq' or zipped `fastq.gz' file and uses Jellyfish
    to count the provided number of kmers of length 'k'.

    Returns the local path to the output counts file.
    """
    check_jellyfish()

    # Use the accession number as the base name
    if output_dir == "":
        base_path = f"{os.path.basename(file_paths[0].replace('_1', ''))}"
    else:
        base_path = f"{output_dir}/{os.path.basename(file_paths[0].replace('_1', ''))}"

    # Modify the file extension to .jf for the output
    jf_file = base_path.replace('.fastq', f'_{k}.jf').replace('.gz', '')

    # The base command for kmer counting
    count_command = f"jellyfish count -m {k} -s {hash_size} -C -t {threads} -o {jf_file}"

    # modifies the base command depending on if the files are zipped or not
    if file_paths[0].endswith('.fastq.gz'):
        zcat_command = get_zcat_command()
        count_command = f"cat {' '.join(file_paths)} | {zcat_command} | {count_command} /dev/fd/0"
    else:
        count_command = f"{count_command} {' '.join(file_paths)}"

    # Run count and dump jellyfish commands
    with Progress(*PROGBAR_COLUMNS) as progress:
        task = progress.add_task(f"Counting {k}-mers...", total=None)

        try_command(count_command, err_msg="Error running Jellyfish count: ")

        counts_file = jf_file.replace(".jf", ".counts")
        dump_command = f"jellyfish dump -c {jf_file} > {counts_file}"

        try_command(dump_command, err_msg="Error running Jellyfish dump: ")
        progress.update(task, total=1, advance=1)
    
    return counts_file