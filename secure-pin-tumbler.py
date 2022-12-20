#!/usr/bin/env python3

import sys
import argparse
import itertools
from pathlib import Path

class PinTumblerCombinations:
    def __init__(self,pins,num_pins,macs,aggressiveness,outfile,columns):
        self.pins = pins
        self.num_pins = num_pins
        self.macs = macs
        self.aggressiveness = aggressiveness
        self.outfile = outfile
        self.columns = columns
        self.combinations = []

    def rpl(self,pin): #Relative Pin Length
        return self.pins.index(pin)

    def valid_combination(self,comb):
        last = self.rpl(comb[0])
        aggressiveness = 0

        #Filter out invalid MACS
        for c in comb:
            delta = abs(self.rpl(c) - last)
            if delta > self.macs:
                return False
            aggressiveness += delta
            last = self.rpl(c)

        #Filter out low aggressiveness
        if aggressiveness < self.aggressiveness:
            return False

        #Make second to last pin as long as possible to make picking very difficult.
        #Last pin should be <= (second to the last) - MACS.
        if len(comb) > 2:
            if self.rpl(comb[-1]) > self.rpl(comb[-2]) - self.macs:
                return False
        return True

    def generate(self):
        self.combinations = []
        for comb in itertools.product(self.pins,repeat = self.num_pins):
            if self.valid_combination(comb):
                self.combinations.append(comb)

        print(f'Total combinations: {len(self.combinations)}')

    def write(self):
        #Write header info
        self.outfile.write((
            'Pin Tumbler Lock Combinations\n'
            f'Pin bitting numbers: {self.pins}\n'
            f'Aggressiveness: {self.aggressiveness}, MACS: {self.macs}, Total: {len(self.combinations)}\n'
            'Use spool pins with smaller bottom pins and use serrated pins with the medium length bottom pins. Some locks support T-pins.\n'))

        combs = self.combinations.copy()
        while len(combs) > 0:
            for comb in combs[:self.columns]:
                self.outfile.write(f'{"".join(comb)} ')
            self.outfile.write('\n')
            combs = combs[self.columns:]

def _validate_pins(value):
    value = value.strip().replace(' ','')
    unique = ''.join(set(value))
    if len(value) == 0 or len(unique) != len(value):
        raise ValueError('Empty or not unique pin bitting numbers. Valid example: "01234567abc".')
    return value

def _validate_num_gte(min):
    def _validator(value):
        num = int(value)
        if num < min:
            raise ValueError(f'Number must be greater than or equal to {min}.')
        return num
    return _validator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Generates secure pin tumbler lock combinations',
        epilog = 'Refer to the key bitting specification for your locks.')
    parser.add_argument(
        dest = 'pins',
        type = _validate_pins,
        help = 'Pin bitting numbers, which must be in order. Example: "0123456789abc"')
    parser.add_argument(
        dest = 'num_pins',
        type = _validate_num_gte(1),
        help = 'Number of total pins. Usually 5')
    parser.add_argument(
        dest = 'macs',
        type = _validate_num_gte(0),
        help = 'MACS or Maximum Adjacent Cut Specification. Example: 4 for most Kwiksets and 7 for most Schlages')
    parser.add_argument(
        dest = 'aggressiveness',
        type = _validate_num_gte(0),
        help = 'Pin bitting aggressiveness or the minimum total difference in pin values')
    parser.add_argument(
        dest = 'outfile',
        type = argparse.FileType('w'),
        help = 'Output text file')
    parser.add_argument(
        '-c','--columns',
        dest = 'columns',
        type = _validate_num_gte(1),
        default = 20,
        help = 'Number of combinations columns. Default: 20')
    args = parser.parse_args()

    generator = PinTumblerCombinations(
        args.pins,args.num_pins,args.macs,args.aggressiveness,args.outfile,args.columns)
    generator.generate()
    generator.write()
    
    print('Done')
