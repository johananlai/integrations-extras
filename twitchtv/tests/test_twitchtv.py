from datadog_checks.twitchtv import TwitchtvCheck


def test_check(aggregator, instance):
    check = TwitchtvCheck('twitchtv', {}, {})
    check.check(instance)

    aggregator.assert_all_metrics_covered()
