# Jellyvision Programming Exercise

As Jellyvision, we would like visibility into engineering activity so that we can track development trends across projects.

We want to consume GitHub’s public API and compute how active a user is in open-source projects.

Despite what the [REST API endpoints for events - GitHub Docs](https://docs.github.com/en/rest/activity/events) suggests, no API key or bearer token is required to fetch public
repo activity.

## Acceptance Criteria
- Write a program to access GitHub’s public API for a user (ie ge0ffrey )
- For each repo that the user has contributed to recently:
  - Find their 3 most common activity types. (e.g. commits, pull requests, comments, merges…)
  - Within that recent activity, flag any repos that the user owns.
