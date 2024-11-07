#!/usr/bin/env python3
"""pyetrade authorization unit tests
   TODO:
       * Test request error
       * Test API URL
"""
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from pyetrade import order


class TestETradeOrder(unittest.TestCase):
    """TestEtradeOrder Unit Test"""

    def test_option_symbol(self):
        expected = "PLTR--220218P00023000"
        self.assertEqual(
            expected, order.option_symbol("PLTR", order.PUT, "2022-02-18", 23)
        )
        self.assertEqual(
            expected, order.option_symbol("PLTR", order.PUT, "2022-02-18", 23.00)
        )
        self.assertEqual(
            expected, order.option_symbol("PLTR", order.PUT, "2022-02-18", "23.0")
        )

    @patch("pyetrade.order.OAuth1Session")
    def test_list_orders(self, MockOAuthSession):
        """test_place_equity_order(MockOAuthSession) -> None
        param: MockOAuthSession
        type: mock.MagicMock
        description: MagicMock of OAuth1Session"""
        # Set Mock returns
        MockOAuthSession().get().json.return_value = {"accountId": "12345"}
        MockOAuthSession().get().text = r"<xml> returns </xml>"
        orders = order.ETradeOrder(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )

        # Test Dev buy order equity
        self.assertEqual(orders.list_orders("12345"), {"accountId": "12345"})
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

        # Test Prod buy order equity
        self.assertEqual(orders.list_orders("12345"), {"accountId": "12345"})
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

        self.assertTrue(
            isinstance(orders.list_orders("12345", resp_format="xml"), dict)
        )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

    @patch("pyetrade.order.OAuth1Session")
    def test_list_order_details(self, MockOAuthSession):
        MockOAuthSession().get().json.return_value = {"accountId": "12345"}
        MockOAuthSession().get().text = r"<xml> returns </xml>"

        orders = order.ETradeOrder(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )

        self.assertTrue(
            isinstance(orders.list_order_details("12345", 123, "json"), dict)
        )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

    def test_find_option_orders(self):
        orders = order.ETradeOrder(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )

        orders.option_symbol = MagicMock(return_value="AAPL--220218C00065000")

        orders.list_orders = MagicMock(
            return_value={
                "OrdersResponse": {
                    "Order": [
                        {
                            "OrderDetail": [
                                {
                                    "Instrument": [
                                        {
                                            "Product": {
                                                "securityType": "OPTN",
                                                "productId": {
                                                    "symbol": "AAPL--220218C00065000"
                                                },
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        )

        # Call the function being tested
        result = orders.find_option_orders(
            "34fsdf43f", "AAPL", "call", "02-08-2021", 65.0
        )

        self.assertTrue(isinstance(result, list))

    # Mock out OAuth1Session
    @patch("pyetrade.order.OAuth1Session")
    def test_place_equity_order(self, MockOAuthSession):
        """test_place_equity_order(MockOAuthSession) -> None
        param: MockOAuthSession
        type: mock.MagicMock
        description: MagicMock of OAuth1Session"""

        # Set Mock returns
        MockOAuthSession().post().text = r"<PreviewOrderResponse><PreviewIds><previewId>321</previewId></PreviewIds></PreviewOrderResponse>"  # noqa: E501
        orders = order.ETradeOrder(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )

        result = orders.place_equity_order(
            accountIdKey="12345",
            symbol="ABC",
            orderAction="BUY",
            clientOrderId="1a2b3c",
            priceType="MARKET",
            quantity=100,
            orderTerm="GOOD_UNTIL_CANCEL",
            marketSession="REGULAR",
        )

        # Test xml buy order equity
        self.assertTrue(isinstance(result, dict))
        # self.assertTrue(MockOAuthSession().post().json.called)
        self.assertTrue(MockOAuthSession().post.called)

        # Test OrderedDict buy order equity
        self.assertEqual(
            orders.place_equity_order(
                accountIdKey="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="MARKET",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            )["PreviewOrderResponse"]["PreviewIds"]["previewId"],
            "321",
        )
        self.assertTrue(MockOAuthSession().post.called)

        # Test json buy order equity
        ret_val = {"PreviewOrderResponse": {"PreviewIds": {"previewId": "321"}}}

        MockOAuthSession().post().json.return_value = ret_val
        self.assertEqual(
            orders.place_equity_order(
                accountIdKey="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="MARKET",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            ),
            ret_val,
        )
        # self.assertTrue(MockOAuthSession().post().json.called)
        self.assertTrue(MockOAuthSession().post.called)

        # Test payload: BUY MARKET
        payload = orders.build_order_payload(
            "PreviewOrderRequest",
            resp_format="json",
            accountId="12345",
            symbol="ABC",
            orderAction="BUY",
            clientOrderId="1a2b3c",
            priceType="MARKET",
            quantity=100,
            orderTerm="GOOD_UNTIL_CANCEL",
            marketSession="REGULAR",
        )

        expected = {
            "PreviewOrderRequest": {
                "orderType": "EQ",
                "clientOrderId": "1a2b3c",
                "Order": {
                    "resp_format": "json",
                    "accountId": "12345",
                    "symbol": "ABC",
                    "orderAction": "BUY",
                    "clientOrderId": "1a2b3c",
                    "priceType": "MARKET",
                    "quantity": 100,
                    "orderTerm": "GOOD_UNTIL_CANCEL",
                    "marketSession": "REGULAR",
                    "Instrument": {
                        "Product": {"securityType": "EQ", "symbol": "ABC"},
                        "orderAction": "BUY",
                        "quantityType": "QUANTITY",
                        "quantity": 100,
                    },
                },
            }
        }
        self.assertTrue(expected == payload)

        # Test payload: SELL STOP
        float_decimals = [
            (
                19.99999,
                "19.99",
            ),  # double values are not exact; SELL: round down to decimal
            (20, "20.00"),  # exact int
            (20.01001, "20.01"),
            (20.01, "20.01"),
            (20.00999, "20.00"),
            (20.00001, "20.00"),
        ]

        for fd in float_decimals:
            for orderAction in ["SELL", "SELL_SHORT"]:
                payload = orders.build_order_payload(
                    "PreviewOrderRequest",
                    accountIdKey="12345",
                    symbol="ABC",
                    orderAction=orderAction,
                    clientOrderId="1a2b3c",
                    priceType="STOP",
                    stopPrice=fd[0],
                    quantity=100,
                    orderTerm="GOOD_UNTIL_CANCEL",
                    marketSession="REGULAR",
                )

                self.assertEqual(
                    payload["PreviewOrderRequest"]["Order"]["stopPrice"], fd[1]
                )

        # Test payload: BUY STOP
        float_decimals = [
            (
                19.99999,
                "20.00",
            ),  # double values are not exact; BUY: round   up to decimal
            (20, "20.00"),  # exact int
            (20.01001, "20.02"),
            (20.01, "20.01"),
            (20.00999, "20.01"),
            (20.00001, "20.01"),
        ]

        for fd in float_decimals:
            for orderAction in ["BUY", "BUY_TO_COVER"]:
                payload = orders.build_order_payload(
                    "PreviewOrderRequest",
                    accountIdKey="12345",
                    symbol="ABC",
                    orderAction=orderAction,
                    clientOrderId="1a2b3c",
                    priceType="STOP",
                    stopPrice=fd[0],
                    quantity=100,
                    orderTerm="GOOD_UNTIL_CANCEL",
                    marketSession="REGULAR",
                )

                self.assertEqual(
                    payload["PreviewOrderRequest"]["Order"]["stopPrice"], fd[1]
                )

    def test_place_equity_order_exception(self):
        """test_place_equity_order_exception(MockOAuthSession) -> None
        param: MockOAuthSession
        type: mock.MagicMock
        description: MagicMock of OAuth1Session"""
        orders = order.ETradeOrder(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )

        # Test exception class
        with self.assertRaises(order.OrderException):
            orders.place_equity_order()
        try:
            orders.place_equity_order()
        except order.OrderException as e:
            print(e)

        # Test STOP
        with self.assertRaises(order.OrderException):
            orders.place_equity_order(
                accountIdKey="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="STOP",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            )
        # Test LIMIT
        with self.assertRaises(order.OrderException):
            orders.place_equity_order(
                accountIdKey="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="LIMIT",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            )
        # Test STOP_LIMIT
        with self.assertRaises(order.OrderException):
            orders.place_equity_order(
                accountIdKey="12345",
                symbol="ABC",
                orderAction="BUY",
                clientOrderId="1a2b3c",
                priceType="STOP_LIMIT",
                quantity=100,
                orderTerm="GOOD_UNTIL_CANCEL",
                marketSession="REGULAR",
            )

    @patch("pyetrade.order.OAuth1Session")
    def test_cancel_order(self, MockOAuthSession):
        """test_cancel_order(MockOAuthSession) -> None
        param: MockOAuthSession
        type: mock.MagicMock
        description: MagicMock of OAuth1Session"""
        MockOAuthSession().put().json.return_value = {"accountIdKey": "12345"}
        MockOAuthSession().put().text = r"<xml> returns </xml>"
        orders = order.ETradeOrder(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        # Prod
        self.assertEqual(
            orders.cancel_order("12345", 42, resp_format="json"),
            {"accountIdKey": "12345"},
        )
        MockOAuthSession().put.assert_called_with(
            "https://api.etrade.com/v1/accounts" "/12345/orders/cancel",
            json={"CancelOrderRequest": {"orderId": 42}},
            timeout=30,
        )
        self.assertTrue(MockOAuthSession().put().json.called)
        self.assertTrue(MockOAuthSession().put.called)
        self.assertTrue(
            isinstance(orders.cancel_order("12345", 42, resp_format="xml"), dict)
        )
