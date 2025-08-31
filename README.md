# Mini-SOC — Wazuh on Docker Swarm

## Project Overview
This repository implements a **Mini Security Operations Center (Mini-SOC)** using **Wazuh** on Docker Swarm.  
The project automates deployment, testing, and basic monitoring of Wazuh components, providing a foundation for learning and experimentation with SOC tools.

## Architecture
- **VM1 (Manager)**: Swarm manager, Ansible controller, GitHub Actions self-hosted runner, and edge Traefik (ingress).  
- **VM2 (Worker)**: Runs Wazuh services (Indexer, Manager, Dashboard) and persistent volumes for storage.  

**Networks:**
- `public`: Overlay network for dashboard and ingress exposure (Traefik).  
- `internal`: Overlay network for internal Wazuh communication (Indexer ↔ Manager).

## Project Structure
stack/ # Docker Swarm stack definitions for Wazuh
ansible/ # Playbooks and inventory for deployment and teardown
.github/workflows/ # CI/CD workflow: Trivy scan, Selenium/API tests, deployment
trivy/ # Example Trivy configuration and policies
tests/ # Automated tests (Selenium + API)
security/ # TLS & policy placeholders (no private keys stored)
README.md # Project overview and instructions


### Key Components
- **Wazuh Stack**: Indexer, Manager, Dashboard (deployed via `docker stack`).  
- **Ansible Playbooks**:
  - `deploy.yml`: Deploys Wazuh stack.
  - `teardown.yml`: Removes stack and cleans up resources.  
- **CI/CD**: GitHub Actions pipeline performs image scanning, testing, and deployment.  
- **Tests**: Selenium and API healthchecks ensure stack functionality.  

## Notes on Secrets & TLS
- **Do not commit sensitive data** (passwords, API keys, TLS private keys). Use:
  - GitHub Actions Secrets
  - Ansible Vault
  - Optional: HashiCorp Vault or SOPS  
- TLS is handled via edge-traefik. Self-signed certificates may trigger browser warnings in local labs.

## Achievements
- Docker Swarm cluster set up (1 manager, 1 worker).  
- Wazuh stack successfully deployed and automated with Ansible.  
- CI/CD workflow integrated with Trivy, Selenium, and API tests.  
- Persistent storage for Indexer and Manager implemented.  

## Known Issues
- **Indexer Stability**: Intermittent exits due to kernel/sysctl limitations (`vm.max_map_count`).  
- **Dashboard Availability**: May be temporarily unreachable if the Indexer is not fully initialized.  
- **TLS Warnings**: Self-signed or lab certificates trigger browser warnings.

## Quick Start (Manager VM)
```bash
# Create overlay networks (if not present)
docker network create -d overlay --attachable public || true
docker network create -d overlay --attachable internal || true

# Deploy Wazuh stack
docker stack deploy -c stack/wazuh-stack.yml wazuh

# Check services and logs
docker stack ps wazuh
docker service logs wazuh_wazuh_indexer --tail 100 -f

