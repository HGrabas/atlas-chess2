#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : PyRogue _chargeInj Module
#-----------------------------------------------------------------------------
# File       : _chargeInj.py
# Author     : Larry Ruckman <ruckman@slac.stanford.edu>
# Created    : 2016-11-17
# Last update: 2016-11-17
#-----------------------------------------------------------------------------
# Description:
# PyRogue _chargeInj Module
#-----------------------------------------------------------------------------
# This file is part of the ATLAS CHESS2 DEV. It is subject to 
# the license terms in the LICENSE.txt file found in the top-level directory 
# of this distribution and at: 
#    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
# No part of the ATLAS CHESS2 DEV, including this file, may be 
# copied, modified, propagated, or distributed except according to the terms 
# contained in the LICENSE.txt file.
#-----------------------------------------------------------------------------

import pyrogue as pr

class chargeInj(pr.Device):
    def __init__(self, name="chargeInj", memBase=None, offset=0, hidden=False, expand=True):
        super(self.__class__, self).__init__(name, "Charge Injection Module",
                        memBase=memBase, offset=offset, hidden=hidden, expand=expand)
                        
        self.add(pr.Variable(name='pulseWidthRaw', units="1/320MHz",description='pulse width minus one', offset=0x14, bitSize=15, bitOffset=0,  base='hex', mode='RW'))
        self.add(pr.Variable(name='pulseWidth',    mode = 'RO', units="ns", base='string',    getFunction=self.nsPulse, dependencies=[self.variables['pulseWidthRaw']]))                
        self.add(pr.Variable(name='pulseDelayRaw', units="1/320MHz",description='pulse delay minus one', offset=0x14, bitSize=15, bitOffset=16, base='hex', mode='RW'))
        self.add(pr.Variable(name='pulseDelay',    mode = 'RO', units="ns", base='string',    getFunction=self.nsPulse, dependencies=[self.variables['pulseDelayRaw']]))
        self.add(pr.Variable(name='invPulse',      description='Invert the pulse',                       offset=0x18, bitSize=1, bitOffset=0, base='bool', mode='RW'))   
        self.add(pr.Variable(name='calPulseInh',   description='Inhibites Qinj pulse to be sent out',    offset=0x1C, bitSize=1, bitOffset=0, base='bool', mode='RW'))   

        for i in range(3):
            self.add(pr.Variable(name='hitDetValid%01i_%01i'%(i,0), offset=(4*i), bitSize=1, bitOffset=13, base='bool', mode='RO')) 
            self.add(pr.Variable(name='hitDetFlag%01i_%01i'%(i,0),  offset=(4*i), bitSize=1, bitOffset=12, base='bool', mode='RO')) 
            self.add(pr.Variable(name='hitDetCol%01i_%01i'%(i,0),   offset=(4*i), bitSize=5, bitOffset=7,  base='hex',  mode='RO')) 
            self.add(pr.Variable(name='hitDetRow%01i_%01i'%(i,0),   offset=(4*i), bitSize=7, bitOffset=0, base='hex', mode='RO'))                     
            self.add(pr.Variable(name='hitDetTimeRaw%01i_%01i'%(i,0), units="1/320MHz", description=' ', offset=(4*i), bitSize=16, bitOffset=16, base='hex', mode='RO')) 
            self.add(pr.Variable(name='hitDetTime%01i_%01i'%(i,0), mode = 'RO', units="ns", base='string', getFunction=self.nsTdc, dependencies=[self.variables['hitDetTimeRaw%01i_%01i'%(i,0)]]))                    
                
        for j in range(1,8):
            for i in range(3):
                self.add(pr.Variable(name='hitDetValid%01i_%01i'%(i,j), offset=(4*i+((j+1)*16)), bitSize=1, bitOffset=13, base='bool', mode='RO')) 
                self.add(pr.Variable(name='hitDetFlag%01i_%01i'%(i,j),  offset=(4*i+((j+1)*16)), bitSize=1, bitOffset=12, base='bool', mode='RO')) 
                self.add(pr.Variable(name='hitDetCol%01i_%01i'%(i,j),   offset=(4*i+((j+1)*16)), bitSize=5, bitOffset=7,  base='hex',  mode='RO')) 
                self.add(pr.Variable(name='hitDetRow%01i_%01i'%(i,j),   offset=(4*i+((j+1)*16)), bitSize=7, bitOffset=0, base='hex', mode='RO'))                     
                self.add(pr.Variable(name='hitDetTimeRaw%01i_%01i'%(i,j), units="1/320MHz", description=' ', offset=(4*i+((j+1)*16)), bitSize=16, bitOffset=16, base='hex', mode='RO')) 
                self.add(pr.Variable(name='hitDetTime%01i_%01i'%(i,j), mode = 'RO', units="ns", base='string', getFunction=self.nsTdc, dependencies=[self.variables['hitDetTimeRaw%01i_%01i'%(i,j)]]))                    
                
                
        self.add(pr.Variable(name = "calPulseVar", description = "Calibration Pulse",
                offset=0x10, bitSize=1, bitOffset=0, base='bool', mode='SL', hidden=True)) 
        self.add(pr.Command(name='calPulse',description='Calibration Pulse',base='None',
                function="""\
                        dev.calPulseVar.set(1)
                        """))                     
                
    @staticmethod
    def nsTdc(dev, var):
        value   = var.dependencies[0].get(read=False)
        fpValue = (value)*3.125
        return '%0.3f'%(fpValue) 

    @staticmethod
    def nsPulse(dev, var):
        value   = var.dependencies[0].get(read=False)
        fpValue = (value+1)*3.125
        return '%0.3f'%(fpValue)         
