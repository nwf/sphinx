# -*- coding: utf-8 -*-
"""
    sphinx.builders.text
    ~~~~~~~~~~~~~~~~~~~~

    Plain-text Sphinx builder.

    :copyright: Copyright 2007-2017 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import codecs
from os import path

from docutils.io import StringOutput

from sphinx.builders import Builder
from sphinx.util import logging
from sphinx.util.osutil import ensuredir, os_path
from sphinx.writers.text import TextWriter

if False:
    # For type annotation
    from typing import Any, Dict, Iterator, Set  # NOQA
    from docutils import nodes  # NOQA
    from sphinx.application import Sphinx  # NOQA

logger = logging.getLogger(__name__)


class TextBuilder(Builder):
    name = 'text'
    format = 'text'
    out_suffix = '.txt'
    allow_parallel = True

    current_docname = None  # type: unicode

    def init(self):
        # type: () -> None
        pass

    def get_outdated_docs(self):
        # type: () -> Iterator[unicode]
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = self.env.doc2path(docname, self.outdir,
                                           self.out_suffix)
            try:
                targetmtime = path.getmtime(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = path.getmtime(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                # source doesn't exist anymore
                pass

    def get_target_uri(self, docname, typ=None):
        # type: (unicode, unicode) -> unicode
        return ''

    def prepare_writing(self, docnames):
        # type: (Set[unicode]) -> None
        self.writer = TextWriter(self)

    def write_doc(self, docname, doctree):
        # type: (unicode, nodes.Node) -> None
        self.current_docname = docname
        destination = StringOutput(encoding='utf-8')
        self.writer.write(doctree, destination)
        outfilename = path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(path.dirname(outfilename))
        try:
            with codecs.open(outfilename, 'w', 'utf-8') as f:  # type: ignore
                f.write(self.writer.output)
        except (IOError, OSError) as err:
            logger.warning("error writing file %s: %s", outfilename, err)

    def finish(self):
        # type: () -> None
        pass


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    app.add_builder(TextBuilder)

    app.add_config_value('text_sectionchars', '*=-~"+`', 'env')
    app.add_config_value('text_newlines', 'unix', 'env')

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
