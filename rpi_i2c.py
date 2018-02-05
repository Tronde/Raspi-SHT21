#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (c) 2015 Martin Steppuhn, www.emsystech.de. All rights reserved.
#
# Redistribution and use in source and binary, must retain the above copyright notice, and the following disclaimer.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
#
# History:
# 24.06.2015    Martin Steppuhn     Initial version

import RPi.GPIO as GPIO  # http://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
import fcntl
import time

class I2C:
    """Wrapper class for I2C with raspberry Pi

    Open the "internal" I2C Port with driver or emulate an I2C Bus on GPIO
    """
    addr = 0
    dev = None
    gpio_scl = 0
    gpio_sda = 0
    delay = 0.001

    def open(self,addr=0, dev=1, scl=0, sda=0):
        """Open I2C-Port

        addr: I2C-Device Address
        dev:  I2C-Port (Raspberry Pi) B,B+,Pi 2 = 1 the first Pi = 0
              For I2C Emulation with GPIO, dev must be None
        scl:  GPIO-Pin for SCL
        sda:  GPIO-Pin for SDA
        """
        self.addr = addr
        self.dev = dev
        self.gpio_scl = scl
        self.gpio_sda = sda

        if (self.dev == None):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.gpio_scl, GPIO.IN)  # SCL=1
            GPIO.setup(self.gpio_sda, GPIO.IN)  # SDA=1
        else:
            self.dev_i2c = open(("/dev/i2c-%s" % self.dev), 'rb+', 0)
            fcntl.ioctl(self.dev_i2c, 0x0706, self.addr)  # I2C Address

    def close(self):
        if (self.dev == None):
            GPIO.setup(self.gpio_scl, GPIO.IN)  # SCL=1
            GPIO.setup(self.gpio_sda, GPIO.IN)  # SDA=1
        else:
            self.dev_i2c.close()

    def write(self, data):
        """Write data to device

        :param data: one ore more bytes (int list)
        """
        if (self.dev == None):
            self._i2c_gpio_start()
            ack = self._i2c_gpio_write_byte(self.addr << 1)
            ack = self._i2c_gpio_write_byte(data[0])  # Trigger T measurement (no hold master)
            self._i2c_gpio_stop()
        else:
            d = bytes(data)
            self.dev_i2c.write(d)

    def read(self, size):
        """Read Bytes from I2C Device

        :param size: Number of Bytes to read
        :return: List with bytes
        """
        data = dict()
        if (self.dev == None):
            self._i2c_gpio_start()
            ack = self._i2c_gpio_write_byte((self.addr << 1) + 1)  # set READ-BIT
            # if not ack: print("I2C-ERROR: READ,NACK1")
            for i in range(size):
                ack = True if ((i + 1) < size) else False
                data[i] = self._i2c_gpio_read_byte(ack)
            self._i2c_gpio_stop()
        else:
            data = self.dev_i2c.read(size)
        return (data)

    ##########################################################################
    ##########################################################################
    #   GPIO Access
    ##########################################################################
    ##########################################################################

    def _i2c_gpio_start(self):
        """Send Start"""
        GPIO.setup(self.gpio_scl, GPIO.IN)  # SCL=1
        GPIO.setup(self.gpio_sda, GPIO.IN)  # SDA=1
        time.sleep(2 * self.delay)
        GPIO.setup(self.gpio_sda, GPIO.OUT)  # SDA=0
        GPIO.output(self.gpio_sda, 0)
        time.sleep(2 * self.delay)
        GPIO.setup(self.gpio_scl, GPIO.OUT)  # SCL=0
        GPIO.output(self.gpio_scl, 0)

    def _i2c_gpio_stop(self):
        """Send Stop"""
        GPIO.setup(self.gpio_sda, GPIO.OUT)  # SDA=0
        GPIO.output(self.gpio_sda, 0)
        time.sleep(2 * self.delay)
        GPIO.setup(self.gpio_scl, GPIO.IN)  # SCL=1
        time.sleep(2 * self.delay)
        GPIO.setup(self.gpio_sda, GPIO.IN)  # SDA=1
        time.sleep(2 * self.delay)

    def _i2c_gpio_write_byte(self, data):
        """Write a single byte"""
        for i in range(8):  # stop
            if (data & 0x80):
                GPIO.setup(self.gpio_sda, GPIO.IN)  # SDA=1
            else:
                GPIO.setup(self.gpio_sda, GPIO.OUT)  # SDA=0
                GPIO.output(self.gpio_sda, 0)
            data = data << 1
            time.sleep(self.delay)
            GPIO.setup(self.gpio_scl, GPIO.IN)  # SCL=1
            time.sleep(self.delay)
            # Clockstretching ToDo
            GPIO.setup(self.gpio_scl, GPIO.OUT)  # SCL=0
            GPIO.output(self.gpio_scl, 0)
            time.sleep(self.delay)

        GPIO.setup(self.gpio_sda, GPIO.IN)  # SDA=1
        time.sleep(self.delay)
        GPIO.setup(self.gpio_scl, GPIO.IN)  # SCL=1
        time.sleep(self.delay)
        # Clockstretching ToDo
        ack = True if (GPIO.input(self.gpio_sda) == 0) else False
        GPIO.setup(self.gpio_scl, GPIO.OUT)  # SCL=0
        GPIO.output(self.gpio_scl, 0)
        time.sleep(self.delay)
        return (ack)  # SCL=0 SDA=1

    def _i2c_gpio_read_byte(self, ack):
        """Read a single byte"""
        data = 0
        for i in range(8):  # stop
            time.sleep(self.delay)
            GPIO.setup(self.gpio_scl, GPIO.IN)  # SCL=1
            time.sleep(self.delay)
            # Clockstretching ToDo
            data = data << 1
            if (GPIO.input(self.gpio_sda)):
                data |= 1
            else:
                data &= ~1
            GPIO.setup(self.gpio_scl, GPIO.OUT)  # SCL=0
            GPIO.output(self.gpio_scl, 0)

        # ACK Bit ausgeben
        if (ack):
            GPIO.setup(self.gpio_sda, GPIO.OUT)  # SDA=0
            GPIO.output(self.gpio_sda, 0)
        else:
            GPIO.setup(self.gpio_sda, GPIO.IN)  # SDA=1

        time.sleep(self.delay)
        GPIO.setup(self.gpio_scl, GPIO.IN)  # SCL=1
        time.sleep(self.delay)
        # Clockstretching ToDo
        GPIO.setup(self.gpio_scl, GPIO.OUT)  # SCL=0
        GPIO.output(self.gpio_scl, 0)
        time.sleep(self.delay)
        GPIO.setup(self.gpio_sda, GPIO.IN)  # SDA=1  freigeben
        return (data)
