import re
from typing import Generator, Counter

import requests

# AI-build regex for GitHub usernames based on GitHub's rules
GITHUB_USERNAME_REGEX = re.compile(
    r"^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,37}[a-zA-Z0-9]$"
)


def validate_github_username(username: str) -> bool:
    if not username:
        return False
    match = re.fullmatch(GITHUB_USERNAME_REGEX, username)
    return bool(match)


def fetch_user_activity(
    username: str,
    n_activities: int = 100,
) -> Generator[dict]:
    if not validate_github_username(username):
        raise ValueError("Invalid GitHub username")

    if n_activities == 0:
        return
    if n_activities < 0:
        raise ValueError("num_activities must be positive")

    activities_count = 0
    page = 1
    while activities_count < n_activities:
        resp = requests.get(
            f"https://api.github.com/users/{username}/events",
            params={"page": page},
        )
        if resp.status_code != 200:
            raise Exception(
                f"Failed to fetch data (HTTP {resp.status_code}): {resp.content}"
            )
        activities_page = resp.json()
        num_activities_on_page = len(activities_page)
        if not num_activities_on_page:
            break

        # Do not over-serve activities, even if we have over-fetched
        if activities_count + num_activities_on_page >= n_activities:
            yield from activities_page[: n_activities - activities_count]
            break

        activities_count += num_activities_on_page

        yield from activities_page

        page += 1


def get_user_owned_repos_from_recent_activities(
    username: str, activities: list[dict]
) -> set[str]:
    if not validate_github_username(username):
        raise ValueError("Invalid GitHub username")
    return {
        repo_name
        for a in activities
        if (repo_name := a["repo"]["name"]).startswith(f"{username}/")
    }


def calc_n_most_common_activities(
    n: int, activities: list[dict]
) -> list[tuple[str, int]]:
    return Counter([activity["type"] for activity in activities]).most_common(n)
