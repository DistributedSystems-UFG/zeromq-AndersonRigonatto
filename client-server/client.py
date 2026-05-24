import sys

import zmq

PORT = 5555

OPERATIONS = [
    "ADD 3 4",
    "SUB 10 7",
    "MUL 5 6",
    "DIV 20 4",
    "DIV 10 0",
]


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 client.py <server-ip>")
        sys.exit(1)

    server_ip = sys.argv[1]

    ctx = zmq.Context()
    sock = ctx.socket(zmq.REQ)
    sock.connect(f"tcp://{server_ip}:{PORT}")
    print(f"Connected to tcp://{server_ip}:{PORT}")

    for op in OPERATIONS:
        print(f"Send : {op}")
        sock.send_string(op)
        reply = sock.recv_string()
        print(f"Reply: {reply}")

    sock.send_string("STOP")
    print(f"Stop reply: {sock.recv_string()}")


if __name__ == "__main__":
    main()
