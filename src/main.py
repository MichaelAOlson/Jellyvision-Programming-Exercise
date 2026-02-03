from collections import defaultdict

from github_activity import (
    fetch_user_activity,
)


def challenge(usernames: list[str]):
    user_push_events = defaultdict(int)
    for username in usernames:
        activities = list(fetch_user_activity(username))
        print(f"Fetched {len(activities)} recent activities for user '{username}'")

        for activity in activities:
            if activity["type"] == "PushEvent":
                user_push_events[username] += 1

        # user_owned_repos = get_user_owned_repos_from_recent_activities(username, activities)
        # print(f"User-owned repos from recent activities: {user_owned_repos}")

        # print("User's most common recent activities:")
        # for activity, count in calc_n_most_common_activities(3, activities):
        #     print(f"{activity} ({count} times)")
    print(
        f"Ranked users by push event count: {list(sorted(user_push_events.items(), key=lambda item: item[1], reverse=True))}"
    )


if __name__ == "__main__":
    usernames = ["ge0ffrey", "MichaelAOlson", "torvalds"]
    challenge(usernames)


# Users table:
# id | username | activity | date
# Repos table:
# repo | user_id
