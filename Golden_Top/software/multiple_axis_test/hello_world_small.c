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

// GLOBALS

int tap_counter = 0;

alt_32 prev_time = 0;

alt_up_accelerometer_spi_dev * acc_dev;

void timer_init() {
    // clock is 50 MHz
    // 0x4C4B40 is one tick per tenth of a second
    // 0x7A120 one tick per 10 millisecond
    // 0xC350 ont tick every millisecond
    // 2FA F080 one per second
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0002);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    // set initial value to the max ( counter counts down )
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0xFFFF);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0xFFFF); 
    // start the timer
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0006); // 0b0...0111

}

// timer is decreasing value every time
// check if the time difference is small enough, in which case ignore the tap

void accelerometer_isr(){
  alt_8 data;
  alt_up_accelerometer_spi_read(acc_dev, 0x30, &data); // read INT source to clear interrupt
  

  // perform write operation to save a snapshot of counter value in snap reg
  IOWR_ALTERA_AVALON_TIMER_SNAPH(TIMER_BASE, 0x1); // value of data doesn't matter
  alt_32 curr_time = IORD_ALTERA_AVALON_TIMER_SNAPH(TIMER_BASE);
  // printf("%u\n", curr_time);

  if ( prev_time - curr_time > 15 ){ // valid tap
    alt_putstr("tap\n");
    tap_counter++;
    printf("%d\n", tap_counter);
  }

  prev_time = curr_time;
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
  alt_up_accelerometer_spi_write(acc_dev, 0x2A, 0b00000001); // enable tap on z axis only
  alt_up_accelerometer_spi_write(acc_dev, 0x21, 0x10); // set DUR (0x10 = 10ms)
  // alt_up_accelerometer_spi_write(acc_dev, 0x22, 0xFF); // set LATENT register (0x20 = 10ms)
  // alt_up_accelerometer_spi_write(acc_dev, 0x23, 0xFF); // set WINDOW
  alt_up_accelerometer_spi_write(acc_dev, 0x1D ,0x16); // set THRESH_TAP (0x30 = 3g)

  // set bits in the accel register to enable interrupts
  alt_up_accelerometer_spi_write(acc_dev, 0x2F, 0b10111111); // set SINGLE_TAP to INT_1 pin
  alt_up_accelerometer_spi_write(acc_dev, 0x2E, 0b01000000); // enable single tap to generate interrupts

  // set function to be executed on interrupt
  alt_irq_register(ACCELEROMETER_SPI_IRQ, 0, accelerometer_isr);

  timer_init();

  while (1){
    // printf("accel interrupts: %d\n", tap_counter);
  };

  return 0;
}
