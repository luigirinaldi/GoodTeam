#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_spi_regs.h"
#include "altera_avalon_pio_regs.h"
#include "altera_avalon_timer.h"
#include <altera_avalon_spi.h>
#include "sys/alt_stdio.h"
#include "sys/alt_irq.h"
#include "alt_types.h"
#include "system.h"
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

#define CHARLIM 256
#define BLANK_SPACES 3
#define SPI_BUFFER_SIZE 4

struct Message{
  char *text;
  int length;
  int loopCount;
};

int getBin(char letter);
void print7seg(const char letters[6]);

// GLOBALS

// int tap_counter = 0;

struct Message currMsg;

// ##### SPI data #####
char newTapData = 0;
__uint16_t send_spi;
// ####################



alt_32 prev_time = 0;

alt_up_accelerometer_spi_dev * acc_dev;

void updateTextISR() {
  IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_1_BASE, 0);
  // printf("printing %s of length %d\n", currMsg.text, currMsg.length);

  if (currMsg.length == 0){
    char buffer[6] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF};
    print7seg(buffer);
  } else if (currMsg.length <= 6){
    // static

    char buffer[6] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF};

    for (int i = 0; i < currMsg.length; i++){
      buffer[i] = getBin(currMsg.text[i]) | 0b10000000;
    }

    buffer[currMsg.length - 1] &= 0b01111111; // add dot at the end of the message

    print7seg(buffer);
  } else {
    char buffer[6];

    for (int i = 0; i < 6; i++){
      if (currMsg.loopCount + i < currMsg.length) {
        buffer[i] = getBin(currMsg.text[currMsg.loopCount + i]) | 0b10000000;
      } else {
        buffer[i] = getBin(currMsg.text[currMsg.loopCount + i - currMsg.length ]) | 0b10000000;
      }

      if (currMsg.loopCount + i == currMsg.length - 1 - BLANK_SPACES) buffer[i] &= 0b01111111; // add the full stop
    }

    print7seg(buffer);

    if (currMsg.loopCount < currMsg.length) currMsg.loopCount++;
    else currMsg.loopCount = 0;
  }
}

void timer_0_init() {
    // clock is 50 MHz
    // 0x4C4B40 is one tick per tenth of a second
    // 0x7A120 one tick per 10 millisecond
    // 0xC350 ont tick every millisecond
    // 2FA F080 one per second
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_0_BASE, 0x0002);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_0_BASE, 0);
    // set initial value to the max ( counter counts down )
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_0_BASE, 0xFFFF);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_0_BASE, 0xFFFF);
    // start the timer
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_0_BASE, 0x0006); // 0b0...0111

}

void timer_1_init() {
  // clock is 50 MHz
  // 0x4C4B40 is one tick per tenth of a second
  // 0x7A120 one tick per 10 millisecond
  // 0xC350 ont tick every millisecond
  // 2FA F080 one per second
  IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_1_BASE, 0x0003);
  IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_1_BASE, 0);
  // set initial value to the max ( counter counts down )
  // 0x17D7840 // every half a second
  // 0xFE502A.AB every third of a second
  IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_1_BASE, 0x502A);
  IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_1_BASE, 0x00FE);
  alt_irq_register(TIMER_1_IRQ, 0, updateTextISR);
  // start the timer
  IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_1_BASE, 0x0007); // 0b0...0111
}

// timer is decreasing value every time
// check if the time difference is small enough, in which case ignore the tap

void accelerometer_isr(){
  alt_8 data;
  alt_up_accelerometer_spi_read(acc_dev, 0x30, &data); // read INT source to clear interrupt


  // perform write operation to save a snapshot of counter value in snap reg
  IOWR_ALTERA_AVALON_TIMER_SNAPH(TIMER_0_BASE, 0x1); // value of data doesn't matter
  alt_32 curr_time = IORD_ALTERA_AVALON_TIMER_SNAPH(TIMER_0_BASE);
  // printf("%u\n", curr_time);

  alt_32 time_diff = prev_time - curr_time;
  alt_32 time_diff_usec = time_diff * 1310;
//   alt_16 time_diff_sec = time_diff_µsec/1000000;
  alt_16 time_diff_msec = time_diff_usec/1000;

  if ( time_diff > 15 ){ // valid tap about 20 ms
    // tap_data[0] = (time_diff_msec>>8) & 0xff; //top 8 bits of timestamp
    // tap_data[1] = time_diff_msec & 0xff; //bottom 8 bits of timestamp

    send_spi = time_diff_msec | 0x8000;
    // printf("Switch values: %x\n", IORD(SWITCHES_BASE, 0) );
    // alt_putstr("tap:");
    // printf("%d\n", time_diff_msec);

    newTapData = 1; // indicate that there is data to send
    send_spi = time_diff_msec; // set data to send
  }

  prev_time = curr_time;
}

