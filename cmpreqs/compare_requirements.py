#!/usr/bin/env python
import subprocess
from io import StringIO

def get_version(line):
    if 'git+' in line or 'hg+' in line:
        return line.split('@')[-1].split('#')[0]
    else:
        d = line.split('==')
        if len(d) > 1:
            return d[1]
        else:
            return


def get_package_name(line):
    if 'git+' in line or 'hg+' in line:
        return line.split('#egg=')[1]
    else:
        return line.split('==')[0]
    
    
def get_requirements(indata):
    requirements = {}
    lines = indata.readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        requirements[get_package_name(line)] = get_version(line)
    return requirements


def req_not_in(requirements1, requirements2):
    return {key: requirements1[key] for key in list(set(requirements1) - set(requirements2))}


def print_columns(rows, titles=False):
    rows = [titles] + rows if titles else rows
    widths = [max(map(len, map(str, col))) for col in zip(*rows)]
    if titles:
        rows = [rows[0]] + [['-' * width for width in widths]] + rows[1:]
    for row in rows:
        print("  ".join((str(val).ljust(width) for val, width in zip(row, widths))))
    
    
def get_input_title(indata, index=None):
    return getattr(indata, 'name', 'Input {}'.format(index or '?'))


def print_title(name):
    print()
    print(name)
    print('=' * len(name))
    
    
def compare(input1, input2):
    requirements1 = get_requirements(input1)
    requirements2 = get_requirements(input2)
    title1, title2 = get_input_title(input1, 1), get_input_title(input2, 2)
    reqs = {name: (version, requirements2[name]) for name, version
            in requirements1.items() if name in requirements2}
    print_title('Different dependencies')
    print_columns([[name, ver[0], ver[1]] for name, ver in reqs.items()
                   if ver[0] != ver[1]], ['Name', title1, title2])
    print_title('Equal dependencies')
    print_columns([[name, ver[0]] for name, ver in reqs.items()
                   if ver[0] == ver[1]], ['Name', 'Version'])
    not_in = {title2: [requirements2, requirements1], title1: [requirements1, requirements2]}
    for file, reqs in not_in.items():
        print_title('Only available on {}'.format(file))
        print_columns([[name, ver] for name, ver in req_not_in(*reqs).items()], ['Name', 'Version'])
        
        
def read_freeze():
    return StringIO(subprocess.check_output(['pip', 'freeze']).decode('utf-8'))
            

def read_pipdeptree():
    data = subprocess.check_output(['pipdeptree']).decode('utf-8')
    data = [x for x in data.split('\n') if x and not x[0] in ['-', ' ', '*']]
    return StringIO('\n'.join(data))

        
if __name__ == '__main__':
    import sys
    compare(open(sys.argv[1]), open(sys.argv[2]))
