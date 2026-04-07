# Push Protection Runbook

## Your Push Was Blocked — Here's What to Do

GitHub's secret scanning push protection detected a potential secret (such as an API key, token, password, or private key) in your commit and blocked the push to prevent a credential leak.

**This is not an error — it's working as intended.** This guide walks you through resolving the block safely.

---

## Step 1: Identify the Secret

When push protection blocks your push, GitHub provides a message in the CLI or web UI that includes:

- The **type of secret** detected (e.g., GitHub Personal Access Token, Azure Storage Key)
- The **file and line number** where the secret was found
- The **commit SHA(s)** containing the secret

Read this message carefully. Note the file path and commit(s) involved — you'll need them for the next steps.

---

## Step 2: Remove the Secret from Your Code

### If the secret is only in your most recent commit

```bash
# 1. Remove or replace the secret in the file
#    (e.g., replace the hardcoded key with an environment variable reference)

# 2. Stage the fix
git add <file>

# 3. Amend the commit to replace it
git commit --amend

# 4. Retry the push
git push
```

### If the secret is in an older commit

> **Important:** Force-pushing is disabled across all Politheon-HQ repositories and linear commit history is required at the enterprise level. This means you **cannot rewrite history** on branches that have already been pushed. The approach depends on whether the branch has been pushed to the remote yet.

**If the branch has NOT been pushed to the remote yet** (the secret is only in local commits):

You can safely rewrite your local history before pushing.

```bash
# 1. Find the first commit containing the secret
#    (GitHub's error message lists the commit SHAs)

# 2. Start an interactive rebase before that commit
git rebase -i <COMMIT_SHA>~1

# 3. In the editor, change "pick" to "edit" for the commit(s) with the secret
#    Example:
#    edit 8728dbe my commit with the secret
#    pick 03d69e5 my next commit
#    pick 8053f7b my latest commit

# 4. When the rebase pauses at the flagged commit:
#    - Remove the secret from the file
#    - Stage the change: git add <file>
#    - Amend the commit: git commit --amend
#    - Continue the rebase: git rebase --continue

# 5. Repeat for any additional flagged commits

# 6. Push normally (no force-push needed since this branch was never pushed)
git push
```

**If the branch HAS already been pushed to the remote:**

Since force-push is disabled, you cannot rewrite the pushed history. Instead:

1. **Remove the secret** from the file in a new commit on your branch.
2. **Push the new commit** — push protection only blocks commits that *introduce* a secret, so the fix commit will push cleanly.
3. **Rotate the credential immediately** — the secret exists in the branch's commit history and must be considered compromised.
4. **Contact the CTO** (Hanna Bodnar) to coordinate repository-level cleanup if the secret made it into a protected branch. Admin-level intervention may be required to remove the secret from history.

> **Note:** Even though the secret will remain in the git history of the pushed commits, rotating the credential renders it useless. The priority is always to **rotate first**, then address history cleanup.

---

## Step 3: Rotate the Credential Immediately

**Even if the secret was never pushed to the remote, rotate it now.** Treat any secret that made it into a commit as potentially compromised.

| Secret Type | Where to Rotate |
|---|---|
| GitHub Personal Access Token | [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens) — revoke and regenerate |
| Azure Storage Key | Azure Portal → Storage Account → Access keys → Rotate key |
| Azure Service Principal / Client Secret | Azure Portal → App Registrations → Certificates & secrets → New client secret |
| LegiScan API Key | **Restricted access** — notify the CTO (Hanna Bodnar) or CEO (Daniel Forcade). Only the CTO and CEO have access to the LegiScan account. |
| Other API Keys | Revoke in the issuing service's dashboard and generate a new one |

After rotating:

