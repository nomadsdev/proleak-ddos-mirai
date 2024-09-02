# Pro Leak DDOS Mirai

Pro Leak DDOS Mirai is a collection of Python scripts designed for educational purposes to demonstrate different types of Denial of Service (DoS) attacks. Inspired by the infamous Mirai botnet, these scripts showcase various techniques for sending a flood of packets to a target IP to overload and disrupt the service.

## Disclaimer

**This project is for educational purposes only.** Misuse of this code can lead to criminal charges brought against the persons in question. The author will not be held responsible for any illegal activities caused by the use of these scripts.

## Features

- **ACK Flood**: A script that sends TCP packets with the ACK flag set to a target IP and port.
- **GRE IP Flood**: A script that sends GRE-encapsulated IP packets with random payloads to multiple target IPs.
- **SYN Flood**: A script that sends TCP SYN packets to a target IP and port, attempting to initiate many connections to overwhelm the target.
- **UDP Flood**: A script that sends UDP packets with random payloads to a target IP and port.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nomadsdev/proleak-ddos-mirai.git
   cd proleak-ddos-mirai
   ```

2. Install dependencies:

   ```bash
   pip install scapy
   ```

3. (Optional) Run scripts as a superuser/administrator if necessary (for example, using `sudo` on Linux).

## Usage

### 1. ACK Flood

The `attack_ack.py` script sends TCP packets with the ACK flag set to a specified target.

```bash
python3 attack_ack.py
```

### 2. GRE IP Flood

The `attack_gre.py` script sends GRE-encapsulated IP packets to multiple targets with random UDP payloads.

```bash
python3 attack_gre.py
```

### 3. SYN Flood

The `attack_syn.py` script sends TCP SYN packets to a specified target, trying to overwhelm the target's ability to handle incoming connections.

```bash
python3 attack_syn.py
```

### 4. UDP Flood

The `attack_udp.py` script sends a flood of UDP packets with random source IP addresses to a specified target.

```bash
python3 attack_udp.py
```

## Scripts Overview

- **attack_ack.py**: Script to perform ACK Flood attacks.
- **attack_gre.py**: Script to perform GRE IP Flood attacks.
- **attack_syn.py**: Script to perform SYN Flood attacks.
- **attack_udp.py**: Script to perform UDP Flood attacks.

## Contributing

If you have any suggestions or improvements, feel free to create a pull request or open an issue.

## License

This project is licensed under the MIT License.
