r""" md
## Usage

Once this plugin is [installed](../README.md#installation), just replace
the plugin name `simple` with `semiliterate` in your `mkdocs.yml` file.
It accepts all of the same parameters, so `mkdocs` will still work as before,
and you will have immediate access to all of the following extensions.
(Note that this documentation assumes a familiarity with the
[usage](https://althack.dev/mkdocs-simple-plugin/v{! ../setup.cfg {
  extract: {start: 'mkdocs~=', stop: '(\d*\.\d*\.?\d*)'}
} !}/mkdocs_simple_plugin/plugin/)
of the `simple` plugin.)
"""

from mkdocs import utils
from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files

from mkdocs_simple_plugin.semiliterate import (
    Semiliterate, LazyFile, ExtractionPattern, StreamExtract)
from mkdocs_simple_plugin.simple import (Simple, SimplePath)
from mkdocs_simple_plugin.plugin import SimplePlugin

import os
import re
import subprocess
import sys
import time
import tempfile
import yaml


class BorrowFile:
    """Just forwards to another stream, and never closes it
    Except it also has its own value of ensurelines.
    """
    def __init__(self, other, ensurelines=True):
        self.other = other
        self.file_name = other.file_name
        self.ensurelines = ensurelines

    def write_just(self, arg):
        self.other.write_just(arg)

    def write(self, arg):
        if (self.ensurelines and not arg.endswith("\n")):
            arg += "\n"
        self.other.write_just(arg)

    def close(self):
        return None


class LazierFile(LazyFile):
    """Just like LazyFile, except with ensurelines parameter
    The parameter controls whether every call to write guarantees a newline
    is written.
    """
    def __init__(self, directory: str, name: str, ensurelines=True):
        super().__init__(directory, name)
        self.ensurelines = ensurelines

    # Basically identical to LazyFile write, so take care to sync
    def write_just(self, arg: str) -> None:
        """ create and write exactly arg to file, no newlines added"""
        if arg is None:
            return
        if self.file_object is None:
            filename = os.path.join(self.file_directory, self.file_name)
            os.makedirs(self.file_directory, exist_ok=True)
            self.file_object = open(filename, 'w+')
        self.file_object.write(arg)

    def write(self, arg: str) -> None:
        if self.ensurelines:
            super().write(arg)
        else:
            self.write_just(arg)


