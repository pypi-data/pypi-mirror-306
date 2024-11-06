from typing import Tuple
from io import BytesIO, TextIOWrapper
import math

import numpy as np
import PIL.Image as im
import rich.progress as prog
from rich.progress import Progress


PROGBAR_COLUMNS = (
    prog.SpinnerColumn(),
    prog.TextColumn("[progress.description]{task.description}"),
    prog.BarColumn(),
    prog.TaskProgressColumn(),
    prog.TimeElapsedColumn(),
)


def contains_valid_characters(input_string: str) -> bool:
    """Checks if the given string contains only valid nucleotides characters.

    Args:
        input_string (str): The string to check for validity.

    Returns:
        bool: Returns true if and only if all characters in the input string are either 'A', 'T', 'C', or 'G'.
    """
    for char in input_string:
        if char not in {"A", "T", "C", "G"}:
            return False

    return True


def parse_count_file_line(line: str, k: int) -> Tuple[str, int]:
    """Reads a single line in a counts file and returns a parsed tuple in the form of (kmer, count)

    Args:
        line (str): The string of the line to parse
        k (int): The expected k-mer length

    Returns:
        Tuple[str, int]: A (str, int) tuple of the parsed line in the form of (kmer, count)
    """
    line_split = line.split()
    kmer = line_split[0]

    if k > 0 and len(kmer) != k:
        raise Exception(f"The k-mer {kmer} does not match the reported length k={k}.")

    if not contains_valid_characters(kmer):
        raise Exception(
            f"Invalid k-mer character in k-mer {kmer} (valid characters are A, T, C, G)"
        )

    try:
        count = line_split[1]

        if count == "" or count.isspace():
            raise Exception()
    except Exception:
        raise Exception(f"Count not provided for k-mer: '{kmer}'")

    try:
        count = int(count)
    except ValueError:
        raise Exception(f"Count for k-mer {kmer} must be an integer'")

    if count < 1:
        raise Exception("All k-mer counts must be ≥1")

    return (kmer, count)


def calculate_pos(
    kmer: str, size: int, corner_labels: Tuple[str, str, str, str]
) -> Tuple[int, int]:
    """Returns the pixel position (x, y) of a k-mer in a CGR image with a given image size

    Args:
        kmer (str): The k-mer as a string
        size (int): The side length (in pixels) of the square image
        corner_labels (Tuple[str, str, str, str]): The labels for the corners of the image (as defined in CGR algorithm)

    Returns:
        Tuple[int, int]: A tuple representing the (x, y) pixel position of the k-mer in the image
    """

    x, y = 0, 0

    # use bit shifting instead of division to avoid floating point values
    offset = size >> 1

    bot_left, _, top_right, bot_right = corner_labels

    for base in reversed(kmer):
        if base == top_right or base == bot_right:
            x += offset

        if base == bot_left or base == bot_right:
            y += offset

        offset >>= 1

    return (x, y)


def generate_image_arr(
    counts_file: TextIOWrapper, verbose=True, size=None, log10=True, normalized=True
) -> np.ndarray:
    """Generates a numpy array representing an image covering RGB channels

    Args:
        input_data (TextIOWrapper): An open k-mer counts file
        verbose (bool, optional): Whether to print a progress bar to the console. Defaults to True.
        size (_type_, optional): The side length (in pixels) of the generated square image. Defaults to None.
        log10 (bool, optional): Whether to take the logarithm of each pixel value. Defaults to True.
        normalized (bool, optional): Whether to normalize all pixels after generating the image. Defaults to True.

    Returns:
        np.ndarray: _description_
    """

    with counts_file:
        counts_file.seek(0)

        (first_kmer, _) = parse_count_file_line(counts_file.readline(), 0)
        k = len(first_kmer)

        num_lines = sum(1 for _ in counts_file) + 1

        counts_file.seek(0)

        if size is None:
            size = 2**k

        r = np.zeros((size, size))
        g = np.zeros((size, size))
        b = np.zeros((size, size))

        with Progress(*PROGBAR_COLUMNS, disable=not verbose) as progress:
            task = progress.add_task("Generating image...\n", total=num_lines)

            for line in counts_file:
                (kmer, count) = parse_count_file_line(line, k)

                if log10:
                    count = math.log10(count)

                # weak H-bonds W = {A, T} and strong H-bonds S = {G, C} on the diagonals
                r_pos = calculate_pos(kmer, size, ("A", "G", "T", "C"))
                r[r_pos] = count

                # purine R = {A, G} and pyrimidine Y = {C, T} on the diagonals
                g_pos = calculate_pos(kmer, size, ("A", "T", "G", "C"))
                g[g_pos] = count

                # amino group M = {A, C} and keto group K = {G, T} on the diagonals
                b_pos = calculate_pos(kmer, size, ("A", "T", "C", "G"))
                b[b_pos] = count

                progress.advance(task, advance=1)

        rgb = np.dstack((r, g, b))

        if normalized:
            rgb = rgb / np.max(rgb)

        return (rgb * 255).astype(np.uint8)


def count_file_to_image(input_data: TextIOWrapper, verbose=True, **kwargs) -> im.Image:
    """
    Takes an open counts file and returns a generated image in the form of a PIL image object

    Args:
        input_data (TextIOWrapper): An open k-mer counts file
        verbose (bool, optional): Whether to print a progress bar to the console. Defaults to True.
        **kwargs: Addition keyword arguments can be provided as refernced in the generate_image_arr function.

    Returns:
        im.Image: The resulting image object
    """

    chaos = generate_image_arr(input_data, verbose, **kwargs)
    return im.fromarray(chaos)


def count_file_to_image_file(
    input_data: TextIOWrapper,
    output_file: str | BytesIO,
    output_type="png",
    verbose=True,
    **kwargs,
):
    """
    Takes an open counts file and creates an image at the provided file path or buffer.

    Args:
        input_data (TextIOWrapper): An open k-mer counts file
        output_file (str | BytesIO): The path to the image output file or the bytes buffer
        output_type (str, optional): The file type of the output image. Defaults to "png".
        verbose (bool, optional): Whether to print a progress bar to the console. Defaults to True.
        **kwargs: Addition keyword arguments can be provided as refernced in the generate_image_arr function.
    """

    img = count_file_to_image(input_data, verbose, **kwargs)
    img.save(output_file, output_type)


def config_count_file_to_image_file(
    input_data: TextIOWrapper,
    output_file: str | BytesIO,
    config: dict,
    output_type="png",
    verbose=True,
):
    """
    Takes an opened counts file and creates an image at the provided file path or buffer with the given output file type.
    Attempts to use config for further kwargs in the count_file_to_image function.

    Args:
        input_data (TextIOWrapper): An open k-mer counts file
        output_file (str | BytesIO): The path to the image output file or the bytes buffer
        config (dict): the dictionary containing the options from a config file
        output_type (str, optional): The file type of the output image. Defaults to "png".
        verbose (bool, optional): Whether to print a progress bar to the console. Defaults to True.
    """

    config_size = config.get("cgr", {}).get("size", None)
    config_log = config.get("cgr", {}).get("log10", True)
    config_normalized = config.get("cgr", {}).get("normalized", True)

    img = count_file_to_image(
        input_data,
        verbose,
        size=config_size,
        log10=config_log,
        normalized=config_normalized,
    )
    img.save(output_file, output_type)
