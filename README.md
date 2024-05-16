# intaturalist-push-notifications
[![retrieve-observations](https://github.com/unaschneck/intaturalist-push-notifications/actions/workflows/observation_reporter.yml/badge.svg)](https://github.com/unaschneck/intaturalist-push-notifications/actions/workflows/observation_reporter.yml)

Receive push notifications on an iPhone for user's newest identifications

## How it Works

- [pyinaturalist: Python client to collect observations based on username](https://github.com/pyinat/pyinaturalist)
- [GitHub Actions: Schedule how often observations are collected and sent](https://github.com/unaschneck/intaturalist-push-notifications/blob/main/.github/workflows/observation_reporter.yml)
- [ntfy: Sends push notifications to a Phone/Desktop](https://github.com/binwiederhier/ntfy)

## How to Setup

Set [INaturalist username](https://www.inaturalist.org/) and [ntfy topic](https://github.com/binwiederhier/ntfy) as a Github Secret

Add lines for each INaturalist username at the end of the [`observation_reporter.yml`](https://github.com/unaschneck/intaturalist-push-notifications/blob/main/.github/workflows/observation_reporter.yml)

```
# Username (example: EXAMPLE_USERNAME) and NTFY (example: EXAMPLE_NTFY) stored in secrets 

python notifications_for_user.py ${{ secrets.EXAMPLE_USERNAME }} ${{ secrets.EXAMPLE_NTFY }} ${{ env.LAST_CREATED_AT }} 

```

Github Action scheduled to retrieve recent observations on a [schedule during (day) UTC time](https://github.com/unaschneck/intaturalist-push-notifications/blob/3dd82fec933843d7758cf164732c0a8cbec6f633/.github/workflows/observation_reporter.yml)

Currently scheduled to check for new observations every ten minutes from 15-2 hours UTC (North American Daytime). Note: Github Actions do not always run exactly every ten minutes (depends on internal Github Runner). But the observations will be collected from the last time a workflow was run.

```
*/10 15-23,0-1 * * *
```

Each observation since previous check is sent as an individual observation to the nfty topic

## Development Environment

To run or test against `intaturalist-push-notifications` github repo/fork, a development environment can be created via conda/miniconda

First, [install Miniconda](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html)

Then, using the existing `environment.yml`, a new conda environment can be create to run/test scripts against

```
conda env create --file environment.yml
```
Once the environment has been built, activate the environment:
```
conda activate push_notifications
```
