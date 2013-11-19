//--------------------------------------------------------------------------------------------------
//                                  _            _     
//                                 | |          | |    
//      ___ _ __ ___  ___ _   _ ___| |_ ___  ___| |__  
//     / _ \ '_ ` _ \/ __| | | / __| __/ _ \/ __| '_ \. 
//    |  __/ | | | | \__ \ |_| \__ \ ||  __/ (__| | | |
//     \___|_| |_| |_|___/\__, |___/\__\___|\___|_| |_|
//                         __/ |                       
//                        |___/    Engineering
//
// Filename:    i2c.c
// Description: I2C Software Implementierung
//
// Open Source Licensing 
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
// Dieses Programm ist Freie Software: Sie können es unter den Bedingungen
// der GNU General Public License, wie von der Free Software Foundation,
// Version 3 der Lizenz oder (nach Ihrer Option) jeder späteren
// veröffentlichten Version, weiterverbreiten und/oder modifizieren.
//
// Dieses Programm wird in der Hoffnung, dass es nützlich sein wird, aber
// OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
// Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
// Siehe die GNU General Public License für weitere Details.
//
// Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
// Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.
//               
// Author:      Martin Steppuhn
// History:     28.08.2012 Initial version
//				31.10.2012 Flexible pin connection
//--------------------------------------------------------------------------------------------------

//=== Includes =====================================================================================

#include "std_c.h"
#include "i2c.h"
#include "bcm2835.h"

//=== Preprocessing directives (#define) ===========================================================

#define	SCL_1		bcm2835_gpio_fsel(pin_scl,BCM2835_GPIO_FSEL_INPT)		// Input -> 1 über Pullup
#define	SCL_0		bcm2835_gpio_fsel(pin_scl,BCM2835_GPIO_FSEL_OUTP)		// Output -> 0 auf GND
#define	SCL			bcm2835_gpio_lev(pin_scl)
#define	SDA_1		bcm2835_gpio_fsel(pin_sda,BCM2835_GPIO_FSEL_INPT)		// Input -> 1 über Pullup
#define	SDA_0		bcm2835_gpio_fsel(pin_sda,BCM2835_GPIO_FSEL_OUTP)		// Output -> 0 auf GND
#define	SDA			bcm2835_gpio_lev(pin_sda)

#define	SSI2C_DELAY	delayMicroseconds(0);

//=== Type definitions (typedef) ===================================================================

//=== Global constants =============================================================================

//=== Global variables =============================================================================

//=== Local constants  =============================================================================

//=== Local variables ==============================================================================

uint8	pin_scl;
uint8	pin_sda;

//=== Local function prototypes ====================================================================

//--------------------------------------------------------------------------------------------------
// Name:		SI2C_SetPort
// Function:  	"Connect" GPIO-Pins to Port
//            
// Parameter: 	scl and sda Pinnumber
// Return:    	-
//--------------------------------------------------------------------------------------------------
void SI2C_SetPort(uint8 scl,uint8 sda)
{
	pin_scl = scl;
	pin_sda = sda;
}

//--------------------------------------------------------------------------------------------------
// Name:		SI2C_Start
// Function:  	Transmit start sequence
//            
// Parameter: 	-
// Return:    	-
//--------------------------------------------------------------------------------------------------
void SI2C_Start(void)
{
	SCL_1; 
	SDA_1; 
	SSI2C_DELAY;
	SSI2C_DELAY;
	SDA_0;
	SSI2C_DELAY;
	SSI2C_DELAY;
	SCL_0; 
	SSI2C_DELAY;
	SSI2C_DELAY;
}

//--------------------------------------------------------------------------------------------------
// Name:		SI2C_Stop
// Function:  	Stopsequenz senden
//            
// Parameter: 	-
// Return:    	-
//--------------------------------------------------------------------------------------------------
void SI2C_Stop(void)
{
	SDA_0;			
	SSI2C_DELAY;
	SSI2C_DELAY;
	SCL_1; 
	SSI2C_DELAY;
	SSI2C_DELAY;
	SDA_1;
	SSI2C_DELAY;
	SSI2C_DELAY;
}

//--------------------------------------------------------------------------------------------------
// Name:		SI2C_SendByte
// Function:  	Byte ausgeben 
//            
// Parameter: 	Byte
// Return:    	1=NACK 0=ACK   (for Errordetection)
//--------------------------------------------------------------------------------------------------
uint8 SI2C_SendByte(uint8 Data)
{
	uint8 i,t,r;
	
	for(i=0;i<8;i++)
	{
		if(Data & 0x80) { SDA_1; }
			else		{ SDA_0; }
		Data <<= 1;
		SSI2C_DELAY;
		SCL_1; 
		SSI2C_DELAY;
		t = 100;
		while(!SCL && t--); SSI2C_DELAY;    // Clockstretching 
		SCL_0; 
		SSI2C_DELAY;
	}
	SDA_1;		
		
	SSI2C_DELAY;		
	SCL_1;
	SSI2C_DELAY;
	
	t = 100;
	while(!SCL && t--); SSI2C_DELAY;    // Clockstretching 
	
	r = SDA ? 1 : 0;
	SCL_0;
	SSI2C_DELAY;
	return(r);
}

//--------------------------------------------------------------------------------------------------
// Name:		SI2C_ReadByte
// Function:  	Byte lesen
//            
// Parameter: 	Ack  1= ACK Bite setzen (low) 0= kein ACK (high)
// Return:    	gelesenes byte
//--------------------------------------------------------------------------------------------------
uint8 SI2C_ReadByte(uint8 Ack)
{
	uint8 i,d,t;
	
	d=0;
	SDA_1;				// damit Input
	for(i=0;i<8;i++)
	{
		SSI2C_DELAY;
		SCL_1; 
		SSI2C_DELAY;

		t = 100;
		while(!SCL && t--); SSI2C_DELAY;    // Clockstretching 


		d <<= 1;
		if(SDA) 	{ d |=  1; }
			else	{ d &= ~1; }

		SSI2C_DELAY;			
		SCL_0;		
		SSI2C_DELAY;
	}
	
	if(Ack) 	{ SDA_0; }
		else	{ SDA_1; }
	SSI2C_DELAY;
	SCL_1; 
	SSI2C_DELAY;
	
	t = 100;
	while(!SCL && t--); SSI2C_DELAY;    // Clockstretching 

	SCL_0;
	SSI2C_DELAY;
	SDA_1;
	return d;	
}

//--------------------------------------------------------------------------------------------------
// Name:		SI2C_SetSclState
// Function:  	Control SCL Pin
//            
// Parameter: 	0 / 1
// Return:    	-
//--------------------------------------------------------------------------------------------------
void SI2C_SetSclState(uint8 State)
{
	if(State) { SCL_1; }
		else  { SCL_0; }
}

//--------------------------------------------------------------------------------------------------
// Name:		SI2C_GetSclState
// Function:  	Read state of SCL Pin
//            
// Parameter: 	-
// Return:    	0 / 1
//--------------------------------------------------------------------------------------------------
uint8 SI2C_GetSclState(void)
{
	if(SCL)   return 1;
		else  return 0;
}


