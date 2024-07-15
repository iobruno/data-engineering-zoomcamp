import operator as op
from functools import reduce
from typing import Any, Dict

import dlt
import httpx
from pipe import groupby, map, select, tee

releases_endpoint = "https://api.github.com/repos/{owner}/{repo}/releases"


@dlt.source
def releases(owner: str, repo: str):

    @dlt.resource
    def fetch_all():
        endpoint = releases_endpoint.format(owner=owner, repo=repo)
        response = httpx.get(endpoint)
        response.raise_for_status()
        yield response.json()

    @dlt.transformer(data_from=fetch_all)
    def download_links_group_by(raw_json: Any, key: str) -> Dict:
        yield (
            raw_json
            | groupby(lambda grouping: grouping[key])
            | map(lambda g: {g[0]: list(g[1])[0].get('assets')})
            | map(lambda kv: {k: parse_download_link(v) for k, v in kv.items()})
        )

    def parse_download_link(mapping):
        return list(mapping | select(lambda item: item.get('browser_download_url')))

    return [fetch_all, download_links_group_by]
