import asyncio
from typing import List
from collections.abc import Callable
import pandas
from ..exceptions import ComponentError
from .tPandas import tPandas


class tPluckCols(tPandas):
    """
    tPluckCols.

    Overview

         Return only the subset of columns from Dataframe.

    .. table:: Properties
       :widths: auto

    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.columns: List = None
        super(tPluckCols, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        await super().start(**kwargs)
        if not self.columns:
            raise ComponentError("Error: need to specify a list of *columns*")
        return True

    async def _run(self):
        return self.data[self.columns].copy()