1. **Update the new credential** in the appropriate secure store:
   - **CI/CD pipelines:** [GitHub Actions Secrets](https://github.com/organizations/Politheon-HQ/settings/secrets/actions) (org-level) or repository-level secrets
   - **Application config:** Azure Key Vault
   - **Local development:** Your local `.env` file (which must be in `.gitignore`)
2. **Verify** that deployments and integrations still work with the new credential.
3. **Document the rotation** — note the date, affected systems, and reason in the relevant Linear issue or create a new one.

---

## Step 4: Store the Secret Properly Going Forward

### Approved storage locations

| Use Case | Storage Method |
|---|---|
| GitHub Actions workflows | GitHub Actions Secrets (org or repo level) |
| Production/Dev application config | Azure Key Vault |
| Local development | `.env` file (must be in `.gitignore`) |

### Do NOT store secrets in

- Source code, config files, or comments
- Notion, Google Docs, Slack messages, or email
- `.env` files that are committed to the repo
- Docker Compose files or Dockerfiles
- Hardcoded in CI workflow YAML

### Example: Using an environment variable instead of a hardcoded key

```php
// BAD — hardcoded secret
$apiKey = 'sk-abc123secretkey456';

// GOOD — read from environment
$apiKey = getenv('LEGISCAN_API_KEY');
```

```yaml
# BAD — secret in workflow file
env:
  API_KEY: sk-abc123secretkey456

# GOOD — reference GitHub Actions secret
env:
  API_KEY: ${{ secrets.LEGISCAN_API_KEY }}
```

---

## Step 5: Request a Bypass (If Needed)

In rare cases, push protection may need to be bypassed — for example, if the detected string is a test fixture, a hash, or an inactive credential used in documentation.

### How bypass works at Politheon

Politheon uses **delegated bypass** for push protection. This means:

1. When your push is blocked, GitHub offers the option to **submit a bypass request**.
2. Select a reason:
   - **"It's used in tests"** — The secret is a test fixture or mock value
   - **"It's a false positive"** — The string isn't actually a secret
   - **"I'll fix it later"** — You acknowledge the risk (use sparingly)
3. Your request is routed to **Enterprise Owners** for approval.
4. You'll receive an **email notification** when the request is approved or denied.
5. If approved, you have **3 hours** to re-push the commit containing the flagged string.

> **Important:** Bypass approval does not mean the secret is safe. If the flagged string is a real credential, you must still rotate it even if the bypass is approved.

### When bypass is appropriate

- Test fixtures with fake/mock credentials
- Hashes or checksums that are not secrets
- Inactive or revoked credentials used in documentation examples
- Patterns that match a secret format but aren't actual secrets

### When bypass is NOT appropriate

- Active production credentials (rotate and remove instead)
- Any credential that grants access to real systems or data
- "I need to push quickly" — speed is not a valid bypass reason

---

## Step 6: Report a False Positive

If push protection is consistently flagging a string that is not a secret, contact the CTO (Hanna Bodnar) to evaluate whether:

1. A **pattern exclusion** should be added for the specific string or pattern
2. A **custom pattern** needs tuning
3. The string should be added to the **push protection allow list**

To report, create a Linear issue in the **Politheon Dev** board with the label `git` and include:

- The pattern type that triggered the block
- The file and string that was flagged
- Why you believe it's a false positive

---

## Quick Reference

| Situation | Action |
|---|---|
| Push blocked, real secret in code | Remove from code → Rotate credential → Store in Key Vault / GitHub Secrets → Re-push |
| Push blocked, secret in old commit (not yet pushed) | Interactive rebase locally → Rotate → Push |
| Push blocked, secret in old commit (already pushed) | Remove secret in new commit → Rotate credential → Contact CTO for history cleanup |
| Push blocked, false positive | Request bypass → Report to CTO for pattern review |
| Push blocked, test fixture | Request bypass with "used in tests" reason |
| Not sure if it's a real secret | **Assume it is.** Rotate first, then investigate. |

---

## Additional Resources

- [GitHub Docs: Working with push protection from the command line](https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/working-with-push-protection-from-the-command-line)
- [GitHub Docs: About push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- [Politheon Security Policy](../SECURITY.md)

---

## Contact

- **CTO / Security:** Hanna Bodnar — Slack or security@politheon.com
- **Push protection bypass approvals:** Enterprise Owners (notification via GitHub)
- **Linear:** Create an issue on the [Politheon Dev board](https://linear.app/politheon) with label `git`