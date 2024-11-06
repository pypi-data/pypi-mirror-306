import os
import sys
from typing import Optional

import typer
from rich import print, panel

import pylagg.cgr_step as cgr_g
import pylagg.ena_download as ena_d
import pylagg.kmer_counting as kmer_c
import pylagg.config as config_p

app = typer.Typer()

def accession_to_cgr(accession: str, k: int, output_dir: str, threads: int, size : int):
    '''
    Takes an accession number and k-mer count and returns a CGR image
    '''
    files = ena_d.ena_download(accession, output_dir) 
    counts_path = kmer_c.fastq_to_kmer_counts(files, k, output_dir=output_dir, threads=threads)

    with open(counts_path, 'r') as f:
        cgr_g.count_file_to_image_file(f, counts_path.replace(".counts", ".png"), size = size)

@app.command()
def cgr(
    input: str = typer.Option(
        None,
        "--input",
        "-i",
        help = "File name if using k-mer input you already have. Must be a .txt file for a single image.",
    ),
    accession_number: str = typer.Option(
        None,
        "--accession-number",
        "-a",
        help = 'Generate an image using an NCBI database accession number. If you would like to use more than one accession number, please list them in quotation marks, separated by commas, or put them in a .txt file with one accession number per line, and input the file name with this flag.',
    ),
    kmer: int = typer.Option(
        10,
        "--kmer",
        "-k",
        help = "Specify your desired k-mer number (Only used when generating from an accession number, if your input is already in k-mer form it will be detected)."
    ),
    output_path: str = typer.Option(
        os.getcwd(),
        "--output-path",
        "-o",
        help="Use this to specify an alternate save location for your generated images. If nothing is specified, the default location is where the terminal is located.",
    ),
    size: Optional[int] = typer.Option(
        None,
        "--size",
        "-s",
        show_default=False,
        help = "Define an alternative side length for your image. Cannot exceed default value of 2^k.",
    ),
    thread_count: int = typer.Option(
        16,
        "--thread-count",
        "-t",
        help = "Amount of threads you wish to use. Threads are only used for k-mer counting when generating from an accession number.",
    ),
    config: str = typer.Option(
        None,
        "--config",
        "-c",
        help = "Use a config file to specify your options. Please include only an input (accession number(s) or kmer file(s)) and the config file's path. If any other options are also specified they will be ignored."
        ),
):
    """
    Generate your graph. Type "lagg cgr --help" to see all options for this command.
    """
    
    # INPUT ERROR CHECKING
    if input and accession_number:
        raise Exception("Please only include a file name OR an accession number(s).\nIf you need help, type 'lagg --help'.")
    # NOTE: melanie edited this to include config. pls change if you want a diff logic here @ollie!
    if not (input or accession_number or config):
        raise Exception("Please include an input, either an accession number(s), the name of a file containing k-mer input(s), or a config file path.\nIf you need help, type 'lagg --help'.")
    if size and (size > 2**kmer or size < 1):
        raise Exception("Your size is invalid. Please check and try again. Size cannot exceed 2^k, or be less than 1.\nIf you need help, type 'lagg --help'.")
    if kmer <= 0:
        raise Exception("Invalid k-mer count. Please use a k-mer count greater than 0. \nIf you need help, type 'lagg --help'.")
    if not(os.path.exists(output_path)):
        raise Exception("The given output path does not exist. Please double check your path and try again. \nIf you need help, type 'lagg --help'.")
    if input and not (os.path.exists(input)):
        raise Exception("The input file name is invalid or does not exist. Please make sure your file name includes either '.txt'\nIf you need help, type 'lagg --help'.")
    if input and not((input.rfind(".txt") != -1)):
        raise Exception("The input is not a supported file type. Supported types are '.txt'. Please convert to a supported file type and try again.\nIf you need help, type 'lagg --help'.")
        
    # END INPUT ERROR CHECKING

    # If output_path is different form current directory, changes directory to the directory of the output files. Allows the program to 
    # work with the files in that directory
    # There was an error message for if the directory doesn't exist
    if output_path != os.getcwd():
        os.chdir(output_path)
    
    #if no size is specified we need a default, and since it relies on other parameters it has to be done here.
    if not size:
        size = 2**kmer
    
    # Pre Process Accession number
    if config:
        config_p.config_accession_to_cgr(config)

    elif accession_number:

        #remove white spaces
        accession_number = accession_number.replace(" ", "")
        
        accession_list = accession_number.split(",")
        
        if(accession_number.rfind(".txt") != -1):
            raise Exception("detecting .txt of accession numbers (not implemented)")
        
        # Image generation with accession number:
        #print("Image generation with accession number not yet implemented")
        for number in accession_list:
            accession_to_cgr(number, kmer, output_path, thread_count, size)
        
    elif input:
        
        counts_file_path = input
        with open(counts_file_path) as f:
            
            # .txt case
            if(input.rfind(".txt") != -1):
                    input = input.replace(".txt", "")
                    
                    #if input.rfind("/") != -1:
                    inputname = input[input.rfind("/") + 1:]
                    
                    cgr_g.count_file_to_image_file(f, output_path + "/" + inputname + ".png", size=size)
                    print("\nSuccessfully created image called '" + inputname + ".png' at " + output_path)
            else:
                #this should never be hit since it's checked above...but just in case
                print("Error with file type")
    else:
        raise Exception("No valid flag. Please use either -a or -i or -c")
 
