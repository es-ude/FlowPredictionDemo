library ieee;
    use ieee.std_logic_1164.all;
    use ieee.std_logic_unsigned.all;
entity linear_1_b_rom is
    port (
        clk : in std_logic;
        en : in std_logic;
        addr : in std_logic_vector(1-1 downto 0);
        data : out std_logic_vector(8-1 downto 0)
    );
end entity linear_1_b_rom;
architecture rtl of linear_1_b_rom is
    type linear_1_b_rom_array_t is array (0 to 2**1-1) of std_logic_vector(8-1 downto 0);
    signal ROM : linear_1_b_rom_array_t:=("00000010","00000000");
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
