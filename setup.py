from setuptools import setup, find_packages

setup(name="snapshot",
    version="0.1",
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        "console_scripts": ['snapshot=snapshot.snapshot:snapshot']
    }
)
