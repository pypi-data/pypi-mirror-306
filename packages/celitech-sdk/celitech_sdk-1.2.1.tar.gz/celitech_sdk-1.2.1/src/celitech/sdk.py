from typing import Union
from .services.destinations import DestinationsService
from .services.packages import PackagesService
from .services.purchases import PurchasesService
from .services.e_sim import ESimService
from .net.environment import Environment


class Celitech:
    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        base_url: Union[Environment, str] = Environment.DEFAULT,
        timeout: int = 60000,
    ):
        """
        Initializes Celitech the SDK class.
        """

        self._base_url = (
            base_url.value if isinstance(base_url, Environment) else base_url
        )
        self.destinations = DestinationsService(base_url=self._base_url)
        self.packages = PackagesService(base_url=self._base_url)
        self.purchases = PurchasesService(base_url=self._base_url)
        self.e_sim = ESimService(base_url=self._base_url)
        self.set_additional_variables(client_id, client_secret)
        self.set_timeout(timeout)

    def set_base_url(self, base_url: Union[Environment, str]):
        """
        Sets the base URL for the entire SDK.

        :param Union[Environment, str] base_url: The base URL to be set.
        :return: The SDK instance.
        """
        self._base_url = (
            base_url.value if isinstance(base_url, Environment) else base_url
        )

        self.destinations.set_base_url(self._base_url)
        self.packages.set_base_url(self._base_url)
        self.purchases.set_base_url(self._base_url)
        self.e_sim.set_base_url(self._base_url)

        return self

    def set_additional_variables(
        self, client_id: str = None, client_secret: str = None
    ):
        """
        Sets the additional variables for the entire SDK.
        """
        self.destinations.set_additional_variables(client_id, client_secret)
        self.packages.set_additional_variables(client_id, client_secret)
        self.purchases.set_additional_variables(client_id, client_secret)
        self.e_sim.set_additional_variables(client_id, client_secret)

        return self

    def set_timeout(self, timeout: int):
        """
        Sets the timeout for the entire SDK.

        :param int timeout: The timeout (ms) to be set.
        :return: The SDK instance.
        """
        self.destinations.set_timeout(timeout)
        self.packages.set_timeout(timeout)
        self.purchases.set_timeout(timeout)
        self.e_sim.set_timeout(timeout)

        return self


# c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
