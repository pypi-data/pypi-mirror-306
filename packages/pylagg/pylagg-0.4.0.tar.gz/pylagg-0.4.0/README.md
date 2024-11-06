# LAGG
Looking at Genomes Graphically (LAGG) is a CLI tool for creating images from DNA sequences.

LAGG is capable of generating an image providing just an SRA (or ENA) accession number and a k-mer count. Of course, the CLI contains more options and even a config-based workflow for more complex processes.

Images are generated using an algorithm based on Chaos Game Representation[^1] (CGR). This process creates images by counting k-mers for a genome / DNA sequence. With genomes aquired from the European Nucleotide Archive (ENA). Options are available to use Cutadapt[^3] to preprocess the genomes before counting.

## Installation
LAGG makes use of Jellyfish[^2] as a dependency for k-mer counting. Installation instructions can be found on the GitHub page for Jellyfish found [here](https://github.com/gmarcais/Jellyfish). Jellyfish is commonly available on major Linux distributions and on Homebrew for MacOS.

After installing dependencies, install LAGG using pip with the following command:
```
pip install pylagg
```

## Usage
Using LAGG is as simple as executing the `lagg` command.

For example, to generate an image from an SRA or ENA accession number:
```
lagg cgr -a <accession> -k <kmer size>
```

Replace `<accession>` with any accession number (try ERR4770013 for a small COVID-19 genome)

The `<kmer_size>` is an integer used when counting kmers which can eventually determine the size of the image. For larger genomes, consider a size of 9-10. For smaller ones, consider 5-8.

For more options or help type `'lagg --help` or visit the documentation site [here](https://laggfront.onrender.com).

## For Contributors
This project uses [Poetry](https://python-poetry.org) to handle dependencies and build the project.
Installation instructions can be found [here](https://python-poetry.org/docs/#installation).

### Install Dependencies
Similar to the CLI, Jellyfish is required to execute k-mer counting for LAGG. Please make sure to have to it installed before continuing. Instructions can be found in the "Installation" section above.

For project dependencies, use `poetry install` to automatically create a new virtual environment with all required packages.

If you'd like to install the dependencies directly within the project directory, use the following command:
```
poetry config virtualenvs.in-project true
```

### Running Tests
To run tests, first, activate the virtual environment using `poetry shell`.

Use `pytest` to run all tests.


[^1]: H. Joel. Jeffrey, “Chaos game representation of gene structure,” Nucleic Acids Research, vol. 18, no. 8, pp. 2163–2170, 1990, doi: https://doi.org/10.1093/nar/18.8.2163.

[^2]: G. Marçais and C. Kingsford, “A fast, lock-free approach for efficient parallel counting of occurrences of k-mers,” Bioinformatics, vol. 27, no. 6, pp. 764–770, Jan. 2011, doi: https://doi.org/10.1093/bioinformatics/btr011.

[^3]: Martin, Marcel. “Cutadapt Removes Adapter Sequences from High-Throughput Sequencing Reads.” EMBnet.journal, vol. 17, no. 1, 2 May 2011, p. 10, journal.embnet.org/index.php/embnetjournal/article/view/200, https://doi.org/10.14806/ej.17.1.200.