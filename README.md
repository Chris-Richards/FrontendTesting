# UI Testing Framework

This repo is a work in progress for quickly getting screenshots of the RapidStorV2 booking system to check new changes across multiple websites we embed the script on.

In the future the goal is to have this application run through a set of automatic tests for the UI/UX and to conduct a series of usability tests on any of our websites.

## Installation

```pip install selenium```

## Usage

Populate the urls array with the desired urls you want to test, make sure these aren't password protected and don't require some user interraction to view the RapidStorV2 application.

```python main.py```

## Writing Tests

Tests are built via JSON file in the tests directory. The limited documentation on how these tests work is below.

I have attempted to use an event based system. Each test file contains a single array of objects (events) in order of execution

### Event Objects

Event objects are made up of a few different items right now, with expansion somewhat taken into consideration but not really.

The available event types and what they do is below:

- ```target_div``` Sets the div element that you want to target for screenshots. This uses a HTML ID tag. Other attributes not supported yet.
- ```find``` Finds an element in the driver. Only 'button' is supported right now.
- ```click``` Clicks the selected button element
- ```screenshot``` Takes a screenshot of the instances set div

## TODO / Feature Ideas

- Better documentation
- Extract key functionality out into a reusable class.
- Build some more in depth UI/UX testing functionality boilerplate outside of just screenshots.
- Figma layout overlay to compare design -> production builds.
- Extrapolate this framework out to support generic testing rather than specifically set steps. Maybe something like a json object that you build a test in by targeting element IDs. Not sure yet.
- Somehow integrate this into github actions to prevent merging of branches into production without a passed test.
- Multi browser capability, currently only supports Firefox but ideally it could run Firefox, Safari and Chrome.