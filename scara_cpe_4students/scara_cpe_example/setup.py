from setuptools import find_packages, setup

package_name = 'scara_cpe_example'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='triton-01',
    maintainer_email='nicolas.lehaut83@gmail.com',
    description='scara trajectory publisher',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [ 'publisher = scara_cpe_example.scara_publisher:main',
        ],
    },
)
