# Version Control

Version control is essential for tracking changes, collaborating with others, and maintaining a history of your project. This guide focuses on Git, the most widely used version control system, though many concepts apply to other VCS tools.

## Git Overview

Git is a distributed version control system that allows you to track changes, work on different branches, and collaborate with others. This documentation assumes you have Git installed and focuses on practical workflows for managing your projects.

!!! tip "Git Installation"

    If you don't have Git installed, download it from [git-scm.com](https://git-scm.com/) or use your system's package manager.

## Setting Up a New Repository

I often start projects before checking them into version control. The following steps guide you through setting up Git for an existing project that you want to version control.

### SSH Key Configuration

Using SSH keys for Git authentication is more secure and convenient than using passwords. This is especially important when working with multiple GitHub accounts or repositories.

#### Start SSH Agent

First, start the SSH agent to manage your keys:

```bash
eval "$(ssh-agent -s)"
```

This will start the SSH agent in the background and allow you to add keys for authentication.

#### Generate SSH Key

Generate a new SSH key using the Ed25519 algorithm (recommended for security):

```bash
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/key-name
```

**Parameters:**

- `-t ed25519` - Uses the Ed25519 algorithm (more secure than RSA)
- `-C "your-email@example.com"` - Adds a comment (typically your email)
- `-f ~/.ssh/key-name` - Specifies the filename for the key

!!! warning "Key Naming"

    Use descriptive names for your keys (e.g., `github-personal`, `github-work`, `basic-bot`) to easily identify which key is for which purpose.

#### Configure SSH for GitHub

When working with multiple GitHub accounts or keys, you'll need to configure SSH to use the correct key for each repository. This is done in your `~/.ssh/config` file.

**Add SSH Configuration:**

```
Host github.com-key-name
    HostName github.com
    AddKeysToAgent yes
    UseKeychain yes
    User git
    IdentityFile ~/.ssh/key-name
```

**Configuration Options:**

- `Host` - The alias you'll use when connecting (e.g., `github.com-basic-bot`)
	- `HostName` - The actual GitHub hostname
	- `AddKeysToAgent` - Automatically add the key to the SSH agent
	- `UseKeychain` - Store the key in macOS keychain (macOS only)
	- `User` - Always `git` for GitHub
	- `IdentityFile` - Path to your private key

!!! info "Multiple GitHub Accounts"

    You will probably have many keys for GitHub. The `Host` label (alias) is what you'll use in your Git remote URLs to specify which key to use.

### Initializing a Git Repository

Once your SSH keys are configured, you can set up your Git repository.

#### Step 1: Create GitHub Repository

1. Create a new repository on GitHub
2. Add your public key to your GitHub account (Settings → SSH and GPG keys)
3. Copy the SSH URL from the repository page

The SSH URL will look like:
```text
git@github.com:username/repository-name.git
```

#### Step 2: Configure Git Remote

When adding the remote, you'll need to update the host to match the label used in your `~/.ssh/config` file.

**Original SSH URL:**
```text
git@github.com:AI-Adoption-Prototyping/basic-chatbot-poc.git
```

**Updated URL with SSH alias:**
```text
git@github.com-basic-bot:AI-Adoption-Prototyping/basic-chatbot-poc.git
```

!!! tip "SSH Alias Usage"

    Replace `github.com` with your SSH config alias (e.g., `github.com-basic-bot`) to use the correct SSH key for authentication.

#### Step 3: Initialize and Connect Repository

Navigate to your project directory and initialize Git:

```bash
cd /path/to/project/directory
git init
git remote add origin git@github.com-basic-bot:AI-Adoption-Prototyping/basic-chatbot-poc.git
git fetch origin
git branch -M main
git push -u origin main
```

**Command Breakdown:**

- `git init` - Initialize a new Git repository
- `git remote add origin <url>` - Add the remote repository
- `git fetch origin` - Fetch remote branches and tags
- `git branch -M main` - Rename current branch to `main`
- `git push -u origin main` - Push to remote and set upstream tracking

!!! success "Repository Ready"

    You should now have Git ready for use and connected. No repository files have been added yet, so you'll start adding files now.

### Initial Setup Best Practices

After connecting your repository, follow these steps to get started properly:

1. **Create `.gitignore`** - Add a `.gitignore` file to exclude unnecessary files
2. **Commit `.gitignore`** - Commit and push the `.gitignore` file first
3. **Add project files** - Add your project files in logical commits
4. **Write clear commit messages** - Use descriptive commit messages

!!! example "Starting with .gitignore"

    I suggest starting with a `.gitignore` file, committing it, and pushing to get started. This ensures you don't accidentally commit files that shouldn't be version controlled.

## Best Practices

### Commit Messages

**Write clear, descriptive commit messages:**

- Use imperative mood ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Add detailed explanation in the body if needed
- Reference issues or tickets when applicable

### Branch Strategy

- Use feature branches for new work
- Keep `main` branch stable and deployable
- Use descriptive branch names
- Delete merged branches to keep the repository clean

### Regular Commits

- Commit frequently with logical, atomic changes
- Don't commit broken code
- Test before committing
- Review changes with `git diff` before committing

!!! warning "Don't Commit Sensitive Information"

    Never commit passwords, API keys, or other sensitive information. Use environment variables or configuration files that are excluded via `.gitignore`.
