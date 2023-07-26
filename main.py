#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
# Copyright (c) 2023 Boris Manojlovic <boris@steki.net>, all rights reserved.
#



import sys

from destination_nfs_json import DestinationNFSJSON

if __name__ == "__main__":
    DestinationNFSJSON().run(sys.argv[1:])
