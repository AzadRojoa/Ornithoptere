from antenne import Antenne
import time

antenne = Antenne(mode='recepteur')
received = []
start_time = None

NB_MESSAGES = 1000

def recevoir_benchmark():
    global start_time
    count = 0
    while count < NB_MESSAGES:
        message = antenne.receive()
        if message and message.startswith("BENCHMARK;"):
            parts = message.split(";")
            idx = int(parts[1])
            sent_ts = float(parts[2])
            recv_ts = time.time()
            latency = recv_ts - sent_ts
            if start_time is None:
                start_time = recv_ts
            received.append((idx, sent_ts, recv_ts, latency))
            count += 1
    end_time = time.time()
    duration = end_time - start_time if start_time else 0
    throughput = NB_MESSAGES / duration if duration > 0 else 0
    avg_latency = sum(r[3] for r in received) / len(received)
    with open("benchmark_receiver_results.txt", "w") as f:
        f.write(f"Total messages: {NB_MESSAGES}\n")
        f.write(f"Duration: {duration:.6f} s\n")
        f.write(f"Throughput: {throughput:.2f} msg/s\n")
        f.write(f"Average latency: {avg_latency:.6f} s\n")
        for r in received:
            f.write(f"{r[0]},{r[1]},{r[2]},{r[3]}\n")

if __name__ == "__main__":
    recevoir_benchmark()
