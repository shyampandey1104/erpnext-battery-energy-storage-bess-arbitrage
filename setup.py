from setuptools import setup, find_packages

setup(
    name="erpnext-battery-energy-storage-bess-arbitrage",
    version="1.0.0",
    description="ERPNext BESS Arbitrage Engine: Grid-Scale Battery Dispatch, IEX DAM/RTM Power Arbitrage & Degradation Cycle Guard.",
    author="Shyam Kumar Pandey",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
