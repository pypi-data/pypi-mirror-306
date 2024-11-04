from setuptools import setup

setup(
    name="oip-tracking-client",
    version="0.0.6",
    author="Rachid Belmeskine",
    author_email="rachid.belmeskine@gmail.com",
    description="This is the API client of Open Innovation Platform - Tracking",
    long_description=open("README.public.md").read(),
    long_description_content_type="text/markdown",
    # url='https://github.com/...',
    python_requires=">=3.7",
    packages=[
        "oip_tracking_client",
        "oip_tracking_client.enums",
        "oip_tracking_client.monitors",
    ],
    install_requires=[
        "requests",
        "pandas",
        "typing",
        "mlflow==2.11.3",
        "numpy",
        "Pillow",
        "matplotlib",
        "plotly",
        "psutil",
    ],
    extras_require={"amd": ["pyamdgpuinfo"], "nvidia": ["pynvml"]},
    license="PRIVATE LICENSE",
)
