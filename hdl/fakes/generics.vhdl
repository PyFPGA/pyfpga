library IEEE;
use IEEE.std_logic_1164.all;

entity Params is
   generic (
      INT : integer:=0;
      REA : real:=0.0;
      LOG : std_logic:='0';
      VEC : std_logic_vector(7 downto 0):="00000000";
      STR : string:="ABCD"
   );
   port (
      d_i :  in std_logic;
      d_o : out std_logic
   );
end entity Params;

architecture RTL of Params is
begin
   d_o <= d_i;
end architecture RTL;
