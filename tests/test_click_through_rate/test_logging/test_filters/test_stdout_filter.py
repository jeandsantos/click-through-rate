import logging

from click_through_rate.log.filters.stdout_filter import StdoutFilter


class TestStdoutFilter:
    def test_filter_returns_false_when_levelno_is_greater_than_info(self, log_record_warning: logging.LogRecord):
        filter_obj = StdoutFilter()
        result = filter_obj.filter(log_record_warning)

        assert result is False

    def test_filter_returns_true_when_levelno_is_info_or_lower(self, log_record_info: logging.LogRecord):
        filter_obj = StdoutFilter()
        result = filter_obj.filter(log_record_info)

        assert result is True
