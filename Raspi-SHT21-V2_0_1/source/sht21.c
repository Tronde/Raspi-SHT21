//------------------------------------------------------------------------------
//                                  _            _     
//                                 | |          | |    
//      ___ _ __ ___  ___ _   _ ___| |_ ___  ___| |__  
//     / _ \ '_ ` _ \/ __| | | / __| __/ _ \/ __| '_ \. 
//    |  __/ | | | | \__ \ |_| \__ \ ||  __/ (__| | | |
//     \___|_| |_| |_|___/\__, |___/\__\___|\___|_| |_|
//                         __/ |                       
//                        |___/    Engineering
//
// Filename:    sht21.c
// Description: Temperatur und Feuchte
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
// History:     14.09.2012 Initial version "Quick and Dirty" 
//------------------------------------------------------------------------------

/**** Includes ****************************************************************/

#include "std_c.h"
#include "i2c.h"
#include "raspi.h"

/**** Preprocessing directives (#define) **************************************/

/**** Type definitions (typedef) **********************************************/

/**** Global constants ********************************************************/

/**** Global variables ********************************************************/

/**** Local constants  ********************************************************/

/**** Local variables *********************************************************/

/**** Local function prototypes ***********************************************/

uint8 SHT21_CalcCrc(uint8 *data,uint8 nbrOfBytes);

//------------------------------------------------------------------------------
// Name:      
// Function:  
//            
// Parameter: 
// Return:    
//------------------------------------------------------------------------------
uint8 SHT21_Read(int16 *temp,uint8 *humidity)
{
	uint8	error;
	uint8	d[3];
	uint8	timeout;
	uint32 val;
	
	error = 0;
	
	//=== Software reset ausführen =============================================
		
	SI2C_Start();
  	error |= SI2C_SendByte((0x40 << 1) + 0);	// Addr + WR
  	error |=SI2C_SendByte(0xFE);				// Soft reset
  	SI2C_Stop();
  	
  	DelayMs(15);
  	
  	//=== User register ======================================================== 
  	// Zwingend notwendig da ein paar bits nicht geändert werden 
  	// dürfen aber nicht definiert sind  
	// Error LSB Bit for NACK error
  	
	SI2C_Start();
  	error |= SI2C_SendByte((0x40 << 1) + 0);	// Addr + WR
  	error |= SI2C_SendByte(0xE7);				// Read user register
  	SI2C_Start();
  	error |= SI2C_SendByte((0x40 << 1) + 1);	// Addr + RD
  	d[0] = SI2C_ReadByte(1);			
  	d[1] = SI2C_ReadByte(0);
  	SI2C_Stop();  
  	
  	if(d[0] == 0) 
	{
		error |= 0x02;
	}
	else if(d[1] == SHT21_CalcCrc(d,1))
	{
		SI2C_Start();
  		error |= SI2C_SendByte((0x40 << 1) + 0);	// Addr + WR
  		error |= SI2C_SendByte(0xE6);			// User register
  		error |= SI2C_SendByte(d[0]);			// Value 
  		SI2C_Stop();
	}
	else
	{
		error |= 0x04;
//		xprintf("%02X %02X \t",d[0],d[1]); 	  	
	}

	//=== Temperatur ===========================================================  	
 			
  	SI2C_Start();
  	error |= SI2C_SendByte((0x40 << 1) + 0);
  	error |= SI2C_SendByte(0xE3);
  	SI2C_Start();
  	error |= SI2C_SendByte((0x40 << 1) + 1);
  	SI2C_SetSclState(1);
  	
  	timeout = 100;
  	while(SI2C_GetSclState()  == 0 && timeout)
  	{
  		DelayMs(1);
  		timeout--;
  	}
	if(timeout == 0) error |= 0x08;
  	
  	d[0] = SI2C_ReadByte(1);
  	d[1] = SI2C_ReadByte(1);
  	d[2] = SI2C_ReadByte(0);
  	SI2C_Stop();
  	
  	//xprintf("%02X %02X %02X\t",d[0],d[1],d[2]); 
  	
  	if(d[2] == SHT21_CalcCrc(d,2))
	{
  		val = d[0];
  		val <<= 8;
  		val += d[1];
  		val &= 0xFFFC;
  		  		
  		//	T = -46,85 + 175,72 * St/65535      da 1/10K -->  * 10
  		//	T = -468,5 + 1757,2 * St/65535		verinfachen
  		//	T = -468,5 + St / 37,2956..			damit Konstante ganzzahlig wird mit 2 erweitern
  		//  T = -937 + 2*St / 37,2956..			Bruch für Division mit 256 erweitern  
  		//	T = (-937 +  (St * 512) / (37,2956.. * 256)  )  / 2
  		//	T = (((St * 512) / 9548) - 937) / 2
  		  		
  		//	val = (((val * 512) / 9548) - 937) / 2;
  		
  		*temp = ((val * 512) / 9548);
  		*temp = ((*temp) - 937) / 2;       
	}
	else
	{
		error |= 0x10;
	}
	
	//=== Feuchte ==============================================================
	
 	SI2C_Start();
  	error |= SI2C_SendByte((0x40 << 1) + 0);
  	error |= SI2C_SendByte(0xE5);
  	SI2C_Start();
  	error |= SI2C_SendByte((0x40 << 1) + 1);
  	SI2C_SetSclState(1);
  	timeout = 100;
  	while(SI2C_GetSclState() == 0 && timeout)
  	{
  		DelayMs(1);
  		timeout--;
  	}
	if(timeout == 0) error |= 0x20;
	
  	d[0] = SI2C_ReadByte(1);
  	d[1] = SI2C_ReadByte(1);
  	d[2] = SI2C_ReadByte(0);
  	SI2C_Stop();
  		
	//xprintf("%02X %02X %02X\t",d[0],d[1],d[2]);  		
  		
  	if(d[2] == SHT21_CalcCrc(d,2))
	{	
  		val = d[0];
  		val <<= 8;
  		val += d[1];
  		val &= 0xFFFC;
  		  			
  		//   T = -6 + 125* Srh/65535      
  		//	 T = -6 + Srh / 524,28
  		//   T = -6 + (Srh * 256) / 134215      |  *256	 wegen Numerik erweitern
  	  		  		
  		val = ((val * 256) / 134215) - 6;
  		*humidity = val;
	}
	else
	{
		error |= 0x40;
	}
  	return(error);
}

//------------------------------------------------------------------------------
// Name:      
// Function:  
//            
// Parameter: 
// Return:    
//------------------------------------------------------------------------------
uint8 SHT21_CalcCrc(uint8 *data,uint8 nbrOfBytes)
{
	// CRC
	//const u16t POLYNOMIAL = 0x131; //P(x)=x^8+x^5+x^4+1 = 100110001
	
	uint8 byteCtr,bit,crc;

	crc = 0;

	//calculates 8-Bit checksum with given polynomial
	for (byteCtr = 0; byteCtr < nbrOfBytes; ++byteCtr)
	{ 
		crc ^= (data[byteCtr]);
		for (bit = 8; bit > 0; --bit)
		{
			if (crc & 0x80) crc = (crc << 1) ^ 0x131;
				else 		crc = (crc << 1);
		}
	}
	return(crc);
}
