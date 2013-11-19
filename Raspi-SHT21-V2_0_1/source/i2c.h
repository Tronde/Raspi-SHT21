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
// Filename:    i2c.h
// Description: I2C Software Implementierung
//              
// Author:      Martin Steppuhn
// History:     28.08.2012 Initial version
//				31.10.2012 Flexible pin connection
//--------------------------------------------------------------------------------------------------

#ifndef I2C_H
#define I2C_H

//=== Includes =====================================================================================	

#include "std_c.h"

//=== Preprocessing directives (#define) ===========================================================

//=== Type definitions (typedef) ===================================================================

//=== Global constants (extern) ====================================================================

//=== Global variables (extern) ====================================================================

//=== Global function prototypes ===================================================================

void  SI2C_SetPort(uint8 Scl,uint8 Sda);
void  SI2C_Start(void);
void  SI2C_Stop(void);
uint8 SI2C_SendByte(uint8 Data);
uint8 SI2C_ReadByte(uint8 Ack);
void  SI2C_SetSclState(uint8 State);
uint8 SI2C_GetSclState(void);

#endif
