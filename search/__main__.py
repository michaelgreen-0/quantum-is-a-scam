from search.searcher import Searcher
import argparse
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("list_to_search", help="List to search", nargs='+', type=int)
    parser.add_argument("element_to_find", help="Element to find", type=int)
    parser.add_argument(
        "--real", 
        help="Use a real quantum IBM instance instead of a local simulator",
        action="store_true",
        dest="use_real_device"
    )
    args = parser.parse_args()

    searcher = Searcher(
        list_to_search = args.list_to_search, 
        use_real_device=args.use_real_device
    )    

    start_classical = time.time()
    classical_result = searcher.classical_search(args.element_to_find)
    end_classical = time.time()
    print(f"Classical search found element at index: {classical_result}")
    print(f"Time: {(end_classical-start_classical):.6f} seconds")

    start_quantum = time.time()
    # For simplicity, we'll search for the binary representation of the index.
    # This is not a perfect comparison to the classical search, but demonstrates Grover's.
    num_qubits = (len(args.list_to_search)-1).bit_length()
    binary_index_to_find = format(args.list_to_search.index(args.element_to_find), f'0{num_qubits}b')
    
    quantum_result = searcher.grover_search(binary_index_to_find)
    end_quantum = time.time()
    
    print(f"Quantum search result: {quantum_result}")
    print(f"Time: {(end_quantum-start_quantum):.6f} seconds")
    searcher.plot_distribution(quantum_result)
    

if __name__ == "__main__":
    main()
