import asyncio
from collections.abc import Callable
from ..exceptions import ComponentError, ConfigError
from .tPandas import tPandas


class tUnnest(tPandas):
    """
    tUnnest.

    Split a Column into several rows, alternative with dropping source column.
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.source_column: str = kwargs.pop('source_column', None)
        self.destination: str = kwargs.get('destination', None)
        self.drop_source: bool = kwargs.get('drop_source', False)
        self.separator: str = kwargs.get('separator', ', ')
        if not self.source_column:
            raise ConfigError(
                "Missing Source_column for making unnest."
            )
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def _run(self):
        try:
            # Split the column into multiple rows
            df = self.data.assign(
                **{
                    self.destination: self.data[self.source_column].str.split(self.separator)
                }
            ).explode(self.destination)
            if self.drop_source is True:
                # Drop the original column
                df = df.drop(columns=[self.source_column])
            return df
        except Exception as err:
            raise ComponentError(
                f"Unknown error {err!s}"
            ) from err
