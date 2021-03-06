"""Main entry point for rickshaw"""
try:
    from pprintpp import pprint
except ImportError:
    from pprint import pprint
import os
import subprocess
import json
from argparse import ArgumentParser
from rickshaw import simspec
from rickshaw import generate


def main(args=None):
    p = ArgumentParser('rickshaw')
    p.add_argument('-n', dest='n', type=int, help='number of files to generate',
                   default=None)
    p.add_argument('-i', dest='i', type=str, help='name of input file', default=None)
    p.add_argument('-rs', dest='rs', action="store_true", help='runs the simulations after they have been generated')
    p.add_argument('-rh', dest='rh', action="store_true", help='runs the simulations after they have been generated')
    p.add_argument('-v', dest='v', action="store_true", help='verbose mode will pretty print generated files')
    ns = p.parse_args(args=args)
    spec = {}
    if ns.i is not None:
        try:
            ext = os.path.splitext(ns.i)[1]
            if ext == '.json':
                with open(ns.i) as jf:
                    spec = json.load(jf)
                    for k,v in simspec['niche_links'].items():
                        spec['niche_links'][k] = set(v)
                    for k,v in simspec['archetypes'].items():
                        spec['archetypes'][k] = set(v)
            elif ext == '.py':
                with open(ns.i) as pf:
                    py_str = pf.read()
                    spec = eval(py_str)
        except:
            pass
    spec = simspec.SimSpec(spec)
            
    if ns.n is not None:
        i = 0
        while i < ns.n:
            try:
                input_file = generate.generate(sim_spec=spec)
                if ns.v:
                    pprint(input_file)
            except Exception:
                continue
            jsonfile = str(i) + '.json'
            with open(jsonfile, 'w') as jf:
                json.dump(input_file, jf, indent=4)
            i += 1
    else:
        input_file = generate.generate(sim_spec=spec)
        if ns.v:
            pprint(input_file)
        jsonfile = 'rickshaw' + '.json'
        with open(jsonfile, 'w') as jf:
            json.dump(input_file, jf, indent=4)        
    if ns.rs:
        p = os.popen('ls *.json').readlines()
        for i in range(len(p)):            
            subprocess.call(['cyclus', p[i].rstrip('\n'), '-o', 'rickshaw.sqlite'])
    if ns.rh:
        p = os.popen('ls *.json').readlines()
        for i in range(len(p)):            
            subprocess.call(['cyclus', p[i].rstrip('\n'), '-o', 'rickshaw.h5'])


if __name__ == '__main__':
    main()
