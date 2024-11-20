import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
# create data

class Filesystem():
    def __init__(self):
        self.sector_size = 4*1024
        self.no_of_sectors_per_block = 16
        self.block_size = 16*self.sector_size
        self.start_of_flash = 0x00000000
        self.end_of_flash = 0x07fff000
        self.flash_config_sector_size = 1
        self.top_metadata_sector_size = 1
        self.metadata_block_size = 15
        self.metadata_sector_size = self.metadata_block_size * self.no_of_sectors_per_block 
        self.main_param_sector_size = 1
        self.region_param_sector_size = 1
        self.whitelist_block_size = 383*2
        self.start_of_tx_pkt_sectors = 0x07842000
        self.mode = 4

        if (self.mode == 0):
            self.multiplier = 1
        elif (self.mode == 4):
            self.multiplier = 2
        elif (self.mode == 11):
            self.multiplier = int(((8/11) * 16)/8)
        else:
            print("mode error!")
            self.multiplier = 1
        self.calculate_addresses()
        self.print_addresses()
        self.calculate_sizes_and_no()
        self.print_sizes()
    
    def calculate_addresses(self):
        self.flash_config_start = self.start_of_flash
        self.flash_config_end = self.start_of_flash + self.sector_size
        self.top_metadata_start = self.flash_config_end
        self.top_metadata_end = self.top_metadata_start + self.sector_size
        self.metadata_start = self.top_metadata_end
        self.metadata_end = self.metadata_start + self.metadata_sector_size * self.sector_size
        self.main_param_start = self.metadata_end
        self.main_param_end = self.main_param_start + self.sector_size
        self.region_param_start = self.main_param_end
        self.region_param_end = self.region_param_start + self.sector_size
        self.whitelist_start = self.region_param_end
        self.whitelist_end = self.whitelist_start + self.whitelist_block_size * self.block_size
        self.rx_pkt_sector_start = self.whitelist_end
        self.rx_pkt_sector_end = self.start_of_tx_pkt_sectors
        self.tx_pkt_sector_end = self.end_of_flash
    
    def print_addresses(self):
        print("self.flash_config_start: \t0x{:08x}".format(self.flash_config_start))
        print("self.flash_config_end: \t0x{:08x}".format(self.flash_config_end))
        print("self.top_metadata_start: \t0x{:08x}".format(self.top_metadata_start))
        print("self.top_metadata_end: \t0x{:08x}".format(self.top_metadata_end))
        print("self.metadata_start: \t0x{:08x}".format(self.metadata_start))
        print("self.metadata_end: \t0x{:08x}".format(self.metadata_end))
        print("self.main_param_start: \t0x{:08x}".format(self.main_param_start))
        print("self.main_param_end: \t0x{:08x}".format(self.main_param_end))
        print("self.region_param_start: \t0x{:08x}".format(self.region_param_start))
        print("self.region_param_end: \t0x{:08x}".format(self.region_param_end))
        print("self.whitelist_start: \t0x{:08x}".format(self.whitelist_start))
        print("self.whitelist_end: \t0x{:08x}".format(self.whitelist_end))
        print("self.rx_pkt_sector_start: \t0x{:08x}".format(self.rx_pkt_sector_start))
        print("self.rx_pkt_sector_end: \t0x{:08x}".format(self.rx_pkt_sector_end))
        print("self.start_of_tx_pkt_sectors: \t0x{:08x}".format(self.start_of_tx_pkt_sectors))
        print("self.tx_pkt_sector_end: \t0x{:08x}".format(self.tx_pkt_sector_end))

    def calculate_sizes_and_no(self):
        self.flash_config_size = 61 * self.multiplier
        self.no_of_flash_config_per_sector = int(self.sector_size/self.flash_config_size)
        self.max_flash_configs = self.no_of_flash_config_per_sector * self.flash_config_sector_size
        self.top_metadata_size = 12 * self.multiplier
        self.no_of_top_metadata = int(self.sector_size/self.top_metadata_size)
        self.max_top_metadata = self.no_of_top_metadata * self.top_metadata_sector_size
        self.metadata_size = 45 * self.multiplier
        self.no_of_metadata = int(self.sector_size/self.metadata_size)
        self.max_metadata = self.no_of_metadata * self.metadata_sector_size
        self.main_param_size = 25 * self.multiplier
        self.no_of_main_param = int(self.sector_size/self.main_param_size)
        self.max_main_param = self.no_of_main_param * self.main_param_sector_size

        self.region_param_size = 1052* self.multiplier
        self.no_of_region_param = int(self.sector_size/self.region_param_size)
        self.max_region_param = self.no_of_region_param * self.region_param_sector_size


        self.whitelist_per_sector = 163* self.multiplier
        self.max_whitelist = self.whitelist_per_sector * self.whitelist_block_size * self.no_of_sectors_per_block

        self.rx_pkt_size = 351* self.multiplier
        self.no_of_rx_pkt_per_sector = int(self.sector_size/self.rx_pkt_size)
        self.max_rx_pkts = int(self.no_of_rx_pkt_per_sector * ((self.rx_pkt_sector_end - self.rx_pkt_sector_start)/self.sector_size))

        self.tx_pkt_size = 308* self.multiplier
        self.no_of_tx_pkt_per_sector = int(self.sector_size/self.tx_pkt_size)
        self.max_tx_pkts = int(self.no_of_tx_pkt_per_sector * ((self.tx_pkt_sector_end - self.rx_pkt_sector_end)/self.sector_size))

    def print_sizes(self):
        print("self.flash_config_size = {:d}".format(self.flash_config_size))
        print("self.no_of_flash_config_per_sector = {:d}".format(self.no_of_flash_config_per_sector))
        print("self.max_flash_configs = {:d}".format(self.max_flash_configs))
        print("self.top_metadata_size = {:d}".format(self.top_metadata_size))
        print("self.no_of_top_metadata = {:d}".format(self.no_of_top_metadata))
        print("self.max_top_metadata = {:d}".format(self.max_top_metadata))
        print("self.metadata_size = {:d}".format(self.metadata_size))
        print("self.no_of_metadata = {:d}".format(self.no_of_metadata))
        print("self.max_metadata = {:d}".format(self.max_metadata))
        print("self.main_param_size = {:d}".format(self.main_param_size))
        print("self.no_of_main_param = {:d}".format(self.no_of_main_param))
        print("self.max_main_param = {:d}".format(self.max_main_param))
        print("self.region_param_size = {:d}".format(self.region_param_size))
        print("self.no_of_region_param = {:d}".format(self.no_of_region_param))
        print("self.max_region_param = {:d}".format(self.max_region_param))
        print("self.whitelist_per_sector = {:d}".format(self.whitelist_per_sector))
        print("self.max_whitelist = {:d}".format(self.max_whitelist))
        print("self.rx_pkt_size = {:d}".format(self.rx_pkt_size))
        print("self.no_of_rx_pkt_per_sector = {:d}".format(self.no_of_rx_pkt_per_sector))
        print("self.max_rx_pkts = {:d}".format(self.max_rx_pkts))
        print("self.tx_pkt_size = {:d}".format(self.tx_pkt_size))
        print("self.no_of_tx_pkt_per_sector = {:d}".format(self.no_of_tx_pkt_per_sector))
        print("self.max_tx_pkts = {:d}".format(self.max_tx_pkts))
    
    def whitelist_readjust(self, new_whitelist_size):
        self.whitelist_block_size = int(new_whitelist_size/(self.whitelist_per_sector * self.no_of_sectors_per_block))
        
        self.calculate_addresses()
        self.print_addresses()
        self.calculate_sizes_and_no()
        self.print_sizes()







new = Filesystem()

new.whitelist_readjust(3000000)

data = {
    "flash_config":[0x00000100,0,0],
    "top": [0x00000200-0x00000100,0,0],
    "metadata": [0x000F0000-0x00000200,0,0],
    "main_param": [0x000F1000-0x000F0000,0,0],
    "region_param": [0x000F2000-0x000F1000,0,0],
    "whitelist": [0x001E0000-0x000F2000,0,0],
    "rx_packets": [0, (0x07840000-0x001E0000),0],
    "tx_packets": [0,0,0x07FF0000-0x07840000],
}

df = pd.DataFrame(data)

df = df.rename(index={0:'filesystem', 1: 'rx storage', 2: 'tx storage'})

print(df)

ax = df.plot.barh(stacked=True)
ax.xaxis.set_major_formatter(lambda x, pos: hex(int(x)))
for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    #print(x,y,width,height)
    if (width != 0):
        ax.text(x+width/2, 
                y+height/2, 
                '{:.0f} %'.format((width/0x07FF0000)*100), 
                horizontalalignment='center', 
                verticalalignment='center')

plt.show()
