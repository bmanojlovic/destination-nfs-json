#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
# Copyright (c) 2023 Boris Manojlovic <boris@steki.net>, all rights reserved.
#

import time
from logging import Logger, getLogger
from typing import Any, Mapping, Dict, List, TextIO
from os import path
import errno
import json

import libnfs 

logger = getLogger("airbyte")
class NFSClient:
    def __init__(
            self,
            host: str,
            shared_directory: str,
            destination_path: str,
            nfsversion: str,
    ):
        logger.info("nfsclient:__init__")
        self.host = host,
        self.shared_directory = shared_directory
        self.destination_path = destination_path
        self.nfsversion = nfsversion
        self.url = url="nfs://" + path.join(host,shared_directory.lstrip('/') + f"?version={nfsversion}")
        self._files: Dict[str, TextIO] = {}
        self.client = libnfs.NFS(url=self.url)
            

    def _get_path(self, stream: str) -> str:
        return path.join(self.destination_path,f"airbyte_json_{stream}.jsonl")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _open(self, stream: str) -> TextIO:
        uri = self._get_path(stream)
        return self.client.open(uri,mode="a+")

    def close(self):
        for file in self._files.values():
            file.close()

    def write(self, stream: str, record: Dict) -> None:
        if stream not in self._files:
            self._files[stream] = self._open(stream)
        text = json.dumps(record)
        self._files[stream].write(f"{text}\n")

    def read_data(self, stream: str) -> List[Dict]:
        with self._open(stream) as file:
            pos = file.tell()
            file.seek(0)
            lines = file.readlines()
            file.seek(pos)
            data = [json.loads(line.strip()) for line in lines]
        return data

    def delete(self, stream: str) -> None:
        try:
            path = self._get_path(stream)
            self.client.unlink(path)
        except IOError as err:
            # Ignore the case where the file doesn't exist, only raise the
            # exception if it's something else
            if err.errno != errno.ENOENT:
                raise
