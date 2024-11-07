# Third Party
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="daily_active_users",  # Replace with your own username
    version="0.1.1",
    author="Mitchell Kotler",
    author_email="mitch@muckrock.com",
    description="Django logging of daily active users",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muckrock/daily-active-users/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "django",
    ],
    python_requires=">=3.6",
)
