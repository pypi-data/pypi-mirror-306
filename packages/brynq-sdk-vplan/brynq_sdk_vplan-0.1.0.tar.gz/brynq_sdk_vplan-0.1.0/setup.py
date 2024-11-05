from setuptools import setup

setup(
    name='brynq_sdk_vplan',
    version='0.1.0',
    description='vPlan wrapper from BrynQ',
    long_description='vPlan wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.vplan"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'pandas>=2,<3'
    ],
    zip_safe=False,
)
