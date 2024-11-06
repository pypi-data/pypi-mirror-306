import os
import requests
from ftplib import FTP
from typing import List

import rich.progress as prog
from rich.progress import Progress

PROGBAR_COLUMNS = (
    prog.SpinnerColumn(),
    prog.TextColumn("[progress.description]{task.description}"),
    prog.BarColumn(),
    prog.DownloadColumn(),
    prog.TaskProgressColumn(),
    prog.TimeElapsedColumn(),
)


def get_accessions_from_config(config: dict) -> List[str]:
    '''
    Reads a dictionary of the config and returns a list of accession numbers from the 'download_args' section.
    '''    
    if 'download_args' not in config:
        raise Exception("No 'download_args' section found in the config file.")

    arguments: dict = config['download_args']

    if 'accession_numbers' not in arguments:
        raise Exception("No 'accession_numbers' section found in 'download_args' in the config file.")
    
    accessions_arg = arguments['accession_numbers']

    if isinstance(accessions_arg, list):    
        if not all(isinstance(item, str) for item in accessions_arg):       
            raise Exception("Value for key 'accession_numbers' in config file must be a list of strings or a string.")

    # we know this will be a string format. we can check if it is a valid file path then parse throught the file
    elif isinstance(accessions_arg, str):
        if (accessions_arg != "" and os.path.exists(accessions_arg)):
            # extract accession numbers from file into a list and set it to accession_list_config
            with open(accessions_arg, 'r') as f:
                acc_nums = f.readlines()
            accessions_arg = [acc.strip() for acc in acc_nums]
        else:
            raise Exception("File path for accession_numbers is invalid or does not exist.")
    
    else:
        raise Exception("Value for key 'accession_numbers' in config file must be a list of strings or a string.")

    accessions = []

    for accession in accessions_arg:
        if accession[:3] == "PRJ":
            accessions.extend(get_project_accessions(accession))
        else:
            accessions.append(accession)

    if accessions == []:
        raise Exception("No accession numbers found in the config file.")
    
    return accessions


def get_project_accessions(prj_accession: str):
    url = f"https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=study_accession={prj_accession}&fields=run_accession"

    response = requests.get(url)

    content = response.content.decode()
    lines = content.splitlines()[1:] # ignore the header line
    return [line.split("\t")[0] for line in lines] # get the first value in a line (the accession)


def ena_download(accession: str, output_dir: str = None) -> List[str]:
    '''
    Downloads fastq.gz files from the ENA FTP server using an accession number. 
    Returns a list of the local file paths of the downloaded files.
    ''' 
    # small argument validations for the accession parameter
    if type(accession) is not str or not accession.isalnum():
        raise Exception(f"Invalid accession number {accession}. Please provide a valid accession number.")

    ftp = FTP('ftp.sra.ebi.ac.uk')
    try:
        ftp.login()

        prefix = accession[:6]
        suffix = accession[6:]

        directory = f'/vol1/fastq/{prefix}/'

        # handles different format of directory for accession numbers
        match len(suffix):
            case 3:
                directory += f'{accession}'
            case 4:
                directory += f"00{suffix[-1]}/{accession}"
            case 5:
                directory += f"0{suffix[-2:]}/{accession}"
            case _:
                raise Exception("Error creating download directory: Accession length is incorrect.")

        try:
            ftp.cwd(directory)
        except Exception:
            raise Exception(f"Failed to access the directory for the provided accession number of {accession}.\n"
                        "Please ensure that the accession number is correct and the corresponding\n"
                        "FASTQ files are available on ENA.")

        file_names = ftp.nlst()
        if (file_names == []):
            raise Exception(f"No files found for the given accession number of {accession}.")
        
        if (output_dir is not None):
            if not os.path.exists(output_dir):
                raise Exception("Output directory given for ENA downloading results does not exist.")

        output_files = []

        with Progress(*PROGBAR_COLUMNS) as progress:
            for file_name in file_names:
                size = ftp.size(f"{file_name}")
                task = progress.add_task(f"Downloading {file_name}", total=size)
                
                # build local file path
                if (output_dir is not None):
                    local_file_path = os.path.join(output_dir, file_name)
                else:
                    local_file_path = file_name

                output_files.append(local_file_path)
                
                # skip download if the entire file already exists
                if os.path.isfile(local_file_path) and os.path.getsize(local_file_path) == size:
                    progress.update(task, advance=size)
                    continue
                try:
                    with open(local_file_path, 'wb') as f:
        
                        def callback(data):
                            f.write(data)
                            progress.update(task, advance=len(data))

                        ftp.retrbinary(f"RETR {file_name}", callback)

                except Exception:
                    raise Exception(f"Download failed to complete for the given SRA accession number of {accession}.\n"
                                "Please ensure that the accession number is correct and the corresponding\n"
                                "FASTQ files are available on ENA, and try again.")
        return output_files
    finally:
        ftp.close()