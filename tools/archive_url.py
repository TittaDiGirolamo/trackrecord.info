#!/usr/bin/env python3
"""
Wayback Machine (Save Page Now) helper for trackrecord.info

Automatically creates (or retrieves) an archive link for a given URL.
Intended to be called during the promote step so every new prediction
gets a mandatory `statement_original_url_archive` field.
"""

from __future__ import annotations

import os
import time
import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)

USER_AGENT = "trackrecord.info-archiver/1.0 (+https://github.com/TittaDiGirolamo/trackrecord.info)"
SAVE_ENDPOINT = "https://web.archive.org/save/"
AVAILABILITY_ENDPOINT = "https://archive.org/wayback/available"
TIMEOUT = 90
MAX_RETRIES = 2


def _get_headers(authenticated: bool = False) -> dict:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    if authenticated:
        access = os.getenv("SAVEPAGENOW_ACCESS_KEY") or os.getenv("INTERNET_ARCHIVE_ACCESS_KEY")
        secret = os.getenv("SAVEPAGENOW_SECRET_KEY") or os.getenv("INTERNET_ARCHIVE_SECRET_KEY")
        if access and secret:
            headers["Authorization"] = f"LOW {access}:{secret}"
    return headers


def _try_fresh_capture(url: str, authenticated: bool = False) -> Optional[str]:
    save_url = f"{SAVE_ENDPOINT}{url}"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(
                save_url,
                headers=_get_headers(authenticated=authenticated),
                allow_redirects=True,
                timeout=TIMEOUT,
            )

            final = resp.url
            if "web.archive.org/web/" in final and url.rstrip("/") in final:
                logger.info("Fresh capture succeeded: %s", final)
                return final

            loc = resp.headers.get("Content-Location") or resp.headers.get("Location")
            if loc and "web.archive.org" in loc:
                if loc.startswith("/"):
                    loc = "https://web.archive.org" + loc
                logger.info("Fresh capture via header: %s", loc)
                return loc

            logger.warning(
                "Save attempt %d returned unexpected response (status %s)",
                attempt, resp.status_code
            )

        except requests.RequestException as e:
            logger.warning("Save attempt %d failed: %s", attempt, e)

        if attempt < MAX_RETRIES:
            time.sleep(3 * attempt)

    return None


def _get_closest_existing(url: str) -> Optional[str]:
    try:
        resp = requests.get(
            AVAILABILITY_ENDPOINT,
            params={"url": url},
            headers={"User-Agent": USER_AGENT},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        closest = data.get("archived_snapshots", {}).get("closest")
        if closest and closest.get("available"):
            archive_url = closest["url"]
            if archive_url.startswith("http://"):
                archive_url = "https://" + archive_url[7:]
            logger.info("Using existing snapshot: %s", archive_url)
            return archive_url
    except Exception as e:
        logger.warning("Availability API failed: %s", e)

    return None


def get_archive_url(url: str, prefer_fresh: bool = True, authenticated: bool = False) -> str:
    if not url or not url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid URL for archiving: {url!r}")

    archive = None

    if prefer_fresh:
        archive = _try_fresh_capture(url, authenticated=authenticated)

    if not archive:
        archive = _get_closest_existing(url)

    if not archive:
        raise RuntimeError(
            f"Could not obtain an archive link for {url}. "
            "Both fresh capture and availability lookup failed."
        )

    return archive


if __name__ == "__main__":
    import argparse
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Archive a URL with the Wayback Machine")
    parser.add_argument("url", help="Live URL to archive")
    parser.add_argument("--no-fresh", action="store_true", help="Skip fresh capture, only use existing")
    parser.add_argument("--auth", action="store_true", help="Use authenticated Save Page Now (env keys)")
    args = parser.parse_args()

    try:
        result = get_archive_url(args.url, prefer_fresh=not args.no_fresh, authenticated=args.auth)
        print(result)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
