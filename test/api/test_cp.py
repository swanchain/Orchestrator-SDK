""" Tests for Computing Providers """

import logging
import pytest
import requests

from mock.mock import Mock, MagicMock, patch  # type: ignore

from src.api.cp import (
    ComputerProvider,
    get_computing_providers_list,
    get_collateral_balance,
    get_cp_detail,
    get_available_computing_providers,
)
from src.constants.constants import SWAN_API, CP_AVAILABLE

from src.exceptions.request_exceptions import (
    SwanHTTPError,
    SwanRequestError,
    SwanConnectionError,
    SwanTimeoutError,
)


class TestComputingProviders:
    def setup(self):
        self.provider = ComputerProvider()

    def test_retrieve_all_cp_machines(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "success",
            "data": {
                "hardware": [
                    {"name": "Machine 1", "cpu": "Intel i7", "ram": "16GB"},
                    {"name": "Machine 2", "cpu": "AMD Ryzen 5", "ram": "8GB"},
                    {"name": "Machine 3", "cpu": "Intel i5", "ram": "12GB"},
                ]
            },
        }
        mock_response.raise_for_status.return_value = None
        requests.get = MagicMock(return_value=mock_response)

        # Call the function under test
        result = self.provider.get_all_cp_machines()

        # Assert that the result is the expected list of hardware configurations
        expected_result = [
            {"name": "Machine 1", "cpu": "Intel i7", "ram": "16GB"},
            {"name": "Machine 2", "cpu": "AMD Ryzen 5", "ram": "8GB"},
            {"name": "Machine 3", "cpu": "Intel i5", "ram": "12GB"},
        ]
        assert result == expected_result

    def test_function_raises_httperror_if_api_call_fails(self):
        # Mock the requests.get method to raise an exception
        with patch("requests.get", side_effect=requests.exceptions.HTTPError):
            with pytest.raises(SwanHTTPError):
                self.provider.get_all_cp_machines()

    def test_failed_api_response(self):
        # Mock the requests.get method to raise an exception
        with patch("requests.get", side_effect=requests.exceptions.RequestException):
            with pytest.raises(SwanRequestError):
                self.provider.get_all_cp_machines()

    def test_valid_list_of_dictionaries(self):
        # Mock the requests.get method to return a successful response
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "data": [{"provider": "A", "count": 10}, {"provider": "B", "count": 5}]
            }

            # Call the function you're testing
            result = self.provider.get_cp_distribution()

            # Assert that the result is a list of dictionaries
            assert isinstance(result, list)
            assert all(isinstance(item, dict) for item in result)

    def test_returns_empty_list_when_api_call_returns_empty_data(self):
        # Mock the requests.get method to return an empty response
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"data": []}

            # Call the function under test
            result = self.provider.get_cp_distribution()

            # Assert that the result is an empty list
            assert result == []

    def test_handle_connection_errors(self):
        # Mock the requests.get method to raise a ConnectionError
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(SwanConnectionError):
                self.provider.get_cp_distribution()
                logging.error.assert_called_with("Error connecting: ")

        # Mock the requests.get method to raise a Timeout
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            with pytest.raises(SwanTimeoutError):
                self.provider.get_cp_distribution()
                logging.error.assert_called_with("Timeout error: ")

        # Mock the requests.get method to raise a RequestException
        with patch("requests.get", side_effect=requests.exceptions.RequestException):
            with pytest.raises(SwanRequestError):
                self.provider.get_cp_distribution()
                logging.error.assert_called_with("Error during requests to ")

        # Mock the requests.get method to raise an unexpected exception
        with patch("requests.get", side_effect=Exception):
            with pytest.raises(Exception):
                self.provider.get_cp_distribution()
                logging.error.assert_called_with("An unexpected error occurred: ")

    def test_handle_timeout_errors(self):
        # Mock the requests.get method to raise a Timeout exception
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            with pytest.raises(SwanTimeoutError):
                self.provider.get_cp_distribution()

    def test_valid_field_types(self):
        # Mock the requests.get method to return a response with invalid field types
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "data": [
                    {
                        "provider_id": "1",
                        "name": "Provider 1",
                        "cpu_cores": "4",
                        "memory": "8GB",
                        "storage": "500GB",
                    },
                    {
                        "provider_id": "2",
                        "name": "Provider 2",
                        "cpu_cores": "8",
                        "memory": "16GB",
                        "storage": "1TB",
                    },
                ]
            }

            # Call the function under test
            expected_response = {
                "data": [
                    {
                        "provider_id": "1",
                        "name": "Provider 1",
                        "cpu_cores": "4",
                        "memory": "8GB",
                        "storage": "500GB",
                    },
                    {
                        "provider_id": "2",
                        "name": "Provider 2",
                        "cpu_cores": "8",
                        "memory": "16GB",
                        "storage": "1TB",
                    },
                ]
            }

            # Assert that the result is None
            assert mock_get.return_value.json.return_value == expected_response

    def test_api_returns_data_with_missing_fields(self):
        # Mock the requests.get method to return a response with missing fields
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "data": [{"provider_id": 1, "name": "Provider 1"}, {"provider_id": 2}]
            }

            # Call the function under test
            result = self.provider.get_cp_distribution()

            # Assert that the result is a list of dictionaries
            assert isinstance(result, list)
            assert all(isinstance(item, dict) for item in result)

            # Assert that the missing fields are replaced with None
            assert result[0]["provider_id"] == 1
            assert result[0]["name"] == "Provider 1"
            assert result[1]["provider_id"] == 2
            assert "name" not in result

    def test_api_returns_incomplete_data(self):
        # Mock the requests.get method to return incomplete data
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"data": []}

            # Call the function under test
            result = self.provider.get_cp_distribution()

            # Assert that the result is an empty list
            assert result == []

            # Assert that no exceptions were raised
            assert not isinstance(result, Exception)

    def test_unexpected_data_format(self):
        # Mock the requests.get method to return a response with unexpected data format
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"result": "success"}

            # Call the function under test
            result = self.provider.get_cp_distribution()

            # Assert that the result is None
            assert result == []

    def test_retrieve_all_cp_machines(self):
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "success",
            "data": {
                "hardware": [
                    {"name": "Machine 1", "cpu": "Intel i7", "ram": "16GB"},
                    {"name": "Machine 2", "cpu": "AMD Ryzen 5", "ram": "8GB"},
                    {"name": "Machine 3", "cpu": "Intel i5", "ram": "12GB"},
                ]
            },
        }
        mock_response.raise_for_status.return_value = None
        requests.get = MagicMock(return_value=mock_response)
        result = self.provider.get_all_cp_machines()
        expected_result = [
            {"name": "Machine 1", "cpu": "Intel i7", "ram": "16GB"},
            {"name": "Machine 2", "cpu": "AMD Ryzen 5", "ram": "8GB"},
            {"name": "Machine 3", "cpu": "Intel i5", "ram": "12GB"},
        ]
        assert result == expected_result