@app.command()               
def ena(
    accession_number: str = typer.Option(
        None,
        "--accession-number",
        "-a",
        help = 'Download a fastq file using an NCBI database accession number. If you would like to use more than one accession number, please list them in quotation marks, separated by commas, or put them in a .txt file with one accession number per line, and input the file name with this flag.',
    ),
    kmer: bool = typer.Option(
        False,
        "--kmer",
        "-k",
        help = "If you would also like your download to be k-mer counted. By default, will not k-mer count."
    ),
    kmer_k_value: int = typer.Option(
        10,
        "--kmer-kvalue",
        "-v",
        help = "Specify your desired k-mer k value, if you want k-mer counting."
    ),
    output_path: str = typer.Option(
        os.getcwd(),
        "--output-path",
        "-o",
        help="Use this to specify an alternate save location for your downloaded files (and k-mer count files, if generating). If nothing is specified, the default location is where the terminal is located.",
    ),
    thread_count: int = typer.Option(
        16,
        "--thread-count",
        "-t",
        help = "Amount of threads you wish to use. Threads are only used for k-mer counting.",
    ),
):
    """
    Only download a fastq file from ENA without generating a graph, and optionally k-mer count it too!
    """
    
    accession_number = accession_number.replace(" ", "")
        
    accession_list = accession_number.split(",")
        
    if(accession_number.rfind(".txt") != -1):
        raise Exception("detecting .txt of accession numbers (not implemented)")
    
    for number in accession_list:  
        files = ena_d.ena_download(number, output_path)
    
        if kmer:
            print(files)
            kmer_c.fastq_to_kmer_counts(files, kmer_k_value, output_path, thread_count)
            print("Successfully downloaded and created k-mer counts at " + output_path)
        else:
            print("Successfully downloaded file(s) at " + output_path)
            
@app.command()
def jellyfish(
    input_fastq: str = typer.Option(
        None,
        "--input-fastq",
        "-i",
        help = 'Convert a fastq file you already have downloaded. Input the file path and name using this flag.',
    ),
    kmer_k_value: int = typer.Option(
        10,
        "--kmer-kvalue",
        "-v",
        help = "Specify your desired k-mer k value."
    ),
    output_path: str = typer.Option(
        os.getcwd(),
        "--output-path",
        "-o",
        help="Use this to specify an alternate save location for your k-mer count files. If nothing is specified, the default location is where the terminal is located.",
    ),
    thread_count: int = typer.Option(
        16,
        "--thread-count",
        "-t",
        help = "Amount of threads you wish to use for your kmer counting.",
    ),
    ):
    """
    Generate a k-mer count from a fastq file already downloaded on your computer!
    """
    
    kmer_c.fastq_to_kmer_counts([input_fastq], kmer_k_value, output_path, thread_count)


def cli():
    try:
        app()
    except Exception as e:
        print(panel.Panel(f"{e}", title="[red]Error", title_align="left", border_style="red"))
        sys.exit()
