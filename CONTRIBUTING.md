# Contributing to Warlock-Agents

This document outlines the branch taxonomy, commit message standards, and development workflows to maintain high codebase hygiene, automated changelog generation, and clean traceability.

## Branch Strategy & Taxonomy

All development work must occur on a feature or task branch before targeting the `main` trunk. Use the following prefix categories:

### Branch Prefix Categories

*   `feat/` - Application feature delivery blocks (e.g., FastMCP endpoints, API integrations)
*   `infra/` - Declarative infrastructure and environment configurations (e.g., Terraform, GCP configurations)
*   `fix/` - Immediate bug triage, error corrections, and hotfixes
*   `test/` - Verification frameworks, test suites, and mock enhancements
*   `docs/` - Runbook updates, architectural blueprints, and inline documentation
*   `chore/` - Maintenance, dependency updates, and boilerplate cleanup

### Branch Naming Convention

Format: `<type>/phase<num>-<short-description>` or `<type>/issue-<id>-<description>`

**Examples:**
*   `infra/phase2-cloud-run`
*   `feat/issue-4-github-api`
*   `test/phase1-mocking`
*   `docs/phase1-git-hygiene`

---

## Commit Message Conventions

We adhere to the [Conventional Commits](https://www.conventionalcommits.org/) specification. This enables automated changelog generation and clear version boundaries.

### Commit Format

```
<type>(<scope>): <short description>

[Optional body explaining rationale or context]

[Optional footer(s) for issue linking, e.g., Closes #12]
```

### Approved Types

*   `feat`: A new user-facing or system feature.
*   `fix`: A bug fix or patch.
*   `infra`: Infrastructure or CI/CD changes (Terraform, Docker, Cloud Build).
*   `docs`: Documentation changes only.
*   `test`: Adding missing tests or correcting existing tests.
*   `chore`: Maintenance tasks, dependency updates, file restructuring.

### Scope Boundaries

Specify the logical area of the codebase being modified:
*   `arch`: Project structure, repository layout, and design conventions.
*   `storage`: Firestore client, strategy registry, and local FS fallback mechanisms.
*   `mcp`: FastMCP transport layers, tools, resources, and server setup.
*   `ci-cd`: GitHub Actions, Cloud Build configurations, and deployment pipelines.

### Examples

*   `feat(mcp): implement network transport layer via FastMCP ASGI daemon`
*   `infra(storage): define terraform resources for Firestore Native mode`
*   `test(storage): add offline-first mock pytest suite for firestore client`
*   `docs(arch): document cloud migration roadmap and phase matrices`

---

## Pull Request Guidelines

1.  **Branch Check:** Ensure your branch name aligns with the taxonomy.
2.  **Commit Hygiene:** Squash intermediate or redundant commits before requesting review.
3.  **Automation Linkage:** Link associated issues or project cards in the PR description using keywords (e.g., `Closes #4` or `Fixes #7`).
