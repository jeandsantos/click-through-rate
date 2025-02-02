from click_through_rate.components.download_data import download_data


class TestDownloadData:
    def test_download_data(self):
        result = download_data()

        assert result is None
