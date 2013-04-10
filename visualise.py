#!/usr/bin/env jython
#
# Copyright (C) 2013 Simon Cook
# Contributor Simon Cook <simon.cook@embecosm.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.  
#
# This program parses the output from an e-server instance and shows core
# activity (well, really gdb connectivity) in a visual way

import sys
from time import sleep, strftime
from javax.swing import JButton, JFrame, Box, BoxLayout, JPanel, JLabel, JTextArea
from java.awt import Component, GridLayout, Color, Font, Dimension, GridBagLayout

cores = []
demo = False
MINPORT = 51000

def createMainWindow():
	# Create window
	frame = JFrame('Epiphany Core Visualisation',
		defaultCloseOperation = JFrame.EXIT_ON_CLOSE,
		size = (660,675)
	)

	# Main layout
	mainLayout = JPanel()
	frame.add(mainLayout)

	# Title
	#title = JLabel('hello', JLabel.CENTER)
	#mainLayout.add(title)

	# Cores
	corepanel = JPanel(GridLayout(8,8))
	global cores
	cores = []
	for i in range(0,64):
		core = JPanel(GridLayout(2,1))
		core.setPreferredSize(Dimension(80,80))
		corename = '(' + str(i%8) + ',' + str(i/8) + ')'
                namelabel = JLabel(corename, JLabel.CENTER)
		namelabel.setFont(Font("Dialog", Font.PLAIN, 18))
		portname = str(i+MINPORT)
		portlabel = JLabel(portname, JLabel.CENTER)
	        portlabel.setFont(Font("Dialog", Font.PLAIN, 16))
		core.add(namelabel)
		core.add(portlabel)
		core.setBackground(Color.BLACK)
		corepanel.add(core)
		cores.append(core)
	mainLayout.add(corepanel)

	frame.visible = True

if __name__ == '__main__':
	createMainWindow()
	if demo:
		while True:
			for i in range(0,64):
				if cores[i].getBackground() == Color.BLACK:
					cores[i].setBackground(Color.RED)
				else:
					cores[i].setBackground(Color.BLACK)
				sleep(1)
	else:
		while True:
			try:
				line = sys.stdin.readline()
				if line[:26] == 'Listening for RSP on port ':
					# GDB Server Disconnect
					port = int(line[26:31])
					port -= MINPORT
					print 'Red-lighting core', port, 'on', (port+MINPORT), '(', (port%8), ',', (port/8), ')'
					cores[port].setBackground(Color.RED)
				elif line[5:25] == ': connected to port ':
					# GDB Server Connect
					port = int(line[25:30])
					port -= MINPORT
					print 'Green-lighting Core',  port, 'on', (port+MINPORT), '(', (port%8), ',', (port/8), ')'
					cores[port].setBackground(Color.GREEN) 
			except:
				# FIXME, race condition in e-server printout
				print '*** Check test.txt ***'
			#sleep(0.02)
