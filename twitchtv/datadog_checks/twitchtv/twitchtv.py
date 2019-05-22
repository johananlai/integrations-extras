import requests
import simplejson as json
from six.moves.urllib.parse import urljoin

from datadog_checks.checks import AgentCheck


class TwitchtvCheck(AgentCheck):
    CHECK_NAME = 'twitchtv'

    def __init__(self, name, init_config, agentConfig, instances=None):
        super(TwitchtvCheck, self).__init__(name, init_config, agentConfig, instances)

    def check(self, instance):
        # parse config fields
        self._validate_instance(instance)
        api_url = instance['api_url']
        client_id = instance['client_id']
        channels = instance.get("channels", [])

        # get channel metrics from API
        payload = {}
        tags = {}
        try:
            payload = self._get_channel_data(instance, api_url, client_id, channels)
            tags = self._get_game_tags(instance, api_url, client_id, payload)
        except Exception, e:
            self.log.error("Failed to get metrics with error: {}".format(e))

        # send to DD
        try:
            self._report_channel_metrics(instance, follows)
        except Exception, e:
            self.log.error("Failed to report channel metrics with error: {}".format(e))

        # get follower metrics from API
        users_payload = {}
        follows = {}
        try:
            users_payload = self._get_user_data(instance, api_url, client_id, channels)
            follows = self._get_all_follows(instance, api_url, client_id, users_payload)
        except Exception, e:
            self.log.error("Failed to get user follows with error: {}".format(e))

        # send to DD
        try:
            self._report_follows_metrics(instance, payload, tags)
        except Exception, e:
            self.log.error("Failed to report follows metrics with error: {}".format(e))

    def _validate_instance(self, instance):
        if any([x for x in ['api_url', 'client_id', 'channels'] if x not in instance]):
            raise Exception("Missing 'api_url', 'client_id', or 'channels' in config")

    def _report_channel_metrics(self, instance, payload, tags):
        metric_name = 'twitchtv.live.viewers'
        for ch in payload['data']:
            self.gauge(metric_name, ch['viewer_count'],
                       tags=instance.get('tags', []) +
                            ['channel:' + ch['user_name']] +
                            ['language:' + ch['language']] +
                            ['game:' + tags[ch['user_name']]])

    def _report_follows_metrics(self, instance, follows):
        metric_name = 'twitchtv.followers'
        for ch, total in follows.items():
            self.gauge(metric_name, total,
                       tags=instance.get('tags', []) +
                            ['channel:' + ch])

    def _get_channel_data(self, instance, api_url, client_id, channels):
        path = "streams"
        headers = {'Client-ID': client_id}
        params = [('user_login', ch) for ch in channels]
        
        r = requests.get(urljoin(api_url, path), headers=headers, params=params, timeout=60)
        r.raise_for_status()

        return json.loads(r.text)

    def _get_game_data(self, instance, api_url, client_id, game_id):
        path = "games"
        headers = {'Client-ID': client_id}
        params = {'id': game_id}

        r = requests.get(urljoin(api_url, path), headers=headers, params=params, timeout=60)
        r.raise_for_status()

        return json.loads(r.text)

    def _get_game_tags(self, instance, api_url, client_id, payload):
        tags = {}

        for ch in payload['data']:
            try:
                game_payload = self._get_game_data(instance, api_url, client_id, ch['game_id'])
                tags[ch['user_name']] = game_payload['data'][0]['name']
            except Exception, e:
                self.log.error("Failed to get game name with error: {}".format(e))

        return tags

    def _get_user_data(self, instance, api_url, client_id, channels):
        path = "users"
        headers = {'Client-ID': client_id}
        params = [('login', ch) for ch in channels]

        r = requests.get(urljoin(api_url, path), headers=headers, params=params, timeout=60)
        r.raise_for_status()

        return json.loads(r.text)

    def _get_follow_data(self, instance, api_url, client_id, user_id):
        path = "users/follows"
        headers = {'Client-ID': client_id}
        params = {'to_id': user_id}

        r = requests.get(urljoin(api_url, path), headers=headers, params=params, timeout=60)
        r.raise_for_status()

        return json.loads(r.text)

    def _get_all_follows(self, instance, api_url, client_id, payload):
        follows = {}

        for ch in payload['data']:
            try:
                follow_payload = self._get_follow_data(instance, api_url, client_id, ch['id'])
                follows[ch['login']] = follow_payload['total']
            except Exception, e:
                self.log.error("Failed to get user follows with error: {}".format(e))

        return follows

