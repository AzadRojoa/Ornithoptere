from antenne import Antenne
import time

NB_MESSAGES = 1000
antenne = Antenne(mode='emetteur')

results = []

def envoyer_benchmark():
    for i in range(NB_MESSAGES):
        timestamp = time.time()
        message = f"BENCHMARK;{i};{timestamp}".encode('utf-8')
        t0 = time.time()
        success = antenne.send(message)
        t1 = time.time()
        results.append((i, timestamp, t1 - t0, success))
        time.sleep(0.005)  # pour éviter la saturation

    with open("benchmark_sender_results.txt", "w") as f:
        for r in results:
            f.write(f"{r[0]},{r[1]},{r[2]},{r[3]}\n")

if __name__ == "__main__":
    envoyer_benchmark()
