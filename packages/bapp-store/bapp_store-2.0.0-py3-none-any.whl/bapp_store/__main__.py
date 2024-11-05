import argparse
import requests
import re
import os
import subprocess
import json
import shutil
from rich.console import Console
from rich.table import Table


def fetch_github_repositories(query=None):
    search_query = "topic:beepy-app"
    if query:
        search_query += f" {query}"

    response = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": search_query},
        headers={"Accept": "application/vnd.github.v3+json"},
    )
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print("Failed to fetch data from GitHub")
        return []


def display_repositories(repositories):
    if not repositories:
        print("No packages found matching your search criteria.")
        return

    console = Console()
    table = Table(title="Available Packages")

    table.add_column("Package Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Stars", justify="right", style="green")

    for repo in repositories:
        package_name = f"{repo['owner']['login']}/{repo['name']}"
        description = repo["description"] or "No description"
        stars = str(repo["stargazers_count"])
        table.add_row(package_name, description, stars)

    console.print(table)


def is_valid_package_name(package_name, repositories):
    """Validate package name format and existence in repositories."""
    pattern = r"^[a-zA-Z0-9-]+/[a-zA-Z0-9-]+$"
    if not re.match(pattern, package_name):
        return False

    # Check if the package exists in the fetched repositories
    return any(
        f"{repo['owner']['login']}/{repo['name']}" == package_name
        for repo in repositories
    )


def install_package(package_name):
    """Clone the GitHub repository to a sensible location."""
    install_dir = "/tmp/bapp-store-packages"
    os.makedirs(install_dir, exist_ok=True)

    repo_url = f"https://github.com/{package_name}.git"
    clone_dir = os.path.join(install_dir, package_name.split("/")[1])

    # Delete the tmp dir before cloning into it:
    subprocess.run(["rm", "-fr", clone_dir])

    try:
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
        print(f"Package {package_name} installed successfully in {clone_dir}")
        version = extract_version(clone_dir)
        target_dir = os.path.expanduser(
            f"~/bapp-store-packages/packages/{package_name}/{version}"
        )

        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            shutil.copytree(clone_dir, target_dir, dirs_exist_ok=True)
            print(f"Package {package_name} version {version} copied to {target_dir}")
            subprocess.run(["just", "beepy-install"], cwd=target_dir, check=True)
            update_installed_packages(package_name, version)
        else:
            print(
                f"Package {package_name} version {version} already exists at {target_dir}"
            )
        shutil.rmtree(clone_dir)
        print(f"Temporary directory {clone_dir} deleted.")
    except subprocess.CalledProcessError:
        print(f"Failed to install package {package_name}.")


def extract_version(clone_dir):
    """Extract the version string from bapp-details.json."""
    details_file = os.path.join(clone_dir, "bapp-details.json")
    try:
        with open(details_file, "r") as file:
            data = json.load(file)
            version = data.get("version", "Unknown version")
            print(f"Package version: {version}")
        return version
    except FileNotFoundError:
        print("bapp-details.json not found.")
    except json.JSONDecodeError:
        print("Error decoding bapp-details.json.")


def update_installed_packages(package_name, version):
    """Update the installed_packages.json file with the new package."""
    installed_packages_file = os.path.expanduser(
        "~/bapp-store-packages/installed_packages.json"
    )
    package_entry = {"name": package_name, "version": version}

    if not os.path.exists(installed_packages_file):
        # Create the file with an initial structure
        with open(installed_packages_file, "w") as file:
            json.dump({"packages": [package_entry]}, file, indent=4)
    else:
        # Load existing data and update it
        with open(installed_packages_file, "r") as file:
            data = json.load(file)

        data["packages"].append(package_entry)

        with open(installed_packages_file, "w") as file:
            json.dump(data, file, indent=4)

    print(
        f"Package {package_name} version {version} recorded in installed_packages.json."
    )


def list_installed_packages():
    """List all installed packages using Rich."""
    installed_packages_file = os.path.expanduser(
        "~/bapp-store-packages/installed_packages.json"
    )

    if not os.path.exists(installed_packages_file):
        print("No packages installed.")
        return

    with open(installed_packages_file, "r") as file:
        data = json.load(file)

    packages = data.get("packages", [])

    if not packages:
        print("No packages installed.")
        return

    console = Console()
    table = Table(title="Installed Packages")

    table.add_column("Package Name", style="cyan", no_wrap=True)
    table.add_column("Version", style="magenta")

    for package in packages:
        table.add_row(package["name"], package["version"])

    console.print(table)


def remove_package(package_name):
    """Remove a package by running 'just beepy-remove' and deleting its directory."""
    installed_packages_file = os.path.expanduser(
        "~/bapp-store-packages/installed_packages.json"
    )

    if not os.path.exists(installed_packages_file):
        print("No packages installed.")
        return

    with open(installed_packages_file, "r") as file:
        data = json.load(file)

    packages = data.get("packages", [])
    package_versions = [pkg for pkg in packages if pkg["name"] == package_name]

    if not package_versions:
        print(f"Package {package_name} not found in installed packages.")
        return

    for package in package_versions:
        version = package["version"]
        package_dir = os.path.expanduser(
            f"~/bapp-store-packages/packages/{package_name}/{version}"
        )

        if os.path.exists(package_dir):
            try:
                subprocess.run(["just", "beepy-remove"], cwd=package_dir, check=True)
                print(f"Package {package_name} version {version} removed successfully.")
            except subprocess.CalledProcessError:
                print(f"Failed to remove package {package_name} version {version}.")
                return

    # Remove all versions of the package
    package_base_dir = os.path.expanduser(
        f"~/bapp-store-packages/packages/{package_name}"
    )
    shutil.rmtree(package_base_dir, ignore_errors=True)
    print(f"All versions of package {package_name} deleted.")

    # Update the installed packages file
    data["packages"] = [pkg for pkg in packages if pkg["name"] != package_name]
    with open(installed_packages_file, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Package {package_name} removed from installed_packages.json.")


def main():
    parser = argparse.ArgumentParser(description="bapp-store Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Help command
    help_parser = subparsers.add_parser("help", help="Show help message")
    search_parser = subparsers.add_parser("search", help="Search for a package")
    search_parser.add_argument(
        "package_name", type=str, help="Name of the package to search"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all available packages")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install a package")
    install_parser.add_argument(
        "package_name", type=str, help="Name of the package to install"
    )

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a package")
    remove_parser.add_argument(
        "package_name", type=str, help="Name of the package to remove"
    )

    # List-installed command
    list_installed_parser = subparsers.add_parser(
        "list-installed", help="List all installed packages"
    )

    args = parser.parse_args()

    if args.command == "search":
        print(f"Searching for package: {args.package_name}")
        repositories = fetch_github_repositories(args.package_name)
        display_repositories(repositories)
    elif args.command == "list":
        print("Listing all available packages from GitHub with topic 'beepy-app':")
        repositories = fetch_github_repositories()
        display_repositories(repositories)
    elif args.command == "install":
        repositories = fetch_github_repositories()
        if is_valid_package_name(args.package_name, repositories):
            print(f"Installing package: {args.package_name}")
            install_package(args.package_name)
        else:
            print("Package not found")
    elif args.command == "remove":
        remove_package(args.package_name)
    elif args.command == "list-installed":
        list_installed_packages()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
