//--------------------------------------------------------------------------------------------------
//                                  _            _     
//                                 | |          | |    
//      ___ _ __ ___  ___ _   _ ___| |_ ___  ___| |__  
//     / _ \ '_ ` _ \/ __| | | / __| __/ _ \/ __| '_ \. 
//    |  __/ | | | | \__ \ |_| \__ \ ||  __/ (__| | | |
//     \___|_| |_| |_|___/\__, |___/\__\___|\___|_| |_|
//                         __/ |                       
//                        |___/    Engineering (www.emsystech.de)
//
// Filename:    main.c
// Description: Raspi-SHT21
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
// History:     05.09.2012 Initial version "Quick and Dirty" 
//				01.11.2012 Flexible PIN Configuration for I2C and Harrdwaredetection for Raspberry
//--------------------------------------------------------------------------------------------------

//=== Includes =====================================================================================

#include <stdio.h>
#include "bcm2835.h"
#include "raspi.h"
#include <unistd.h>
#include <stdlib.h>
#include "i2c.h"
#include "sht21.h"
#include "time.h"

//=== Preprocessing directives (#define) ===========================================================

#define	PIN_LED		4

//=== Type definitions (typedef) ===================================================================

//=== Global constants =============================================================================

//=== Global variables =============================================================================

//=== Local constants  =============================================================================

//=== Local variables ==============================================================================

//=== Local function prototypes ====================================================================


//--------------------------------------------------------------------------------------------------
// Name:      
// Function:  
//            
// Parameter: 
// Return:    
//--------------------------------------------------------------------------------------------------
int main(int argc, char **argv)
{ 
	int16	Temperature;
	uint8	Humidity;
	uint8	SHT21_Error;
	float 	Temp;
	FILE	*fp;
	time_t TimeCounter;
	time_t TimeCounterLocal;
	struct tm * Time;
	int 	Led,HwRev;
	
	Led = 0;
	
	printf("Raspi-SHT21 V2.0.0 by Martin Steppuhn (www.emsystech.de) [" __DATE__ " " __TIME__"]\n");

	if (!bcm2835_init())
	{
		printf("bcm2835_init() failed!\r\n");
		return 1;
	}
	bcm2835_gpio_fsel(PIN_LED,BCM2835_GPIO_FSEL_OUTP);		// LED: Output
	bcm2835_gpio_clr(PIN_LED);								// LED: Register auf low

	
	HwRev = GetRaspberryHwRevision();
	printf("RaspberryHwRevision=%i\r\n",HwRev);
	
	if(HwRev < 2) 	SI2C_SetPort(1,0);	 // Hardware Revision 1.0
		else		SI2C_SetPort(3,2);  // Hardware Revision 2.0
	
		
	while (1)
    {
		Led++;
		
		if(Led & 1) bcm2835_gpio_set(PIN_LED);	
			else	 bcm2835_gpio_clr(PIN_LED);	
	
		time ( &TimeCounter );
		
		if((TimeCounter % 10) == 0)		// alle 10 sec messen
		{
			SHT21_Error = SHT21_Read(&Temperature,&Humidity);
			Temp = Temperature;
			Temp /= 10;
			
			Time = localtime (&TimeCounter);   // wichtig für Timezone und Sommerzeit
			TimeCounterLocal = TimeCounter - timezone;			
			if(Time->tm_isdst) TimeCounterLocal += 3600;	// Sommerzeit
			
			printf("%02d.%02d.%d %02d:%02d:%02d\t",Time->tm_mday,Time->tm_mon+1,Time->tm_year+1900,Time->tm_hour, Time->tm_min, Time->tm_sec);
			printf("%u\t%.1f\t%u\r\n",(unsigned int)TimeCounterLocal,Temp,Humidity);
			
			if(SHT21_Error) printf("ERROR=0x%X\r\n",SHT21_Error);
		
			if((TimeCounter % 900) == 0)		// alle 15min speichern
			{
				fp = fopen("sht21-data.csv","a+");
				if(fp != NULL)
				{
					fprintf(fp,"%02d.%02d.%d %02d:%02d\t",Time->tm_mday,Time->tm_mon+1,Time->tm_year+1900,Time->tm_hour, Time->tm_min);
					fprintf(fp,"%u\t",(unsigned int)TimeCounterLocal);  
					if(!SHT21_Error) fprintf(fp,"%.1f\t%u",Temp,Humidity);
					fprintf(fp,"\r\n");
					fclose(fp);
					system("./run.sh");
				}
				else
				{
					printf("FileIO Error\r\n");
				}
			}
		}
		sleep(1);
    }
	return(0);
}