int main()
{ 
  // tap_data = (alt_u8*) malloc(SPI_BUFFER_SIZE);

  // rx_spi_data = (alt_u8*) malloc(SPI_BUFFER_SIZE);

  currMsg.text = calloc(CHARLIM, sizeof(char));

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

  timer_0_init();
  timer_1_init();

  // printf("Entered Main\n");

  alt_16 rcvd_spi;

  while (1){
    
    if (newTapData) IOWR_ALTERA_AVALON_SPI_TXDATA(SPI_BASE, send_spi | 0x8000);
    else IOWR_ALTERA_AVALON_SPI_TXDATA(SPI_BASE, IORD(SWITCHES_BASE, 0) >> 1); // ignore bottom bit since it's broken on my FPGA
    // IOWR_ALTERA_AVALON_SPI_TXDATA(SPI_BASE, send_spi | ((newTapData & 0b1) << 15)); // send the data setting the MSbit if there is new data to send
    newTapData = 0; // reset new data

    usleep(75); // delay to send data

    rcvd_spi = IORD_ALTERA_AVALON_SPI_RXDATA(SPI_BASE); // read incoming data

    if ((rcvd_spi >> 8) == -1) {
      alt_up_accelerometer_spi_write(acc_dev, 0x2E, 0b00000000); // disble single tap to generate interrupts, stop the acceleometer from generating taps and possibly breaking the uart communication
      IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_1_BASE, 0x000b); // disable timer interrupt
      
      alt_8 num_char = rcvd_spi & 0xFF; // extract bottom 8 bits
      // printf("about to receive %d chars\n", num_char);

      char *inc_msg = calloc(sizeof(char), 255);

      for (int i = 0; i < num_char; i++){
        IOWR_ALTERA_AVALON_SPI_TXDATA(SPI_BASE, 0 ); // write nothing just to get resposne
        usleep(75); // wait for resposne

        rcvd_spi = IORD_ALTERA_AVALON_SPI_RXDATA(SPI_BASE); // read data
        usleep(75); // wait a bit IMPORTANT!!!! FOR SOME REASON

        inc_msg[i] = rcvd_spi;// save char 

      } 
      // alt_putstr(inc_msg);
      // putchar('\n');

      // Write to the HEX digits
      memcpy(currMsg.text, inc_msg, (num_char + BLANK_SPACES) * sizeof(char)); // copy data
      if (num_char > 6) currMsg.length = num_char + BLANK_SPACES; // add blanks
      else currMsg.length = num_char;

      currMsg.loopCount = 0;

      free(inc_msg);

      alt_up_accelerometer_spi_write(acc_dev, 0x2E, 0b01000000); // enable single tap to generate interrupts
      IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_1_BASE, 0x0007); // 0b...1011; start the timer up again
    }
    // second_lot = IORD_ALTERA_AVALON_SPI_RXDATA(SPI_BASE + 1);

    // printf("sent: %i \treceived: %i %d\n", send_S, rcvd_S);

    usleep(10000);
  };

  return 0;
}


//Prints each of the letters out to the screen
void print7seg(const char letters[6]){
	//Takes the binary value for each letter and places it on each of the six 7-segment displays
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_5_BASE, letters[0]);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_4_BASE, letters[1]);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_3_BASE, letters[2]);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_2_BASE, letters[3]);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_1_BASE, letters[4]);
  IOWR_ALTERA_AVALON_PIO_DATA(HEX_0_BASE, letters[5]);
	return;
}

//Gets the binary representation of the character
int getBin(char letter){
	/*Based on the character entered, we convert to binary so the 7-segment knows which lights to turn on.
	The 7-segment has inverted logic so a 0 means the light is on and a 1 means the light is off.
	The rightmost bit starts the index at HEX#[0], and the leftmost bit is HEX#[6], the pattern
	for the 7-segment is shown in the DE0_C5 User Manual*/
	switch(letter){
	case '0':
		return 0b1000000;
	case '1':
		return 0b1111001;
	case '2':
		return 0b0100100;
	case '3':
		return 0b0110000;
	case '4':
		return 0b0011001;
	case '5':
		return 0b0010010;
	case '6':
		return 0b0000010;
	case '7':
		return 0b1111000;
	case '8':
		return 0b0000000;
	case '9':
		return 0b0010000;
	case 'A':
		return 0b0001000;
	case 'B'://Lowercase
		return 0b0000011;
	case 'C':
		return 0b1000110;
	case 'D'://Lowercase
		return 0b0100001;
	case 'E':
		return 0b0000110;
	case 'F':
		return 0b0001110;
	case 'G':
		return 0b0010000;
	case 'H':
		return 0b0001001;
	case 'I':
		return 0b1111001;
	case 'J':
		return 0b1110001;
	case 'K':
		return 0b0001010;
	case 'L':
		return 0b1000111;
  case 'M':
    return 0b0101010; // shitty M
	case 'N':
		return 0b0101011;
	case 'O':
		return 0b1000000;
	case 'P':
		return 0b0001100;
	case 'Q':
		return 0b0011000;
	case 'R'://Lowercase
		return 0b0101111;
	case 'S':
		return 0b0010010;
	case 'T':
		return 0b0000111;
	case 'U':
		return 0b1000001;
	case 'V':
		return 0b1100011;
  case 'W':
    return 0b0010101;  // skunked W
	case 'X':
		return 0b0011011;  // skunked X
	case 'Y':
		return 0b0010001;
	case 'Z':
		return 0b0100100;
  case ':':
    return 0b0111111;
	default:
		return 0b11111111;
	}
}
