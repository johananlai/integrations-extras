from datadog_checks.twitch import TwitchCheck


def test_check(aggregator, instance):
    check = TwitchCheck('twitch', {}, {})
    check.check(instance)

    aggregator.assert_all_metrics_covered()
