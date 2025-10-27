# GitHub Deployment Guide

This document explains how to set up and deploy the TERASS業動サポートAI project to GitHub. It is written for beginners with no prior experience with Git or GitHub.

## What are Git and GitHub?

- **Git** is a version control system that tracks changes to files so you can revert to previous versions and collaborate with others.
- **GitHub** is a web service that hosts Git repositories online. It provides tools for collaboration, such as pull requests, issues, and actions for continuous integration.

## 1. Clone the repository

1. Install Git from https://git-scm.com/ and create a GitHub account if you do not have one.
2. Open a terminal (macOS/Linux) or PowerShell (Windows).
3. Run the following command to download the repository to your computer:

```
git clone https://github.com/koki-187/TERASS-ADVISER.git
```

This creates a folder named `TERASS-ADVISER` on your computer.

## 2. Working with branches

It is best practice to create a new branch for your changes rather than committing directly to `main`. To create and switch to a new branch:

```
cd TERASS-ADVISER
git checkout -b docs-update
```

Replace `docs-update` with a descriptive name, such as `feature/loan-checker` or `bugfix/typo`.

## 3. Making changes

Edit or create files in your branch as needed. Once you are happy with your changes, stage and commit them:

```
git add path/to/your/file.md
git commit -m "Add deployment guide"
```

Use clear commit messages to describe what you changed.

## 4. Push your changes and open a pull request

Push your branch to GitHub:

```
git push origin docs-update
```

After pushing, open your repository in a web browser. GitHub will show a banner inviting you to "Compare & pull request." Click it, fill in the title and description, and create the pull request. Other members can review your changes before merging them into `main`.

## 5. Deploy keys and access tokens

For CI systems or servers that need to access the repository, generate an SSH deploy key:

1. Run `ssh-keygen -t ed25519 -C "deploy-key"` and follow the prompts.
2. Copy the contents of the generated `.pub` file.
3. On GitHub, go to **Settings → Deploy keys** and click **Add deploy key**. Give it a name and paste the public key.

Alternatively, you can create a personal access token (classic or fine‑grained) from **Settings → Developer settings → Personal access tokens** and use it when authenticating over HTTPS.

## 6. Continuous Integration (CI)

This repository includes GitHub Actions workflows. The file `.github/workflows/terass_build.yml` defines how to build the project and generate distributable packages. These workflows run automatically when you push to certain branches or open a pull request.

To provide secrets to CI workflows:

1. Go to **Settings → Secrets and variables → Actions**.
2. Click **New repository secret**.
3. Add your secret name (e.g., `OPENAI_API_KEY`) and its value.

Never add secrets directly to the code or commit them to the repository.

## 7. Good practices

- Do not commit API keys, passwords, or other secret information. Manage secrets with Bitwarden and inject them at runtime.
- Use the provided `.env.example` file as a template for required environment variables. Do not commit a `.env` file.
- Write meaningful commit messages and branch names.
- Use pull requests for all changes to facilitate code review and maintain a clean history.

---

Following these steps will help you deploy and manage this project on GitHub safely and effectively.
