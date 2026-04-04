from setuptools import setup, find_packages

setup(name="snapshot",
    version="0.1",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "prompt_toolkit"
    ],
    entry_points={
        "console_scripts": [
            'ss=snapshot.snapshot:snapshot',
            'sr=snapshot.snapshot:snapshot_rereference',
            'si=snapshot.snapshot:snapshot_inspect',
            ]
    }
)
