from setuptools import setup, find_packages

setup(
    name="algosto",
    version="0.0.13",
    author="Melvine Nargeot",
    author_email="melvine.nargeot@gmail.com",
    description="Algosto implements stochastic optimization algorithms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Melvin-klein/algosto",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[],
)
