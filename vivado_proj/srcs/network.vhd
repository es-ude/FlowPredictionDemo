library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.all;

entity network is
    port (
        enable: in std_logic;
        clock: in std_logic;

        x_address: out std_logic_vector(2-1 downto 0);
        y_address: in std_logic_vector(1-1 downto 0);

        x: in std_logic_vector(8-1 downto 0);
        y: out std_logic_vector(8-1 downto 0);

        done: out std_logic
    );
end network;

architecture rtl of network is
    signal i_linear_0_clock : std_logic := '0';
    signal i_linear_0_done : std_logic := '0';
    signal i_linear_0_enable : std_logic := '0';
    signal i_linear_0_x : std_logic_vector(7 downto 0) := (others => '0');
    signal i_linear_0_x_address : std_logic_vector(1 downto 0) := (others => '0');
    signal i_linear_0_y : std_logic_vector(7 downto 0) := (others => '0');
    signal i_linear_0_y_address : std_logic_vector(3 downto 0) := (others => '0');
    signal i_linear_1_clock : std_logic := '0';
    signal i_linear_1_done : std_logic := '0';
    signal i_linear_1_enable : std_logic := '0';
    signal i_linear_1_x : std_logic_vector(7 downto 0) := (others => '0');
    signal i_linear_1_x_address : std_logic_vector(3 downto 0) := (others => '0');
    signal i_linear_1_y : std_logic_vector(7 downto 0) := (others => '0');
    signal i_linear_1_y_address : std_logic_vector(0 downto 0) := (others => '0');
    signal i_relu_0_clock : std_logic := '0';
    signal i_relu_0_enable : std_logic := '0';
    signal i_relu_0_x : std_logic_vector(7 downto 0) := (others => '0');
    signal i_relu_0_y : std_logic_vector(7 downto 0) := (others => '0');
begin
    done <= i_linear_1_done;
    i_linear_0_clock <= clock;
    i_linear_0_enable <= enable;
    i_linear_0_x <= x;
    i_linear_0_y_address <= i_linear_1_x_address;
    i_linear_1_clock <= clock;
    i_linear_1_enable <= i_linear_0_done;
    i_linear_1_x <= i_relu_0_y;
    i_linear_1_y_address <= y_address;
    i_relu_0_clock <= clock;
    i_relu_0_enable <= i_linear_0_done;
    i_relu_0_x <= i_linear_0_y;
    x_address <= i_linear_0_x_address;
    y <= i_linear_1_y;
    --------------------------------------------------------------------------------
    -- Instantiate all layers
    --------------------------------------------------------------------------------
    i_linear_0 : entity work.linear_0(rtl)
    port map(
      clock => i_linear_0_clock,
      done => i_linear_0_done,
      enable => i_linear_0_enable,
      x => i_linear_0_x,
      x_address => i_linear_0_x_address,
      y => i_linear_0_y,
      y_address => i_linear_0_y_address
    );
    i_relu_0 : entity work.relu_0(rtl)
    port map(
      clock => i_relu_0_clock,
      enable => i_relu_0_enable,
      x => i_relu_0_x,
      y => i_relu_0_y
    );
    i_linear_1 : entity work.linear_1(rtl)
    port map(
      clock => i_linear_1_clock,
      done => i_linear_1_done,
      enable => i_linear_1_enable,
      x => i_linear_1_x,
      x_address => i_linear_1_x_address,
      y => i_linear_1_y,
      y_address => i_linear_1_y_address
    );
end rtl;
