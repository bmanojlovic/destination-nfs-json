#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
# Copyright (c) 2023 Boris Manojlovic <boris@steki.net>, all rights reserved.
#



from setuptools import find_packages, setup

MAIN_REQUIREMENTS = [
    "airbyte-cdk", "libnfs"
]

TEST_REQUIREMENTS = ["pytest~=6.2"]

setup(
    name="destination_nfs_json",
    description="Destination NFS JSON implementation.",
    author="Airbyte",
    author_email="boris@steki.net",
    packages=find_packages(),
    install_requires=MAIN_REQUIREMENTS,
    package_data={"": ["*.json"]},
    extras_require={
        "tests": TEST_REQUIREMENTS,
    },
)
