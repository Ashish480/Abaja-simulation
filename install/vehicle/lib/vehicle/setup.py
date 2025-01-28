from setuptools import setup

package_name = 'vehicle'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    py_modules=['calibration_publisher'],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'calibration_publisher = vehicle.calibration_publisher:main',
        ],
    },
)

