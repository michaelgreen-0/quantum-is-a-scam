from .factorer import Factorer
import argparse
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("number_to_factor", help="Number to factor", type=int)
    parser.add_argument(
        "--real", 
        help="Use a real quantum IBM instance instead of a local simulator",
        action="store_true",
        dest="use_real_device"
    )
    args = parser.parse_args()

    factorer = Factorer(
        N = args.number_to_factor, 
        use_real_device=args.use_real_device
    )    

    start_classical = time.time()
    p_classical, q_classical = factorer.classical_factor()
    end_classical = time.time()
    print(f"Classical Factors: {p_classical}, {q_classical}")
    print(f"Time: {(end_classical-start_classical):.6f} seconds")

    start_quantum = time.time()
    for i in range(5):
        p_q, q_q = factorer.shor_factor()
        if p_q and q_q and p_q * q_q == args.number_to_factor:
            found_factors = 1
            break
    end_quantum = time.time()
    if found_factors:
        print(f"Quantum Factors: {p_q}, {q_q}")
        print(f"Time: {(end_quantum-start_quantum):.6f} seconds")
    

if __name__ == "__main__":
    main()
