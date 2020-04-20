library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity Params is
   generic (
      BOO : boolean:=FALSE;
      INT : integer:=0;
      LOG : std_logic:='0';
      VEC : std_logic_vector(7 downto 0):="00000000";
      STR : string:="ABCD";
      REA : real:=0.0
   );
   port (
      boo_o : out std_logic;
      int_o : out std_logic_vector(7 downto 0);
      log_o : out std_logic;
      vec_o : out std_logic_vector(7 downto 0);
      str_o : out std_logic;
      rea_o : out std_logic
   );
end entity Params;

architecture RTL of Params is
begin

   assert BOO=True       report "The boolean is not True" severity failure;
   assert INT=92         report "The integer is not 92" severity failure;
   assert LOG='1'        report "The std_logic is not '1'" severity failure;
   assert VEC="11001100" report "The std_logic_vector is not 11001100" severity failure;
   assert STR="WXYZ"     report "The string is not WXYZ" severity failure;
   assert REA=1.0        report "The real is not 1.0" severity failure;

   boo_o <= '1' when BOO else '0';
   int_o <= std_logic_vector(to_unsigned(INT, 8));
   log_o <= LOG;
   vec_o <= VEC;
   str_o <= '1' when STR="WXYZ" else '0';
   rea_o <= '1' when REA=1.0 else '0';

end architecture RTL;
