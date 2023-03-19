
module nios_accelerometer (
	accelerometer_spi_external_interface_I2C_SDAT,
	accelerometer_spi_external_interface_I2C_SCLK,
	accelerometer_spi_external_interface_G_SENSOR_CS_N,
	accelerometer_spi_external_interface_G_SENSOR_INT,
	clk_clk,
	hex_0_external_connection_export,
	hex_1_external_connection_export,
	hex_2_external_connection_export,
	hex_3_external_connection_export,
	hex_4_external_connection_export,
	hex_5_external_connection_export,
	led_external_connection_export,
	reset_reset_n,
	spi_external_MISO,
	spi_external_MOSI,
	spi_external_SCLK,
	spi_external_SS_n);	

	inout		accelerometer_spi_external_interface_I2C_SDAT;
	output		accelerometer_spi_external_interface_I2C_SCLK;
	output		accelerometer_spi_external_interface_G_SENSOR_CS_N;
	input		accelerometer_spi_external_interface_G_SENSOR_INT;
	input		clk_clk;
	output	[7:0]	hex_0_external_connection_export;
	output	[7:0]	hex_1_external_connection_export;
	output	[7:0]	hex_2_external_connection_export;
	output	[7:0]	hex_3_external_connection_export;
	output	[7:0]	hex_4_external_connection_export;
	output	[7:0]	hex_5_external_connection_export;
	output	[9:0]	led_external_connection_export;
	input		reset_reset_n;
	input		spi_external_MISO;
	output		spi_external_MOSI;
	output		spi_external_SCLK;
	output		spi_external_SS_n;
endmodule
