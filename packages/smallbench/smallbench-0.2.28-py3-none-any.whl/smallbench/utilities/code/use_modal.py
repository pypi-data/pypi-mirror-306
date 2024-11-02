import io
from typing import Dict, Optional, Tuple
# import asyncio
# import time

import modal

# Create a shared App object
app = modal.App.lookup("agent-sandboxes", create_if_missing=True)


async def execute_code_modal_async(
    script_to_run_by_name: str,
    scripts_by_name: Dict[str, str],
    dir_name: str,
    python_version="3.9",
    packages=[],
    verbose=False,
) -> Tuple[str, Optional[str]]:
    default_packages = [
        "pandas",
        "numpy",
    ]
    packages = list(set(packages + default_packages))
    for name, script in scripts_by_name.items():
        if (
            "from matplotlib import pyplot as plt" not in script
            and "import pyplot as plt" in script
        ):
            print("Whoops!")
            script = script.replace(
                "import pyplot as plt", "import matplotlib.pyplot as plt"
            )
            scripts_by_name[name] = script
        if "os." in script and not "import os" in script:
            print("Whoops!")
            script = "import os\n" + script
            scripts_by_name[name] = script
    # with modal.enable_output():
    with modal.NetworkFileSystem.ephemeral() as nfs:
        for name, script in scripts_by_name.items():
            await nfs.write_file.aio(name, io.BytesIO(script.encode()))
        image = modal.Image.debian_slim(python_version=python_version)

        # Initialize a set to store unique system packages to install
        system_packages = set()

        # Check if OpenCV-related packages are present
        if any(pkg.lower() in ["opencv", "opencv-python"] for pkg in packages):
            system_packages.update(
                [
                    "libjpeg-dev",
                    "libpng-dev",
                    "libtiff-dev",
                    "libavcodec-dev",
                    "libavformat-dev",
                    "libswscale-dev",
                    "libv4l-dev",
                    "libxvidcore-dev",
                    "libx264-dev",
                    "libgtk-3-dev",
                    "libatlas-base-dev",
                    "gfortran",
                    "libgl1-mesa-glx",
                    "libglib2.0-0",
                ]
            )

        # Check if Pillow-related packages are present
        if any(pkg.lower() in ["pillow", "pil"] for pkg in packages):
            system_packages.update(
                [
                    "libjpeg-dev",
                    "zlib1g-dev",
                    "libpng-dev",
                    "libtiff-dev",
                    "libfreetype6-dev",
                    "liblcms2-dev",
                    "libwebp-dev",
                    "tcl8.6-dev",
                    "tk8.6-dev",
                    "python3-tk",
                ]
            )

        # If there are system packages to install, perform the installation
        if system_packages:
            system_install_command = "apt-get update && apt-get install -y " + " ".join(
                system_packages
            )
            image = image.run_commands(system_install_command)
            print(f"Installed system packages: {', '.join(system_packages)}")

        # Proceed with pip installations if there are Python packages to install
        if packages:
            # print("-----------------")
            # print(f"Script to run: {script_to_run_by_name}")
            # print(f"Scripts by name: {scripts_by_name}")
            # print(f"Packages: {packages}")

            # Install 'uv' first if it's in the packages list or required separately
            if "uv" in packages:
                image = image.pip_install("uv")
                # print("Installed 'uv' package via pip.")

            # Prepare the pip install command for the remaining packages
            remaining_packages = [pkg for pkg in packages if pkg.lower() != "uv"]
            if remaining_packages:
                package_install_command = " ".join(remaining_packages)
                image = image.run_commands(f"pip install {package_install_command}")
                # print(f"Installed Python packages: {', '.join(remaining_packages)}")

            # print("Finished building image.")

        sb = modal.Sandbox.create(
            "bash",
            "-c",
            f"cd /vol && python -W ignore {script_to_run_by_name}",
            image=image,
            timeout=120,
            cloud="aws",
            network_file_systems={"/vol": nfs},
            app=app,
        )
        await sb.wait.aio()
        stdout = await sb.stdout.read.aio()
        stderr = await sb.stderr.read.aio()

        if "IndentationError:" in stderr:
            print("Indent error found!")

        if stderr:
            error_details = (
                f"\n\n--- Execution Details ---\n"
                f"Script to Run: {script_to_run_by_name}\n"
                f"Scripts:\n{scripts_by_name}\n"
                f"Directory Name: {dir_name}\n"
                f"Packages: {packages}\n"
            )
            stderr += error_details

        return stdout, stderr


