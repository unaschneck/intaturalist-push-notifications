# intaturalist-push-notifications
[![retrieve-observations](https://github.com/unaschneck/intaturalist-push-notifications/actions/workflows/observation_reporter.yml/badge.svg)](https://github.com/unaschneck/intaturalist-push-notifications/actions/workflows/observation_reporter.yml)

Receive push notifications on an iPhone for user's newest identifications

## How it Works

- pyinaturalist
- ntfy
- GitHub Actions

Github Action scheduled to retrieve recent observations on a [schedule during (day) UTC time](https://github.com/unaschneck/intaturalist-push-notifications/blob/3dd82fec933843d7758cf164732c0a8cbec6f633/.github/workflows/observation_reporter.yml#L5)

Each observation since previous check is sent as an individual observation to the nfty topic

## How to Setup

Set [INaturalist username](https://www.inaturalist.org/) and [ntfy topic](https://github.com/binwiederhier/ntfy) as a Github Secret

Add lines for each INaturalist username at the end of the [`observation_reporter.yml`](https://github.com/unaschneck/intaturalist-push-notifications/blob/main/.github/workflows/observation_reporter.yml)

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
