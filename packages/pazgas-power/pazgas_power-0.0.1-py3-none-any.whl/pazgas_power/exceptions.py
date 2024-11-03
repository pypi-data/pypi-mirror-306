"""This module contains the set of PazGas Power API exceptions."""


class PazGasPowerError(Exception):
    """Exception raised for errors in PazGas Power API."""

    def __init__(self, error):
        self.error = error
        super().__init__(self.error)
