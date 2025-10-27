# Commit from Issue Comment Workflow

## Overview

This GitHub Actions workflow allows you to commit files directly from issue comments or through manual dispatch. It's designed to provide a safe, auditable path for adding files to the repository.

## Usage

### Method 1: Issue Comment

Post a comment on any issue with a fenced code block in this format:

````markdown
```file name=path/to/your/file.txt
Your file content goes here.
Multiple lines are supported.
```
````

The workflow will:
1. Parse the comment for file blocks
2. Extract the file path and content
3. Create the file (and any necessary directories)
4. Commit and push the changes
5. Comment back on the issue with the commit status

### Method 2: Manual Dispatch

1. Go to **Actions** → **Commit File from Issue Comment**
2. Click **Run workflow**
3. Enter the issue number to process
4. The workflow will process the latest comment on that issue

## File Format

- Use triple backticks with `file` and `name=` parameter
- The `file` keyword is optional but recommended for clarity
- Path can include directories (they'll be created automatically)
- Multiple files can be committed from a single comment

### Examples

#### Single File
````markdown
```file name=docs/new-document.md
# New Document

This is the content of the new document.
```
````

#### Multiple Files
````markdown
```file name=src/utils/helper.py
def helper_function():
    return "Hello"
```

```file name=tests/test_helper.py
def test_helper():
    assert helper_function() == "Hello"
```
````

#### Different Extensions
````markdown
```file name=config/settings.json
{
  "key": "value",
  "number": 42
}
```
````

## Workflow Permissions

The workflow requires the following permissions:
- `contents: write` - To create and commit files
- `issues: read` - To read issue comments
- `pull-requests: write` - To comment on issues

These permissions are explicitly declared in the workflow file.

## Repository Compatibility

- Works with the default `GITHUB_TOKEN`
- No additional secrets required
- Compatible with existing repository workflows
- Only processes issue comments (not PR comments)

## Security Considerations

- Only commits files specified in the comment
- Creates a clear audit trail with commit messages referencing the issue
- Comments back on the issue for transparency
- Uses bot account for commits: `github-actions[bot]`

## Troubleshooting

### No file blocks found
If you see "No file blocks found in comment", ensure:
- You're using triple backticks (\`\`\`)
- The `name=` parameter is on the same line as the opening backticks
- There's a newline between the opening backticks and the file content

### Workflow didn't trigger
- Check that the comment was on an issue (not a PR)
- Verify the workflow file is on the default branch
- Check the Actions tab for any error messages

## Example Comment

Here's a complete example comment that would create a new file:

````markdown
Hi! Please add this new configuration file:

```file name=config/app-settings.yml
app_name: TERASS-ADVISER
version: 1.0.0
features:
  - loan_checker
  - picks_integration
```

This will be used for application configuration.
````
