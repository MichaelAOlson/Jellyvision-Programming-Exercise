# Jellyvision Programming Exercise

## Overview
As Jellyvision, we would like visibility into engineering activity so that we can track development trends across projects.

We want to consume GitHub’s public API and compute how active a user is in open-source projects.

Despite what the [REST API endpoints for events - GitHub Docs](https://docs.github.com/en/rest/activity/events) suggests, no API key or bearer token is required to fetch public
repo activity.

### Acceptance Criteria
- Write a program to access GitHub’s public API for a user (ie ge0ffrey )
- For each repo that the user has contributed to recently:
  - Find their 3 most common activity types. (e.g. commits, pull requests, comments, merges…)
  - Within that recent activity, flag any repos that the user owns.

## How to run
1. Install the `uv` tool if you don't have it already
2. Update src/main.py with the desired GitHub username
3. Run:
  ```bash
  uv sync
  uv run src/main.py
  ```

A nice-to-have would be to extend this to provide a CLI interface to specify the GitHub username as an argument using something like Argparse

Another nice-to-have would be to sleep/retry GitHub API calls to avoid rate limiting.

## Run tests
To run the tests, use the following command:
```bash
pytest
```
or alternatively using `uv`:
```bash
uv run pytest
```

## Formatting/linting
To run code formatting and linting, run the following:
```bash
ruff format
ruff check --fix
```
