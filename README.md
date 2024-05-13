# intaturalist-push-notifications
[![retrieve-observations](https://github.com/unaschneck/intaturalist-push-notifications/actions/workflows/observation_reporter.yml/badge.svg)](https://github.com/unaschneck/intaturalist-push-notifications/actions/workflows/observation_reporter.yml)

Receive push notifications on an iPhone for user's newest identifications

## How it Works

- pyinaturalist
- ntfy
- GitHub Actions

## How to Setup

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
