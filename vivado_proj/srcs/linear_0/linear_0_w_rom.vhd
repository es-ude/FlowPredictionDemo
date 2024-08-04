library ieee;
    use ieee.std_logic_1164.all;
    use ieee.std_logic_unsigned.all;
entity linear_0_w_rom is
    port (
        clk : in std_logic;
        en : in std_logic;
        addr : in std_logic_vector(5-1 downto 0);
        data : out std_logic_vector(8-1 downto 0)
    );
end entity linear_0_w_rom;
architecture rtl of linear_0_w_rom is
    type linear_0_w_rom_array_t is array (0 to 2**5-1) of std_logic_vector(8-1 downto 0);
    signal ROM : linear_0_w_rom_array_t:=("00011000","00000100","11101010","11111000","11100010","11110110","11111110","00010000","11011110","00000010","00001101","00011010","00011100","11111001","00111100","11101101","00001101","00100011","11101111","11110011","11100100","11111010","11110100","11111001","00001111","11111010","00010110","11100000","11011111","11110111","00000000","00000000");
    attribute rom_style : string;
    attribute rom_style of ROM : signal is "auto";
begin
    ROM_process: process(clk)
    begin
        if rising_edge(clk) then
            if (en = '1') then
                data <= ROM(conv_integer(addr));
            end if;
        end if;
    end process ROM_process;
end architecture rtl;
