from setuptools import setup, find_packages

setup(
    name="EasyProject",
    version="0.1.0",
    author="Oliver Bullock",
    author_email="oliver@kinetic-code.org",
    description="Library used to easily manage a Project Plan.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/oliver/EasyProject",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # Add your project's dependencies here
        # e.g., 'requests>=2.20.0',
        'pywin32>=306'
    ],
)