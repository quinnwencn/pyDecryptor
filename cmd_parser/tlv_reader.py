import struct


class TLVReader:
    def __init__(self, file_path):
        self._file = file_path
        self.tlv_data = self._read_tlv_file()

    def _read_tlv_file(self):
        tlv_data = {}
        with open(self._file, 'rb') as file:
            while True:
                # 读取 Type 和 Length（每个占 2 个字节）
                type_data = file.read(2)
                if not type_data:  # 文件结束
                    break
                length_data = file.read(2)
                length = struct.unpack('<H', length_data)[0]  # 大端字节序解包

                # 读取 Value
                value_data = file.read(length)
                tlv_data[int.from_bytes(type_data, 'little')] = value_data

        return tlv_data

    def get_value_by_type(self, type_id):
        """通过 type 获取对应的 value"""
        return self.tlv_data.get(type_id, None)