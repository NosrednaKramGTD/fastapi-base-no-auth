# Git SSH Configuration for Multiple Repositories

Guide for configuring SSH keys to work with multiple GitHub repositories and organizations.

## Overview

When working with multiple GitHub repositories or organizations, you may need to use different SSH keys for different repositories. This guide shows you how to configure SSH to automatically use the correct key for each repository.

## Understanding SSH Keys

### Personal SSH Keys vs Deploy Keys

- **Personal SSH Keys**: Added to your GitHub account, can access all repositories you have permission to access, can push and pull
- **Deploy Keys**: Repository-specific, read-only by default, cannot be used for other repositories

### The Problem

If you try to push to a repository using a deploy key (read-only), you'll get an error like:

```
ERROR: Permission to NosrednaKramGTD/fastapi-base-no-auth.git denied to deploy key
fatal: Could not read from remote repository.
```

This happens because deploy keys are tied to a specific repository and are read-only.

## Solution: SSH Config Host Aliases + IdentitiesOnly

Use SSH config host aliases to map different SSH keys to different GitHub repositories. **Critical**: Always include `IdentitiesOnly yes` to prevent SSH from trying other keys.

### Why `IdentitiesOnly yes` is Essential

By default, SSH tries all keys in your SSH agent and keychain when connecting. If you have multiple keys loaded, SSH will try them in order and use the first one that works - even if it's not the key you specified in `IdentityFile`. This can cause:

- Wrong key being used for authentication
- "Permission denied to deploy key" errors
- Authentication failures even with correct keys configured

Setting `IdentitiesOnly yes` restricts SSH to **only** use the keys explicitly listed in the `IdentityFile` directive, ensuring the correct key is always used.

### Step 1: Create or Identify Your SSH Keys

List your existing SSH keys:

```bash
ls -la ~/.ssh/*.pub
```

You should see keys like:
- `~/.ssh/id_rsa.pub` (default personal key)
- `~/.ssh/basic-bot.pub` (specific project key)
- `~/.ssh/fastapi-base.pub` (specific project key)

### Step 2: Configure SSH Config

Edit your SSH config file:

```bash
nano ~/.ssh/config
# or
vim ~/.ssh/config
```

Add host aliases for each repository/key combination:

```ssh
# Default GitHub (uses your personal key)
Host github.com
    HostName github.com
    PreferredAuthentications publickey
    IdentitiesOnly yes
    IdentityFile ~/.ssh/nosrednakram_github

# Project-specific host alias
Host github.com-basic-bot
    HostName github.com
    AddKeysToAgent yes
    UseKeychain yes
    IdentitiesOnly yes
    User git
    IdentityFile ~/.ssh/basic-bot

# Another project-specific host alias
Host github.com-fastapi-base
    HostName github.com
    AddKeysToAgent yes
    UseKeychain yes
    IdentitiesOnly yes
    User git
    IdentityFile ~/.ssh/fastapi-base
```

**Important**: The `IdentitiesOnly yes` setting is crucial! It tells SSH to only use the keys explicitly specified in the `IdentityFile` directive, preventing SSH from trying other keys in your SSH agent or keychain. Without this, SSH may try multiple keys and use the wrong one.

### Step 3: Configure Git Remote URLs

Update your git remote to use the SSH host alias:

```bash
# Instead of:
git remote set-url origin git@github.com:username/repo.git

# Use the host alias:
git remote set-url origin git@github.com-fastapi-base:username/repo.git
```

### Step 4: Test SSH Connection

Test that your SSH key works:

```bash
ssh -T git@github.com-fastapi-base
```

You should see:
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

**Important**: If you see a different repository name in the message, that key is a deploy key for that repository and won't work for pushing to other repositories.

## Common Issues and Solutions

### Issue 1: "Permission denied to deploy key"

**Problem**: You're using a deploy key (read-only) to try to push.

**Solution**:
1. Use a personal SSH key instead of a deploy key
2. Add your personal SSH key to your GitHub account (Settings → SSH and GPG keys)
3. Update your SSH config to use the personal key
4. Update the git remote URL to use the correct host alias

### Issue 2: Wrong key is being used

**Problem**: Git is using the wrong SSH key, even though you've specified the correct one.

**Solution**:
1. Add `IdentitiesOnly yes` to your SSH config entry - this prevents SSH from trying other keys:
   ```ssh
   Host github.com-fastapi-base
       HostName github.com
       AddKeysToAgent yes
       UseKeychain yes
       IdentitiesOnly yes  # ← Add this!
       User git
       IdentityFile ~/.ssh/fastapi-base
   ```
2. Check your git remote URL: `git remote -v`
3. Ensure it uses the correct host alias (e.g., `git@github.com-fastapi-base:...`)
4. Check your SSH config has the correct `IdentityFile` for that host alias
5. Test the connection: `ssh -T git@github.com-fastapi-base`

**Why `IdentitiesOnly yes` matters**: By default, SSH tries all keys in your SSH agent and keychain. If you have multiple keys loaded, SSH might try them in order and use the first one that works, even if it's not the one you specified. `IdentitiesOnly yes` restricts SSH to only use the keys explicitly listed in `IdentityFile`.

### Issue 3: Key not in SSH agent

**Problem**: SSH agent doesn't have the key loaded.

**Solution**:
```bash
# Add key to SSH agent
ssh-add ~/.ssh/fastapi-base

# On macOS, add to keychain (persists across reboots)
ssh-add --apple-use-keychain ~/.ssh/fastapi-base
```

### Issue 4: Multiple keys for same repository

