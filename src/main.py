from github_activity import (
    fetch_user_activity,
    get_user_owned_repos_from_recent_activities,
    calc_n_most_common_activities,
)


def main():
    username = "ge0ffrey"
    # username = "MichaelAOlson"
    activities = list(fetch_user_activity(username))
    print(f"Fetched {len(activities)} recent activities for user '{username}'")

    user_owned_repos = get_user_owned_repos_from_recent_activities(username, activities)
    print(f"User-owned repos from recent activities: {user_owned_repos}")

    print("User's most common recent activities:")
    for activity, count in calc_n_most_common_activities(3, activities):
        print(f"{activity} ({count} times)")


if __name__ == "__main__":
    main()
