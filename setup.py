import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name="thermostat", # Replace with your own username
    version="0.0.1",
    author="Jordan Medlock",
    author_email="jordanemedlock@gmail.com",
    description="Home Raspberry Pi Thermostat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jordanemedlock/thermostat",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    package_data={
        "": ["*.html", "*.js", "*.css", "*.ts", "*.scss", "*.css.map"]
    }
)