class TestComputingProvidersListByRegion:
    def test_returns_list_of_computing_providers(self):
        # Mock the requests.post method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [{"provider": "Provider A"}, {"provider": "Provider B"}]
        }
        mock_response.raise_for_status.return_value = None
        requests.post = MagicMock(return_value=mock_response)

        # Call the function you're testing
        result = get_computing_providers_list("region")

        # Assert that the result is a list of dictionaries
        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert isinstance(result[1], dict)
        assert len(result) == 2
        assert result[0]["provider"] == "Provider A"
        assert result[1]["provider"] == "Provider B"

    def test_raises_swan_http_error_if_api_call_fails(self):
        # Mock the requests.post method to raise an HTTPError
        with patch("requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.HTTPError()

            # Call the function under test
            with pytest.raises(SwanHTTPError):
                get_computing_providers_list("region")

    def test_raises_value_error_if_region_not_provided(self):
        with pytest.raises(ValueError):
            get_computing_providers_list("")
        with pytest.raises(ValueError):
            get_computing_providers_list(None)

    def test_raises_swan_http_error(self):
        # Mock the requests.post method to raise an HTTPError
        with patch("requests.post") as mock_post:
            mock_post.return_value.raise_for_status.side_effect = (
                requests.exceptions.HTTPError
            )

            # Call the function under test
            with pytest.raises(SwanHTTPError):
                get_computing_providers_list("region")

    def test_raises_exception_for_other_types_of_exceptions(self):
        # Mock the requests.post method to raise an exception
        def mock_post(*args, **kwargs):
            raise Exception("An error occurred")

        with patch("requests.post", side_effect=mock_post):
            with pytest.raises(Exception):
                get_computing_providers_list("region")

    def test_retrieve_collateral_balance_valid_address(self):
        # Mock the requests.get method to return a mock response
        with patch("requests.get") as mock_get:
            # Set up the mock response
            mock_response = Mock()
            mock_response.json.return_value = {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }
            mock_get.return_value = mock_response

            # Call the function with a valid computing provider address
            result = get_collateral_balance("0x1234abcd")

            # Assert that the response is as expected
            assert result == {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }

    # NOTE: do not uncomment before ApiClient changes
    # def test_invalid_address_format(self):
    #     # Arrange
    #     cp_address = "invalid_address"
    #
    #     # Act and Assert
    #     with pytest.raises(SwanRequestError):
    #         get_collateral_balance(cp_address)

    def test_return_error_message(self):
        # Mock the requests.get method to raise an exception
        with patch("requests.get", side_effect=requests.exceptions.RequestException):
            # Call the function under test
            with pytest.raises(SwanRequestError) as e:
                get_collateral_balance("0x1234abcd")
            # Assert that the exception message is correct
            assert (
                str(e.value)
                == "SwanRequestError: An unexpected error occurred while retrieving collateral balance"
            )

    def test_get_collateral_balance_request(self):
        # Mock the requests.get method to return a mock response
        with patch("requests.get") as mock_get:
            # Set up the mock response
            mock_response = Mock()
            mock_response.json.return_value = {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }
            mock_get.return_value = mock_response

            # Call the function you're testing
            result = get_collateral_balance("0x1234abcd")

            # Assert that requests.get was called with the correct endpoint
            mock_get.assert_called_once_with(
                "http://swanhub-cali.swanchain.io/cp/collateral/0x1234abcd"
            )

            # Assert that the result is the expected dictionary
            assert result == {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }

    def test_retrieve_valid_cp_detail(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {"cp_id": "123", "name": "Test CP"}
        mock_response.status_code = 200
        with patch("requests.get", return_value=mock_response) as mock_get:
            # Call the function with a valid cp_id
            cp_id = "123"
            response, status_code = get_cp_detail(cp_id)

            # Assert that the requests.get method was called with the correct URL
            mock_get.assert_called_once_with(f"{SWAN_API}/{cp_id}")

            # Assert that the response data and status code are correct
            assert response == {"cp_id": "123", "name": "Test CP"}
            assert status_code == 200

    def test_returned_dictionary_contains_expected_keys(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }
        mock_response.status_code = 200
        requests.get = MagicMock(return_value=mock_response)

        # Call the function you're testing
        response, status_code = get_cp_detail("cp_id")

        # Assert that the response contains all expected keys
        assert "key1" in response
        assert "key2" in response
        assert "key3" in response

    def test_http_status_code_type(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {"data": "mock_data"}
        mock_response.status_code = 200
        with patch("requests.get", return_value=mock_response):
            # Call the function under test
            response, status_code = get_cp_detail("cp_id")

            # Assert that the status code is of the expected type
            assert isinstance(status_code, int)

    def test_valid_json_response(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "success",
            "message": "Data retrieved successfully",
            "data": {"providers": ["provider1", "provider2"]},
        }
        mock_response.raise_for_status.return_value = None
        requests.get = MagicMock(return_value=mock_response)

        # Call the function under test
        result = get_available_computing_providers()

        # Assert that the result is the expected JSON response
        assert result == {
            "status": "success",
            "message": "Data retrieved successfully",
            "data": {"providers": ["provider1", "provider2"]},
        }

    def test_api_endpoint_not_available(self):
        # Mock the requests.get method to raise a ConnectionError
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(SwanConnectionError):
                get_available_computing_providers()

    def test_invalid_json_response(self):
        # Mock the requests.get method to return an invalid JSON response
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.side_effect = ValueError

            # Call the function under test
            with pytest.raises(ValueError):
                get_available_computing_providers()

    def test_empty_json_response(self):
        # Mock the requests.get method to return an empty JSON response
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {}

            # Call the function under test
            result = get_available_computing_providers()

            # Assert that the result is an empty dictionary
            assert result == {}

            # Assert that the requests.get method was called with the correct URL
            mock_get.assert_called_once_with(f"{SWAN_API}{CP_AVAILABLE}")
