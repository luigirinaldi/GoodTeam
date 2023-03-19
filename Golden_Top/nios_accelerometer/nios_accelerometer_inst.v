	nios_accelerometer u0 (
		.accelerometer_spi_external_interface_I2C_SDAT      (<connected-to-accelerometer_spi_external_interface_I2C_SDAT>),      // accelerometer_spi_external_interface.I2C_SDAT
		.accelerometer_spi_external_interface_I2C_SCLK      (<connected-to-accelerometer_spi_external_interface_I2C_SCLK>),      //                                     .I2C_SCLK
		.accelerometer_spi_external_interface_G_SENSOR_CS_N (<connected-to-accelerometer_spi_external_interface_G_SENSOR_CS_N>), //                                     .G_SENSOR_CS_N
		.accelerometer_spi_external_interface_G_SENSOR_INT  (<connected-to-accelerometer_spi_external_interface_G_SENSOR_INT>),  //                                     .G_SENSOR_INT
		.clk_clk                                            (<connected-to-clk_clk>),                                            //                                  clk.clk
		.led_external_connection_export                     (<connected-to-led_external_connection_export>),                     //              led_external_connection.export
		.reset_reset_n                                      (<connected-to-reset_reset_n>),                                      //                                reset.reset_n
		.hex_0_external_connection_export                   (<connected-to-hex_0_external_connection_export>),                   //            hex_0_external_connection.export
		.hex_2_external_connection_export                   (<connected-to-hex_2_external_connection_export>),                   //            hex_2_external_connection.export
		.hex_3_external_connection_export                   (<connected-to-hex_3_external_connection_export>),                   //            hex_3_external_connection.export
		.hex_1_external_connection_export                   (<connected-to-hex_1_external_connection_export>),                   //            hex_1_external_connection.export
		.hex_4_external_connection_export                   (<connected-to-hex_4_external_connection_export>),                   //            hex_4_external_connection.export
		.hex_5_external_connection_export                   (<connected-to-hex_5_external_connection_export>),                   //            hex_5_external_connection.export
		.spi_external_MISO                                  (<connected-to-spi_external_MISO>),                                  //                         spi_external.MISO
		.spi_external_MOSI                                  (<connected-to-spi_external_MOSI>),                                  //                                     .MOSI
		.spi_external_SCLK                                  (<connected-to-spi_external_SCLK>),                                  //                                     .SCLK
		.spi_external_SS_n                                  (<connected-to-spi_external_SS_n>)                                   //                                     .SS_n
	);

