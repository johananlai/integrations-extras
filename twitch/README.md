# Agent Check: Twitch

## Overview

This check monitors [Twitch][1].

## Setup

### Installation

The Twitch check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

### Configuration

1. Edit the `twitch.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting your twitch performance data.
   See the [sample twitch.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3]

### Validation

[Run the Agent's `status` subcommand][4] and look for `twitch` under the Checks section.

## Data Collected

### Metrics

Twitch does not include any metrics.

### Service Checks

Twitch does not include any service checks.

### Events

Twitch does not include any events.

## Troubleshooting

Need help? Contact [Datadog Support][5].

[1]: **LINK_TO_INTEGERATION_SITE**
[2]: https://github.com/DataDog/integrations-core/blob/master/twitch/datadog_checks/twitch/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://docs.datadoghq.com/help/
