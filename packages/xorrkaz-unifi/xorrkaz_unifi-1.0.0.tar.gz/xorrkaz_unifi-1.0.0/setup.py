from setuptools import setup, find_packages


setup(
    name="xorrkaz-unifi",
    version="1.0.0",
    description="Utilities for working with UniFi controllers",
    author="Joe Clarke",
    author_email="jclarke@marcuscom.com",
    license="MIT",
    setup_requires=["wheel"],
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
