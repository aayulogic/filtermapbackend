from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='drf-filtermapbackend',
    packages=find_packages(include=['filter_map']),
    version='0.0.1',
    description='FilterBackend which takes mapping of query params to field name.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Aayulogic Pvt. Ltd.',
    author_email='info@aayulogic.com',
    license='GNU GENERAL PUBLIC LICENSE',
    url="https://github.com/aayulogic/filtermapbackend/",
    project_urls={
        "Bug Tracker": "https://github.com/aayulogic/filtermapbackend/issues",
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        ],
    install_requires=[
        'Django>=2.2',
        'django-filter>=2.1.0',
        'djangorestframework>=3.9.2'
    ],
    tests_require=['pytest'],
    test_suite='pytest',
    python_requires='>=3.6',
)
