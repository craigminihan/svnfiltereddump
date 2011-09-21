
import tempfile
import shutil
import os
import re
from subprocess import Popen, check_call, PIPE, STDOUT
from string import join;

def chomp(x):
    if x[-1:] == "\n":
        return x[:-1]
    else:
        return x

def get_output_of_command(args):
    process = Popen(args, stdout=PIPE, stderr=PIPE )
    output = chomp(process.stdout.read())
    process.stdout.close()
    error = process.stderr.read()
    process.stderr.close()
    status = os.waitpid(process.pid, 0)[1]
    if status != 0:
        cmd_str = join(args, ' ')
        raise Exception("Command '%s' failed with status %d:\n%s" % ( cmd_str, status, error ) )
    return output


class TestEnvironment:
    def __init__(self):
        self.work_dir = tempfile.mkdtemp()
        self.tmp_index = 0
        self.repo_path = self.work_dir + '/repo'
        self.repo_url = 'file://' + self.repo_path
        self.repo_working_copy = self.work_dir + '/wc'
        self.dev_null = open('/dev/null', 'w')
       
        check_call( [ 'svnadmin', 'create',  self.repo_path ] )
        check_call( [ 'svn', 'co', self.repo_url, self.repo_working_copy ], stdout=self.dev_null )

        # Make sure we get english error messages - needed in is_existing_in_rev
        if re.search('utf8', os.getenv('LANG'), re.I) is None:
            os.putenv('LANG', 'en_US.utf8')

    def __enter__(self):
        return self

    def __exit__(self):
        shutil.rmtree(self.work_dir)
        self = None

    def mkdir(self, name):
        os.chdir(self.repo_working_copy)
        check_call( [ 'svn', 'mkdir', '--parents', name ], stdout=self.dev_null)

    def add_file(self, name, content):
        self.change_file(name, content)
        check_call( [ 'svn', 'add', name ], stdout=self.dev_null)

    def copy_file(self, source, target):
        check_call( [ 'svn', 'copy', source, target ], stdout=self.dev_null)

    def rm_file(self, name):
        check_call( [ 'svn', 'rm', name ], stdout=self.dev_null)

    def propset(self, path, key, value):
        os.chdir(self.repo_working_copy)
        check_call( [ 'svn', 'propset', key, value, path], stdout=self.dev_null)

    def change_file(self, name, content):
        os.chdir(self.repo_working_copy)
        fh = open(name, 'w')
        fh.write(content)
        fh.close()

    def commit(self, comment):
        os.chdir(self.repo_working_copy)
        check_call( [ 'svn', 'commit', '-m', comment ], stdout=self.dev_null )
