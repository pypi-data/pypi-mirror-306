# setup.py

from setuptools import setup, find_packages

setup(
    name="ip_checker_boyuan",
    version="1.0.0",
    description="A simple IP address checker",
    author="Boyuan Lian",
    packages=find_packages(),
    py_modules=["ip_checker_boyuan"],
    entry_points={
        "console_scripts": [
            "ip_checker_boyuan=ip_checker_boyuan:get_ip_address"
        ]
    },
    install_requires=[],
)
