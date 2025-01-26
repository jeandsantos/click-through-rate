import pytest

from click_through_rate.main import run_pipeline


class TestRunPipeline:
    @pytest.mark.slow
    @pytest.mark.integration
    def test_run_pipeline(self, url_data: str):
        run_pipeline(url=url_data)
