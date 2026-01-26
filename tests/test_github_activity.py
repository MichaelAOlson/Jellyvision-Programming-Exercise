import pytest

from unittest.mock import patch, MagicMock
from github_activity import (
    fetch_user_activity,
    get_user_owned_repos_from_recent_activities,
    calc_n_most_common_activities,
)


class TestFetchUserActivity:
    def test_fetch_user_activity_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            [{"type": "PushEvent", "repo": {"name": "user/repo1"}}],
            [{"type": "PullRequestEvent", "repo": {"name": "user/repo2"}}],
            [],
        ]

        with patch("requests.get", return_value=mock_response):
            activities = list(fetch_user_activity("testuser", n_activities=30))
            assert len(activities) == 2
            assert activities[0]["type"] == "PushEvent"

    def test_fetch_user_activity_empty_username(self):
        with pytest.raises(ValueError, match="Invalid GitHub username"):
            list(fetch_user_activity(""))

    def test_fetch_user_activity_invalid_username_format(self):
        with pytest.raises(ValueError, match="Invalid GitHub username"):
            list(fetch_user_activity("user-"))

    def test_fetch_user_activity_http_error(self):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.content = b"Not Found"

        with patch("requests.get", return_value=mock_response):
            with pytest.raises(Exception, match="Failed to fetch data"):
                list(fetch_user_activity("nonexistent"))

    def test_fetch_user_activity_multiple_pages(self):
        """Even if we only get two results at a time, it will keep going until n_activities is met"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            [{"type": "PushEvent", "repo": {"name": "user/repo1"}}],
            [{"type": "PullRequestEvent", "repo": {"name": "user/repo2"}}],
        ]

        with patch("requests.get", return_value=mock_response):
            activities = list(fetch_user_activity("testuser", n_activities=30))
            assert len(activities) == 30

    def test_fetch_user_activity_n_activities_zero(self):
        with patch("requests.get") as mock_get:
            activities = list(fetch_user_activity("testuser", n_activities=0))
            assert len(activities) == 0
            mock_get.assert_not_called()

    def test_fetch_user_activity_n_activities_negative(self):
        with pytest.raises(ValueError, match="num_activities must be positive"):
            list(fetch_user_activity("testuser", n_activities=-5))

    def test_fetch_user_activity_exact_match(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"type": "PushEvent", "repo": {"name": "user/repo1"}},
            {"type": "PushEvent", "repo": {"name": "user/repo2"}},
            {"type": "PushEvent", "repo": {"name": "user/repo3"}},
        ]

        with patch("requests.get", return_value=mock_response):
            activities = list(fetch_user_activity("testuser", n_activities=2))
            assert len(activities) == 2

    def test_fetch_user_activity_empty_response(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        with patch("requests.get", return_value=mock_response):
            activities = list(fetch_user_activity("testuser", n_activities=10))
            assert len(activities) == 0


class TestGetUserOwnedReposFromRecentActivities:
    def test_get_user_owned_repos_success(self):
        activities = [
            {"repo": {"name": "testuser/repo1"}},
            {"repo": {"name": "testuser/repo2"}},
            {"repo": {"name": "other/repo3"}},
        ]
        result = get_user_owned_repos_from_recent_activities("testuser", activities)
        assert result == {"testuser/repo1", "testuser/repo2"}

    def test_get_user_owned_repos_empty_activities(self):
        result = get_user_owned_repos_from_recent_activities("testuser", [])
        assert result == set()

    def test_get_user_owned_repos_no_matching_repos(self):
        activities = [
            {"repo": {"name": "other/repo1"}},
            {"repo": {"name": "another/repo2"}},
        ]
        result = get_user_owned_repos_from_recent_activities("testuser", activities)
        assert result == set()

    def test_get_user_owned_repos_duplicate_repos(self):
        activities = [
            {"repo": {"name": "testuser/repo1"}},
            {"repo": {"name": "testuser/repo1"}},
        ]
        result = get_user_owned_repos_from_recent_activities("testuser", activities)
        assert result == {"testuser/repo1"}

    def test_get_user_owned_repos_invalid_username_format(self):
        with pytest.raises(ValueError, match="Invalid GitHub username"):
            get_user_owned_repos_from_recent_activities("user-", [])


class TestCalcNMostCommonActivities:
    def test_calc_n_most_common_activities_success(self):
        activities = [
            {"type": "PushEvent"},
            {"type": "PushEvent"},
            {"type": "PullRequestEvent"},
            {"type": "IssueEvent"},
        ]
        result = calc_n_most_common_activities(2, activities)
        assert result == [("PushEvent", 2), ("PullRequestEvent", 1)]

    def test_calc_n_most_common_activities_empty_activities(self):
        result = calc_n_most_common_activities(3, [])
        assert result == []

    def test_calc_n_most_common_activities_n_exceeds_types(self):
        activities = [
            {"type": "PushEvent"},
            {"type": "PullRequestEvent"},
        ]
        result = calc_n_most_common_activities(5, activities)
        assert len(result) == 2
        assert result[0][0] in ["PushEvent", "PullRequestEvent"]

    def test_calc_n_most_common_activities_single_type(self):
        activities = [
            {"type": "PushEvent"},
            {"type": "PushEvent"},
        ]
        result = calc_n_most_common_activities(1, activities)
        assert result == [("PushEvent", 2)]

    def test_calc_n_most_common_activities_n_zero(self):
        activities = [
            {"type": "PushEvent"},
            {"type": "PushEvent"},
        ]
        result = calc_n_most_common_activities(0, activities)
        assert result == []

    def test_calc_n_most_common_activities_all_same_type(self):
        activities = [
            {"type": "PushEvent"},
            {"type": "PushEvent"},
            {"type": "PushEvent"},
        ]
        result = calc_n_most_common_activities(1, activities)
        assert result == [("PushEvent", 3)]
