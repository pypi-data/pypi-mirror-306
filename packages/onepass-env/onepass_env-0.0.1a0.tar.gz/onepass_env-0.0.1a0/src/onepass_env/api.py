import logging
import os
import re
from typing import Optional, IO

import dotenv
from dotenv.main import StrPath
from onepassword import OnePassword

_logger = logging.getLogger(__name__)


def load(
    dotenv_path: Optional[StrPath] = None,
    stream: Optional[IO[str]] = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
    encoding: Optional[str] = "utf-8",
) -> None:
    dotenv.load_dotenv(
        dotenv_path=dotenv_path,
        stream=stream,
        verbose=verbose,
        override=override,
        interpolate=interpolate,
        encoding=encoding,
    )

    ref_pattern = re.compile(r"op://.+")

    op = OnePassword()
    for item in os.environ:
        if ref_pattern.match(os.environ[item]):
            os.environ[item] = op.read(os.environ[item])
