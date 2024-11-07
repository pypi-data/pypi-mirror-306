import logging
from logging import Logger
from typing import Any

from eth_typing import ChecksumAddress
from web3.contract import Contract

from pyrfx.config_manager import ConfigManager
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import get_available_tokens, get_reader_contract


class Markets:
    """
    A class that handles the retrieval and management of market data, including token addresses and metadata.
    """

    def __init__(self, config: ConfigManager, log_level: int = logging.INFO) -> None:
        """
        Initialize the Markets class with a configuration object and logger.

        :param config: ConfigManager object containing chain configuration.
        :param log_level: Logging level for the logger.
        """
        self.config: ConfigManager = config

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self._prices: dict[str, dict[str, int]] = {}
        self.info: dict[str, dict[str, Any]] = self._process_markets()

    def get_index_token_address(self, market_key: str) -> str:
        """
        Retrieve the index token address for a given market key.

        :param market_key: The key representing the market.
        :return: The index token address as a string.
        """
        return self.info[market_key]["index_token_address"]

    def get_long_token_address(self, market_key: str) -> str:
        """
        Retrieve the long token address for a given market key.

        :param market_key: The key representing the market.
        :return: The long token address as a string.
        """
        return self.info[market_key]["long_token_address"]

    def get_short_token_address(self, market_key: str) -> str:
        """
        Retrieve the short token address for a given market key.

        :param market_key: The key representing the market.
        :return: The short token address as a string.
        """
        return self.info[market_key]["short_token_address"]

    def get_market_symbol(self, market_key: str) -> str:
        """
        Retrieve the market symbol for a given market key.

        :param market_key: The key representing the market.
        :return: The market symbol as a string.
        """
        return self.info[market_key]["market_symbol"]

    def get_decimal_factor(self, market_key: str, long: bool = False, short: bool = False) -> int:
        """
        Retrieve the decimal factor for a market, either for long or short tokens.

        :param market_key: The key representing the market.
        :param long: Flag to retrieve long token's decimal factor.
        :param short: Flag to retrieve short token's decimal factor.
        :return: The decimal factor as an integer.
        """
        if long:
            return self.info[market_key]["long_token_metadata"]["decimals"]
        elif short:
            return self.info[market_key]["short_token_metadata"]["decimals"]
        return self.info[market_key]["market_metadata"]["decimals"]

    def is_synthetic(self, market_key: str) -> bool:
        """
        Check if a market is synthetic.

        :param market_key: The key representing the market.
        :return: True if the market is synthetic, otherwise False.
        """
        return self.info[market_key]["market_metadata"].get("synthetic", False)

    def get_available_markets(self) -> dict[ChecksumAddress, dict[str, Any]]:
        """
        Get a dictionary of available markets for a given chain.

        :return: A dictionary containing the available markets.
        """
        return self._process_markets()

    def _get_available_markets_raw(self) -> list[tuple[str, str, str, str]]:
        """
        Fetch the raw market data from the reader contract.

        :return: A tuple containing the raw market data.
        """
        reader_contract: Contract = get_reader_contract(self.config)
        return reader_contract.functions.getMarkets(
            self.config.contracts.data_store.contract_address, 0, 2**256 - 1
        ).call()

    def _process_markets(self) -> dict[ChecksumAddress, dict[str, Any]]:
        """
        Process the raw market data and structure it into a dictionary.

        :return: A dictionary containing the decoded market data.
        """
        available_tokens: dict[ChecksumAddress, dict[str, ChecksumAddress | int | bool]] = get_available_tokens(
            self.config
        )
        raw_markets: list[tuple[str, str, str, str]] = self._get_available_markets_raw()
        decoded_markets: dict[str, dict[str, Any]] = {}

        for raw_market in raw_markets:
            try:
                if not self._is_index_token_in_signed_prices_api(index_token_address=raw_market[1]):
                    continue

                market_symbol: str = self._get_market_symbol(available_tokens=available_tokens, raw_market=raw_market)
                decoded_markets[self.config.to_checksum_address(raw_market[0])] = self._decode_market_data(
                    available_tokens=available_tokens, raw_market=raw_market, market_symbol=market_symbol
                )
                self.logger.info(
                    f"Market processed: {decoded_markets[raw_market[0]]['rfx_market_address']} | "
                    f"{decoded_markets[raw_market[0]]['market_symbol']:7} | "
                    f"{decoded_markets[raw_market[0]]['long_token_metadata']['symbol']}-"
                    f"{decoded_markets[raw_market[0]]['short_token_metadata']['symbol']}"
                )
            except KeyError:
                decoded_markets[self.config.to_checksum_address(raw_market[0])] = self._decode_market_data(
                    available_tokens=available_tokens, raw_market=raw_market, is_swap_market=True
                )
                self.logger.info(f"Swap market processed: {raw_market[0]}")

        return decoded_markets

    @staticmethod
    def _decode_market_data(
        available_tokens: dict[str, dict[str, str | int | bool]],
        raw_market: tuple[str, str, str, str],
        market_symbol: str | None = None,
        is_swap_market: bool = False,
    ) -> dict[str, Any]:
        """
        Decode the raw market data into a structured dictionary.

        :param available_tokens: A dictionary mapping token addresses to metadata.
        :param raw_market: A tuple containing raw market data from the contract.
        :param market_symbol: The market symbol for the current market.
        :param is_swap_market: Flag to indicate if the market is a swap market.
        :return: A dictionary containing the decoded market data.
        """
        if is_swap_market:
            return {
                "rfx_market_address": raw_market[0],
                "market_symbol": f"SWAP {available_tokens[raw_market[2]]['symbol']}-{available_tokens[raw_market[3]]['symbol']}",
                "index_token_address": raw_market[1],
                "market_metadata": {
                    "symbol": f"SWAP {available_tokens[raw_market[2]]['symbol']}-{available_tokens[raw_market[3]]['symbol']}"
                },
                "long_token_metadata": available_tokens.get(raw_market[2], {}),
                "long_token_address": raw_market[2],
                "short_token_metadata": available_tokens.get(raw_market[3], {}),
                "short_token_address": raw_market[3],
            }
        else:
            return {
                "rfx_market_address": raw_market[0],
                "market_symbol": market_symbol,
                "index_token_address": raw_market[1],
                "market_metadata": available_tokens.get(raw_market[1], {}),
                "long_token_metadata": available_tokens.get(raw_market[2], {}),
                "long_token_address": raw_market[2],
                "short_token_metadata": available_tokens.get(raw_market[3], {}),
                "short_token_address": raw_market[3],
            }

    @staticmethod
    def _get_market_symbol(available_tokens: dict[str, dict[str, Any]], raw_market: tuple) -> str:
        """
        Generate the market symbol for a given market, handling cases for swaps.

        :param available_tokens: A dictionary mapping token addresses to metadata.
        :param raw_market: A tuple containing raw market data from the contract.
        :return: The market symbol as a string.
        """
        market_symbol: str = available_tokens[raw_market[1]]["symbol"]
        if raw_market[2] == raw_market[3]:
            market_symbol = f"{market_symbol}2"
        return market_symbol

    def _is_index_token_in_signed_prices_api(self, index_token_address: str) -> bool:
        """
        Check if the index token is included in the signed prices API.

        :param index_token_address: The address of the index token.
        :return: True if the index token is present in the API, otherwise False.
        """
        try:
            if not self._prices:
                self._prices: dict[str, dict[str, int]] = OraclePrices(config=self.config).get_recent_prices()

            if index_token_address == self.config.zero_address:
                return True
            return bool(self._prices.get(index_token_address))

        except KeyError:
            self.logger.warning(f"Market {index_token_address} is not live on RFX.")
            return False