class StreamInclusion(StreamExtract):
    r""" md  An extension of the StreamExtract class which adds

### Inclusion syntax

While extracting content from a file (because it matches one of the
`semiliterate` patterns, rather than just `include`),
an unescaped expression of the form

`{! FILENAME YAML !}`

(which may span multiple lines) will trigger file inclusion. The FILENAME may
be a bare word, in which case it cannot contain whitespace, or it may be
enclosed in single or double quotes. Note that FILENAME is interpreted relative
to the directory in which the file containing the `{! .. !}` expression
resides. The YAML is interpreted exactly as the extraction options to a
`semiliterate` item as
[documented](https://althack.dev/mkdocs-simple-plugin/v{! ../setup.cfg { extract: {start: 'mkdocs~=', stop: '(\d*\.\d*\.?\d*)'}, ensurelines: false} !}/mkdocs_simple_plugin/plugin/index.html#semiliterate)
for the `simple` extension, subject to the extensions below. The text
extracted from FILENAME is interpolated at the current location in the file
currently being written. Recursive inclusion is supported.

The simplest example of such an inclusion directive is just
`{! boilerplate.md !}`, which (because of the conventions for extraction
parameters) simply interpolates the entire contents of `boilerplate.md`
at the current location.

For an example that uses more of the extraction parameters, the current
version number of mkdocs-semiliterate is extracted into the
[Overview](../README.md) of this documentation via

` {! ../README.md extract: { start: 'repo:.*(\{!.*!\})', stop: 'repo' } !}`

to take advantage of the beginning of the `setup.cfg` file:
```
{! ../setup.cfg terminate: long !}...
```

(and of course both of the code snippets just above are extracted into this
page with `{! ... !}`, as you can see in the
[source code](https://code.studioinfinity.org/glen/mkdocs-semiliterate/src/branch/main/mkdocs_semiliterate/plugin.py)
for the plugin.)

Note that a `{! ... !}` directive must be in a line that semiliterate would
normally copy. That is, semiliterate does not examine lines after
the `terminate` regexp, or when no mode of extraction is active.
It also doesn't check any text written from lines that match these
special expressions, including `start` and `stop`.
Moreover, on such normally-transcribed lines,
it's the text **after** the application of any semiliterate `replace`ments that
is checked for `{! ... !}`.
     """  # noqa: E501

    include_open = re.compile(r'''(?<![`\\])(\{\!\s*)([\s'"])''')
    include_quoted_file = re.compile(
        r'''(['"])(?P<fn>.*?)\1\s+(?P<yml>[\s\S]*?)\s?\!\}''')
    include_bare_file = re.compile(r'\s(?P<fn>.*?)\s+(?P<yml>[\s\S]*?)\s?\!\}')

    def __init__(self, input_stream, output_stream, include_root,
                 terminate=None, patterns=None, extract=None, **kwargs):
        if terminate and not hasattr(terminate, 'search'):
            terminate = re.compile(terminate)
        if patterns is None and extract:
            # Sadly we must reiterate the pattern parsing here, because of
            # inclusions not coming from a [DS]emiliterate object
            extractions = []
            if isinstance(extract, dict):
                extract = [extract]
            for extract_params in extract:
                extractions.append(ExtractionPattern(**extract_params))
            if len(extractions) > 0:
                patterns = extractions
        super().__init__(input_stream, output_stream,
                         terminate, patterns, **kwargs)
        self.include_root = include_root

    def extract_line(self, line, extraction_pattern):
        """Copy line to the output stream, applying all specified replacements
           and handling inclusion syntax.
        """
        line = extraction_pattern.replace_line(line)
        if line is None:
            return
        include_match = StreamInclusion.include_open.search(line)
        if not include_match:
            self.output_stream.write(line)
            return
        # OK, we have found (the start of) an inclusion and must process it
        preamble = line[:include_match.start()]
        remainder = line[include_match.end(1):]
        doublequoted = False
        body_pattern = StreamInclusion.include_quoted_file
        if include_match[2].isspace():
            body_pattern = StreamInclusion.include_bare_file
        elif include_match[2] == '"':
            doublequoted = True
        body_match = body_pattern.search(remainder)
        if not body_match:
            for extra_line in self.input_stream:
                remainder += extraction_pattern.replace_line(extra_line)
                body_match = body_pattern.search(remainder)
                if body_match:
                    break
        if not body_match:
            errmsg = "semiliterate: End of file while scanning for `!}`"
            utils.log.error(errmsg)
            raise EOFError(errmsg)
        filename = body_match['fn']
        r""" md
### Double-quoted filenames and special extraction

Standard Python escape sequences in double-quoted filenames are interpreted
as usual; for example you can write
```
{! ../tests/fixtures/quoted-filename/README.md extract:
  start: '(.*!.*)'
  stop: '\s'
!}
```
to include a file whose name (`snippet/Say "Don't"`, in this case) has both
double and single quotes.

Further, `semiliterate` supports some special escape sequences for
doublequoted file names to include text from other places than current files
in the project tree:

`\git`: extracts a version of a file from the Git archive of the project
(presuming it is under Git version control) and then
includes content from that file. For example, you could write
```
{! ../tests/fixtures/git-inclusion/README.md extract:
  start: '(.*!.*)'
  stop: '\s'
!}
```

to extract content starting after the `### install` line from the
`mkdocs.yml` file in the Git commit of this repository
tagged `0.1.0`. This feature is primarily useful if you are documenting the
development or changes to a project over time, or are documenting a feature
in a specific past release of your project, and want to be sure that
material included in your documentation does _not_ change as the project
progresses. (This behavior is as opposed to the usual case, in which you want
your documentation to incorporate the most up-to-date version of extracted
content.)

The precise behavior for a FILENAME argument in a `{! ... !}` inclusion of the
form

`"\git SPECIFIER"`

is that the output of `git show SPECIFIER` is written to a temporary file,
and that file is extracted from.

`\syspath`: searches for the remainder of the doublequoted filename in the
python `sys.path` and includes content from the found file. For example, you
could write
```
{! ../tests/fixtures/theme-modification/doc_theme/.base.generator extract:
  start: '(.*!.*)'
!}
```
to create a version of the "base.html" of the "readthedocs" theme with
additional content at the very top of the body. As the example suggests, this
mechanism is primarily useful to tweak an mkdocs theme in ways not
anticipated by the `{%- block ... %}` directives placed by the theme writer.
"""
        gitextract = False
        syspathextract = False
        if doublequoted:
            if filename[:5] == r'\git ':
                gitextract = True
                filename = filename[5:]
            elif filename[:9] == r'\syspath ':
                syspathextract = True
                filename = filename[9:]
            filename = (filename.encode('latin-1', 'backslashreplace')
                                .decode('unicode-escape'))
        include_path = os.path.join(self.include_root, filename)
        if gitextract:
            (write_handle, include_path) = tempfile.mkstemp()
            utils.log.info(
                f"semiliterate: git extracting {filename} to {include_path}")
            contents = subprocess.check_output(['git', 'show', filename])
            os.write(write_handle, contents)
            os.close(write_handle)
        if syspathextract:
            for dirname in sys.path:
                candidate = os.path.join(dirname, filename)
                if os.path.isfile(candidate):
                    include_path = candidate
                    break
        new_root = os.path.dirname(include_path)
        try:
            include_parameters = yaml.safe_load(body_match['yml'])
        except Exception as err:
            newmsg = (f"While attempting to include '{include_path}', could"
                      + f" not parse yaml '{body_match['yml']}'.")
            if hasattr(err, 'message'):
                raise SyntaxError(
                    f"{newmsg} YAML parser reports: {err.message}")
            raise SyntaxError(f"{newmsg} Caught exception: {str(err)}")
        if not include_parameters:
            include_parameters = {}
        with open(include_path) as include_file:
            self.output_stream.write(preamble)
            inclusion = StreamInclusion(
                include_file,
                BorrowFile(self.output_stream,
                           include_parameters.get('ensurelines', True)),
                new_root,
                **include_parameters)
            if inclusion.extract():
                self.wrote_something = True
        self.output_stream.write(remainder[body_match.end():])


