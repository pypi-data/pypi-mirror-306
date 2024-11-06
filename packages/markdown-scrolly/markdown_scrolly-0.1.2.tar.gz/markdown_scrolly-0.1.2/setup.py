import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="markdown-scrolly",
    version="0.1.2",
    author="Willy Pregliasco",
    author_email="willy.pregliasco@gmail.com",
    description=("MD renderer for control aestetics using CSS "
                " and to include simple scroll animations."),
    license_files = ('LICENSE',),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "Gitlab Page": "https://gitlab.com/wpregliasco/markdown-scrolly",
        "Bug Tracker": "https://gitlab.com/wpregliasco/markdown-scrolly/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["markdown"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        "scrolly": ["resources/*"],  # Include all files in 'resources' folder
    },
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "scrolly = scrolly.cli:main",
            "html_package = scrolly.cli_pkg:main"
        ]
    }
)
