library IEEE;
use IEEE.std_logic_1164.all;

entity Top is
   port (
      clk_i :  in std_logic;
      led_o : out std_logic
   );
end entity Top;

architecture Structural of Top is
   constant FREQ : positive := 50e6;

   component Blinking is
   generic (
      FREQ  : positive:=25e6;
      SECS  : positive:=1
   );
   port (
      clk_i :  in std_logic;
      led_o : out std_logic
   );
   end component Blinking;
begin

   dut: Blinking
      generic map (FREQ => FREQ, SECS => 1)
      port map (clk_i => clk_i, led_o => led_o);

end architecture Structural;
