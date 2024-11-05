from setuptools import setup, find_packages

setup(
    name="tabs2music",
    version="0.0.8",
    packages=find_packages(),
    install_requires=[
        "midi2audio==0.1.1",
        "MIDIUtil==1.2.1",
    ],
    author="Yusef Ahmed",
    description="Converts guitar tabs (.txt) into audio (.wav)",
    license='MIT',
    url='https://github.com/yusefahmd/tabs2music',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)