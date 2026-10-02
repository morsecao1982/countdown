#!/usr/bin/env python3
"""
One-shot launcher: tells the Chromecast to run the countdown page as a
registered Custom Receiver app. Run this once; after it launches, the
Chromecast fetches and runs the page entirely on its own (from
https://countdown-one-flame.vercel.app/), so the computer can be shut
down immediately after.

Usage:
    python3 launch.py
"""

import sys
import time

import pychromecast

APP_ID = "09EBFFA8"
DEVICE_NAME = "Living Room TV"


def main():
    print(f"Discovering Chromecast '{DEVICE_NAME}'...")
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=[DEVICE_NAME]
    )

    if not chromecasts:
        print(f"Could not find a Chromecast named '{DEVICE_NAME}' on this network.")
        print("Double-check it's powered on and on the same Wi-Fi as this computer.")
        sys.exit(1)

    cast = chromecasts[0]
    cast.wait()

    # disableIdleTimeout means the app never auto-terminates, so re-launching
    # the same App ID while it's already running just refocuses the existing
    # session instead of reloading the page — any code changes since the
    # last launch would silently not show up. Force a real stop first so
    # every run of this script is a guaranteed-fresh page load.
    if cast.status.app_id == APP_ID:
        print("App already running — quitting it first to force a fresh reload...")
        cast.quit_app()
        time.sleep(5)

    print(f"Launching app {APP_ID}...")
    cast.start_app(APP_ID)

    # Give it a moment to confirm the launch before we exit.
    time.sleep(3)
    print(f"Launched. Current app on device: {cast.status.display_name}")
    print("You can now safely shut down this computer.")

    pychromecast.discovery.stop_discovery(browser)


if __name__ == "__main__":
    main()
