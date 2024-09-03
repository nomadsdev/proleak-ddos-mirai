# Pro Leak DDOS Mirai

Pro Leak DDOS Mirai is a collection of Python scripts inspired by the Mirai botnet, designed for educational purposes to demonstrate different types of Denial of Service (DoS) attacks. These scripts emulate various techniques used in large-scale botnets, sending floods of packets to a target IP to disrupt and overload services.

## Disclaimer

**This project is for educational purposes only.** Unauthorized use of these scripts against systems without permission is illegal and unethical. The author is not responsible for any misuse or damage caused by the use of this code.

## Features

- **Raw UDP Flood**: Floods the target with UDP packets using raw sockets to bypass certain network defenses.
- **SYN Flood**: Sends TCP SYN packets to initiate fake connections, overwhelming the target's resources.
- **ACK Flood**: Floods the target with TCP packets with the ACK flag set, which can bypass certain firewalls.
- **GRE IP Flood**: Sends GRE-encapsulated IP packets with random UDP payloads, targeting multiple IPs.
- **Configurable Attack Script**: Uses `all.py` with a configuration file (`attack_config.ini`) to easily manage and launch multiple attacks simultaneously.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nomadsdev/proleak-ddos-mirai.git
   cd proleak-ddos-mirai
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Some scripts may require elevated privileges to run (e.g., using `sudo` on Linux).

## Usage

### 1. Raw UDP Flood

The `raw_udp_flood.py` script sends UDP packets using raw sockets to the specified target.

```bash
python3 raw_udp_flood.py
```

### 2. SYN Flood

The `syn_flood.py` script sends TCP SYN packets to a specified target, aiming to exhaust the target's ability to manage incoming connections.

```bash
python3 syn_flood.py
```

### 3. ACK Flood

The `ack_flood.py` script sends TCP packets with the ACK flag set, which may pass through firewalls that only inspect connection initiation (SYN packets).

```bash
python3 ack_flood.py
```

### 4. GRE IP Flood

The `gre_ip_flood.py` script sends GRE-encapsulated IP packets to multiple target IPs, with random payloads to obscure the attack signature.

```bash
python3 gre_ip_flood.py
```

### 5. Configurable Attack with `all.py`

The `all.py` script allows you to configure and execute multiple types of attacks simultaneously using a configuration file (`attack_config.ini`).

#### Configuration

Create or edit the `attack_config.ini` file to specify the target details and which attacks to run. Below is an example configuration:

```ini
[Target]
ip = 192.168.1.1
port = 80

[Attacks]
raw_udp_flood = True
syn_flood = False
ack_flood = True
send_gre_ip_packets = False
```

- **Target Section**: Specify the target IP and port.
- **Attacks Section**: Enable or disable specific attack methods by setting their value to `True` or `False`.

#### Running the Configurable Attack Script

```bash
python3 all.py
```

This will execute the enabled attacks from the configuration file against the specified target.

## Code Overview

- **raw_udp_flood.py**: Implements a UDP flood attack using raw sockets.
- **syn_flood.py**: Executes a SYN flood attack to overwhelm TCP connections.
- **ack_flood.py**: Performs an ACK flood attack, typically bypassing basic firewall defenses.
- **gre_ip_flood.py**: Launches a GRE IP flood with encapsulated UDP payloads to multiple targets.
- **all.py**: Manages multiple attacks through a configuration file (`attack_config.ini`).

## Contributing

Contributions are welcome! If you have suggestions, improvements, or want to report issues, please submit a pull request or open an issue on the repository.
