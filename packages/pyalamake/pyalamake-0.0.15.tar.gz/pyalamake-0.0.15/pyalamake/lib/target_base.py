import os

from .svc import svc


# --------------------
## base class for all targets
class TargetBase:
    # --------------------
    ## constructor
    #
    # @param target_name  the target name
    def __init__(self, target_name):
        ## target name
        self._target = target_name

        ## list of source files
        self._src_files = []

        ## param string for compilation options
        self._compile_opts = ''

        ## list of include directories
        self._includes = []
        ## param string for include directories
        self._inc_dirs = ''

        ## list link directories this target;  holds paths to search for libraries
        self._link_dirs = []
        ## param string for link directories
        self._link_paths = ''
        ## list link libraries for this target; holds shortened library names
        self._link_libs = []
        ## list of link paths for this target; holds full path and library name
        self._link_files = []
        ## param string for link libraries
        self._libs = ''

        ## info for the clean rule for this target
        self._clean = {}
        ## info for cleaning the coverage generated
        self._clean_cov = {}

        ## help for this target
        self._help = {}
        ## list of rules for this target
        self._rules = []
        ## list of lines in the makefile for all aspects of this target
        self._lines = []

    # --------------------
    ## return the name of this target
    # @return the name of this target
    @property
    def target(self):
        return self._target

    # === target rules

    # --------------------
    ## add a new rule for this target
    #
    # @param rule  the name of the rule
    def add_rule(self, rule):
        self._rules.append(rule)

    # --------------------
    ## return the list of rules for this target
    # @return list of rules
    @property
    def rules(self):
        return self._rules

    # === clean rules

    # --------------------
    ## add clean target to list of patterns to clean
    #
    # @param pattern   the pattern to add
    # @return None
    def add_clean(self, pattern):
        if pattern not in self._clean:
            self._clean[pattern] = 1

    # --------------------
    ## return list of clean patterns for this target
    # @return return list of clean patterns
    @property
    def clean(self):
        return self._clean

    # === help text

    # --------------------
    ## add halp line for the given rule
    #
    # @param rule   the rule this help applies to
    # @param desc   the description for this help
    # @return None
    def _add_help(self, rule, desc):
        if rule in self._help:
            svc.log.warn(f'add_help: target "{rule}" already has description')
            svc.log.warn(f'   prev: {self._help[rule]}')
            svc.log.warn(f'   curr: {desc}')
            svc.log.warn('   replacing...')
        self._help[rule] = desc

    # --------------------
    ## return current help lines
    # @return list of help lines
    @property
    def help(self):
        return self._help

    # === source files

    # --------------------
    ## return current list of source files for this target
    # @return current lis tof source files
    @property
    def sources(self):
        return self._src_files

    # --------------------
    ## add new source files for this target
    #
    # @param srcs   list or string of source files to add
    # @return None
    def add_sources(self, srcs):
        if isinstance(srcs, list):
            pass
        elif isinstance(srcs, str):
            # convert to a list
            srcs = [srcs]
        else:
            svc.abort(f'add_sources: can only add strings: {srcs}')

        for src in srcs:
            if not isinstance(src, str):
                svc.abort(f'add_sources(): accepts only str or list of str, {src} is {type(src)}')

            # TODO add .h to dependency (if possible)
            if not src.endswith('.h'):
                self._src_files.append(os.path.expanduser(src))

    # === compilation flags

    # --------------------
    ## return compile options string for this target
    # @return compile options
    @property
    def compile_options(self):
        return self._compile_opts

    # --------------------
    ## add compile options to current string of compile options
    #
    # @param opts   the new options to add
    # @return None
    def add_compile_options(self, opts):
        self._compile_opts += ' ' + opts

    # === include directories

    # --------------------
    ## return list of include directories for this target
    # @return list of include directories
    @property
    def include_directories(self):
        return self._includes

    # --------------------
    ## add list of include directories to inc_dirs
    #
    # @param inc_list  list of include directories
    # @return None
    def add_include_directories(self, inc_list):
        if isinstance(inc_list, list):
            pass
        elif isinstance(inc_list, str):
            # convert to a list
            inc_list = [inc_list]
        else:
            svc.abort('add_include_directories(): accepts only str or list of str')

        for inc_dir in inc_list:
            if not isinstance(inc_dir, str):
                svc.abort(f'add_include_directories(): accepts only str or list of str, {inc_dir} is {type(inc_dir)}')
            self._includes.append(os.path.expanduser(inc_dir))

        self._update_inc_dirs()

    # --------------------
    ## update include directories parameter to use in command line
    #
    # @return None
    def _update_inc_dirs(self):
        self._inc_dirs = ''
        for incdir in self._includes:
            self._inc_dirs += f'"-I{incdir}" '

    # === link libraries

    # --------------------
    ## return list of link libraries for this target
    # @return list of link library names
    @property
    def link_libraries(self):
        return self._link_libs

    # --------------------
    ## add list of libraries to link_libs
    #
    # @param lib_list  the list of library names to add
    # @return None
    def add_link_libraries(self, lib_list):
        if isinstance(lib_list, list):
            pass
        elif isinstance(lib_list, str):
            # convert to a list
            lib_list = [lib_list]
        else:
            svc.abort('add_link_libraries(): accepts only str or list of str')

        for lib in lib_list:
            if not isinstance(lib, str):
                svc.abort(f'add_link_libraries(): accepts only str or list of str, {lib} is {type(lib)}')
            self._link_libs.append(lib)

        self._update_link_libs()

    # --------------------
    ## return list of link files
    #
    # @return list of link files
    @property
    def link_files(self):
        return self._link_files

    # --------------------
    ## add list of files to link list
    #
    # @param file_list  list of files to link
    # @return None
    def add_link_files(self, file_list):
        if isinstance(file_list, list):
            pass
        elif isinstance(file_list, str):
            # convert to a list
            file_list = [file_list]
        else:
            svc.abort('add_link_files(): accepts only str or list of str')

        for path in file_list:
            if not isinstance(path, str):
                svc.abort(f'add_link_files(): accepts only str or list of str, {path} is {type(path)}')
            self._link_files.append(os.path.expanduser(path))

        self._update_link_libs()

    # --------------------
    ## update the link libraries command line info
    #
    # @return None
    def _update_link_libs(self):
        ## see base class for self._libs
        self._libs = ''
        ## see base class for self._link_libs
        for lib in self._link_libs:
            self._libs += f'-l{lib} '

        ## see base class for self._link_files
        for file in self._link_files:
            self._libs += f'"{file}" '

    # --------------------
    ## return list of link directories
    #
    # @return list of link directories
    @property
    def link_dirs(self):
        return self._link_dirs

    # --------------------
    ## add list of link directories to link_dirs
    #
    # @param link_list  list of link directories
    # @return None
    def add_link_directories(self, link_list):
        if isinstance(link_list, list):
            pass
        elif isinstance(link_list, str):
            # convert to a list
            link_list = [link_list]
        else:
            svc.abort('add_link_directories(): accepts only str or list of str')

        for link_dir in link_list:
            if not isinstance(link_dir, str):
                svc.abort(f'add_link_directories(): accepts only str or list of str, {link_dir} is {type(link_dir)}')
            self._link_dirs.append(os.path.expanduser(link_dir))

        self._update_link_dirs()

    # --------------------
    ## update the link directories command line info
    #
    # @return None
    def _update_link_dirs(self):
        self._link_paths = ''
        for ldir in self._link_dirs:
            self._link_paths += f'-L{ldir} '

    # === macos specific

    # --------------------
    ## update homebrew library and include directories for macOS.
    # ignored if not macOS.
    #
    # @return None
    def add_homebrew(self):
        if svc.gbl.os_name == 'macos':
            self.add_link_directories('/opt/homebrew/lib')
            self.add_include_directories('/opt/homebrew/include')

    # === gen functions

    # --------------------
    ## generate a path to an object file in this target
    #
    # @param file  the filename to use for the object file
    # @return obj: path to object file, dst_dir: path to the directory the object file is in
    def _get_obj_path(self, file):
        obj = f'{svc.gbl.build_dir}/{self.target}-dir/{file}.o'
        # TODO works in windows?
        obj = obj.replace('//', '/')

        mmd_inc = f'{svc.gbl.build_dir}/{self.target}-dir/{file}.d'
        mmd_inc = mmd_inc.replace('//', '/')

        dst_dir = os.path.dirname(obj)
        return obj, mmd_inc, dst_dir

    # --------------------
    ## generate a rule
    #
    # @param rule   the rule's name
    # @param deps   the dependencies on this rule
    # @param desc   the description for this rule (comment in the makefile)
    def _gen_rule(self, rule, deps, desc):
        self._writeln(f'#-- {desc}')
        self._add_help(rule, desc)
        if deps:
            self._writeln(f'{rule}: {deps}')
        else:
            self._writeln(f'{rule}:')

    # --------------------
    ## generate line to reset coverate info
    #
    # @param reset_rule  the name of the reset rule
    # @return None
    def _gen_reset_coverage(self, reset_rule):
        self._gen_rule(reset_rule, '', f'{self.target}: reset coverage info')

        for pattern in self._clean_cov:
            self._writeln(f'\trm -f {svc.gbl.build_dir}/{pattern}')
        self._writeln('')

    # --------------------
    ## generate lines to clean and generated directories and files given
    #
    # @return None
    def gen_clean(self):
        clean_cov_rule = ''
        if self._clean_cov:
            reset_rule = f'{self.target}-cov-reset'
            self._gen_reset_coverage(reset_rule)
            clean_cov_rule = reset_rule

        rule = f'{self.target}-clean'
        self._gen_rule(rule, clean_cov_rule, f'{self.target}: clean files in this target')

        patterns = {}
        for pattern in self.clean:
            patterns[pattern] = 1
        for pattern in patterns:
            self._writeln(f'\trm -f {svc.gbl.build_dir}/{pattern}')
        self._writeln('')

    # --------------------
    ## various common checks for valid info
    #
    # @return None
    def _common_check(self):
        for file in self._src_files:
            if not os.path.isfile(file):
                svc.log.warn(f'{self.target}: source file {file} not found')

        for incdir in self._includes:
            if not os.path.isdir(incdir):
                svc.log.warn(f'{self.target}: include directory {incdir} not found')

        # _link_libs # can't do, these may be generated
        # _link_files # can't do, these may be generated

    # === for writing to Makefile

    # --------------------
    ## return the list of lines for this target
    #
    # @return the list of lines
    @property
    def lines(self):
        return self._lines

    # --------------------
    ## save the given line to be generated later
    #
    # @param line  the line to write
    # @return None
    def _writeln(self, line):
        self._lines.append(line)
