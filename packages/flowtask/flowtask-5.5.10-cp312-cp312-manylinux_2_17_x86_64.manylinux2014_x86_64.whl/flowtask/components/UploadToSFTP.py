import asyncio
from collections.abc import Callable
import asyncssh
from ..exceptions import ComponentError, FileNotFound
from .UploadTo import UploadToBase
from ..interfaces.SSHClient import SSHClient


class UploadToSFTP(SSHClient, UploadToBase):
    """
    uploadToSFTP.

    Upload a file (or collection of files) to a SSH/SFTP Server.
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.mdate = None
        self.local_name = None
        self.filename: str = ""
        self.whole_dir: bool = False
        self.preserve = True
        self.block_size: int = 65356
        self.max_requests: int = 1
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """start Method."""
        await super(UploadToSFTP, self).start(**kwargs)
        if hasattr(self, "source"):
            self.whole_dir = (
                self.source["whole_dir"] if "whole_dir" in self.source else False
            )
        if hasattr(self, "destination"):
            self.directory = self.destination["directory"]
        try:
            if self.previous and self.input:
                self.filename = self.input
            elif self.file:
                self.filename = self.process_pattern("file")
        except (NameError, KeyError):
            pass
        return self

    def upload_progress(self, srcpath, dstpath, bytes_copied, total_bytes):
        self._pb.reset(total=total_bytes)
        self._pb.update(bytes_copied)
        self._pb.refresh()

    async def run(self):
        """Running Download file."""
        self._result = None
        status = False
        try:
            print('CREDENTIALS > ', self.credentials)
            async with await self.open(
                host=self.host,
                port=self.port,
                tunnel=self.tunnel,
                credentials=self.credentials,
            ):
                async with self._connection.start_sftp_client() as sftp:
                    # check all versions of functionalities
                    args = {
                        "block_size": self.block_size,
                        "max_requests": self.max_requests,
                        "progress_handler": self.upload_progress,
                        "error_handler": self.err_handler,
                    }
                    if self.whole_dir is True:
                        self._logger.debug(
                            f"Uploading all files on directory {self.source_dir}"
                        )
                        file = "{}/*".format(self.source_dir)
                        p = self.source_dir.glob("**/*")
                        self.filename = [x for x in p if x.is_file()]
                    else:
                        file = self.filename
                    args["remotepath"] = self.directory
                    if hasattr(self, "source"):
                        args["recurse"] = True if "recursive" in self.source else False
                    if not file:
                        raise FileNotFound(f"There is no local File: {file}")
                    self.start_progress(total=len(file))
                    try:
                        self._logger.debug(f"Uploading file: {file} to {self.directory}")
                        status = await sftp.mput(file, **args)
                        self.close_progress()
                    except OSError as err:
                        self._logger.error(f"Upload SFTP local error: {err}")
                        return False
                    except asyncssh.sftp.SFTPError as err:
                        self._logger.error(f"SFTP UploadTo Server error: {err}")
                        return False
                    except asyncssh.Error as err:
                        self._logger.error(f"Upload 2 SFTP: connection failed: {err}")
                    except Exception as err:
                        self._logger.exception(err)
                        raise
        except asyncio.CancelledError:
            self._logger.info(
                f"{self.host} CANCELED~"
            )
            # break
        except (asyncio.TimeoutError, ComponentError) as err:
            raise ComponentError(f"{err!s}") from err
        except Exception as err:
            raise ComponentError(f"{err!s}") from err
        if status is False:
            return False
        else:
            self.add_metric("SFTP_FILES", self.filename)
            self._result = self.filename
            return self._result
