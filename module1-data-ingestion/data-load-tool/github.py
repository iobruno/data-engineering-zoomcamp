import dlt
import httpx
from typing import List, Dict
from itertools import groupby

releases_endpoint = "https://api.github.com/repos/{owner}/{repo}/releases"


@dlt.resource
def fetch_releases_from(owner: str, repo: str) -> List[Dict]:
    endpoint = releases_endpoint.format(owner=owner, repo=repo)
    response = httpx.get(endpoint)
    response.raise_for_status()
    yield response.json()


@dlt.resource
def fetch_releases_from_grouping_by(owner: str, repo: str, group_key: str) -> Dict:
    raw_json = fetch_releases_from(owner=owner, repo=repo)
    yield {
        group_key: list(artifacts)[0]
        for group_key, artifacts in groupby(raw_json, lambda key: key[group_key])
    }
