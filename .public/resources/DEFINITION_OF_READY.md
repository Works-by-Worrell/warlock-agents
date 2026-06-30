# Definition of Ready

## 1. Terminology & Conformance (RFC-2119)
> [!NOTE]
> The keywords 'MUST', 'MUST NOT', 'REQUIRED', 'SHALL', 'SHALL NOT', 'SHOULD', 'SHOULD NOT', 'RECOMMENDED', 'MAY', and 'OPTIONAL' in this document are to be interpreted as described in BCP 14 [RFC-2119] [RFC-8174].

---

## 2. Mandatory Ticket Structure

Every YouTrack ticket MUST contain the following sections before submitting to the YouTrack API and moved to the "Ready" stage:

### Summary
- **Requirement:** MUST be a single line. SHOULD be prefixed with [{component-name}] (e.g. [warlock-agents]) if known.
- **SSE Context:** Keep it concise. No marketing fluff (e.g. [WBW-10] Expose Definition of Ready as MCP Resource).

### Description
- **Requirement:** MUST contain the subsections below formatted in Markdown.

#### Context & Why
- **Requirement:** MUST state the immediate system problem or need.
- **SSE Context:** Explain how this advances the stability or functionality of the project. If it ties into the Exfiltration goal (e.g. automating interview prep, parsing local resume data) that dependency MUST be documented here.

#### Technical Implementation Plan
- **Requirement:** SHOULD guide the implementation without hand-holding too much
- **SSE Context:** Expect a Senior Software Engineer will be taking on this ticket and set the implementation at the appropriate level of detail the industry expects an SSE to work from.

#### Acceptance Criteria
- **Requirement:** MUST be a checklist (` - [ ] `). Each item MUST be binary (either it works or it doesn't).
- **SSE Context:** Focus on functional contracts (e.g. ` - [ ] The resource://definitions/ready URI returns the correct Markdown content`).

#### Verification & Testing Instructions
- **Requirement:** MUST provide CLI commands or test inputs.
- **SSE Context:** A senior doesn't guess if code works. These instructions should be able to be executed in local environment for bench testing as well as post-deployment integration testing.

### Tags
- **Requirement:** MUST use tag names matching existing YouTrack tags (`Warlock`, `Stability`, `Exfiltration`).
- **SSE Context:** Exfiltration tasks should always have `#Exfiltration` so you can build a clean tracking dashboard in the UI.

### Priority
- **Requirement:** MUST map to YouTrack's default priority levels (`Minor`, `Normal`, `Major`, `Critical`, `Show-stopper`).
