# Commit Signing Guide

## Why We Require Signed Commits

Politheon requires signed commits on all protected branches. Commit signing cryptographically verifies that a commit was authored by the person it claims to be from, preventing impersonation and ensuring the integrity of our codebase. This is enforced at the enterprise level via GitHub rulesets — unsigned commits will be rejected.

---

## Prerequisites

Before starting, make sure you have **Git** installed and available in your terminal or command prompt.

- **macOS:** Git is included with Xcode Command Line Tools. Run `git --version` to confirm, or install via `xcode-select --install` or `brew install git` if you use [Homebrew](https://brew.sh/).
- **Windows:** Install [Git for Windows](https://gitforwindows.org/), which includes Git Bash. Use **Git Bash** for the commands in this guide unless otherwise noted.

---

## Choose Your Signing Method

| Method | Recommendation | Notes |
|---|---|---|
| **SSH signing** | **Recommended** | Simpler setup, uses the same key type you may already use for Git authentication. No additional software needed. |
| **GPG signing** | Supported | More established standard, wider tooling support. Requires installing GPG. |

If you don't have a strong preference, **use SSH signing** — it's easier to set up and maintain.

---

## Option 1: SSH Signing (Recommended)

### Step 1: Generate an SSH signing key

If you already have an SSH key you use for GitHub authentication, you can reuse it for signing. Otherwise, generate a new one.

**macOS:**

```bash
ssh-keygen -t ed25519 -C "your_name@politheon.com"
```

When prompted, save the key to the default location (`~/.ssh/id_ed25519`). Set a passphrase for additional security.

**Windows (Git Bash):**

```bash
ssh-keygen -t ed25519 -C "your_name@politheon.com"
```

When prompted, save the key to the default location (`C:\Users\YourName\.ssh\id_ed25519`). Set a passphrase for additional security.

### Step 2: Upload your public key to GitHub

Copy your public key:

**macOS:**

```bash
pbcopy < ~/.ssh/id_ed25519.pub
```

**Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

**Windows (PowerShell):**

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | Set-Clipboard
```

Then:

1. Go to [GitHub → Settings → SSH and GPG keys](https://github.com/settings/keys).
2. Click **New SSH key**.
3. Set the **Key type** to **Signing Key**.
4. Paste your public key and save.

> **Important:** If you're using the same key for both authentication and signing, you need to upload it **twice** — once as an "Authentication Key" and once as a "Signing Key." These are separate entries in GitHub.

### Step 3: Configure Git to use SSH signing

**macOS:**

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

**Windows (Git Bash):**

```bash
git config --global gpg.format ssh
git config --global user.signingkey "C:\Users\YourName\.ssh\id_ed25519.pub"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

> **Tip (Windows):** Replace `YourName` with your actual Windows username, or use the `~/.ssh/id_ed25519.pub` shorthand in Git Bash — it resolves to the same path.

### Step 4: Verify it works

```bash
# Make a test commit
echo "test" >> test.txt
git add test.txt
git commit -m "test: verify commit signing"

# Check that the commit is signed
git log --show-signature -1
```

You should see output indicating the commit is signed with your SSH key. Delete the test commit when done:

```bash
git reset --soft HEAD~1
git checkout -- test.txt
```

### Optional: Configure the SSH agent

The SSH agent is **not required** for commit signing to work. However, if you set a passphrase on your key and you're being prompted to enter it on every commit, the SSH agent can cache it for you.

**macOS:**

macOS often handles this automatically through Keychain. If you're still getting passphrase prompts, run:

```bash
# Start the SSH agent
eval "$(ssh-agent -s)"

# Add your key with Apple Keychain integration
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

To make this persistent across terminal sessions, add the following to `~/.ssh/config`:

```
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

**Windows:**

If you're getting passphrase prompts on every commit, open **PowerShell as Administrator** and run:

```powershell
# Ensure the SSH agent service is running
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
```

Then add your key (in Git Bash or PowerShell):

```bash
ssh-add ~/.ssh/id_ed25519
```

---

## Option 2: GPG Signing

### Step 1: Install GPG

**macOS (via Homebrew):**

```bash
brew install gnupg
```

**Windows:**

Download and install [Gpg4win](https://www.gpg4win.org/). This includes GPG and a key management GUI (Kleopatra). After installation, `gpg` will be available in Git Bash and Command Prompt.

### Step 2: Generate a GPG key

```bash
gpg --full-generate-key
```

When prompted:
- Select **RSA and RSA** (option 1)
- Key size: **4096** bits
- Expiration: set a reasonable expiration (e.g., 1 year) — you can extend it later
- Enter your name and **Politheon email address**
- Set a passphrase

### Step 3: Get your GPG key ID

```bash
gpg --list-secret-keys --keyid-format=long
```

Look for the line starting with `sec` and copy the key ID after the `/`. For example, if you see `sec rsa4096/3AA5C34371567BD2`, the key ID is `3AA5C34371567BD2`.

### Step 4: Upload your public key to GitHub

```bash
gpg --armor --export 3AA5C34371567BD2
```

1. Copy the entire output (including the `-----BEGIN PGP PUBLIC KEY BLOCK-----` and `-----END PGP PUBLIC KEY BLOCK-----` lines).
2. Go to [GitHub → Settings → SSH and GPG keys](https://github.com/settings/keys).
3. Click **New GPG key**.
4. Paste your public key and save.

### Step 5: Configure Git to use GPG signing

```bash
git config --global user.signingkey 3AA5C34371567BD2
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

### Step 6: Configure GPG for passphrase entry

**macOS:**

```bash
# Install pinentry for macOS
brew install pinentry-mac

# Configure GPG to use it
echo "pinentry-program $(which pinentry-mac)" >> ~/.gnupg/gpg-agent.conf

# Restart the GPG agent
gpgconf --kill gpg-agent
```

Also add this to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export GPG_TTY=$(tty)
```

**Windows:**

Gpg4win includes a graphical pinentry program that handles passphrase prompts automatically. If Git can't find GPG, you may need to tell Git where it is:

```bash
# Find the GPG path (usually one of these)
# C:\Program Files (x86)\GnuPG\bin\gpg.exe
# C:\Program Files\GnuPG\bin\gpg.exe

git config --global gpg.program "C:\Program Files (x86)\GnuPG\bin\gpg.exe"
```

> **Tip (Windows):** If you're using Git Bash and GPG prompts aren't appearing, add `export GPG_TTY=$(tty)` to your `~/.bashrc` file in Git Bash.

### Step 7: Verify it works

```bash
echo "test" >> test.txt
git add test.txt
git commit -m "test: verify GPG commit signing"
git log --show-signature -1
```

You should see `Good signature` in the output. Clean up when done:

```bash
git reset --soft HEAD~1
git checkout -- test.txt
```

---

## Verifying Your Setup on GitHub

After pushing a signed commit, go to the commit on GitHub. You should see a **"Verified"** badge next to the commit. If you see **"Unverified"**, check that:

1. Your signing key's public key is uploaded to GitHub (as a **Signing Key** for SSH, or a **GPG key** for GPG).
2. The email address on the key matches your Git `user.email` and is a verified email on your GitHub account.
3. Signing is enabled in your Git config (`commit.gpgsign = true`).

---

## Troubleshooting

### "error: gpg failed to sign the data"

**macOS:** This usually means GPG can't access the terminal for passphrase entry. Make sure `GPG_TTY` is set:

```bash
export GPG_TTY=$(tty)
```

**Windows:** Git may not be able to find GPG. Set the path explicitly:

```bash
git config --global gpg.program "C:\Program Files (x86)\GnuPG\bin\gpg.exe"
```

### Push rejected: "Commits must have verified signatures"

Your commit isn't signed, or the signature can't be verified by GitHub. Run `git log --show-signature -1` to check locally, and verify your public key is uploaded to GitHub.

### SSH signing: "error: Load key ... invalid format"

Make sure `user.signingkey` points to the **.pub** (public key) file, not the private key:

**macOS:**

```bash
# Correct
git config --global user.signingkey ~/.ssh/id_ed25519.pub

# Wrong
git config --global user.signingkey ~/.ssh/id_ed25519
```

**Windows:**

```bash
# Correct
git config --global user.signingkey "C:\Users\YourName\.ssh\id_ed25519.pub"

# Wrong
git config --global user.signingkey "C:\Users\YourName\.ssh\id_ed25519"
```

### Commits show as "Unverified" on GitHub

- Confirm the email in `git config user.email` matches a verified email on your GitHub account.
- For SSH: confirm the key is uploaded as a **Signing Key** (not just Authentication Key).
- For GPG: confirm the key's email identity matches your GitHub email.

### Windows: SSH agent not running

If you get errors about the SSH agent, open **PowerShell as Administrator** and run:

```powershell
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
```

---

## Quick Reference

```bash
# Check if signing is enabled
git config --global commit.gpgsign

# Check which key is configured
git config --global user.signingkey

# Check signing format (ssh or gpg)
git config --global gpg.format

# View the signature on your last commit
git log --show-signature -1
```

---

## Additional Resources

- [GitHub Docs: Signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
- [GitHub Docs: Telling Git about your signing key](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key)
- [Politheon Security Policy](../SECURITY.md)