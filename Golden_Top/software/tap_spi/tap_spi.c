#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_stdio.h"
#include "sys/alt_irq.h"
#include "alt_types.h"
#include <altera_avalon_spi.h>
#include <stdlib.h>
#include <stdio.h>

// GLOBALS

int tap_counter = 0;

alt_32 prev_time = 0;

alt_u8 *tap_data;

alt_up_accelerometer_spi_dev * acc_dev;

void timer_init() {
    // clock is 50 MHz
    // 0x4C4B40 is one tick per tenth of a second
    // 0x7A120 one tick per 10 millisecond
    // 0xC350 ont tick every millisecond
    // 2FA F080 one per second
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0002); // sets cont. bit; making counter continuous
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);  // something else
    // set initial value to the max ( counter counts down )
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0xFFFF);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0xFFFF);
    // start the timer
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0006); // 0b0...0110

}

// timer is decreasing value every time
// check if the time difference is small enough, in which case ignore the tap

void accelerometer_isr(){
  alt_u8 data;
  alt_up_accelerometer_spi_read(acc_dev, 0x30, &data); // read INT source to clear interrupt


  // perform write operation to save a snapshot of counter value in snap reg
  IOWR_ALTERA_AVALON_TIMER_SNAPH(TIMER_BASE, 0x1); // value of data doesn't matter
  alt_32 curr_time = IORD_ALTERA_AVALON_TIMER_SNAPH(TIMER_BASE);
  // printf("%u\n", curr_time);
  alt_32 time_diff = prev_time - curr_time;
  alt_32 time_diff_µsec = time_diff * 1310;
//   alt_16 time_diff_sec = time_diff_µsec/1000000;
  alt_16 time_diff_msec = time_diff_µsec/1000;


  if ( time_diff > 16 ){  // valid tap if 20ms have passed since last tap

    tap_data[0] = (time_diff_msec>>8) & 0xff; //top 8 bits of timestamp
    tap_data[1] = time_diff_msec & 0xff; //bottom 8 bits of timestamp
    alt_putstr("taps: ");
    tap_counter++;
    printf("%d\n", tap_counter);
    alt_putstr("time since last tap: ");
    printf("%d", time_diff_msec);
    alt_putstr(" msec\n");
    alt_avalon_spi_command(SPI_BASE, 0 ,0x2, tap_data, 0, 0, 0);

  }
  
  prev_time = curr_time;

}

int main()
{ 
  tap_data = (alt_u8*) malloc(2);

  alt_putstr("DETECTING TAPS: \n");

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
