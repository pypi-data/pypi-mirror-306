from pyetrade import alerts


# Mock out OAuth1Session
def test_list_alerts(mocker):
    """test_list_alerts(MockOAuthSession) -> None
    param: MockOAuthSession
    type: mock.MagicMock
    description: MagicMock object for OAuth1Sessions"""
    MockOAuthSession = mocker.patch("pyetrade.alerts.OAuth1Session")
    # Set Mock returns
    MockOAuthSession().get().json.return_value = "{'alert': 'abc123'}"
    MockOAuthSession().get().text = r"<xml> returns </xml>"

    alert = alerts.ETradeAlerts("abc123", "xyz123", "abctoken", "xyzsecret", dev=True)
    default_params = {"count": 25, "direction": "DESC"}

    # Test Dev JSON
    assert alert.list_alerts(resp_format="json") == "{'alert': 'abc123'}"
    # Test API URL
    MockOAuthSession().get.assert_called_with(
        "https://apisb.etrade.com/v1/user/alerts.json", params=default_params
    )

    # Test Dev XML
    assert dict(alert.list_alerts(resp_format="xml")) == {"xml": "returns"}
    MockOAuthSession().get.assert_called_with(
        "https://apisb.etrade.com/v1/user/alerts", params=default_params
    )
    alert = alerts.ETradeAlerts("abc123", "xyz123", "abctoken", "xyzsecret", dev=False)

    # Test Prod JSON
    assert alert.list_alerts(resp_format="json") == "{'alert': 'abc123'}"
    # Test API URL
    MockOAuthSession().get.assert_called_with(
        "https://api.etrade.com/v1/user/alerts.json", params=default_params
    )

    # test Prod XML
    assert alert.list_alerts(resp_format="xml") == {"xml": "returns"}

    MockOAuthSession().get.assert_called_with(
        "https://api.etrade.com/v1/user/alerts", params=default_params
    )

    assert alert.list_alerts(count=301, resp_format="json") == "{'alert': 'abc123'}"
    MockOAuthSession().get.assert_called_with(
        "https://api.etrade.com/v1/user/alerts.json",
        params={"count": 300, "direction": "DESC"},
    )

    assert MockOAuthSession().get().json.called
    assert MockOAuthSession().get.called


# Mock out OAuth1Session
def test_list_alert_details(mocker):
    """test_list_alerts(MockOAuthSession) -> None
    param: MockOAuthSession
    type: mock.MagicMock
    description: MagicMock object for OAuth1Sessions"""
    MockOAuthSession = mocker.patch("pyetrade.alerts.OAuth1Session")
    # Set Mock returns
    MockOAuthSession().get().json.return_value = "{'alert': 'abc123'}"
    MockOAuthSession().get().text = r"<xml> returns </xml>"

    alert = alerts.ETradeAlerts("abc123", "xyz123", "abctoken", "xyzsecret", dev=True)
    default_params = {"htmlTags": False}

    # Test Dev JSON
    assert alert.list_alert_details(1234, resp_format="json") == "{'alert': 'abc123'}"
    # Test API URL
    MockOAuthSession().get.assert_called_with(
        "https://apisb.etrade.com/v1/user/alerts.json/1234", params=default_params
    )  # noqa: E501

    # Test Dev XML
    assert dict(alert.list_alert_details(1234, resp_format="xml")) == {"xml": "returns"}
    MockOAuthSession().get.assert_called_with(
        "https://apisb.etrade.com/v1/user/alerts/1234", params=default_params
    )
    assert dict(alert.list_alert_details(1234, resp_format="xml")) == {"xml": "returns"}

    alert = alerts.ETradeAlerts("abc123", "xyz123", "abctoken", "xyzsecret", dev=False)
    # Test Prod JSON
    assert alert.list_alert_details(1234, resp_format="json") == "{'alert': 'abc123'}"

    # Test API URL
    MockOAuthSession().get.assert_called_with(
        "https://api.etrade.com/v1/user/alerts.json/1234", params=default_params
    )
    assert dict(alert.list_alert_details(1234, resp_format="xml")) == {"xml": "returns"}

    MockOAuthSession().get.assert_called_with(
        "https://api.etrade.com/v1/user/alerts/1234", params=default_params
    )
    assert MockOAuthSession().get().json.called
    assert MockOAuthSession().get.called


# Mock out OAuth1Session
def test_delete_alert(mocker):
    """test_list_alerts(MockOAuthSession) -> None
    param: MockOAuthSession
    type: mock.MagicMock
    description: MagicMock object for OAuth1Sessions"""
    MockOAuthSession = mocker.patch("pyetrade.alerts.OAuth1Session")
    # Set Mock returns
    MockOAuthSession().delete().json.return_value = "{'alert': 'abc123'}"
    MockOAuthSession().delete().text = r"<xml> returns </xml>"
    alert = alerts.ETradeAlerts("abc123", "xyz123", "abctoken", "xyzsecret", dev=True)
    # Test Dev JSON
    assert alert.delete_alert(1234, resp_format="json") == "{'alert': 'abc123'}"
    # Test API URL
    MockOAuthSession().delete.assert_called_with(
        "https://apisb.etrade.com/v1/user/alerts.json/1234"
    )
    # Test Dev XML
    assert dict(alert.delete_alert(1234, resp_format="xml")) == {"xml": "returns"}
    MockOAuthSession().delete.assert_called_with(
        "https://apisb.etrade.com/v1/user/alerts/1234"
    )

    alert = alerts.ETradeAlerts("abc123", "xyz123", "abctoken", "xyzsecret", dev=False)
    # Test Prod JSON
    assert alert.delete_alert(1234, resp_format="json") == "{'alert': 'abc123'}"
    # Test API URL
    MockOAuthSession().delete.assert_called_with(
        "https://api.etrade.com/v1/user/alerts.json/1234"
    )

    # Test Prod XML
    assert dict(alert.delete_alert(1234, resp_format="xml")) == {"xml": "returns"}

    MockOAuthSession().delete.assert_called_with(
        "https://api.etrade.com/v1/user/alerts/1234"
    )
    assert MockOAuthSession().delete().json.called
    assert MockOAuthSession().delete.called
