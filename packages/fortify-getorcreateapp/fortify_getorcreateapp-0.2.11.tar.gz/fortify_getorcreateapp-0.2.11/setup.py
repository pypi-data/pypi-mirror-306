import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fortify_getorcreateapp",
    version="0.2.11",
    author="Fabio Arciniegas",
    author_email="fabio_arciniegas@trendmicro.com",
    description="Get fortify application and version ids, create if they don't exist",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://dsgithub.trendmicro.com/cloudone-common/fortify-getorcreateapp",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts':
        ['fortify-getorcreateapp=fortify_getorcreateapp.fortify_getorcreateapp:cli'],
    },
    test_suite='nose.collector',
    tests_require=['nose'],
    python_requires='>=3.6',
    install_requires=[
        'fortifyapi',
        'requests'
    ]
)
