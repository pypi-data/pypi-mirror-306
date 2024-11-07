import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plutonium-238",
    version="0.2.9",
    author="tom",
    author_email="tom@google.com",
    description="SCA Agent, Copyright@Plutonium",
    entry_points={
        "console_scripts": ["plutonium=plutonium.cli:main",]
    },
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.google.com",
    packages=["plutonium",],
    include_package_data=True,
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "Topic :: Security",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
)
