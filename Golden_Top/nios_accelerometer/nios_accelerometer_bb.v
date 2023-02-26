
module nios_accelerometer (
	clk_clk,
	reset_reset_n,
	led_external_connection_export,
	accelerometer_spi_external_interface_I2C_SDAT,
	accelerometer_spi_external_interface_I2C_SCLK,
	accelerometer_spi_external_interface_G_SENSOR_CS_N,
	accelerometer_spi_external_interface_G_SENSOR_INT);	

	input		clk_clk;
	input		reset_reset_n;
	output	[9:0]	led_external_connection_export;
	inout		accelerometer_spi_external_interface_I2C_SDAT;
	output		accelerometer_spi_external_interface_I2C_SCLK;
	output		accelerometer_spi_external_interface_G_SENSOR_CS_N;
	input		accelerometer_spi_external_interface_G_SENSOR_INT;
endmodule
