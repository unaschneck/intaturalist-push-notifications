# intaturalist-push-notifications
[![retrieve-observations](https://github.com/unaschneck/intaturalist-push-notifications/actions/workflows/observation_reporter.yml/badge.svg)](https://github.com/unaschneck/intaturalist-push-notifications/actions/workflows/observation_reporter.yml)

Receive push notifications on an phone or desktop for a given user's newest identifications

## How it Works

- [pyinaturalist]((https://github.com/pyinat/pyinaturalist): Python client to collect observations based on username
- [GitHub Actions](https://github.com/unaschneck/intaturalist-push-notifications/blob/main/.github/workflows/observation_reporter.yml): Schedule how often observations are collected and sent
- [ntfy:](https://github.com/binwiederhier/ntfy) Sends push notifications to a Phone/Desktop

## How to Setup

Set [INaturalist username](https://www.inaturalist.org/) and [ntfy topic](https://github.com/binwiederhier/ntfy) as a Github Secret

Add lines for each INaturalist username at the end of the [`observation_reporter.yml`](https://github.com/unaschneck/intaturalist-push-notifications/blob/main/.github/workflows/observation_reporter.yml)

```
# Username (example: EXAMPLE_USERNAME) and NTFY (example: EXAMPLE_NTFY) stored in secrets 

python notifications_for_user.py ${{ secrets.EXAMPLE_USERNAME }} ${{ secrets.EXAMPLE_NTFY }} ${{ env.LAST_CREATED_AT }} 

```

Github Action scheduled to retrieve recent observations on a [schedule during (day) UTC time](https://github.com/unaschneck/intaturalist-push-notifications/blob/3dd82fec933843d7758cf164732c0a8cbec6f633/.github/workflows/observation_reporter.yml)

Currently scheduled to check for new observations every ten minutes during UTC North American Daytime. 

Note: Github Actions do not always run exactly every ten minutes (depends on internal Github Runner), but the observations will be collected from when the last collection of observations were collected.

```
*/10 16-23,0-2 * * *
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
