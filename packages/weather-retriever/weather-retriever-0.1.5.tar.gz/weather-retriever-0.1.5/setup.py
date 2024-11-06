from setuptools import setup


def requirements():
    with open("requirements.txt", encoding="utf-8-sig") as f:
        requirements = f.readlines()
    return requirements


def readme():
    with open("README.md", encoding="utf-8-sig") as f:
        README = f.read()
    return README


if __name__ == "__main__":
    setup(
        name="weather-retriever",
        version="0.1.5",
        packages=["weather_retriever"],
        install_requires=requirements(),
        include_package_data=True,  # Include files specified in 'MANIFEST.in'.
        author="KimRass",
        author_email="purflow64@gmail.com",
        description="Natural Language Weather Retriever",
        long_description=readme(),
        long_description_content_type="text/markdown",
        url="https://github.com/KimRass/weather-retriever",
        license="Apache License 2.0",
    )
