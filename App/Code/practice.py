#generator
def process_log_file(file_path, substring):
    with open(file_path, 'r') as file:
        for line in file:
            if substring in line:
                yield line


file_path = r"enb.log"
substring = "RRC DL DCCH PDU for RNTI 110"


for occ in process_log_file(file_path, substring):
    print(occ)