**Problem**: You have multiple keys and need to use a specific one.

**Solution**: Create a specific host alias in SSH config and use it in your git remote URL.

## Best Practices

### 1. Use Personal SSH Keys for Write Access

- Personal SSH keys can push to any repository you have access to
- Deploy keys are read-only and repository-specific
- Use personal keys for development work

### 2. Use Descriptive Host Aliases

Use clear, descriptive names for your host aliases:

```ssh
Host github.com-project-name
Host github.com-org-name
Host github.com-personal
```

### 3. Always Use `IdentitiesOnly yes`

**Critical**: Always include `IdentitiesOnly yes` in your SSH config entries to prevent SSH from trying other keys:

```ssh
Host github.com-fastapi-base
    HostName github.com
    AddKeysToAgent yes
    UseKeychain yes
    IdentitiesOnly yes  # Prevents SSH from trying other keys
    User git
    IdentityFile ~/.ssh/fastapi-base
```

Without this setting, SSH may try keys from your SSH agent or keychain in order, potentially using the wrong key.

### 4. Keep SSH Config Organized

Group related configurations together and add comments:

```ssh
# Personal GitHub account
Host github.com
    HostName github.com
    IdentitiesOnly yes
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/personal_key

# Work organization
Host github.com-work-org
    HostName github.com
    IdentitiesOnly yes
    AddKeysToAgent yes
    UseKeychain yes
    User git
    IdentityFile ~/.ssh/work_key

# Specific project
Host github.com-fastapi-base
    HostName github.com
    IdentitiesOnly yes
    AddKeysToAgent yes
    UseKeychain yes
    User git
    IdentityFile ~/.ssh/fastapi-base
```

### 4. Test Before Pushing

Always test your SSH connection before attempting to push:

```bash
ssh -T git@github.com-fastapi-base
```

## Example: Setting Up for This Project

For the `fastapi-base-no-auth` repository:

1. **Ensure you have a personal SSH key with write access**:
   - If not, generate one: `ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/fastapi-base-write`
   - Add it to your GitHub account (Settings → SSH and GPG keys)

2. **Update SSH config**:
```ssh
Host github.com-fastapi-base
    HostName github.com
    AddKeysToAgent yes
    UseKeychain yes
    IdentitiesOnly yes
    User git
    IdentityFile ~/.ssh/fastapi-base-write  # Use key with write access
```

**Note**: The `IdentitiesOnly yes` setting is essential - it ensures SSH only uses the specified key and doesn't try other keys from your agent or keychain.

3. **Update git remote**:
```bash
git remote set-url origin git@github.com-fastapi-base:NosrednaKramGTD/fastapi-base-no-auth.git
```

4. **Test connection**:
```bash
ssh -T git@github.com-fastapi-base
```

5. **Try pushing**:
```bash
git push -u origin main
```

## Adding SSH Keys to GitHub

### For Personal SSH Keys (Write Access)

1. Copy your public key:
   ```bash
   cat ~/.ssh/your_key.pub | pbcopy  # macOS
   # or
   cat ~/.ssh/your_key.pub | xclip -sel clip  # Linux
   ```

2. Go to GitHub → Settings → SSH and GPG keys
3. Click "New SSH key"
4. Paste your public key
5. Give it a descriptive title
6. Click "Add SSH key"

### For Deploy Keys (Read-Only)

1. Copy your public key (same as above)
2. Go to your repository → Settings → Deploy keys
3. Click "Add deploy key"
4. Paste your public key
5. **Uncheck "Allow write access"** (unless you need it)
6. Click "Add key"

**Note**: Deploy keys are repository-specific and read-only by default.

## Troubleshooting Checklist

- [ ] SSH key exists and has correct permissions (`chmod 600 ~/.ssh/key_name`)
- [ ] SSH config has `IdentitiesOnly yes` to prevent trying other keys
- [ ] SSH config has correct host alias configuration
- [ ] Git remote URL uses the correct host alias
- [ ] SSH key is added to SSH agent (`ssh-add ~/.ssh/key_name`)
- [ ] SSH key is added to GitHub (personal key or deploy key)
- [ ] SSH connection test succeeds (`ssh -T git@host-alias`)
- [ ] Key has write access (personal key, not read-only deploy key)

## Quick Reference

```bash
# List SSH keys
ls -la ~/.ssh/*.pub

# Test SSH connection
ssh -T git@github.com-fastapi-base

# Check git remote URL
git remote -v

# Update git remote URL
git remote set-url origin git@github.com-fastapi-base:username/repo.git

# Add key to SSH agent
ssh-add ~/.ssh/key_name

# Add key to macOS keychain (persists)
ssh-add --apple-use-keychain ~/.ssh/key_name

# View SSH config
cat ~/.ssh/config

# Edit SSH config
nano ~/.ssh/config
```

## Summary

- Use **personal SSH keys** for write access to repositories
- Use **SSH config host aliases** to map keys to repositories
- **Always include `IdentitiesOnly yes`** in SSH config to prevent SSH from trying other keys
- Update **git remote URLs** to use the host aliases
- **Test connections** before pushing
- **Deploy keys are read-only** and repository-specific

**Key Takeaway**: The `IdentitiesOnly yes` setting is critical when working with multiple SSH keys. Without it, SSH may try keys from your agent or keychain in order and use the wrong one, even if you've specified a different key in `IdentityFile`.

For this project, ensure you're using a personal SSH key (not a deploy key) that has write access to the `NosrednaKramGTD/fastapi-base-no-auth` repository, and include `IdentitiesOnly yes` in your SSH config.
