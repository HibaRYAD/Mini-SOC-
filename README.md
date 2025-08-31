# Mini-SOC — Wazuh on Docker Swarm (Mini SOC Project)

## Project summary
This repository contains a Mini Security Operations Center (Mini-SOC) implementation that deploys **Wazuh** (Indexer, Manager, Dashboard) on a **Docker Swarm** cluster, with CI/CD integration (GitHub Actions self-hosted runner), security scanning (Trivy), automated deployment (Ansible), and automated smoke tests (Selenium + API health checks).

## Architecture (high level)
- **VM1 (Manager)** — Swarm manager, Ansible controller, GitHub Actions self-hosted runner, edge Traefik (ingress).
- **VM2 (Worker)** — Runs Wazuh services (Indexer / Manager / Dashboard), persistent volumes for indexes and manager data.
- **Optional VM3 (Attacker for Part 2)** — Kali Linux to generate test malicious traffic.

Network:
- `public` overlay network: for ingress and dashboard exposure (Traefik).
- `internal` overlay network: for Wazuh internal communication (indexer, manager).

## What is included (implemented files & features)
- `stack/wazuh-stack.yml` — Docker Swarm stack definition for Wazuh (Indexer, Manager, Dashboard). Uses Wazuh images `4.9.2`. Dashboard is labelled for existing `edge-traefik` ingress.
- `ansible/`:
  - `inventories/hosts.yml` — sample inventory for manager and worker nodes.
  - `playbooks/deploy.yml` — Ansible playbook to copy stack files and deploy the Wazuh stack.
  - `playbooks/teardown.yml` — Ansible playbook to remove the stack.
- `.github/workflows/ci.yml` — CI/CD pipeline:
  - Trivy scans (config & image policy checks).
  - Tests (Selenium & API) on `ubuntu-latest`.
  - Deploy via Ansible on a `self-hosted` runner (runs only on `main` branch).
- `trivy/trivy-scan.yml` — example Trivy scan configuration (fail on HIGH/CRITICAL).
- `tests/selenium/` — Selenium smoke test and requirements.
- `tests/api/` — API healthcheck test.
- `security/` — placeholders for TLS and policy docs (do not store private keys in the repo).
- `README.md` — project overview and implemented components.

## Notes about secrets & TLS
- **Do not commit secrets** (admin passwords, TLS private keys, API keys). Use:
  - GitHub Actions Encrypted Secrets + Ansible to create Swarm secrets, or
  - Ansible Vault for local group_vars, or
  - HashiCorp Vault / SOPS (optional).
- TLS for the dashboard is served by the existing `edge-traefik` in the Swarm. For local labs, `wazuh.lab` or a similar host can be mapped in the local `/etc/hosts`. Self-signed certs are acceptable for lab use; Let’s Encrypt / ACME must be used with public DNS.

## What was done (implemented)
- Docker Swarm cluster brought up (1 manager, 1 worker).
- Wazuh stack deployed (Indexer, Manager, Dashboard) via `docker stack`.
- Ansible playbooks created to automate deployment and teardown.
- GitHub Actions workflow added (Trivy scan, tests, deploy).
- Selenium and API tests implemented and included.
- Trivy policy file included as example.
- `edge-traefik` considered and dashboard labeled for ingress.

## Current issues observed (as of latest test runs)
- **Indexer intermittent exits**: some indexer tasks initially failed with kernel/sysctl-related errors (`vm.max_map_count`), which were fixed by setting `vm.max_map_count=262144` on the worker host. Other transient `task: non-zero exit (1)` errors were observed indicating occasional container restarts; logs must be reviewed per failure to identify root cause.
- **Dashboard reachability**: dashboard may not be consistently reachable if the Indexer is not stabilized; when Indexer is running, the Dashboard service can still show transient task failures but typically a replica runs successfully.
- **Local TLS**: lab uses self-signed certificates or edge-traefik; browsers will warn on first load. Let’s Encrypt is not configured for local private IPs.

## How to run (manual commands examples)
> These commands are examples; adapt paths and host IPs as required.

On manager (VM1):
```bash
# ensure overlay networks exist
docker network create -d overlay --attachable public || true
docker network create -d overlay --attachable internal || true

# deploy stack (stack file is in repo)
docker stack deploy -c stack/wazuh-stack.yml wazuh

# check services
docker stack ps wazuh
docker service logs wazuh_wazuh_indexer --tail 100 -f

