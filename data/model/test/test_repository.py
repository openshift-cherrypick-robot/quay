import os
from datetime import timedelta

import pytest

from data.database import BlobUpload, Repository
from data.model.repository import (
    create_repository,
    get_estimated_repository_count,
    get_filtered_matching_repositories,
    get_size_during_upload,
)
from data.model.storage import get_image_location_for_name
from test.fixtures import *


def test_duplicate_repository_different_kinds(initialized_db):
    # Create an image repo.
    assert create_repository("devtable", "somenewrepo", None, repo_kind="image")

    # Try to create an app repo with the same name, which should fail.
    assert not create_repository("devtable", "somenewrepo", None, repo_kind="application")


@pytest.mark.skipif(
    os.environ.get("TEST_DATABASE_URI", "").find("mysql") >= 0,
    reason="MySQL requires specialized indexing of newly created repos",
)
@pytest.mark.parametrize(
    "query",
    [
        (""),
        ("e"),
    ],
)
@pytest.mark.parametrize(
    "authed_username",
    [
        (None),
        ("devtable"),
    ],
)
def test_search_pagination(query, authed_username, initialized_db):
    # Create some public repos.
    repo1 = create_repository(
        "devtable", "somenewrepo", None, repo_kind="image", visibility="public"
    )
    repo2 = create_repository(
        "devtable", "somenewrepo2", None, repo_kind="image", visibility="public"
    )
    repo3 = create_repository(
        "devtable", "somenewrepo3", None, repo_kind="image", visibility="public"
    )

    repositories = get_filtered_matching_repositories(query, filter_username=authed_username)
    assert len(repositories) > 3

    next_repos = get_filtered_matching_repositories(
        query, filter_username=authed_username, offset=1
    )
    assert repositories[0].id != next_repos[0].id
    assert repositories[1].id == next_repos[0].id


def test_get_estimated_repository_count(initialized_db):
    assert get_estimated_repository_count() >= Repository.select().count()


def test_get_size_during_upload(initialized_db):
    upload_size = 100
    repo1 = create_repository(
        "devtable", "somenewrepo", None, repo_kind="image", visibility="public"
    )
    location = get_image_location_for_name("local_us")
    BlobUpload.create(
        repository=repo1.id,
        uuid="123",
        storage_metadata="{}",
        byte_count=upload_size,
        location=location.id,
    )
    size = get_size_during_upload(repo1.id)
    assert size == upload_size
