from setuptools import setup, find_packages

from lib import version

setup(
    name="ocrodjvu",
    version=version.__version__,
    packages=find_packages(exclude=['tests','tests.*']),
    scripts=["hocr2djvused"],

    install_requires=["python-djvulibre", "pyicu"],

    package_data={
    },
    test_suite='nose.collector'
)
