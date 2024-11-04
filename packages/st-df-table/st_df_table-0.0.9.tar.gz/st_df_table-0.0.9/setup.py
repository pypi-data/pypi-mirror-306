from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="st-df-table",
    version="0.0.9",
    author="Piotr Synowiec",
    author_email="psynowiec@gmail.com",
    description="Alternative to `st.table` with configuration displaying Pandas DataFrame",
    license="MIT",
    keywords=["streamlit", "streamlit-component"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mysiar-org/st-table",
    project_urls={
        "Documentation": "https://mysiar-org.github.io/st-df-table",
        "Changelog": "https://github.com/mysiar-org/st-table/blob/master/CHANGELOG.md",
        "Issues": "https://github.com/mysiar-org/st-table/issues",
        "Examples": "https://mysiar-org-st-table-st-df.streamlit.app",
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
    install_requires=["streamlit >= 0.63", "pandas"],
    extras_require={
        "devel": [
            "wheel",
        ]
    },
)
