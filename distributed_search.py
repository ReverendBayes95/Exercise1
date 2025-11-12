import string
from itertools import combinations

# Method 1: Using string module to get all printable characters
all_characters = string.ascii_letters + string.digits

def create_input_string(base_chars, length):
    
    if isinstance(base_chars, str):
        input_string = list(base_chars)
    else:
        input_string = base_chars.copy()

    def add_combinations(s, r):
        for i in combinations(base_chars, r):
            if len(s) >= length:  # Stop if we've reached desired length
                break
            s.append(''.join(i))
        return s

    choose = 2    
    while len(input_string) < length:
        input_string = add_combinations(input_string, choose)
        choose += 1

    if len(input_string) >= length:
        return input_string[:length]
    
def sequential_search(s, x):
    """A simple sequential search function.
    Args:
        s (str or list): The input string or list of characters to search through.
        x (any): The element to search for.
    Returns:
        int: 1 if found, 0 otherwise.
    """
    for i in range(len(s)):
        if s[i] == x:
            return 1
    return 0

def create_chunks(s, p):
    """Splits the string s into p chunks.
    Args:
        s (str or list): The input string or list of characters to split.
        p (int): The number of chunks to create.
        Returns:
            list: A list containing p chunks of the input string.
    """
    chunk_size = len(s) // p
    chunks = []
    for i in range(p):
        start_index = i * chunk_size
        if i == p - 1:  # Last chunk takes the remainder
            end_index = len(s)
        else:
            end_index = (i + 1) * chunk_size
        chunks.append(s[start_index:end_index])
    return chunks

def search_processor(args):
    """Worker function for parallel search that can be pickled."""
    chunk, target = args
    return sequential_search(chunk, target)

def parallel_search(s, x, p):
    """
    Performs a parallel search for element x in string s using p processes.
    Args:
        s (str or list): The input string or list of characters to search through.
        x (any): The element to search for.
        p (int): The number of parallel processes to use.

    Returns:
        int: 1 if found, 0 otherwise.
    """
    from concurrent.futures import ProcessPoolExecutor
    chunks = create_chunks(s, p)

    # Create arguments as (chunk, target) pairs
    processor_args = [(chunk, x) for chunk in chunks]

    with ProcessPoolExecutor(max_workers=p) as executor:
        results = list(executor.map(search_processor, processor_args))

    return 1 if any(results) else 0

if __name__ == '__main__':
    input_sequence = create_input_string(all_characters, 100000000)
    x = input_sequence[-1]

    import time

    # Time sequential search
    start = time.perf_counter()
    seq_result = sequential_search(input_sequence, x)
    seq_time = time.perf_counter() - start
    print(f"Sequential search time: {seq_time:.6f} seconds")

    # Time parallel search
    start = time.perf_counter()
    par_result = parallel_search(input_sequence, x, 4)
    par_time = time.perf_counter() - start
    print(f"Parallel search time: {par_time:.6f} seconds")

    # Calculate speedup
    if par_time > 0:
        speedup = seq_time / par_time
        print(f"Speedup: {speedup:.2f}x")