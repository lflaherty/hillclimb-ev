#!/usr/bin/env python3

"""
Creates a new commit with all of the submodules with new commits, with the
commit message outlining all of the new changes.
"""

from subprocess import PIPE, run
import re

GIT_STATUS = ['git', 'status']
GIT_DIFF = ['git', 'diff']
GIT_LOG = ['git', 'log']
GIT_ADD = ['git', 'add'] # needs the directory added
GIT_COMMIT = ['git', 'commit', '-m'] # needs the message appended
PATTERN_NEW_COMMITS = r'modified:\s+([\w/-]+) \([\w, ]*new commits[\w, ]*\)'
PATTERN_HASH_DIFF = r'{}\n.*\n-Subproject commit ([\w\d]+)\n\+Subproject commit ([\w\d]+)' # needs to be formatted to include path
PATTERN_LOG = r'commit [\w\d]+\n.+\n.+\n\n.   (.*)\n'


"""
Returns the stdout from the given command
"""
def run_command(command, cwd=None):
    result = run(command, stdout=PIPE, stderr=PIPE, cwd=cwd, universal_newlines=True)
    if result.returncode != 0:
        raise Exception('git status returned error', result.returncode, result.stderr)
    return result.stdout


def get_log_summary_lines(subdir, hash_old, hash_new):
    hash_diff_str = '{}..{}'.format(hash_old, hash_new)
    raw_git_log = run_command(GIT_LOG + [hash_diff_str], cwd=subdir)
    log_entries = re.findall(PATTERN_LOG, raw_git_log)

    log_summary = ['{}:'.format(subdir)]

    for entry in log_entries:
        log_summary.append('    {}'.format(entry))
    log_summary.append('')

    return log_summary


def main():
    git_status = run_command(GIT_STATUS)
    git_diff = run_command(GIT_DIFF)
    changed_repos = re.findall(PATTERN_NEW_COMMITS, git_status)

    log_summary = ['Update submodules', '']

    for match in changed_repos:
        print('Changes in %s' % match)

        diff_pattern = PATTERN_HASH_DIFF.format(match.replace('/', '\/'))
        hash_diffs = re.findall(diff_pattern, git_diff)
        hash_old = hash_diffs[0][0]
        hash_new = hash_diffs[0][1]

        print('commit {} -> {}'.format(hash_old, hash_new))
        log_summary += get_log_summary_lines(match, hash_old, hash_new)

        run_command(GIT_ADD + [match])
        print()
    
    print('Committing...')
    commit_msg = '\n'.join(log_summary)
    print(commit_msg)
    git_commit = run_command(GIT_COMMIT + [commit_msg])
    print(git_commit)

if __name__ == '__main__':
    main()
