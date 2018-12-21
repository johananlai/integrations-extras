import requests

from datadog_checks.checks import AgentCheck


class TwitchCheck(AgentCheck):
    CHECK_NAME = 'twitch'

    def __init__(self, name, init_config, agentConfig, instances=None):
        super(TwitchCheck, self).__init__(name, init_config, agentConfig, instances)

    def check(self, instance):
        if 'api_url' not in instance:
            raise Exception("Missing 'api_url' in Twitch config")

        api_url = instance['api_url']

        if 'client_id' not in instance:
            raise Exception("Missing 'client_id' in Twitch config")

        client_id = instance['client_id']
