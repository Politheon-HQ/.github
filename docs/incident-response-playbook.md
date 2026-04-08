# Incident Response Playbook

## Purpose

This playbook provides step-by-step procedures for engineers to follow when a security or operational incident occurs. It covers the most common incident types at Politheon and is designed to be actionable under pressure — follow the steps in order.

---

## General Principles

**When in doubt, escalate.** It's always better to raise an alarm that turns out to be minor than to miss something critical.

- **Don't troubleshoot alone** — loop in the CTO immediately for any security incident.
- **Don't delete evidence** — preserve logs, screenshots, error messages, and timestamps.
- **Communicate early** — a short "we're looking into it" is better than silence.
- **Rotate first, investigate second** — if credentials may be compromised, rotate them before you understand the full scope.

---

## Incident Severity Levels

| Severity | Definition | Response Time | Examples |
|---|---|---|---|
| **Critical** | Active data breach, production down, or credential compromise with confirmed unauthorized access | Immediate — drop everything | Exposed production database credentials, confirmed unauthorized access to systems, production fully down |
| **High** | Potential credential exposure, service degradation, or vulnerability actively being exploited | Within 1 hour | Secret detected in pushed code, critical CVE in production dependency, partial service outage |
| **Medium** | Vulnerability identified but not yet exploited, non-production secret exposure | Within 24 hours | Dependabot critical alert, secret leaked in dev environment, failed security scan |
| **Low** | Minor security finding, informational alert | Within 1 week | Low-severity Dependabot alert, push protection false positive pattern, minor misconfiguration |

---

## Playbook 1: Exposed Secret / Credential Leak

**Trigger:** Push protection bypass alert, secret scanning alert, or you realize a credential was committed to a repo.

### Immediate Steps (within 15 minutes)

1. **Rotate the credential immediately.** Do not wait to assess impact — rotate first.
   - See the [Push Protection Runbook](push-protection-runbook.md) for rotation locations by secret type.
   - If the credential is the LegiScan API key or any other restricted credential, notify the CTO (Hanna Bodnar) or CEO (Daniel Forcade) immediately.

2. **Determine the exposure scope.**
   - Was the secret pushed to the remote? Check `git log` and the GitHub commit history.
   - Was the branch merged to `main` or any protected branch?
   - How long was the secret exposed? Check commit timestamps.
   - Is the repo public or private?

3. **Notify the CTO** via Slack with:
   - What credential was exposed
   - Which repo and branch
   - How long it was exposed
   - Whether it has been rotated

### Follow-Up (within 24 hours)

4. **Verify the new credential works** across all systems that depend on it (CI/CD, production, dev environments).

5. **Check for unauthorized usage.**
   - Review access logs for the affected service (Azure Activity Log, GitHub Audit Log, etc.).
   - Look for unexpected API calls, deployments, or data access during the exposure window.

6. **Remove the secret from git history** if possible. Since force-push is disabled on pushed branches, coordinate with the CTO for admin-level history cleanup if the secret reached a remote branch.

7. **Create a Linear issue** in the Politheon Dev board with the label `security` documenting:
   - What happened
   - Timeline of exposure and response
   - What was rotated
   - Whether unauthorized access was detected
   - What will be done to prevent recurrence

---

## Playbook 2: Production Outage

**Trigger:** Production application is down, unresponsive, or returning errors at scale.

### Immediate Steps (within 15 minutes)

1. **Confirm the outage.**
   - Check the production URL — is it returning errors or timing out?
   - Check Azure Portal for the relevant App Service / Container App status.
   - Check Application Insights for error spikes or availability drops.

2. **Notify the team** in Slack with:
   - What is down (specific service or full application)
   - When it started (if known)
   - Any recent deployments or changes that may have caused it

3. **Check recent changes.**
   - Was there a recent deployment? Check GitHub Actions workflow runs.
   - Were there any infrastructure changes (Azure resource modifications, DNS changes)?
   - Did a dependency update roll out?

4. **Attempt immediate remediation.**
   - If a recent deployment caused it: roll back by re-deploying the last known working commit.
   - If a resource is down: restart the App Service / Container App in Azure Portal.
   - If it's a database issue: check Azure Database metrics and connectivity.

### Follow-Up (within 24 hours)

5. **Document the incident timeline** in a Linear issue:
   - When the outage started
   - When it was detected
   - What caused it
   - What fixed it
   - When service was restored

6. **Conduct a post-mortem** (for Critical/High severity):
   - What went wrong?
   - How was it detected?
   - How can we prevent it?
   - What monitoring or alerting gaps exist?

---

## Playbook 3: Critical Dependency Vulnerability

**Trigger:** Dependabot alert for a critical or high-severity CVE in a production dependency, or a Trivy scan flags a critical vulnerability in a container image.

### Immediate Steps (within 4 hours for Critical, 24 hours for High)

1. **Assess the vulnerability.**
   - Read the CVE details in the Dependabot alert or Trivy scan results.
   - Is the vulnerable code path actually used in our application?
   - Is there a known exploit in the wild?

2. **Check if a patch is available.**
   - Does the Dependabot PR already have a fix? Review and merge it.
   - If no automated fix: check the dependency's release notes for a patched version.

