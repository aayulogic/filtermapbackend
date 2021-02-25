from setuptools import find_packages, setup

setup(
    name='filter_map',
    packages=find_packages(include='filter_map'),
    version='0.0.1',
    description='FilterMapBackend is FilterBackend  like DjangoFilterBackend',
    author='Aayulogic Pvt. Ltd.',
    license='GNU GENERAL PUBLIC LICENSE',
    install_requires=[        
        'Django>=2.2',
        'django-filter>=2.1.0',
        'djangorestframework>=3.9.2'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)