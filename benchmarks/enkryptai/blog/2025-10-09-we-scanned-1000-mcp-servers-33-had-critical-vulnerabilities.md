---
title: "We Scanned 1,000 MCP Servers. ~33% Had Critical Vulnerabilities"
url: https://www.enkryptai.com/blog/we-scanned-1-000-mcp-servers-33-had-critical-vulnerabilities
date: 2025-10-09
author: Nitin Birur
category: Product Updates
collected: 2026-02-08
---

# We Scanned 1,000 MCP Servers. ~33% Had Critical Vulnerabilities

## Key Findings

### Critical Statistics
- **32% of servers** contained at least one critical vulnerability
- **Average of 5.2 vulnerabilities** per server
- **One server had 26 vulnerabilities**
- **Zero servers** had security documentation

### Vulnerability Types Discovered

1. **Command Injection (28% of servers)** - Shell commands with unsanitized user input
2. **Prompt Injection Possibilities (35% of servers)** - Tool outputs exploitable by attackers
3. **Authorization Bypass (41% of servers)** - Most common issue; missing access controls
4. **Path Traversal (19% of servers)** - Unsanitized file paths enabling directory attacks
5. **Resource Exhaustion (15% of servers)** - Unbounded operations causing denial of service
6. **Network Security Issues (23% of servers)** - Missing TLS validation and SSRF vulnerabilities

## Why Traditional Scanners Fail

"Traditional code scanning tools aren't built for MCP's unique architecture" because they miss:
- LLM-driven exploits
- Prompt injection attacks
- Authorization semantic gaps
- Adversarial prompts
- Protocol-level vulnerabilities specific to agent behavior patterns

## Case Studies

### kubernetes-mcp-server
Featured 26 total vulnerabilities including:
- 13 critical command injections (CVSS 9.8)
- 8 resource exhaustion issues
- 4 path traversal flaws

### postmark-mcp-server
A real-world attack scenario where a malicious server silently exfiltrated every email processed while appearing legitimate.

## Solution: MCP Security Stack

Enkrypt AI introduced a three-layer defense approach:

1. **MCP Registry** - Curated server discovery with security scores
2. **MCP Scanner** - Automated pre-deployment validation with four-layer analysis
3. **MCP Gateway** - Runtime enforcement with rate limiting, input validation, and anomaly detection

The scanner provides CVSS scoring, line-by-line code references, impact analysis, and remediation guidance within 5-10 minutes.

## Adoption Metrics

- 1,000+ servers scanned
- 1,000+ vulnerabilities discovered and fixed
- 500+ organizations using the platform
- Zero false positives in critical findings
