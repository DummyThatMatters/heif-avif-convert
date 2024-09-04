from setuptools import setup, find_packages

setup(
    name='heic_conv',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'alive-progress',
        'Pillow',
        'pillow_heif',

    ],
    entry_points={
        'console_scripts': [
            'process = heic_conv.main:process',
        ],
    },
)