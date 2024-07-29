from router import Router

def setup_network():
    # Define enrutadores y sus vecinos
    r1 = Router('R1', 5001, [5002, 5003])
    r2 = Router('R2', 5002, [5001, 5003])
    r3 = Router('R3', 5003, [5001, 5002])

    r1.start()
    r2.start()
    r3.start()

if __name__ == "__main__":
    setup_network()