def execute_code_modal_sync(
    script_to_run_by_name: str,
    scripts_by_name: Dict[str, str],
    dir_name: str,
    python_version="3.9",
    packages=[],
    verbose=False,
) -> Tuple[str, Optional[str]]:
    default_packages = [
        "pandas",
        "numpy",
    ]
    packages = list(set(packages + default_packages))

    with modal.enable_output():
        with modal.NetworkFileSystem.ephemeral() as nfs:
            for name, script in scripts_by_name.items():
                nfs.write_file(name, io.BytesIO(script.encode()))
            image = modal.Image.debian_slim(python_version=python_version)
            if packages:
                image = image.pip_install("uv")
                package_install_command = " ".join(packages)
                image = image.run_commands(f"uv pip install {package_install_command}")
            sb = modal.Sandbox.create(
                "bash",
                "-c",
                f"cd /vol && python -W ignore {script_to_run_by_name}",
                image=image,
                timeout=120,
                cloud="aws",
                network_file_systems={"/vol": nfs},
                app=app,
            )
            sb.wait()
            stdout = sb.stdout.read()
            stderr = sb.stderr.read()

            if "IndentationError:" in stderr:
                print("Indent error found!")

            if stderr:
                error_details = (
                    f"\n\n--- Sandbox Execution Details ---\n"
                    f"Script to Run: {script_to_run_by_name}\n"
                    f"Scripts: {scripts_by_name}\n"
                    f"Directory Name: {dir_name}\n"
                    f"Packages: {packages}\n"
                )
                stderr += error_details

            return stdout, stderr


# import io
# from typing import Dict, Optional, Tuple

# import modal


# async def execute_code_modal_async(
#     script_to_run_by_name: str,
#     scripts_by_name: Dict[str, str],
#     dir_name: str,
#     python_version="3.9",
#     packages=None,
#     verbose=False,
# ) -> Tuple[str, Optional[str]]:
#     result = "Modal execution failed"
#     sterror = None
#     try:
#         with modal.NetworkFileSystem.ephemeral() as nfs:
#             for name, script in scripts_by_name.items():
#                 await nfs.write_file.aio(name, io.BytesIO(script.encode()))
#             image = modal.Image.debian_slim(python_version=python_version)
#             if packages:
#                 image = image.pip_install("uv")
#                 package_install_command = " ".join(packages)
#                 image = image.run_commands(
#                     f"uv pip install --system --compile-bytecode {package_install_command}"
#                 )
#             sb = modal.Sandbox.create(
#                 "bash",
#                 "-c",
#                 f"cd /vol && python -W ignore {script_to_run_by_name}",
#                 image=image,
#                 timeout=120,
#                 cloud="aws",
#                 network_file_systems={"/vol": nfs},
#             )
#             await sb.wait.aio()
#             stdout = await sb.stdout.read.aio()
#             stderr = await sb.stderr.read.aio()
#             result = stdout
#             sterror = stderr
#     except modal.exception.SandboxTimeoutError:
#         result = "Execution timed out after 60 seconds"
#         sterror = None
#     return result, sterror


# def execute_code_modal_sync(
#     script_to_run_by_name: str,
#     scripts_by_name: Dict[str, str],
#     dir_name: str,
#     python_version="3.9",
#     packages=None,
#     verbose=False,
# ) -> Tuple[str, Optional[str]]:
#     result = "Modal execution failed"
#     sterror = None
#     try:
#         with modal.NetworkFileSystem.ephemeral() as nfs:
#             for name, script in scripts_by_name.items():
#                 nfs.write_file(name, io.BytesIO(script.encode()))
#             image = modal.Image.debian_slim(python_version=python_version)
#             if packages:
#                 image = image.pip_install("uv")
#                 package_install_command = " ".join(packages)
#                 image = image.run_commands(
#                     f"uv pip install --system --compile-bytecode {package_install_command}"
#                 )
#             sb = modal.Sandbox.create(
#                 "bash",
#                 "-c",
#                 f"cd /vol && python -W ignore {script_to_run_by_name}",
#                 image=image,
#                 timeout=120,
#                 cloud="aws",
#                 network_file_systems={"/vol": nfs},
#             )
#             sb.wait()
#             stdout = sb.stdout.read()
#             stderr = sb.stderr.read()
#             result = stdout
#             sterror = stderr
#     except modal.exception.SandboxTimeoutError:
#         result = "Execution timed out after 60 seconds"
#         sterror = None
#     return result, sterror
