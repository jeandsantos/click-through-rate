import logging

from click_through_rate.log.filters.stderr_filter import StderrFilter


class TestStderrFilter:
    def test_filter_returns_true_when_levelno_is_greater_than_info(self, log_record_warning: logging.LogRecord):
        filter_obj = StderrFilter()
        result = filter_obj.filter(log_record_warning)

        assert result is True

    def test_filter_returns_false_when_levelno_is_info_or_lower(self, log_record_info: logging.LogRecord):
        filter_obj = StderrFilter()
        result = filter_obj.filter(log_record_info)

        assert result is False
