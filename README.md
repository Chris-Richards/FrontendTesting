# UI Testing Framework

This repo is a work in progress for quickly getting screenshots of the RapidStorV2 booking system to check new changes across multiple websites we embed the script on.

In the future the goal is to have this application run through a set of automatic tests for the UI/UX and to conduct a series of usability tests on any of our websites.

## Installation

```pip install selenium```

## Usage

Populate the urls array with the desired urls you want to test, make sure these aren't password protected and don't require some user interraction to view the RapidStorV2 application.

```python main.py```

## TODO / Feature Ideas

- Extract key functionality out into a reusable class.
- Build some more in depth UI/UX testing functionality boilerplate outside of just screenshots.
- Figma layout overlay to compare design -> production builds.
- Extrapolate this framework out to support generic testing rather than specifically set steps. Maybe something like a json object that you build a test in by targeting element IDs. Not sure yet.
- Somehow integrate this into github actions to prevent merging of branches into production without a passed test.