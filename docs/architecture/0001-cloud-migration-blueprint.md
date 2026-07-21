# Warlock-Agents: Production-Grade Architectural Blueprint
## Cloud-Native, $0-Cost Portfolio Showcase Engineering Plan

---

## Task ID Reference Matrix

| ID Format | Sub-Code | Domain | Covers |
|-----------|----------|--------|--------|
| **P1-G**n | G = GitHub | GitHub API & Credentials | PAT provisioning, GraphQL node discovery |
| **P1-R**n | R = Repository | Git Hygiene & Standards | Repo restructuring, branch taxonomy, commit conventions |
| **P1-T**n | T = Testing | Test Architecture | Offline-first pytest suite, mocking strategy |
| **P1-B**n | B = Board | Project Board | GitHub Project v2 automation setup |
| **P2-T**n | T = Terraform | IaC Declarations | All `infra/` blocks: state, variables, resources, outputs |
| **P3-D**n | D = Docker | Container & Pipeline | Dockerfile layers, Cloud Build YAML pipeline, GitHub trigger |
| **P4-N**n | N = Network/NoSQL | Transport & Data | FastMCP HTTP transport, Firestore schema, storage strategy |
| **P5-A**n | A = Automation | Routing & Scripts | GitHub sync scripts, domain ingress, CLI proxy config |

> **Format:** `P{phase}-{sub-code}{sequence}` — e.g., `P2-T3` = Phase 2 · Terraform group · 3rd task

---

## Phase 1: Workspace Strategy, Git Hygiene, & Isolated Testing

- [x] **[P1-G1] Provision Fine-Grained GitHub Organization PAT**
  Configure a Fine-Grained Personal Access Token (PAT) under your GitHub profile settings to authorize your automated agent toolchain to manage organization-level artifacts.
  * **Scope Allocations:** Set Repository permissions for `Issues` and `Metadata` to **Read & Write** across your target portfolio repositories (`flag-ship`, `warlock-agents`).
  * **Organization Permissions:** Grant **Read & Write** capabilities for `Organization programmatic planning boards` (or `Projects`) explicitly within the `Works-by-Worrell` organization boundary.
  * **Local Environment Bootstrap:** Export the generated secret into your local shell profile to clear credential boundaries for your automated agent runtime session:
    ```bash
    export GH_TOKEN="github_pat_your_secure_token_here"
    ```

- [x] **[P1-G2] Extract Target Project v2 Node IDs via GraphQL API**
  Execute asynchronous network lookups against GitHub’s GraphQL endpoint using the pre-authenticated GitHub CLI (`gh`) to harvest the immutable node identity hashes required by your CLI agent for card placement.
  * **Project Node Discovery:** Query the organization layer to isolate the unique global identifier for your target board instance:
    ```bash
    gh api graphql -f query='
      query {
        organization(login: "Works-by-Worrell") {
          projectV2(number: 1) {
            id
            title
          }
        }
      }'
    ```
  * **Status Column Option Extraction:** Use the retrieved Project Node ID hash to extract the explicit single-select option IDs assigned to your Kanban columns (`Backlog`, `In Flight`, `Completed`):
    ```bash
    gh api graphql -f query='
      query {
        node(id: "PROJECT_NODE_ID_FROM_STEP_1") {
          ... on ProjectV2 {
            fields(first: 20) {
              nodes {
                ... on ProjectV2SingleSelectField {
                  id
                  name
                  options {
                    id
                    name
                  }
                }
              }
            }
          }
        }
      }'
    ```

- [x] **[P1-G3] Create Works-by-Worrell GitHub Pages Organization Site**
  Initialize the public-facing portfolio landing page by creating and enabling a GitHub Pages site at the organization level. This serves as the primary display surface for the Works-by-Worrell brand, routed through Squarespace in Phase 5 (P5-A4).
  * **Repository Creation:** Create a new repository named `Works-by-Worrell.github.io` under the `Works-by-Worrell` GitHub organization. This naming convention is required by GitHub Pages for org-level sites.
  * **Enable GitHub Pages:** In the repository settings, navigate to **Pages** and set the source to the `main` branch root. Verify the site is accessible at `https://works-by-worrell.github.io`.
  * **Scaffold Minimal Landing Page:** Commit an `index.html` at the root establishing the portfolio identity. Full content development is deferred until the Squarespace routing is confirmed in P5-A4.

