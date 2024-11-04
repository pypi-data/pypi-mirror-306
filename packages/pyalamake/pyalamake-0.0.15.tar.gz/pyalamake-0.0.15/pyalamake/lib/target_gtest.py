import os

from .svc import svc
from .target_base import TargetBase


# --------------------
## generate a gtest target
class TargetGtest(TargetBase):
    # --------------------
    ## create a gtest target instance
    #
    # @param targets      current list of targets
    # @param target_name  name of new target to add
    @classmethod
    def create(cls, targets, target_name):
        impl = TargetGtest(target_name)
        targets.append(impl)
        return impl

    # --------------------
    ## constructor
    #
    # @param target_name  the name of this target
    def __init__(self, target_name):
        super().__init__(target_name)

        ## list of object files
        self._objs = ''
        ## compiler to use
        self._cxx = 'g++'

        ## list of compile options
        self._compile_opts = '-g -fdiagnostics-color=always -fprofile-arcs -ftest-coverage -DGTEST_HAS_PTHREAD=1 -std=gnu++20'

        ## list of build directories
        self._build_dirs = {}

        ## list of include directories
        self._includes = []
        self._update_inc_dirs()

        ## list of link libraries to add
        self._link_libs = ['gtest', 'pthread']
        if svc.gbl.os_name != 'macos':
            self._link_libs.append('gcov')
        self._update_link_libs()

        ## list of link options
        self._ld_opts = ''
        if svc.gbl.os_name == 'macos':
            self._ld_opts += '--coverage '

        ## list of coverage directories
        self._cov_dirs = []

    # --------------------
    ## return target type
    #
    # @return gtest target
    @property
    def target_type(self):
        return 'gtest'

    # --------------------
    ## add coverage directories to list to cover
    #
    # @param cov_list   list of directories to add
    # @return None
    def add_coverage(self, cov_list):
        if isinstance(cov_list, list):
            pass
        elif isinstance(cov_list, str):
            # convert to a list
            cov_list = [cov_list]
        else:
            svc.abort('add_coverage(): accepts only str or list of str')

        for cov_dir in cov_list:
            if not isinstance(cov_dir, str):
                svc.abort(f'add_coverage(): accepts only str or list of str, {cov_dir} is {type(cov_dir)}')
            self._cov_dirs.append(cov_dir)

    # --------------------
    ## check target for any issues
    #
    # @return None
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

        for covdir in self._cov_dirs:
            if not os.path.isdir(covdir):
                svc.log.warn(f'{self.target}: coverage directory {covdir} not found')

    # --------------------
    ## gen gtest target
    #
    # @return None
    def gen_target(self):
        svc.log.highlight(f'{self.target}: gen target, type:{self.target_type}')

        self._gen_args()
        self._gen_init()
        self._gen_app()
        self._gen_link()
        self._gen_coverage()
        self._gen_run()

    # --------------------
    ## create output directory
    #
    # @return None
    def _gen_args(self):
        # create output build directory
        self._build_dirs[svc.gbl.build_dir] = 1

        for file in self.sources:
            _, _, dst_dir = self._get_obj_path(file)
            self._build_dirs[dst_dir] = 1

        self._writeln('')

    # --------------------
    ## gen initial content for gtest target
    #
    # @return None
    def _gen_init(self):
        rule = f'{self.target}-init'
        self.add_rule(rule)

        self._gen_rule(rule, '', f'{self.target}: initialize for {svc.gbl.build_dir} build')
        for blddir in self._build_dirs:
            self._writeln(f'\t@mkdir -p {blddir}')
        self._writeln('')

    # --------------------
    ## gen coverage to clean patterns list
    #
    # @param pattern  directory or pattern to add to list to clean
    # @return None
    def _add_clean_cov(self, pattern):
        if pattern not in self._clean_cov:
            self._clean_cov[pattern] = 1

    # --------------------
    ## gen app build target
    #
    # @return None
    def _gen_app(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)

        build_deps = ''
        for file in self.sources:
            obj, mmd_inc, dst_dir = self._get_obj_path(file)

            # gen clean paths
            clean_path = dst_dir.replace(f'{svc.gbl.build_dir}/', '')
            self.add_clean(f'{clean_path}/*.o')
            self.add_clean(f'{clean_path}/*.d')
            # coverage related cleans
            self.add_clean(f'{clean_path}/*.gcno')
            self._add_clean_cov(f'{clean_path}/*.gcda')

            self._writeln(f'-include {mmd_inc}')
            self._writeln(f'{obj}: {file}')
            self._writeln(f'\t{self._cxx} -MMD -c {self._inc_dirs} {self._compile_opts} {file} -o {obj}')
            self._objs += f'{obj} '
            build_deps += f'{file} '
        self._writeln('')

        self._gen_rule(rule, self._objs, f'{self.target}: build source files')
        self._writeln('')

    # --------------------
    ## gen link target
    #
    # @return None
    def _gen_link(self):
        rule = f'{self.target}-link'
        self.add_rule(rule)

        exe = f'{svc.gbl.build_dir}/{self.target}'
        self._writeln(f'{exe}: {self._objs}')
        self._writeln(f'\t{self._cxx} {self._objs} {self._ld_opts} {self._link_paths} {self._libs} -o {exe}')
        self._writeln('')
        ## see baseclass for definition of self.target
        self.add_clean(self.target)

        self._gen_rule(rule, f'{exe} {self.target}-build', f'{self.target}: link')
        self._writeln('')

    # --------------------
    ## gen coverage target
    #
    # @return None
    def _gen_coverage(self):
        rule = f'{self.target}-cov'
        # don't add to rules

        # TODO delete if not needed
        # utdir = f'{svc.gbl.build_dir}/{self.target}-dir'
        report_page = f'{svc.gbl.build_dir}/{self.target}.html'

        cmd = ('gcovr --html-details '  # show individual source files
               # TODO check if -r is needed for os=ubuntu
               # f'-r {utdir} '  # default to debug for unit test coverage
               '--no-color '  # no color for text output
               '--sort=uncovered-percent '  # sort source files based on percentage uncovered lines
               '--print-summary '  # print summary to stdout
               f'-o {report_page} ')  # location of report main page

        if not self._cov_dirs:
            svc.log.warn('gen_coverage: cov_dirs is empty, use add_coverage()')

        for cov_dir in self._cov_dirs:
            cmd += f'--filter {cov_dir} '

        self.add_clean(f'{self.target}.html')
        self.add_clean(f'{self.target}.css')
        self.add_clean(f'{self.target}.**.html')

        self._gen_rule(rule, '', f'{self.target}: show coverage')
        self._writeln(f'\t{cmd}')
        self._writeln(f'\t@echo "see {report_page}" for HTML report')
        self._writeln('')

        # TODO check if lcov is worth setting up?
        # WORKS lcov --capture --rc branch_coverage=1 --rc derive_function_end_line=0 --ignore-errors inconsistent
        #       --directory debug/ut-dir/ut
        #       -o coverage.info
        #       --include "/Users/arrizza/projects/web/pyalamake/src2/*"
        #       --gcov-tool /usr/bin/gcov
        # WORKS genhtml coverage.info --rc branch_coverage=1 --rc derive_function_end_line=0 -o debug/coverage

    # --------------------
    ## gen target to run gtest target
    #
    # @return None
    def _gen_run(self):
        rule = f'{self.target}-run'
        # don't add rule

        exe = f'{svc.gbl.build_dir}/{self.target}'

        self._gen_rule(rule, f'{self.target}-link', f'{self.target}: run executable, use s="args_here" to pass in args')
        self._writeln(f'\t{exe} $(if $s, $s, )')
        self._writeln('')
