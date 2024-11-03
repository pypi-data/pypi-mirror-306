from setuptools import setup, find_packages

setup(
    name="autocash",
    version="0.2",
    author="DarkSide",
    author_email="support@darksidehost.com",
    description="auto payments lib, Egypt and Iraq",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LSEGITHUB/VFCashPython",
    packages=find_packages(),
    install_requires=[
        "requests"  # أي مكتبات أخرى تحتاجها
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
