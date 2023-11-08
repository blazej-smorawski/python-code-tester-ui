from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="pomorski_czarodziej_components",
    version="0.0.1",
    author="Błażej Smorawski",
    author_email="blazej.smorawski@gmail.com",
    description="Streamlit custom components used at pomorskiczarodziej.pl",
    long_description=setuptools.find_packages(),
    long_description_content_type="text/markdown",
    url="",
    packages=["front_page_component"],
    package_dir={"deps.pomorski_czarodziej_components": "pomorski_czarodziej_components"},
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        "streamlit >= 0.63",
    ],
    extras_require={
        "devel": [
            "wheel",
            "pytest==7.4.0",
            "playwright==1.39.0",
            "requests==2.31.0",
            "pytest-playwright-snapshot==1.0",
            "pytest-rerunfailures==12.0",
        ]
    }
)