class SemiliteratePlugin(SimplePlugin):
    r""" md   An extension of the mkdocs-simple-plugin
### Additional plugin parameters

`semiliterate` adds a couple of new plugin parameters to further tailor its
behavior as compared to `simple`. They are described in this section, with
default values in parentheses at the beginning of each entry.

{! plugin.py extract:
  start: '[*]super_config_scheme'
  replace:
  - ["\\('(.*)',\\s*$", '\1\n']
  - ['config_options.Type.*?default=([^\)]*)', ':  (\1)']
  - '^\s*#(.*\s*)$'
terminate: '^\s*\)'
!}
    """
    super_config_scheme = SimplePlugin.config_scheme
    config_scheme = (
        # Note documentation of each new parameter **follows** the parameter.
        *super_config_scheme,
        ('exclude',
         config_options.Type(list, default=['.o'])),
        #    Files whose name contains a string in this list will not be
        #    processed by `semiliterate`, regardless of whether they might
        #    match `include`, the `semiliterate` patterns, or
        #    standard Markdown.
        ('copy_standard_markdown',
         config_options.Type(bool, default=False)),
        #    Whether to add MkDocs' list of standard Markdown extensions to
        #    the `include` parameter so that Markdown files will be
        #    directly copied to the docsite. Note that the `simple` behavior
        #    corresponds to a _true_ value for `copy_standard_markdown`, but
        #    `semiliterate` still incorporates all standard Markdown files
        #    because of the following `extract_standard_markdown` parameter.
        ('extract_standard_markdown',
         config_options.Type(dict, default={})),
        #    If the `enable` key of this dict parameter is true
        #    (it defaults to the opposite of `copy_standard_markdown`),
        #    it adds a semiliterate block causing extraction (and hence
        #    include-directive processing) from all standard Markdown files
        #    (as defined by MkDocs). The remaining keys of this parameter are
        #    included as parameters of that semiliterate block. Thus, the
        #    default values of the parameters arrange for Markdown files to be
        #    copied "as-is", except possibly for embedded inclusions.
        #    On the other hand, setting this parameter to `{enable: false}`
        #    (which is also the default when `copy_standard_markdown` is true)
        #    will prevent automatic extraction (and hence disable
        #    inclusion-directive processing) from standard Markdown files.
        ('extract_on_copy',
         config_options.Type(bool, default=False)),
        #    Whether to also attempt extraction from a file that is copied
        #    verbatim (because of matching the `include_extensions`).
    )

    def on_config(self, config, **kwargs):
        # Save the include extensions before SimplePlugin modifies them:
        saved_includes = self.config['include']
        new_config = super().on_config(config, **kwargs)
        self.config['saved_includes'] = saved_includes
        curpath = os.path.abspath('.')
        self.custom_dir = None
        for themedir in config['theme'].dirs:
            common = os.path.commonpath(
                [os.path.abspath('.'), os.path.abspath(themedir)])
            if common == curpath:
                self.custom_dir = os.path.relpath(themedir, curpath)
                newthemedir = os.path.join(
                    self.config['build_dir'], self.custom_dir)
                utils.log.debug(
                    'mkdocs-semiliterate: found theme.custom_dir = '
                    + self.custom_dir
                    + f"; adding theme directory {newthemedir}")
                config['theme'].dirs.insert(0, newthemedir)
                break
        return new_config

    # Override rather than extend so that we use Semisimple instead of simple
    # Note code must track mkdocs_simple_plugin, with the added section for
    # the custom_dir at the bottom.
    def on_files(self, files: Files, /, *,
                 config: MkDocsConfig):
        """Update files based on plugin settings."""
        # Configure Semisimple
        semisimple = Semisimple(**self.config)

        # Save paths to add to watch if serving
        do_copy = self.config["copy"]
        self.paths = semisimple.build_docs(
            self.dirty, self.last_build_time, do_copy)
        self.last_build_time = time.time()

        if not self.config["merge_docs_dir"]:
            # If not merging, remove files that are from the docs dir
            abs_docs_dir = os.path.abspath(config['docs_dir'])
            for _, file in files.src_uris.items():
                if file.abs_src_path.startswith(abs_docs_dir):
                    files.remove(file)

        for path in self.paths:
            file = File(
                src_dir=os.path.abspath(path.output_root),
                path=path.output_relpath,
                dest_dir=config.site_dir,
                use_directory_urls=config["use_directory_urls"]
            )
            if file.src_uri in files.src_uris:
                files.remove(file)
            files.append(file)

        # If we designated a subdirectory for the theme, ignore files in it
        if self.custom_dir:
            sources = files.src_paths
            for path in sources:
                if path.startswith(self.custom_dir):
                    utils.log.debug(
                        f"mkdocs-semiliterate: ignoring {path} "
                        + f"from theme directory {self.custom_dir}")
                    files.remove(sources[path])

        return files


