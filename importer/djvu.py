from __future__ import print_function

import os
import sys

import djvu.decode


def print_text(sexpr, level=0):
    if level > 0:
        print(' ' * (2 * level - 1), end=' ')
    if isinstance(sexpr, djvu.sexpr.ListExpression):
        if len(sexpr) == 0:
            return
        print(str(sexpr[0].value), [sexpr[i].value for i in xrange(1, 5)])
        for child in sexpr[5:]:
            print_text(child, level + 1)
    else:
        print(sexpr)


class Context(djvu.decode.Context):

    def handle_message(self, message):
        if isinstance(message, djvu.decode.ErrorMessage):
            print(message, file=sys.stderr)
            # Exceptions in handle_message() are ignored, so sys.exit()
            # wouldn't work here.
            os._exit(1)

    def process(self, path):
        document = self.new_document(djvu.decode.FileURI(path))
        document.decoding_job.wait()
        for page in document.pages:
            page.get_info()
            print_text(page.text.sexpr)


def main():
    if len(sys.argv) != 2:
        print(
            'Usage: {prog} <djvu-file>'.format(prog=sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    context = Context()
    context.process(sys.argv[1])

# if __name__ == '__main__':
#    main()
