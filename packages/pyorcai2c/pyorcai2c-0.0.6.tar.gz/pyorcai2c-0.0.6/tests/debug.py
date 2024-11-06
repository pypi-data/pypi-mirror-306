import os, sys

cwd = os.getcwd()
sys.path.insert(0, f'{cwd}')
from pyorcai2c.pyorcai2c import ftdi
import pyorcai2c.utils as u

i2c = ftdi(b'DD290424A')
slave = 0x02
regmap_filepath = os.path.join(cwd, 'regmaps', 'pmic01.json')
regmap = i2c.load_register_map(regmap_filepath)

# res = i2c.write(slave=slave, target=0, data=[0xff, 0xff])

res = i2c.read(
    slave=slave, 
    target=[
        0x04, 
        0x02, 
        0x05, 
        0xA1, 
        0xA3, 
        0xA2, 
        0x06, 
        'ChargeCtrl1', 
        'ChargeCtrl2', 
        'LDO1Mode', 
        'LDO2Ctrl', 
        'LDO2Voltage', 
        'tst_bias_a',
        'TstCntrl7',
        'LDO1Voltage'
    ]
)
print(res)

res = i2c.write(
    slave=slave, 
    target={
    0x02:0xAA,
    0x01:0xEA,
    0x10:0xCD,
    0x05:0xFE,
    0x06:0xBB,
    'LDO2Voltage':0x55,
    'Buck1Ctrl2':0x33,
    'unused_Buck1Ctrl2_b2':1,
    'unused_Buck1Ctrl2_b4':1,
    'unused_Buck1Ctrl2_b5':0,
    'Buck1Ton':255,
    'Buck1VRegA':0
    }
)
print(res)