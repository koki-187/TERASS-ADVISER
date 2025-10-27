# Secrets Management Guide

This guide explains how to manage secret information like API keys and passwords safely when working on the TERASS業動サポートAI project.

## What are secrets?

Secrets are sensitive pieces of information such as API keys, access tokens, login credentials, or passwords. Never share secrets publicly or store them in your code repository. Instead, load them securely using environment variables and a secrets manager.

## Why use Bitwarden?

We use [Bitwarden](https://bitwarden.com/help/) because it provides a secure vault for storing and managing secrets. Bitwarden Secrets Manager allows you to inject secrets as environment variables at run time without writing them to disk.

### Setting up Bitwarden CLI

If you have not installed the Bitwarden CLI:

- Download the CLI from the Bitwarden website.
- Log in with your Bitwarden account using `bws login`.
- Create a project in Bitwarden Secrets Manager for your development environment.

## Renaming secret keys

When creating secrets, choose simple keys containing only letters, numbers, and underscores. This ensures they can be used as environment variable names. For example:

- Instead of `ChatGPTのAPIキー`, use `OPENAI_API_KEY`.
- Instead of `私の秘密-PW`, use `DATABASE_PASSWORD`.

If you already have secrets with non‑ASCII names, you can rename them:

```bash
bws secret edit <secret-id> --key NEW_KEY_NAME
```

You can find the secret ID using `bws secret list`. Replace `<secret-id>` and `NEW_KEY_NAME` with your values.

Alternatively, you can run your application with the `--uuids-as-keynames` option to use the secret UUIDs as environment variable names.

## Injecting secrets when running locally

To run the application locally with secrets:

```bash
# Replace <PROJECT_ID> with your Bitwarden project ID
bws run --project-id <PROJECT_ID> -- python terass_assistant_with_scenarios.py
```

The `bws run` command will export all the secrets in your project as environment variables. Your code should read the values using `os.environ.get("OPENAI_API_KEY")` or a similar function.

### Tip for beginners

- **Terminal** (or Command Prompt/PowerShell) is an application where you type commands. On Windows, you can search for “PowerShell.” On Mac, open “Terminal” from the Applications → Utilities folder.
- The `--project-id` is a unique identifier for your Bitwarden Secrets Manager project. You can find it in the Bitwarden web interface.

## Using secrets in GitHub Actions

Do not commit secrets to the repository. Instead, add secrets to your GitHub repository settings:

1. Go to your repository on GitHub → **Settings → Secrets and variables → Actions**.
2. Click **New repository secret**.
3. Enter a name (e.g., `OPENAI_API_KEY`) and paste the secret value from Bitwarden.

These secrets will be available to GitHub Actions workflows during CI builds.

## Do not commit `.env` files

A `.env` file contains environment variable definitions. If you create such a file for local development, add it to `.gitignore` so that it is never committed. Instead, provide an example file called `.env.example` that lists the required variable names but not the values.

---

By following these guidelines, you can keep your secrets safe and avoid accidental exposure. If you are unsure about any step, consult the [Bitwarden help documentation](https://bitwarden.com/help/) or ask a team member for assistance.
