import subprocess
import pkg_resources


def is_package_installed(package_name):
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False


def pkg_install(module: str):
    if is_package_installed(module) is False:
        subprocess.run(["pip", "install", module], check=True)
