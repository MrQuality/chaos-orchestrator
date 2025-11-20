# chaos-orchestrator


This project is a chaos engineering orchestration tool designed to test the resilience of distributed systems.

## Overview

The `chaos-orchestrator` is an evolving suite of tools dedicated to chaos engineering, aimed at bolstering the resilience of distributed systems. Our initial focus is on foundational capabilities, such as comprehensively listing all pods within a designated Kubernetes namespace, providing the necessary visibility for targeted chaos experiments.

## Features

- List all pods within a designated Kubernetes namespace.

## Getting Started

### Prerequisites

- Python 3.x
- Kubernetes
- python-dotenv

### Installation

```bash
git clone https://github.com/your-org/chaos-orchestrator.git
cd chaos-orchestrator
```

### Usage

Run the script using Python:

```powershell
python.exe .\chaos.py
```

#### Example Output

```json
2025-11-19 18:17:18,942 - WARNING - SSL Verification disabled via KUBE_VERIFY_SSL. This is unsafe for production.
2025-11-19 18:17:18,942 - INFO - Starting Pod Enumeration Stream...
{"name": "coredns-64fd4b4794-p5cfq", "namespace": "kube-system", "ip": "10.42.0.31", "phase": "Running", "node": "k3s-chaos-02", "start_time": "2025-11-08 16:12:42+00:00"}
{"name": "helm-install-traefik-7rg9b", "namespace": "kube-system", "ip": null, "phase": "Succeeded", "node": "k3s-chaos-02", "start_time": "2025-11-08 16:12:41+00:00"}
{"name": "helm-install-traefik-crd-2j5qk", "namespace": "kube-system", "ip": null, "phase": "Succeeded", "node": "k3s-chaos-02", "start_time": "2025-11-08 16:12:41+00:00"}
{"name": "local-path-provisioner-774c6665dc-df5qn", "namespace": "kube-system", "ip": "10.42.0.30", "phase": "Running", "node": "k3s-chaos-02", "start_time": "2025-11-08 16:12:42+00:00"}
{"name": "metrics-server-7bffcd44-8jcj6", "namespace": "kube-system", "ip": "10.42.0.29", "phase": "Running", "node": "k3s-chaos-02", "start_time": "2025-11-08 16:12:42+00:00"}
{"name": "svclb-traefik-d2254c8b-57c7h", "namespace": "kube-system", "ip": "10.42.0.33", "phase": "Running", "node": "k3s-chaos-02", "start_time": "2025-11-08 16:13:46+00:00"}
{"name": "traefik-c98fdf6fb-v959x", "namespace": "kube-system", "ip": "10.42.0.32", "phase": "Running", "node": "k3s-chaos-02", "start_time": "2025-11-08 16:13:46+00:00"}
2025-11-19 18:17:18,988 - INFO - Stream complete. Processed 7 pods.
```

## Configuration

This project uses environment variables for configuration. You can set these variables directly in your shell or by creating a `.env` file in the project root.

- `KUBE_VERIFY_SSL`: Boolean value to disable SSL verification for Kubernetes API calls. Set to `False` to disable (e.g., for local development with self-signed certificates). Defaults to `True`.
- `KUBECONFIG`: Path to the kubeconfig file. If not set, the default kubeconfig path (`~/.kube/config`) is used.

Example `.env` file:

```
KUBE_VERIFY_SSL=False
KUBECONFIG=/path/to/your/kubeconfig
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue.

## License

MIT License
