import os

from cutadapt.cli import main
from rich import progress as prog
from rich.progress import Progress

PROGBAR_COLUMNS = (
    prog.SpinnerColumn(),
    prog.TextColumn("[progress.description]{task.description}"),
    prog.BarColumn(),
    prog.TimeElapsedColumn()
)

def trim(input_file: list[str], config: dict):

    #Checks that the incoming list isn't empty
    if not input_file:
        raise Exception("No file names received from ENA download")
    
    #Checks that the file paths exist in the input_file list
    for files in input_file:
        if not os.path.isfile(files):
            raise Exception("Invalid files paths received from ENA download")
        

    command = []  # Initialize an empty list to hold the commands

    if len(input_file) == 2:
        command.append("--interleaved")
    
    
    arguments = config['cutadapt']
    
    # Iterate through each key and its associated list
    for key, value in arguments.items():
        if isinstance(value, list):
            for item in value:
                command.append(f"{key}")

                # Only append the item if it's not an empty string
                if item:
                    command.append(f"{item}")
        else:
            # Append the key
            command.append(f"{key}")

            # Check if value is not an empty list or empty string and append it
            if value not in ["", []]:
                command.append(f"{value}")
    
    if '-o' not in command:
        # Automatically generate the output file name by adding "_trimmed" before the extension
    
        name, ext = os.path.splitext(input_file[0])
        name, second_ext = os.path.splitext(name)
        name = name.rstrip("_1") #if there are 2 fastq files, will look at first file name, remove _1 from the end
        output_file= f"{name}_trimmed{second_ext}{ext}"
        command.append('-o')
        command.append(output_file)

    else:
        raise Exception("Can not create own output file name. Bulk runs will create only one file with that name. Please remove the -o flag in config file")

    for files in input_file:
        command.append(files)

    with Progress(*PROGBAR_COLUMNS) as progress:
        task = progress.add_task("Trimming with Cutadapt...", total=None)
        main(command)
        progress.update(task, total=1, advance=1)

    return output_file