class Semisimple(Simple):
    """Mkdocs Semisimple Plugin"""
    def __init__(self, semiliterate, exclude, saved_includes,
                 copy_standard_markdown, extract_standard_markdown,
                 extract_on_copy, **kwargs):
        # Since we have extensions in Demiliterate, suppress the semiliterate
        # configuration until we handle it ourselves:
        super().__init__(semiliterate=[], **kwargs)
        self.semiliterate = [Demiliterate(**item) for item in semiliterate]
        self.exclude = exclude
        self.extract_on_copy = extract_on_copy
        dflt_enable = False
        if not copy_standard_markdown:
            self.doc_glob = set(saved_includes)
            dflt_enable = True
        if extract_standard_markdown.get('enable', dflt_enable):
            ext_pat = '|'.join(re.escape(s) for s in utils.markdown_extensions)
            self.semiliterate.append(
                Demiliterate(
                    pattern=re.compile(f"^(.*(?:{ext_pat}))$"),
                    destination=r'\1',
                    **extract_standard_markdown))

    def is_doc_file(self, name: str) -> bool:
        if any(ext in name for ext in self.exclude):
            return False
        return super().is_doc_file(name)

    def try_extract(self, from_dir: str, name: str, to_dir: str) -> list:
        if any(ext in name for ext in self.exclude):
            return []
        if not self.extract_on_copy and self.is_doc_file(name):
            return []
        return super().try_extract(from_dir, name, to_dir)

    # Had to override this because the simple version hardcoded that if a file
    # was copied, it could not be extracted. So check carefully for changes in
    # simple. Only the line marked # REMOVED was commented out
    def build_docs(
            self,
            dirty=False,
            last_build_time=None,
            do_copy=False) -> list:
        """Build the docs directory from workspace files."""
        paths = []
        files = self.get_files()
        for file in files:
            if not os.path.isfile(file):
                continue
            if dirty and last_build_time and (
                    os.path.getmtime(file) <= last_build_time):
                continue
            from_dir = os.path.dirname(file)
            name = os.path.basename(file)
            build_prefix = os.path.normpath(
                os.path.join(self.build_dir, from_dir))

            doc_paths = self.get_doc_file(
                from_dir, name, build_prefix, True)
            if doc_paths:
                paths.append(
                    SimplePath(
                        output_root=".",
                        output_relpath=os.path.relpath(path=file, start="."),
                        input_path=file)
                )
                utils.log.info("mkdocs-semiliterate: Added %s", file)
                # continue    # REMOVED

            extracted_paths = self.try_extract(from_dir, name, build_prefix)
            for path in extracted_paths:
                paths.append(
                    SimplePath(
                        output_root=self.build_dir,
                        output_relpath=os.path.relpath(
                            path=path,
                            start=self.build_dir),
                        input_path=file))
                utils.log.info(
                    "mkdocs-semiliterate: Extracted %s -> %s", file, path)
            if extracted_paths:
                continue

        return paths


