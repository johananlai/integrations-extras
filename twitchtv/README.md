# Agent Check: Twitchtv

## Overview

This check monitors [Twitch.tv][1].

## Setup

### Installation

The Twitch.tv check is not included in the [Datadog Agent][2] package, so you will
need to install it yourself.

### Configuration

1. Edit the `twitchtv.d/conf.yaml` file, in the `conf.d/` folder at the root of your
   Agent's configuration directory to start collecting your twitchtv performance data.
   See the [sample twitchtv.d/conf.yaml][2] for all available configuration options.

2. [Restart the Agent][3]

### Validation

[Run the Agent's `status` subcommand][4] and look for `twitchtv` under the Checks section.

## Data Collected

### Metrics

See [metadata.csv][6] for a list of metrics provided by this integration.

### Service Checks

Twitchtv does not include any service checks.

### Events

Twitchtv does not include any events.

## Troubleshooting

Need help? Contact [Datadog Support][5].

[1]: **twitch.tv**
[2]: https://github.com/johananlai/integrations-extras/blob/master/twitchtv/datadog_checks/twitchtv/data/conf.yaml.example
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://docs.datadoghq.com/help/
[6]: https://github.com/johananlai/integrations-extras/blob/master/twitchtv/metadata.csv
