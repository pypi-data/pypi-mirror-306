from setuptools import setup, find_packages

setup(
    name="XenValidator",
    version="0.1.2",
    author="Xenigma",
    author_email="helpworkagents@gmail.com",
    description="XenValidator is schema validation library for Python, You can Validate Strings, Numbers, Objects, Arrays, Dates, URLs & more. You can even create your custom validators! Make sure to give it a ⭐ on github.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/XenigmaAi/validator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
