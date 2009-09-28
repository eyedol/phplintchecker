#!/bin/env python

import subprocess
import sys
import os

from optparse import OptionParser

"""capture commands standard output"""
def command_output(cmd):
    return subprocess.Popen(
            cmd.split(),stdout=subprocess.PIPE).communicate()[0]

"""list updated or added files"""
def files_changed(svnlook_cmd):

    def filename(line):
        return line[4:]

    def added_or_updated(line):
        return line and line[0] in ("A","U")
    
    return [
        filename(line)
        for line in command_output(svnlook_cmd % "changed").split("\n")
        if added_or_updated(line)]

"""return a file content"""
def file_contents(filename,svnlook_cmd):
    return command_output(
        "%s %s" % (svnlook_cmd % "cat",filename))

""" php lin checking """
def php_lint_checking(svnlook_cmd):
    
    """ check if its drupal module files """
    def is_drupal_mod_files(fname):
        return os.path.splitext(fname)[1] in ".module .inc .php".split()
    file_with_errors = [
        ff for ff in files_changed(svnlook_cmd)
        if is_drupal_mod_files(ff)]
    if len( file_with_errors ) > 0:
        print "The following files contains errors"

def main():
    usage = """usage: %prog REPOS TXN
Run pre-commit options on a repository transaction."""

    paser = OptionParser(usage=usage)
    parser.add_option("-r","--revision",
            help="Test mode. TXN actually refers to a revision",
            action="Store_true",default=False)
    errors = 0

    try:
        (opts,(repos,txn_or_rvn)) = parser.parse_args()
        svnlook_opt = ("--transaction","--revision")[opts.revision]
        svnlook_cmd = "svnlook %s %s %s %s" % ( "%s", repos,look_opt,
                txn_or_rvn)
    except:
        parser.print_help()
        errors += 1

    return errors

if __name__ == "__main__":
    sys.exit(main())