- [x] **[P1-R1] Repository Restructuring**
  Re-architect the local repository layout into a strictly decoupled, domain-driven structure. This ensures a clean separation of concerns between application logic, infrastructure declarations, and CI/CD pipelines, preventing configuration bleed and maintaining an industry-grade portfolio standard.

  Target Directory Map:
  ```
  warlock-agents/
  ├── .github/
  │   └── workflows/
  │       └── cicd.yaml
  ├── config/
  │   └── secrets.template.env
  ├── docs/
  │   └── architecture/
  │       └── 0001-cloud-migration-blueprint.md
  ├── infra/
  │   ├── main.tf
  │   ├── variables.tf
  │   ├── outputs.tf
  │   └── terraform.tfvars
  ├── python-app/
  │   ├── .venv/
  │   ├── src/
  │   │   └── worksbyworrell/
  │   │       └── warlock/
  │   │           ├── __init__.py
  │   │           ├── main.py
  │   │           ├── agents/
  │   │           │   ├── __init__.py
  │   │           │   └── base.py
  │   │           └── storage/
  │   │               ├── __init__.py
  │   │               └── firestore_client.py
  │   ├── tests/
  │   │   ├── __init__.py
  │   │   ├── conftest.py
  │   │   ├── test_agents.py
  │   │   ├── test_storage.py
  │   │   └── mock_data/
  │   │       └── warlock_prime.json
  │   ├── scripts/
  │   │   └── seed_github_data.py
  │   ├── .python-version
  │   ├── pyproject.toml
  │   ├── uv.lock
  │   └── requirements.txt
  ├── Dockerfile
  ├── cloudbuild.yaml
  └── README.md
  ```
  > **Blueprint Manifest:** The `0001-cloud-migration-blueprint.md` file tracks the structural migration lifecycle from a prototype segmented file system to the stateless Google Cloud Run and Native Mode Firestore tier.

- [x] **[P1-R2] Establish Git Lifecycle Standards (CONTRIBUTING.md)**
  Draft a comprehensive `CONTRIBUTING.md` at the root directory to define the project's branch strategy and delivery boundaries.
  * **Branch Taxonomy:** Enforce explicit type-prefixes to categorize development activity before it targets the `main` trunk:
    * `feat/` -> Application feature delivery blocks
    * `infra/` -> Declarative infrastructure and environment changes
    * `fix/` -> Immediate bug triage and error resolution
    * `test/` -> Verification frameworks and mock enhancements
    * `docs/` -> Runbook updates, architectural diagrams, and documentation
    * `chore/` -> Maintenance, dependencies, and configuration cleanup
  * **Changelog Triggers:** Align commit messages with Conventional Commits rules (`feat(mcp): message`, `fix(storage): message`) to ensure development history reads seamlessly like an official technical changelog.

- [x] **[P1-R3] Conventional Commit & Branch-Naming Workflows**
  Establish a highly disciplined development lifecycle using a standardized Git branch and commit format. This ensures your public repository profile displays clear software craftsmanship and automated traceability.
  * **Branch Structure:** `<type>/phase<num>-<short-description>` or `<type>/issue-<id>-<description>`
    * Examples: `infra/phase2-cloud-run`, `feat/issue-4-github-api`, `test/phase1-mocking`
  * **Commit Format:** `<type>(<scope>): <short description>`
    * Standard Types: `feat` (new feature), `fix` (bug fix), `infra` (Terraform/GCP changes), `docs` (runbooks/documentation), `test` (adding/refactoring tests), `chore` (dependencies/maintenance)
    * Scope Boundaries: `arch`, `storage`, `mcp`, `ci-cd`