class Demiliterate(Semiliterate):
    r""" md Extends Semiliterate to use StreamInclusion, not StreamExtract

semiliterate.ensurelines
:   (true) Guarantees that a newline is trancribed for each line of the input,
    even if a start, stop, terminate, or replacement pattern would have
    suppressed the newline. Note this can be set separately for each block
    (i.e. filename pattern) within the semiliterate parameter. The default
    setting corresponds to the `simple` behavior, so setting this to "false"
    allows you to suppress newlines with judicious use of these patterns.
    """

    def __init__(
            self,
            pattern: str,
            destination: str = None,
            terminate: str = None,
            extract: list = None,
            ensurelines=True):
        super().__init__(pattern, destination, terminate, extract)
        self.ensurelines = ensurelines

    # Note that this has diverged noticeably from the
    # Semiliterate.try_extraction method that it overrides, especially
    # in regards to adjusting the destination directory.
    # Hence, great care must be taken when mkdocs-simple-plugin is updated
    # to make sure that any changes to this method are reflected in the
    # code below:
    def try_extraction(
            self,
            from_directory,
            from_file,
            destination_directory,
            **kwargs) -> list:
        """Try to extract documentation from file with name.

        Args:
            from_directory (str): The source directory
            from_file (str): The source filename within directory
            destination_directory (str): The destination directory

        Returns a list of extracted files.
        """
        to_file = self.filename_match(from_file)
        if not to_file:
            return []
        from_file_path = os.path.join(from_directory, from_file)
        to_file_path = os.path.join(destination_directory, to_file)  # ## ADDED
        (destination_directory, to_file) = os.path.split(to_file_path)  # ADDED
        try:
            with open(from_file_path) as original_file:
                utils.log.debug(
                    f"mkdocs-semiliterate: Scanning {from_file_path}... ")
                # extraction = StreamExtract(
                extraction = StreamInclusion(
                    input_stream=original_file,
                    output_stream=LazierFile(
                        destination_directory, to_file, self.ensurelines),
                    include_root=from_directory,  # ## ADDED
                    terminate=self.terminate,
                    patterns=self.extractions,
                    **kwargs)
                return extraction.extract()
        except (UnicodeDecodeError) as error:
            utils.log.debug("mkdocs-semiliterate: Skipped  %s", from_file_path)
            utils.log.debug(
                "mkdocs-semiliterate: Error details: %s", str(error))
        except (OSError, IOError) as error:
            utils.log.error("mkdocs-semiliterate: could not build %s\n %s",
                            from_file_path, str(error))
        return []

# start-md
# ### Adjusting the mkdocs theme

# `semiliterate` also makes it possible to add generated files to the mkdocs
# theme. It does this by detecting if a `theme.custom_dir` parameter has been
# set in the mkdocs configuration, and if so, it adds the corresponding
# directory in the generated docs dir to the theme search path. (Note this
# means that
# files in the corresponding subdirectory of your project will be copied into
# the resulting doc site unless their names start with a '.')
# end-md
