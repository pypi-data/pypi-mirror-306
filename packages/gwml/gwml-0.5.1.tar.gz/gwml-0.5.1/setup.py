from setuptools import setup, find_packages

setup(
    name="gwml",
    version="0.5.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    entry_points={"console_scripts": ["gwml = gwml.main:main"]},
    zip_safe=False,
)
