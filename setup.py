import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twitch-chat-analyzer", # Replace with your own username
    version="0.0.4",
    author="Rainbow",
    author_email="c.rainbow.678@gmail.com",
    description="Twitch chat analyzer from past broadcasts, designed for Jupyter notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/c-rainbow/twitch-chat-analyzer-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
