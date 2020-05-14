import os
import platform
import subprocess
import shutil


def run_command(cmd_arg_list, workdir_path):
    """
    Run a subprocess command.

    @param cmd_arg_list: A list of the command and its arguments.
    @param workdir: Absolute path to the working directory the command should be run in.
    @raises: subprocess.CallProcessError if an error occurred.
    """
    use_shell = ("Windows" in platform.system())

    process = subprocess.Popen(cmd_arg_list, stdout=subprocess.PIPE, universal_newlines=True, shell=use_shell,
                               cwd=workdir_path)
    for stdout_line in iter(process.stdout.readline, ""):
        print(stdout_line.rstrip())
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, ' '.join(cmd_arg_list))

def copy_dir(src_dir, dst_dir):
    """
    Copy directory like shutil.copytree.  It replaces the contents of dst_dir completely with the contents of src_dir.


    @param src_dir: The absolute path to the source directory to copy.
    @param dst_dir: The absolute path to the destination directory to copy.
    """
    if os.path.isdir(dst_dir):
        print("Removing previous copy of {dst_dir}".format(dst_dir=dst_dir))
        shutil.rmtree(dst_dir)
    print("Copying {src_dir} to {dst_dir}\n".format(src_dir=src_dir, dst_dir=dst_dir))
    shutil.copytree(src_dir, dst_dir)

if __name__ == '__main__':
    # Configure CMake.
    cmake_cmd_list = [
        'cmake',
        '-g "Ninja"',
        '-DCMAKE_BUILD_TYPE={}'.format(os.environ.get('__PARSE_ARG_BUILD_CONFIG')),
        '-DCMAKE_VERBOSE_MAKEFILE={}'.format(os.environ.get('__PARSE_ARG_BUILD_VERBOSE')),
        '-DTBB_BUILD_SHARED=ON',
        '-DTBB_BUILD_TBBMALLOC=ON',
        '-DTBB_BUILD_TBBMALLOC_PROXY=ON',
        '-DTBB_BUILD_STATIC=ON',
        os.environ.get('REZ_BUILD_SOURCE_PATH'),
    ]
    run_command(cmake_cmd_list, os.environ.get('REZ_BUILD_PATH'))

    # Do the build.
    cmake_cmd_list = ['cmake', '--build', '.']
    if int(os.environ.get('__PARSE_ARG_BUILD_JOBS_NUM')) > 0:
        cmake_cmd_list.append('--')
        cmake_cmd_list.append('-j{}'.format(os.environ.get('__PARSE_ARG_BUILD_JOBS_NUM')))
    run_command(cmake_cmd_list, os.environ.get('REZ_BUILD_PATH'))

    if int(os.environ['REZ_BUILD_INSTALL']) != 0:
        # Do the installation to the REZ repository.
        cmake_cmd_list = [
            'cmake',
            '--install',
            '.',
            '--prefix',
            os.environ.get('REZ_BUILD_INSTALL_PATH')
        ]
        run_command(cmake_cmd_list, os.environ.get('REZ_BUILD_PATH'))

        copy_dir(os.path.join(os.environ.get('REZ_BUILD_SOURCE_PATH'), 'include', 'serial'),
                 os.path.join(os.environ.get('REZ_BUILD_INSTALL_PATH'), 'include', 'serial'))
