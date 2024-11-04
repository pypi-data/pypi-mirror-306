from setuptools import setup, find_packages

setup(
    name="noir-game-engine",
    version="0.1.0",
    description="A beginner-friendly game engine for text-based adventures",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Andrew Muratov",
    author_email="andrewamuratov@gmail.com",
    url="https://github.com/yourusername/noir",  # Update with your repository URL
    packages=find_packages(),
    install_requires=["InquirerPy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)