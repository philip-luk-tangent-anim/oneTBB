# This file configures rez-build to include the following arguments.

# Build configuration choices.
parser.add_argument('-bc', '--build_config', dest='build_config',
                    choices=['Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'],
                    default = 'RelWithDebInfo', help='build configuration (default: RelWithDebInfo)')

# Build with verbosity on (i.e. enable CMAKE_VERBOSE_MAKEFILE)
parser.add_argument('-bv', '--build_verbose', dest='build_verbose', action='store_true',
                    help='build with build system verbosity enabled')

# Number of parallel build jobs.
# The maximum number of concurrent processes to use when building.
# If <jobs> is omitted the native build tool’s default number is used.
parser.add_argument('-bj', '--build_jobs_num', dest='build_jobs_num', type=int, default=32,
                    help='Number of parallel build jobs (default: 32, A value of 0 means Ninja will automatically calculate the number)')
