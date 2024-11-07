import shutil
import subprocess
import sys

NPM = "npm"


def execute(cmd: str):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
    if popen.stdout is None:
        raise Exception(f"Failed to execute command {cmd}.")

    for stdout_line in iter(popen.stdout.readline, ""):
        sys.stdout.write(stdout_line)
        sys.stdout.flush()

    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def main():
    if shutil.which(NPM) is None:
        print(
            """

BUILD ERROR: npm not found!!!
  *    Please install NPM and Node.js before installing rawjs2dict.
  *    Refer to the documentation for installing NPM and Node.js here: https://nodejs.org/en/download

        """
        )
        raise Exception("BUILD ERROR: npm not found.")
    else:
        execute(f"{NPM} i --no-package-lock")


if __name__ == "__main__":
    main()
