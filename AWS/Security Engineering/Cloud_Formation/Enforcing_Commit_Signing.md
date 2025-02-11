---
title: "Enforcing Commit Signing with YubiKey on GitHub"
description: "Ensuring Secure and Verified Commits in GitHub Repositories"
---

# 🔐 Enforcing Commit Signing with YubiKey on GitHub

## 📌 Overview
Commit signing ensures that every commit in a Git repository is **cryptographically verified** using **GPG keys or SSH keys**. Using a **YubiKey** as a hardware-backed GPG smart card strengthens security, making it much harder for attackers to forge commits or push malicious code.

### **Why Commit Signing Matters**
✅ **Prevents tampering**: Ensures all commits come from authorized developers.
✅ **Builds trust**: Teams can confidently merge only signed and verified commits.
✅ **Protects repositories**: Prevents supply chain attacks via unsigned commits.
✅ **Complies with security policies**: Many organizations require verified commits.

---

## 🛠 **Setting Up YubiKey for Commit Signing**

### **1️⃣ Install Required Software**
Ensure you have:
- **GnuPG (GPG)**: For managing encryption keys.
- **GPG tools for YubiKey**: To handle smart card interactions.
- **Git**: Ensure your version supports signed commits.

#### **Install on Linux/macOS**:
```sh
brew install gnupg pinentry-mac # macOS
sudo apt install gnupg2 scdaemon pcscd -y # Linux
```

#### **Install on Windows**:
Download and install [Gpg4win](https://gpg4win.org/).

---

### **2️⃣ Generate or Import a GPG Key**
To generate a new GPG key:
```sh
gpg --full-generate-key
```
Select RSA **4096 bits** and set an **expiration date**. Once done, list your keys:
```sh
gpg --list-secret-keys --keyid-format LONG
```
Copy the `KEY_ID` from the output.

To move this key to YubiKey:
```sh
gpg --edit-key KEY_ID
```
Then enter:
```sh
keytocard
```
Select **Authentication Key** and confirm.

---

### **3️⃣ Configure Git to Use Your Key**
Set up Git to use your key for signing commits:
```sh
git config --global user.signingkey KEY_ID
git config --global commit.gpgsign true
```
Test it:
```sh
echo "test" | gpg --clearsign
```
If successful, your YubiKey is ready for signing!

---

## 🚀 **GitHub Actions: Enforcing Signed Commits**
The following **GitHub Actions workflow** (`.github/workflows/validate-signing.yml`) ensures all commits are **signed and verified** before merging.

```yaml
name: "Enforce Signed Commits"

on: 
  pull_request:
    branches: [main, develop]

jobs:
  check-signatures:
    name: "Verify Commit Signatures"
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Ensures full commit history

      - name: Validate Commit Signatures
        run: |
          if ! git log --pretty="%G?" HEAD | grep -q 'G'; then
            echo "❌ Unsigned commits detected!"
            exit 1
          fi
          echo "✅ All commits are signed."

      - name: Ensure YubiKey-Signed Commits Only
        run: |
          ALLOWED_KEY="0xYOUR_YUBIKEY_GPG_KEY_ID"
          if ! git log --pretty="%G? %GF" HEAD | grep -q "G $ALLOWED_KEY"; then
            echo "❌ Commit not signed with the approved YubiKey."
            exit 1
          fi
          echo "✅ Commits signed with the approved YubiKey."
```

---

## 🔍 **Verifying Signed Commits in GitHub**
Once commits are signed, GitHub will show a **"Verified" badge** in pull requests. You can also check manually:
```sh
git log --show-signature
```
To enforce signed commits **in repository settings**:
1. Go to **GitHub Repository → Settings → Branches**.
2. Enable **"Require signed commits"** under branch protection rules.
3. Developers must sign commits to merge PRs.

---

## 📢 **Conclusion**
✅ **Secure your commits** with YubiKey-backed GPG signatures.
✅ **Enforce signing policies** using GitHub Actions.
✅ **Strengthen repository security** by allowing only signed commits.

> **🔗 Further Reading:** [GitHub Docs - GPG Commit Verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)

🚀 **Fork this repo, contribute, and improve security practices!**
