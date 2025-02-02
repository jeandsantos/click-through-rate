import pytest
from pytest import MonkeyPatch

from click_through_rate.enums import Environment
from click_through_rate.main import ctr_pipeline


class TestMain:
    @pytest.mark.slow
    @pytest.mark.integration
    def test_ctr_pipeline(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv("ENVIRONMENT", Environment.DEV)

        result = ctr_pipeline()

        assert result
