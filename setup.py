from pathlib import Path

from setuptools import find_packages, setup

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="django-utils",
    version="0.1.0",
    author="buswedg",
    author_email="buswedg@djangomango.com",
    url="https://github.com/djangomango/django-utils/",
    license="GNU Lesser General Public License v3 (LGPLv3)",
    description="Collection of common utilities, helpers, mixins, and middleware for Django.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "django_utils": ["helpers/data/*"],
    },
    install_requires=[
        "Django>=4.2",
    ],
    extras_require={
        "all": [
            "python-magic>=0.4.27",
            "requests>=2.28.0",
        ],
        "requests": ["requests>=2.28.0"],
        "magic": ["python-magic>=0.4.27"],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.10",
)
