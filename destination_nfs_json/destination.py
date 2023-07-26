#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
# Copyright (c) 2023 Boris Manojlovic <boris@steki.net>, all rights reserved.
#

import uuid
from typing import Any, Iterable, Mapping

from airbyte_cdk import AirbyteLogger
from airbyte_cdk.destinations import Destination
from airbyte_cdk.models import AirbyteConnectionStatus, AirbyteMessage, ConfiguredAirbyteCatalog, DestinationSyncMode, Status, Type
import libnfs
from os import path

from logging import Logger, getLogger

from .client import NFSClient
logger = getLogger("airbyte")

class DestinationNFSJSON(Destination):
    def write(
        self, config: Mapping[str, Any], configured_catalog: ConfiguredAirbyteCatalog, input_messages: Iterable[AirbyteMessage]
    ) -> Iterable[AirbyteMessage]:
        

        with NFSClient(**config) as writer:
            for configured_stream in configured_catalog.streams:
                if configured_stream.destination_sync_mode == DestinationSyncMode.overwrite:
                    writer.delete(configured_stream.stream.name)

            for message in input_messages:
                if message.type == Type.STATE:
                    yield message
                elif message.type == Type.RECORD:
                    record = message.record
                    writer.write(record.stream, record.data)
                else:
                    # ignore other message types for now
                    continue


    def check(self, logger: AirbyteLogger, config: Mapping[str, Any]) -> AirbyteConnectionStatus:
        try:
            stream = str(uuid.uuid4())
            with NFSClient(**config) as writer:
                writer.write(stream, {"value": "_airbyte_connection_check"})
                writer.delete(stream)
            return AirbyteConnectionStatus(status=Status.SUCCEEDED)
        except Exception as e:
            return AirbyteConnectionStatus(status=Status.FAILED, message=f"An exception occurred: {repr(e)}")
