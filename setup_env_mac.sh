#!/bin/bash
#
# setup_env_mac.sh
#
# One-time setup script for macOS to persist Bitwarden secrets as environment variables.
#
# This script exports all secrets from the specified Bitwarden project into a
# file at ``$HOME/.terass/terass.env`` in KEY=VALUE format and configures your
# shell to source this file automatically.  After running, restart your
# terminal session to pick up the new environment variables.

set -euo pipefail

# Verify necessary environment variables exist
if [[ -z "${BWS_ACCESS_TOKEN:-}" ]]; then
  echo "BWS_ACCESS_TOKEN environment variable is not set. Exiting." >&2
  exit 1
fi

PROJECT_ID="${BWS_PROJECT_ID:-}"
if [[ -z "$PROJECT_ID" ]]; then
  echo "BWS_PROJECT_ID environment variable is not set and no project ID provided. Exiting." >&2
  exit 1
fi

# Create a directory for storing the env file
ENV_DIR="$HOME/.terass"
mkdir -p "$ENV_DIR"
ENV_FILE="$ENV_DIR/terass.env"

# Export secrets from Bitwarden as KEY=VALUE lines
echo "Exporting secrets to $ENV_FILE..."
bws secret list --project-id "$PROJECT_ID" --output json \
  | jq -r '.[] | "\(.key)=\(.value)"' > "$ENV_FILE"

# Append sourcing logic to common shell RC files if not already present
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
  if [[ -f "$rc" ]]; then
    if ! grep -q "source \"$ENV_FILE\"" "$rc"; then
      {
        echo ""
        echo "# Load TERASS environment variables on shell start"
        echo "if [ -f \"$ENV_FILE\" ]; then"
        echo "  set -a"
        echo "  source \"$ENV_FILE\""
        echo "  set +a"
        echo "fi"
      } >> "$rc"
      echo "Updated $rc to source $ENV_FILE"
    fi
  fi
done

echo "All secrets exported. Restart your terminal session to apply the new variables."
