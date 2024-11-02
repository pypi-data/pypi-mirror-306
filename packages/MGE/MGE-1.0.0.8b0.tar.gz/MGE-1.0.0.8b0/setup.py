from setuptools import setup

setup(
    name="MGE",
    version="1.0.0.8-beta",
    license='zlib',
    description="LibMGE is a graphical user interface library for developing 2D programs and games.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lucas Guimarães",
    author_email="commercial@lucasguimaraes.pro",
    url="https://libmge.org/",
    project_urls={
        "Source": "https://github.com/MonumentalGames/LibMGE",
        "Documentation": "https://docs.libmge.org/",
        "Author Website": "https://lucasguimaraes.pro/"
    },
    python_requires=">=3.5",
    packages=[
          "MGE",
          "MGE/_sdl",
          "MGE/_InputsEmulator",
          "MGE/_ConsoleScripts"
    ],
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        'License :: OSI Approved :: zlib/libpng License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'MGE=MGE._ConsoleScripts:main',
            'mge=MGE._ConsoleScripts:main',
        ],
    },
    keywords="2D development, graphical interface, games",
)
