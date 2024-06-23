library IEEE;
use IEEE.std_logic_1164.all;
library blink_lib;
use blink_lib.blink_pkg.all;

entity Top is
  generic (
    FREQ : natural := 0
  );
  port (
    clk_i :  in std_logic;
    led_o : out std_logic
  );
end entity Top;

architecture ARCH of Top is
begin

  assert FREQ > 0 report "FREQ must be greater than 0" severity failure;

  blink_i: Blink
  generic map (FREQ => FREQ)
  port map (clk_i => clk_i, led_o => led_o);

end architecture ARCH;
