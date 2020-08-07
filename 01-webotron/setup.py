from setuptools import setup

setup(
    name='webotron',
    version='0.1',
    author='Chris Kilpatrick',
    author_email='chris.kilpatrick@outlook.com',
    description='Webotron is a tool to deploy static websites to AWS.',
    license='GPLv3+',
    packages=['webotron'],
    url='https://github.com/ckckcklab/aws-python-automation/tree/master/01-webotron',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    '''
)