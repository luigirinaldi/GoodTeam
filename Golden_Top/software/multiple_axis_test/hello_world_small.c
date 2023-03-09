/* 
 * "Small Hello World" example. 
 * 
 * This example prints 'Hello from Nios II' to the STDOUT stream. It runs on
 * the Nios II 'standard', 'full_featured', 'fast', and 'low_cost' example 
 * designs. It requires a STDOUT  device in your system's hardware. 
 *
 * The purpose of this example is to demonstrate the smallest possible Hello 
 * World application, using the Nios II HAL library.  The memory footprint
 * of this hosted application is ~332 bytes by default using the standard 
 * reference design.  For a more fully featured Hello World application
 * example, see the example titled "Hello World".
 *
 * The memory footprint of this example has been reduced by making the
 * following changes to the normal "Hello World" example.
 * Check in the Nios II Software Developers Manual for a more complete 
 * description.
 * 
 * In the SW Application project (small_hello_world):
 *
 *  - In the C/C++ Build page
 * 
 *    - Set the Optimization Level to -Os
 * 
 * In System Library project (small_hello_world_syslib):
 *  - In the C/C++ Build page
 * 
 *    - Set the Optimization Level to -Os
 * 
 *    - Define the preprocessor option ALT_NO_INSTRUCTION_EMULATION 
 *      This removes software exception handling, which means that you cannot 
 *      run code compiled for Nios II cpu with a hardware multiplier on a core 
 *      without a the multiply unit. Check the Nios II Software Developers 
 *      Manual for more details.
 *
 *  - In the System Library page:
 *    - Set Periodic system timer and Timestamp timer to none
 *      This prevents the automatic inclusion of the timer driver.
 *
 *    - Set Max file descriptors to 4
 *      This reduces the size of the file handle pool.
 *
 *    - Check Main function does not exit
 *    - Uncheck Clean exit (flush buffers)
 *      This removes the unneeded call to exit when main returns, since it
 *      won't.
 *
 *    - Check Don't use C++
 *      This builds without the C++ support code.
 *
 *    - Check Small C library
 *      This uses a reduced functionality C library, which lacks  
 *      support for buffering, file IO, floating point and getch(), etc. 
 *      Check the Nios II Software Developers Manual for a complete list.
 *
 *    - Check Reduced device drivers
 *      This uses reduced functionality drivers if they're available. For the
 *      standard design this means you get polled UART and JTAG UART drivers,
 *      no support for the LCD driver and you lose the ability to program 
 *      CFI compliant flash devices.
 *
 *    - Check Access device drivers directly
 *      This bypasses the device file system to access device drivers directly.
 *      This eliminates the space required for the device file system services.
 *      It also provides a HAL version of libc services that access the drivers
 *      directly, further reducing space. Only a limited number of libc
 *      functions are available in this configuration.
 *
 *    - Use ALT versions of stdio routines:
 *
 *           Function                  Description
 *        ===============  =====================================
 *        alt_printf       Only supports %s, %x, and %c ( < 1 Kbyte)
 *        alt_putstr       Smaller overhead than puts with direct drivers
 *                         Note this function doesn't add a newline.
 *        alt_putchar      Smaller overhead than putchar with direct drivers
 *        alt_getchar      Smaller overhead than getchar with direct drivers
 *
 */

#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_stdio.h"
#include "sys/alt_irq.h"
#include "alt_types.h"
#include <stdlib.h>
#include <stdio.h>

#define ACCEL_INT_1 0x00021038
#define ACCEL_INT_1 0x00021039

// GLOBALS

volatile tap_counter = 0;

volatile alt_up_accelerometer_spi_dev * acc_dev;
volatile alt_32 acc_x = 0;
volatile alt_32 acc_y = 0;
volatile alt_32 acc_z = 0;

// offsets
alt_32 x_off = -15;
alt_32 y_off = 4;
alt_32 z_off = 256; // g value

// time

dt = 1; // 1 us

// velocity

alt_32 x_v = 0;

// position

alt_32 x_p = 0;

void sys_timer_isr(){

  IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);

  alt_up_accelerometer_spi_read_x_axis(acc_dev, & acc_x);
  alt_up_accelerometer_spi_read_y_axis(acc_dev, & acc_y);
  alt_up_accelerometer_spi_read_z_axis(acc_dev, & acc_z);
  acc_x = acc_x - x_off;
  acc_y = acc_y - y_off;
  acc_z = acc_z - z_off;
  printf("%d,%d,%d\n", acc_x, acc_y, acc_z);
}

void timer_init(void * isr) {
    // clock is 50 MHz
    // 0x4C4B40 is one tick per tenth of a second
    // 0x7A120 one tick per 10 millisecond
    // 0xC350 ont tick every millisecond
    // 2FA F080 one per second
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0xA120);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0007); 
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007); // 0b0...0111

}



void accelerometer_isr(){
  alt_putstr("received accelerometer interrupt!\n");
  alt_8 data;
  alt_up_accelerometer_spi_read(acc_dev, 0x2B, &data);
  // alt_printf("axis: x %x, y %x, z %x\n", (data & 0b100) >> 2, (data & 0b10) >> 1, data & 0b1);
  alt_printf("axis: %x\n", data & 0b111);
  data = 0;
  alt_up_accelerometer_spi_read(acc_dev, 0x30, &data);
  alt_printf("INT_SOURCE: %x, %x\n", data, tap_counter++);
}

int main()
{ 
  alt_putstr("Hello from Nios II!\n");
  alt_putstr("Printing 3 axis accelerometer info:\n");
  
  /* Event loop never exits. */


  acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
  }

  // set bits to enable tap detection
  alt_up_accelerometer_spi_write(acc_dev, 0x2A, 0b00000001); // enable tap on all axes
  alt_up_accelerometer_spi_write(acc_dev, 0x21, 0x10); // set DUR (0x10 = 10ms for some reason)
  alt_up_accelerometer_spi_write(acc_dev, 0x1D ,0x30); // set THRESH_TAP (0x30 = 3g)

  // set bits in the accel register to enable interrupts
  alt_up_accelerometer_spi_write(acc_dev, 0x2F, 0b10111111); // set SINGLE_TAP to INT_1 pin
  alt_up_accelerometer_spi_write(acc_dev, 0x2E, 0b01000000); // enable single tap to generate interrupts

  // set function to be executed on interrupt
  alt_irq_register(ACCELEROMETER_SPI_IRQ, 0, accelerometer_isr);

  // timer_init(sys_timer_isr);

  while (1){
  };

  return 0;
}