3. **Apply the fix.**
   - Update the dependency version.
   - Run tests to confirm nothing breaks.
   - Open a PR, get it reviewed, and merge.

4. **If no patch is available:**
   - Assess whether a workaround exists (configuration change, disabling the affected feature).
   - If the risk is critical and no workaround exists, notify the CTO to evaluate whether the dependency should be replaced or the affected functionality should be temporarily disabled.

### Follow-Up

5. **Verify the fix is deployed** to production.

6. **Close the Dependabot alert** or Trivy finding once resolved.

7. **Document** in the relevant Linear issue if the vulnerability required non-trivial action beyond merging a Dependabot PR.

---

## Playbook 4: Vulnerability Report

**Trigger:** A vulnerability is reported — either discovered internally by a team member, flagged by automated tooling (CodeQL, Dependabot, Trivy), or in rare cases reported externally via security@politheon.com. While all Politheon repos are private, the `.github` repo and `SECURITY.md` are public, so external reports about Politheon's public-facing infrastructure (website, APIs) are possible.

### For internal discovery or automated tooling

1. **Create a Linear issue** in the Politheon Dev board with the label `security`. Include:
   - Summary of the vulnerability
   - How it was discovered
   - What systems are affected
   - Severity assessment using the levels above

2. **Remediate** based on severity and the relevant playbook above.

3. **Document the resolution** in the Linear issue.

### For external reports (via security@politheon.com)

1. **Acknowledge the report** within 48 hours. Do not share details about your systems or confirm whether the vulnerability exists in your initial response. Example:

   > Thank you for reporting this. We take security seriously and will investigate. We'll follow up with you as we learn more.

2. **Create a Linear issue** in the Politheon Dev board with the label `security`. Include:
   - Summary of the reported vulnerability
   - Reporter's contact info
   - Date received

3. **Assess the report.**
   - Is this a valid vulnerability? Reproduce it if possible.
   - What is the severity? Use the severity levels above.
   - What systems are affected?

4. **If the vulnerability is valid:** Remediate based on severity, then notify the reporter once fixed. Thank them for the report without disclosing internal architecture details.

5. **If the report is not valid:** Respond to the reporter explaining why. Be respectful — false reports are still valuable because they show someone cared enough to look. Close the Linear issue with a note explaining the assessment.

---

## Playbook 5: Compromised Account

**Trigger:** A team member's GitHub, Azure, or Microsoft 365 account may have been compromised — suspicious login, unexpected changes, or the team member reports unauthorized access.

### Immediate Steps (within 30 minutes)

1. **Revoke sessions and reset credentials.**
   - **GitHub:** Go to the user's settings → Sessions → Revoke all. Reset password and regenerate any PATs.
   - **Azure / Microsoft 365:** Reset password in Entra ID, revoke all active sessions, review MFA status.

2. **Notify the CTO** with:
   - Which account was compromised
   - What access that account had (repos, Azure resources, admin roles)
   - Any suspicious activity observed

3. **Review audit logs.**
   - **GitHub:** Check the org audit log at `github.com/organizations/Politheon-HQ/settings/audit-log` for actions taken by the compromised account.
   - **Azure:** Check Entra ID sign-in logs and Azure Activity Log for unusual activity.
   - **Microsoft 365:** Check the Unified Audit Log in the Microsoft Purview compliance portal.

4. **Assess the blast radius.**
   - What repos did this account have write access to?
   - Were any secrets, deployments, or configurations modified?
   - Were any new PATs, SSH keys, or OAuth apps created under the account?

### Follow-Up (within 24 hours)

5. **Rotate any secrets** the compromised account had access to — even if there's no evidence they were exfiltrated.

6. **Review and restore** any changes made by the compromised account (reverted commits, deleted branches, modified settings).

7. **Ensure MFA is enabled** on the restored account before restoring access.

8. **Document the incident** in a Linear issue with the full timeline, scope, and remediation steps.

---

## After Every Incident

Regardless of the incident type, complete these steps:

1. **Linear issue exists** with the `security` label documenting the incident, timeline, and resolution.
2. **Post-mortem completed** for Critical and High severity incidents — what happened, why, and what changes will prevent recurrence.
3. **Action items tracked** — any follow-up work (monitoring improvements, policy changes, infrastructure hardening) should be captured as separate Linear issues.
4. **Notify stakeholders** — for Critical incidents, the CTO and CEO should align on whether customers, partners, or regulatory bodies need to be informed.
5. **Update documentation** — if the incident revealed a gap in this playbook or other docs, update them.

---

## Key Contacts

| Role | Contact | When to Notify |
|---|---|---|
| **CTO** | Hanna Bodnar — Slack or security@politheon.com | All security incidents, all Critical/High operational incidents |
| **CEO** | Daniel Forcade — Slack | Critical incidents, any incident with potential customer or legal impact |

---

## Additional Resources

- [Push Protection Runbook](push-protection-runbook.md) — Secret exposure remediation
- [Commit Signing Guide](commit-signing-guide.md) — Ensuring commit integrity
- [Politheon Security Policy](../SECURITY.md) — Org-wide security overview