- [x] **[P1-T1] Offline-First (Yellowstone-Compliant) Test Suite Architecture**
  Implement a deterministic testing strategy that completely isolates the unit testing phase from network dependencies or live cloud runtimes using a pytest framework with robust mocking of the google-cloud-firestore SDK.
  
  Global Fixtures (tests/conftest.py):
  ```python
  import pytest
  from unittest.mock import MagicMock

  @pytest.fixture
  def mock_firestore_client(mocker):
      mock_db = MagicMock()
      mocker.patch("google.cloud.firestore.Client", return_value=mock_db)
      return mock_db
  ```

  Storage Layer Tests (tests/test_storage.py):
  ```python
  import pytest
  from unittest.mock import MagicMock
  from src.storage.firestore_client import _load_from_firestore

  def test_load_from_firestore_success(mock_firestore_client):
      mock_doc = MagicMock()
      mock_doc.exists = True
      mock_doc.to_dict.return_value = {"overlay_id": "recruiters_pass", "restricted_mode": False}
      mock_firestore_client.collection.return_value.document.return_value.get.return_value = mock_doc

      result = _load_from_firestore(agent_id="warlock_prime", client=mock_firestore_client)

      assert result["restricted_mode"] is False
  ```

- [x] **[P1-B1] GitHub Organization Project Board Automation Setup**
  Establish a highly visible, automated public GitHub Project (v2) at the organization level (Works-by-Worrell) to showcase software craftsmanship and operational lifecycle visibility to external observers.
  * Define three foundational columns: `Todo`, `In Progress`, and `Done`. *(Note: live board uses these names — not the originally spec'd `Backlog` / `In Flight` / `Completed`.)*
  * Configure automated workflow rules using GitHub Actions to automatically transition Issues into `In Progress` upon branch creation or PR linkage, and move them to `Done` when a merge event to the production branch occurs.
  * Use native issue linking prefixes like `Closes #<id>` or `Fixes #<id>` within your Pull Request descriptions to trigger automated card lifecycle updates automatically.

---

## Phase 2: Declarative Cloud Footprint (Terraform with Firestore)

- [x] **[P2-T1] Remote State & Provider Declarations**
  Initialize infra/main.tf with a secure, remote Google Cloud Storage (GCS) backend block to ensure state persistence outside the local runtime environment.

  Configuration Blocks:
  ```
  terraform {
    required_version = ">= 1.5.0"
    backend "gcs" {
      bucket = "worksbyworrell-tf-state"
      prefix = "warlock-agents/prod"
    }
    required_providers {
      google = {
        source  = "hashicorp/google"
        version = "~> 5.0"
      }
    }
  }

  provider "google" {
    project = var.project_id
    region  = var.region
  }
  ```

- [x] **[P2-T2] Variables Configuration**
  Define input schema barriers in infra/variables.tf to control parameters dynamically across environments.

  Configuration Blocks:
  ```
  variable "project_id" {
    type        = string
    description = "The target GCP project ID."
  }

  variable "region" {
    type        = string
    default     = "us-central1"
    description = "Target regional compute zone optimized for cost and features."
  }

  variable "domain_name" {
    type        = string
    default     = "warlock.worksbyworrell.com"
    description = "Custom ingress route for the portfolio entrypoint."
  }
  ```

- [x] **[P2-T3] Core Resource Blocks (Cloud Run, Firestore, and Secret Manager)**
  Append the declarative definitions for the zero-cost computing layer, database, and secrets layer to infra/main.tf.

  Configuration Blocks:
  ```
  resource "google_firestore_database" "database" {
    project     = var.project_id
    name        = "(default)"
    location_id = var.region
    type        = "FIRESTORE_NATIVE"
    deletion_policy = "DELETE" 
  }

  resource "google_artifact_registry_repository" "repo" {
    location      = var.region
    repository_id = "warlock-agents-registry"
    description   = "Docker repository optimized for minimal image retention"
    format        = "DOCKER"
  }

  resource "google_cloud_run_v2_service" "warlock_service" {
    name     = "warlock-agents-core"
    location = var.region
    ingress  = "INGRESS_TRAFFIC_ALL"

    template {
      scaling {
        max_instance_count = 3  
        min_instance_count = 0  
      }

      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.repo.repository_id}/warlock-core:latest"
        
        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
          startup_cpu_boost = true
        }

        env {
          name  = "FASTMCP_TRANSPORT"
          value = "streamable-http"
        }

        env {
          name = "GH_TOKEN"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.github_token.secret_id
              version = "latest"
            }
          }
        }
      }
    }
  }

  resource "google_secret_manager_secret" "github_token" {
    secret_id = "github-app-token"
    replication {
      auto {}
    }
  }

  # Grant the Cloud Run default Compute SA permission to read the secret at runtime.
  # Without this IAM binding, Cloud Run will fail to resolve GH_TOKEN on container startup.
  resource "google_secret_manager_secret_iam_member" "github_token_accessor" {
    secret_id = google_secret_manager_secret.github_token.secret_id
    role      = "roles/secretmanager.secretAccessor"
    member    = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  }
  ```

- [x] **[P2-T4] Artifact Registry Lifecycle Cleanup Policy**
  Configure strict retention barriers to explicitly keep the active image storage size below the 500 MB Free Tier threshold. Add this block directly inside infra/main.tf:

  Configuration Blocks:
  ```
  resource "google_artifact_registry_repository_iam_member" "cleanup_policy_binding" {
    project    = var.project_id
    location   = google_artifact_registry_repository.repo.location
    repository = google_artifact_registry_repository.repo.name
    role       = "roles/artifactregistry.repoAdmin"
    member     = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  }

  resource "google_cloud_scheduler_job" "purge_old_images" {
    name             = "cleanup-registry-layers"
    description      = "Trigger automated cleanup of dangling or historical container tags"
    schedule         = "0 0 * * 1" 
    time_zone        = "America/Denver"
    attempt_deadline = "320s"

    pubsub_target {
      topic_name = google_pubsub_topic.cleanup_topic.id
      data       = base64encode("{\"action\": \"KEEP_3_TAGS\"}")
    }
  }

  resource "google_pubsub_topic" "cleanup_topic" {
    name = "artifact-registry-cleanup"
  }
  ```

- [x] **[P2-T5] Outputs Definition**
  Expose structural metadata paths in infra/outputs.tf for consumption by delivery tools:

  Configuration Blocks:
  ```
  output "cloud_run_url" {
    value       = google_cloud_run_v2_service.warlock_service.uri
    description = "The dynamic, system-assigned public URL for the Cloud Run instance."
  }
  ```

> **Phase 2 Implementation & Deployment Session Notes:**
> * **Project Boundaries:** Provisioned under project `worksbyworrell-nprd` in region `us-central1`.
> * **Generalized Registry Strategy:** Customized Artifact Registry repository ID to `worksbyworrell-registry` and container image to `warlock-agents-core:latest` to support generic non-prod container management across projects (and synchronized `cloudbuild.yaml` accordingly).
> * **API Automation & State Store:** State backend linked to GCS `gs://worksbyworrell-tf-state`. Automated 6 core GCP APIs via `google_project_service` resource loops.
> * **Cloud Run Container Runtime:** Updated `python-app/src/worksbyworrell/warlock/main.py` CLI parser to fall back to `FASTMCP_TRANSPORT` and `PORT` environment variables dynamically on container boot.
> * **WSL 2 Toolchain:** Installed native `docker-ce-cli` and disabled Docker Desktop Resource Saver mode to preserve permanent Unix socket communication at `/mnt/wsl/docker-desktop-bind-mounts/Ubuntu/docker.sock`.

---

## Phase 3: The Containerized Environment & Caching Matrix

- [x] **[P3-D1] Multi-Stage Performance-Optimized Dockerfile**
  Isolate build-time toolchains from production layers. This keeps the final image lightweight, accelerates cold-start execution on Cloud Run, and guarantees that layers stay within tight free-tier memory allowances.

  Dockerfile Content:
  ```dockerfile
  FROM python:3.11-slim AS builder
  WORKDIR /app
  RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
  COPY python-app/requirements.txt .
  RUN --mount=type=cache,target=/root/.cache/pip pip install --user --no-warn-script-location -r requirements.txt

  FROM python:3.11-slim AS runner
  WORKDIR /app
  COPY --from=builder /root/.local /root/.local
  COPY python-app/src/worksbyworrell /app/worksbyworrell
  ENV PATH=/root/.local/bin:$PATH
  ENV PYTHONUNBUFFERED=1
  EXPOSE 8080
  ENTRYPOINT ["python", "-m", "worksbyworrell.warlock.main"]
  ```

- [x] **[P3-D2] Declarative Pipeline (cloudbuild.yaml) Configuration**
  Design the deployment pipeline to validate correctness before provisioning artifacts. The execution order requires a successful test suite run before compiling any image layers.

  Cloud Build Content:
  ```yaml
  steps:
    - name: 'python:3.11-slim'
      id: 'Execute Test Suite'
      entrypoint: 'bash'
      args:
        - '-c'
        - |
          cd python-app
          pip install -r requirements.txt pytest pytest-mock
          PYTHONPATH=src pytest tests/ --strict-markers

    - name: 'gcr.io/cloud-builders/docker'
      id: 'Build Optimized Container'
      waitFor: ['Execute Test Suite']
      env:
        - 'DOCKER_BUILDKIT=1'
      entrypoint: 'bash'
      args:
        - '-c'
        - |
          docker build \
            --cache-from=us-central1-docker.pkg.dev/$PROJECT_ID/worksbyworrell-registry/warlock-agents-core:latest \
            -t us-central1-docker.pkg.dev/$PROJECT_ID/worksbyworrell-registry/warlock-agents-core:latest \
            -t us-central1-docker.pkg.dev/$PROJECT_ID/worksbyworrell-registry/warlock-agents-core:${_TAG} \
            .

    - name: 'gcr.io/cloud-builders/docker'
      id: 'Push Artifact Layers'
      args: [
        'push', 
        'us-central1-docker.pkg.dev/$PROJECT_ID/worksbyworrell-registry/warlock-agents-core:latest'
      ]

    - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
      id: 'Deploy to Cloud Run Environment'
      entrypoint: 'gcloud'
      args:
        - 'run'
        - 'deploy'
        - 'warlock-agents-core'
        - '--image=us-central1-docker.pkg.dev/$PROJECT_ID/worksbyworrell-registry/warlock-agents-core:latest'
        - '--region=us-central1'
        - '--platform=managed'

  options:
    logging: CLOUD_LOGGING_ONLY

  substitutions:
    _TAG: 'manual'
  ```

- [x] **[P3-D3] Automated GitHub Push/Merge Cloud Build Trigger**
  Establish automated continuous deployment by binding GitHub pushes to the `main` branch to execute `cloudbuild.yaml` seamlessly without requiring manual `gcloud builds submit` invocations.

  Terraform Resource Block (infra/main.tf):
  ```hcl
  resource "google_cloudbuild_trigger" "github_main_trigger" {
    name        = "deploy-on-main-merge"
    description = "Automatically trigger Cloud Build on PR merge to main branch"
    filename    = "cloudbuild.yaml"

    github {
      owner = "Works-by-Worrell"
      name  = "warlock-agents"
      push {
        branch = "^main$"
      }
    }

    substitutions = {
      _TAG = "latest"
    }

    depends_on = [google_project_service.apis]
  }
  ```

> **Phase 3 Implementation & Deployment Session Notes:**
> * **Container Optimization:** Built multi-stage Docker image with pip cache mounting (`DOCKER_BUILDKIT=1`). Verified Streamable-HTTP startup and health checks on port 8080.
> * **CI/CD Pipeline Validation:** Finalized `cloudbuild.yaml` with test execution (`PYTHONPATH=src pytest tests/`), BuildKit cache support, artifact pushing, and Cloud Run deployment (`entrypoint: 'gcloud'`).
> * **Native AR Storage Management:** Updated `infra/main.tf` to adopt native Artifact Registry `cleanup_policies` (`keep-recent-3-versions` and `delete-untagged-images`), capping storage under ~216 MB (well below the 500 MB Free Tier limit) and deprecating legacy Cloud Scheduler / PubSub resources.
> * **Automated Deployment Trigger:** Configured 2nd Gen Cloud Build Trigger (`deploy-on-main-merge`) bound to repository `Works-by-Worrell/warlock-agents` on `main` branch merges.


---

## Phase 4: Network Transport, NoSQL Schema, & State Realignment

- [x] **[P4-N1] FastMCP Network Layer Transformation**
  Transition the FastMCP runtime server out of standard input/output (stdio) pipelines into an asynchronous, network-exposed Streamable-HTTP ASGI daemon. Update python-app/src/worksbyworrell/warlock/main.py:

  Python Implementation:
  ```python
  import os
  import uvicorn
  from mcp.server.fastmcp import FastMCP

  mcp = FastMCP("Warlock-Agents")

  @mcp.resource("warlock://metrics")
  def get_warlock_metrics() -> str:
      return "### Warlock Operational Status\n* State: **Active**\n* Ingress-Layer: **HTTP**"

  if __name__ == "__main__":
      bind_host = "0.0.0.0"
      bind_port = int(os.environ.get("PORT", 8080))
      uvicorn.run("worksbyworrell.warlock.main:mcp.asgi_app", host=bind_host, port=bind_port, log_level="info")
  ```

- [x] **[P4-N2] Layered Security Document Architecture Design**
  Configure Firestore to separate public config profiles from private operational data. This prevents leaking keys while merging data in memory at runtime.

  Data Tier Topography:
  ````
  Firestore Root/
  ├── agent_configurations/ {Document ID: "warlock_prime"}
  │   ├── name: "Warlock Core Agent"
  │   └── public_scope: "Portfolio automation and public task triage orchestration"
  └── agent_overlays/       {Document ID: "warlock_prime"}
      ├── github_private_app_key: "sec_enc_0x83F9..."
      └── underlying_model_target: "gemini-1.5-pro"
  ```

- [x] **[P4-N3] Pythonic Functional Strategy Registry Fallback**
  Implement the storage strategy router inside python-app/src/worksbyworrell/warlock/storage/firestore_client.py. This checks for environment context to decide between live Firestore lookups or zero-dependency flat file fallback evaluations, enabling instant out-of-the-box project forkability without complex GoF boilerplate.

  Python Implementation:
  ```python
  import os
  import json
  from google.cloud import firestore

  def _load_from_firestore(agent_id: str, client=None) -> dict:
      db = client or firestore.Client()
      public_ref = db.collection("agent_configurations").document(agent_id).get()
      private_ref = db.collection("agent_overlays").document(agent_id).get()
      
      base = public_ref.to_dict() if public_ref.exists else {}
      overlay = private_ref.to_dict() if private_ref.exists else {}
      return {**base, **overlay}

  def _load_from_local_fs(agent_id: str) -> dict:
      mock_path = os.path.join("tests", "mock_data", f"{agent_id}.json")
      if not os.path.exists(mock_path):
          return {"name": agent_id, "public_scope": "Fallback Demo Mode Enabled"}
          
      with open(mock_path, "r") as f:
          return json.load(f)

  STORAGE_STRATEGIES = {
      "prod": _load_from_firestore,
      "local": _load_from_local_fs
  }

  def get_agent_config(agent_id: str) -> dict:
      env = "prod" if os.environ.get("GCP_PROJECT_ID") else "local"
      strategy = STORAGE_STRATEGIES.get(env, _load_from_local_fs)
      return strategy(agent_id)

  @mcp.resource("warlock://config/{agent_id}")
  def serialize_agent_config(agent_id: str) -> str:
      merged_data = get_agent_config(agent_id)
      
      markdown_output = f"# Integrated Configuration Strategy for: `{agent_id}`\n\n"
      markdown_output += "### Structural Metadata Profiles\n"
      for key, value in merged_data.items():
          if "key" in key or "token" in key:
              markdown_output += f"* **{key}**: `[ENCRYPTED/RESTRICTED_BOUNDARIES]`\n"
          else:
              markdown_output += f"* **{key}**: {value}\n"
              
      return markdown_output
  ```

> **Phase 4 Implementation & Deployment Session Notes:**
> * **FastMCP Streamable-HTTP ASGI Transport (`P4-N1`):** Configured Uvicorn ASGI daemon binding on `0.0.0.0:${PORT:-8080}` in `main.py` with `FASTMCP_TRANSPORT=streamable-http`.
> * **Dual-Collection Firestore Security Schema (`P4-N2`):** Implemented in-memory dictionary merging (`{**public, **private}`) across `agent_configurations` and `agent_overlays` collections in `_load_from_firestore`.
> * **Strategy Router & Secret Redaction (`P4-N3`):** Built `get_agent_config` environment router (`GCP_PROJECT_ID`) with zero-dependency local JSON fallback, and exposed `@mcp.resource("warlock://config/{agent_id}")` with sensitive key masking (`[ENCRYPTED/RESTRICTED_BOUNDARIES]`).
> * **Yellowstone Test Suite & Cloud Verification:** Added 6 isolated pytest cases in `tests/test_storage.py` (100% passing). Verified live Cloud Run deployment (`warlock-agents-core`) with OIDC token-authenticated FastMCP SSE protocol handshakes.

---

## Phase 5: Routing, Domain Handshaking, and Automation

- [ ] **[P5-A1] GitHub Milestone & Ingestion Pipeline Synchronization Script**
  Deploy a synchronization script inside `python-app/scripts/seed_github_data.py` (or module `worksbyworrell.warlock.sync`) to ingest tracking milestones from GitHub REST API (`state=all`) and parse local agent Markdown specs (`.public/agents/*.md` and `.private/agents/*.md`) into Cloud Firestore collections (`portfolio_milestones`, `agent_configurations`, and `agent_overlays`).
  * **Markdown Tokenization:** Parses YAML frontmatter (`name`, `description`, `model`, `tools`) and stores the markdown body as `system_prompt` in Firestore documents without requiring manual JSON conversion.
  * **Hybrid Ingestion Pipeline:** Public milestones and `.public/agents/` are synced via an automated, $0-cost GitHub Actions workflow (`.github/workflows/sync_milestones.yaml`). Private overlays in `.private/agents/` are synced via local developer CLI (`--private` flag with `gcloud auth`) or private GCS bucket EventArc triggers.
  * **Frontend Delivery:** Exposes static `./milestones.json` and `./agents.json` for GitHub Pages (`worksbyworrell.com`) to serve with 0ms latency and $0 CORS complexity, backed by dynamic Cloud Run API lookups (`https://warlock.worksbyworrell.com/api/portfolio`).

  Python Implementation:
  ```python
  import os
  import datetime
  import httpx
  import yaml
  from google.cloud import firestore

  DEFAULT_REPO = "Works-by-Worrell/warlock-agents"

  def fetch_github_milestones(repo: str = DEFAULT_REPO, token: str | None = None) -> list[dict]:
      url = f"https://api.github.com/repos/{repo}/milestones?state=all"
      headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
      if token:
          headers["Authorization"] = f"Bearer {token}"
      with httpx.Client(timeout=10.0) as client:
          resp = client.get(url, headers=headers)
          resp.raise_for_status()
          return resp.json()

  def parse_agent_markdown(file_path: str) -> dict:
      with open(file_path, "r", encoding="utf-8") as f:
          content = f.read()
      if content.startswith("---"):
          parts = content.split("---", 2)
          frontmatter = yaml.safe_load(parts[1]) if len(parts) >= 3 else {}
          body = parts[2].strip() if len(parts) >= 3 else ""
          return {**frontmatter, "system_prompt": body}
      return {"system_prompt": content}

  def sync_github_milestones_to_firestore(repo: str = DEFAULT_REPO):
      token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
      raw_milestones = fetch_github_milestones(repo, token)
      db = firestore.Client() if os.environ.get("GCP_PROJECT_ID") else None
      
      for ms in raw_milestones:
          total = ms.get("open_issues", 0) + ms.get("closed_issues", 0)
          progress = round((ms.get("closed_issues", 0) / total * 100), 2) if total > 0 else 0.0
          payload = {
              "milestone_id": ms["number"],
              "title": ms["title"],
              "description": ms.get("description") or "",
              "state": ms["state"],
              "open_issues": ms.get("open_issues", 0),
              "closed_issues": ms.get("closed_issues", 0),
              "progress_percentage": progress,
              "github_url": ms["html_url"],
              "updated_at": ms.get("updated_at"),
              "synced_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
          }
          if db:
              db.collection("portfolio_milestones").document(str(ms["number"])).set(payload)
          print(f"Synced milestone #{ms['number']}: {ms['title']} ({progress}%)")

  if __name__ == "__main__":
      sync_github_milestones_to_firestore()
  ```

- [ ] **[P5-A2] Squarespace Custom Subdomain Ingress Architecture**
  Map public HTTP traffic from your custom subdomain to your managed Cloud Run instance.
  1. Open the Google Cloud Console and navigate to Cloud Run -> Manage Custom Domains.
  2. Click Add Mapping, choose warlock-agents-core, and set the domain field exactly to warlock.worksbyworrell.com.
  3. Copy the unique Google Search Console TXT token provided during the verification step.
  4. Log in to your Squarespace account, navigate to Settings -> Domains -> worksbyworrell.com -> Advanced DNS Settings.
  5. Add a new TXT Record:
     * Host/Name: @
     * Value: google-site-verification=[PASTE_YOUR_COPIED_TOKEN_HERE]
  6. Add the target routing rules via a CNAME Record inside Squarespace:
     * Host/Name: warlock
     * Type: CNAME
     * Alias Data/Value: ghs.googlehosted.com.

- [ ] **[P5-A3] Refactoring Localized CLI Automation with Secure gcloud Proxying**
  Update your local client CLI scripts (e.g., your Gemini/Antigravity integration tools) to communicate securely with your live cloud backend without exposing it to public, unauthenticated access.
  * Enforce --no-allow-unauthenticated flags within your infrastructure config to secure the environment.
  * In your local development CLI tool, route API interactions through a localized authenticated gcloud proxy loop:

  Local Terminal Commands:
  ```shell
  export TARGET_OIDC_TOKEN=$(gcloud auth print-identity-token)

  curl -X GET https://warlock.worksbyworrell.com/mcp/resources \
    -H "Authorization: Bearer $TARGET_OIDC_TOKEN" \
    -H "Content-Type: application/json"
  ```

- [x] **[P5-A4] Squarespace: Forward Primary Domain to GitHub Pages Organization Site**
  Route the root `worksbyworrell.com` domain from Squarespace to the GitHub Pages organization site established in P1-G3.
  1. Log in to your Squarespace account and navigate to **Settings → Domains → worksbyworrell.com → Advanced DNS Settings**.
  2. Add a CNAME record pointing the `www` subdomain to the GitHub Pages org site:
     * **Host/Name:** `www`
     * **Type:** CNAME
     * **Value:** `works-by-worrell.github.io.`
  3. For the apex domain (`worksbyworrell.com`), add GitHub Pages' four required `A` records:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
  4. In the `Works-by-Worrell.github.io` repository settings under **Pages**, set the **Custom domain** field to `worksbyworrell.com` and enable **Enforce HTTPS**.
  5. Verify propagation (allow up to 24 hours) by navigating to `https://worksbyworrell.com`.

> **Phase 5 Design & Architectural Decision Notes:**
> * **Career Benchmark Alignment:** Standardized architectural guidance and expectations to **Senior Software Engineer (SSE)** (target promotion level for Roger, currently SE2 at ORLY). At enterprise scale (ORLY), Principal is the immediate step above Senior.
> * **GitHub Milestones Provisioning & Backfilling:** Created 5 Phase Milestones on GitHub repository `Works-by-Worrell/warlock-agents` via `gh api`. Linked all 22 existing issues (`#17` through `#38`) to their corresponding Phase Milestones:
>   * Milestone 1 (`Phase 1: Workspace Strategy & Git Hygiene`): 8 closed issues (100% complete).
>   * Milestone 2 (`Phase 2: Declarative Cloud Footprint`): 5 closed issues (100% complete).
>   * Milestone 3 (`Phase 3: Containerization & CI/CD`): 2 closed issues (100% complete).
>   * Milestone 4 (`Phase 4: FastMCP Transport & Security`): 3 closed issues (100% complete).
>   * Milestone 5 (`Phase 5: Routing, Ingress & Automation`): 1 closed (`#38`), 3 open (`#35`, `#36`, `#37`) (25% complete).
> * **GitOps & Hybrid Agent Ingestion:** Designed `.public/agents/*.md` YAML frontmatter auto-tokenization into Firestore `agent_configurations` and `.private/agents/*.md` into `agent_overlays`. Preserves open-source repository forkability while protecting private overlays via local developer CLI execution (`--private`) or GCS EventArc triggers.
> * **$0-Cost Budget Audit:** Confirmed 100% $0.00 operation via unlimited public GitHub Actions Linux minutes and GCP Free Tier allowances (20k Firestore writes/day, 2M Cloud Run calls/month, AR retention capping at ~216MB).
