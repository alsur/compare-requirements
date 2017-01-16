#!/usr/bin/env python


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
    
    
def get_requirements(file):
    requirements = {}
    lines = open(file).readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        requirements[get_package_name(line)] = get_version(line)
    return requirements


def req_not_in(requirements1, requirements2):
    return set(requirements1) - set(requirements2)
    
    
def compare(file1, file2):
    requirements1 = get_requirements(file1)
    requirements2 = get_requirements(file2)
    print('{} <> {}'.format(file1, file2))
    for name, version in requirements1.items():
        if not name in requirements2:
            continue
        version2 = requirements2[name]
        print('{}: {} {} {}'.format(name, version,'==' if version == version2 else '!=', version2))
    not_in = {file1: [requirements2, requirements1], file2: [requirements1, requirements2]}
    for file, reqs in not_in.items():
        print('\n')
        for req in req_not_in(*reqs):
            print('{} not present in file {}'.format(req, file))
            
            
if __name__ == '__main__':
    import sys
    compare(sys.argv[1], sys.argv[2])
