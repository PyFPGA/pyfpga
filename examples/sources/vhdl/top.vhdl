library IEEE;
use IEEE.std_logic_1164.all;
library blink_lib;
use blink_lib.blink_pkg.all;

entity Top is
  generic (
    FREQ : natural := 0;
    SECS : natural := 0
  );
  port (
    clk_i :  in std_logic;
    led_o : out std_logic
  );
end entity Top;

architecture ARCH of Top is
begin

  blink_i: Blink
  generic map (FREQ => FREQ, SECS => SECS)
  port map (clk_i => clk_i, led_o => led_o);

  gen_error : if FREQ=0 or SECS=0 generate
    top_i: entity work.Top
    port map (clk_i => clk_i, led_o => led_o);
  end generate gen_error;

end architecture ARCH;
