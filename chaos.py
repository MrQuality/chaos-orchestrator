"""
Chaos Monkey - Pod Enumerator
=============================

A pragmatic utility to list Kubernetes pods in the kube-system namespace.
Designed for cross-platform execution (Windows Host / Linux Runner).

Architecture:
    - Connectivity: Uses standard kubeconfig with optional SSL bypass.
    - Pattern: Generator-based streaming for memory efficiency.
    - Output: NDJSON for observability integration.
"""

import os
import sys
import json
import logging
import warnings
from typing import Generator, Dict, Any

from dotenv import load_dotenv
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import urllib3

# Load environment variables from .env if present
load_dotenv()

# Configure Basic Logging (System messages go to stderr, Data goes to stdout)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # We send logs to stderr so they don't corrupt the JSON stdout stream
)
logger = logging.getLogger("ChaosMonkey")

def configure_cluster_access() -> None:
    """
    Loads the Kubernetes configuration and handles SSL verification settings.
    
    Strategy:
    1. Load config from KUBECONFIG env var or default location.
    2. Check KUBE_VERIFY_SSL to handle local dev vs CI security contexts.
    """
    try:
        # The load_kube_config helper automatically looks for KUBECONFIG env var
        config.load_kube_config()
        
        # SSL Verification Logic
        verify_ssl = os.getenv("KUBE_VERIFY_SSL", "True").lower() == "true"
        
        if not verify_ssl:
            logger.warning("SSL Verification disabled via KUBE_VERIFY_SSL. This is unsafe for production.")
            # Global disable for urllib3 to suppress the noisy warnings in stdout
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            # Hook into the configuration singleton to disable verification
            configuration = client.Configuration.get_default_copy()
            configuration.verify_ssl = False
            client.Configuration.set_default(configuration)
            
    except config.ConfigException as e:
        logger.error(f"Failed to load Kubernetes config: {e}")
        sys.exit(1)

def stream_pods(namespace: str = "kube-system") -> Generator[Dict[str, Any], None, None]:
    """
    Yields pod details one by one.
    
    Args:
        namespace: The target namespace to scan.
        
    Yields:
        Dict containing minimal pragmatic pod details.
    """
    v1 = client.CoreV1Api()
    
    try:
        # We use list_namespaced_pod. 
        # In a true 'chaos' scenario on massive clusters, we would add 
        # _preload_content=False and stream the raw socket, but for <10k pods
        # the standard iterator is sufficient and cleaner.
        pods = v1.list_namespaced_pod(namespace=namespace, watch=False)
        
        for pod in pods.items:
            # Pragmatic data extraction: only what we need for observability
            payload = {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "ip": pod.status.pod_ip,
                "phase": pod.status.phase,
                "node": pod.spec.node_name,
                "start_time": str(pod.status.start_time)
            }
            yield payload

    except ApiException as e:
        logger.error(f"Kubernetes API Exception: {e}")
        sys.exit(1)

def main():
    """Entry point for the chaos execution."""
    configure_cluster_access()
    
    logger.info("Starting Pod Enumeration Stream...")
    
    try:
        count = 0
        for pod_data in stream_pods():
            # Output Constraint: NDJSON
            # This writes to STDOUT, while our logs go to STDERR.
            # This allows tools like Filebeat/Fluentd to capture clean data.
            print(json.dumps(pod_data))
            count += 1
            
        logger.info(f"Stream complete. Processed {count} pods.")
        
    except KeyboardInterrupt:
        logger.info("Execution interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()