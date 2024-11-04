import setuptools

setuptools.setup(
    name="shervan_shahparnia_calculator_4195",
    version="0.0.5",
    author="Shervan Shahparnia",
    author_email= "shervan.shahparnia@sjsu.edu",
    description="A small but useful calculator package",
    long_description="A small calculator package",
    long_description_content_type="text/markdown",
    url="https://github.com/Sshahparnia/my_calculator",
    packages=['calculator', 'tests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_required='>=3.11',
)


