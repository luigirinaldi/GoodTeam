	component nios_accelerometer is
		port (
			accelerometer_spi_external_interface_I2C_SDAT      : inout std_logic                    := 'X'; -- I2C_SDAT
			accelerometer_spi_external_interface_I2C_SCLK      : out   std_logic;                           -- I2C_SCLK
			accelerometer_spi_external_interface_G_SENSOR_CS_N : out   std_logic;                           -- G_SENSOR_CS_N
			accelerometer_spi_external_interface_G_SENSOR_INT  : in    std_logic                    := 'X'; -- G_SENSOR_INT
			clk_clk                                            : in    std_logic                    := 'X'; -- clk
			led_external_connection_export                     : out   std_logic_vector(9 downto 0);        -- export
			reset_reset_n                                      : in    std_logic                    := 'X'; -- reset_n
			hex_0_external_connection_export                   : out   std_logic_vector(6 downto 0);        -- export
			hex_2_external_connection_export                   : out   std_logic_vector(6 downto 0);        -- export
			hex_3_external_connection_export                   : out   std_logic_vector(6 downto 0);        -- export
			hex_1_external_connection_export                   : out   std_logic_vector(6 downto 0);        -- export
			hex_4_external_connection_export                   : out   std_logic_vector(6 downto 0);        -- export
			hex_5_external_connection_export                   : out   std_logic_vector(6 downto 0);        -- export
			spi_external_MISO                                  : in    std_logic                    := 'X'; -- MISO
			spi_external_MOSI                                  : out   std_logic;                           -- MOSI
			spi_external_SCLK                                  : out   std_logic;                           -- SCLK
			spi_external_SS_n                                  : out   std_logic                            -- SS_n
		);
	end component nios_accelerometer;

	u0 : component nios_accelerometer
		port map (
			accelerometer_spi_external_interface_I2C_SDAT      => CONNECTED_TO_accelerometer_spi_external_interface_I2C_SDAT,      -- accelerometer_spi_external_interface.I2C_SDAT
			accelerometer_spi_external_interface_I2C_SCLK      => CONNECTED_TO_accelerometer_spi_external_interface_I2C_SCLK,      --                                     .I2C_SCLK
			accelerometer_spi_external_interface_G_SENSOR_CS_N => CONNECTED_TO_accelerometer_spi_external_interface_G_SENSOR_CS_N, --                                     .G_SENSOR_CS_N
			accelerometer_spi_external_interface_G_SENSOR_INT  => CONNECTED_TO_accelerometer_spi_external_interface_G_SENSOR_INT,  --                                     .G_SENSOR_INT
			clk_clk                                            => CONNECTED_TO_clk_clk,                                            --                                  clk.clk
			led_external_connection_export                     => CONNECTED_TO_led_external_connection_export,                     --              led_external_connection.export
			reset_reset_n                                      => CONNECTED_TO_reset_reset_n,                                      --                                reset.reset_n
			hex_0_external_connection_export                   => CONNECTED_TO_hex_0_external_connection_export,                   --            hex_0_external_connection.export
			hex_2_external_connection_export                   => CONNECTED_TO_hex_2_external_connection_export,                   --            hex_2_external_connection.export
			hex_3_external_connection_export                   => CONNECTED_TO_hex_3_external_connection_export,                   --            hex_3_external_connection.export
			hex_1_external_connection_export                   => CONNECTED_TO_hex_1_external_connection_export,                   --            hex_1_external_connection.export
			hex_4_external_connection_export                   => CONNECTED_TO_hex_4_external_connection_export,                   --            hex_4_external_connection.export
			hex_5_external_connection_export                   => CONNECTED_TO_hex_5_external_connection_export,                   --            hex_5_external_connection.export
			spi_external_MISO                                  => CONNECTED_TO_spi_external_MISO,                                  --                         spi_external.MISO
			spi_external_MOSI                                  => CONNECTED_TO_spi_external_MOSI,                                  --                                     .MOSI
			spi_external_SCLK                                  => CONNECTED_TO_spi_external_SCLK,                                  --                                     .SCLK
			spi_external_SS_n                                  => CONNECTED_TO_spi_external_SS_n                                   --                                     .SS_n
		);

