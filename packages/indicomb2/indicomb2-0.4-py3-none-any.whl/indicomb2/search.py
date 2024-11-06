import argparse
import os
import urllib
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
import yaml

from indicomb2.markdown import Markdown
from indicomb2.requests import BearerAuth

BASE_URL = "/search/api/search"
SITE = "https://indico.cern.ch"
API_TOKEN = os.environ.get("INDICO_API_TOKEN", None)
DEFAULT_KWARGS = {"site": SITE, "api_token": API_TOKEN}
DEFAULT_PARAMS = {
    "category": "ATLAS Meetings",
    "sort": "mostrecent",
    "type": "contribution",
    "years": 1,
}


def request(site: str, url: str, params: dict, api_token: str):
    items = list(params.items()) if hasattr(params, "items") else list(params)
    items = sorted(items, key=lambda x: x[0].lower())
    url = f"{site}{url}?{urllib.parse.urlencode(items)}"
    response = requests.get(url, auth=BearerAuth(api_token), timeout=30)
    response.encoding = response.apparent_encoding
    response.raise_for_status()
    return response.json()


def search(params, kwargs):
    req = request(url=BASE_URL, params=params, **kwargs)
    pages = req["pages"]
    results = req["results"]
    for page in range(2, pages + 1):
        params["page"] = page
        req = request(url=BASE_URL, params=params, **kwargs)
        results += req["results"]
    return results


def make_table(results, target):
    # get data
    data = {"Date": [], "Title": [], "Speakers": []}
    for r in results:
        url = f"{SITE}{r['url']}"
        date = datetime.fromisoformat(r["start_dt"]).strftime("%Y-%m-%d")
        data["Date"].append(f"[{date}]({url})")
        data["Title"].append(r["title"])
        data["Speakers"].append(", ".join(p["name"] for p in r["persons"]))

    # create table
    md = Markdown()
    md += "\n"
    md += md.header("Meeting Contributions", level=2)
    md += md.table(data)

    # write table
    target = Path(target)
    with target.open("a") as f:
        f.write(str(md))


def get_start_range(years: int = 1):
    end_date = (datetime.now(tz=timezone.utc).date() + timedelta(days=30)).isoformat()
    start_date = (datetime.now(tz=timezone.utc).date() - timedelta(days=365 * years)).isoformat()
    return f"[{start_date} TO {end_date}]"


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        type=str,
        help="Path to the config file",
    )
    args = parser.parse_args(args)

    with Path(args.config).open() as f:
        config = yaml.safe_load(f)

    for cfg in config["search"]:
        params = {**DEFAULT_PARAMS, **cfg["params"]}
        params["start_range"] = get_start_range(params.pop("years"))
        results = search(params, DEFAULT_KWARGS)
        make_table(results, cfg["target"])


if __name__ == "__main__":
    main()
