import requests
import simplejson as json
from six.moves.urllib.parse import urljoin

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

        payload = {}
        try:
            payload = self._get_metrics(instance, api_url, client_id)
        except Exception, e:
            self.log.error("Failed to get metrics with error: {}".format(e))

        try:
            self._report_metrics(instance, payload)
        except Exception, e:
            self.log.error("Failed to report metrics with error: {}".format(e))

    def _report_metrics(self, instance, payload):
        metric_name = 'twitch.viewer.count'
        self.count(metric_name, payload['data'][0]['viewer_count'],
                   tags=instance.get('tags', []) + ['channel:' + payload['data'][0]['user_name']])

    def _get_metrics(self, instance, api_url, client_id):
        # TEMP
        path = "streams"

        headers = {'Client-ID': client_id}
        params = {'first': '1'}
        r = requests.get(urljoin(api_url, path), headers=headers, timeout=60)
        r.raise_for_status()

        return json.loads(r.text)

