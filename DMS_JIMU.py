'''
run sudo bash ./setup_can.sh can0 500000 in shell first
'''
import can
import time
fatigue_dict = {'1': '闭眼', '2': '打哈欠','3': '睁眼睡','4': '低头','5': '左顾右盼','6': '无人脸',
                '7': '打电话','8': '抽烟','9': '遮挡','10': '抬头','11': '安全带',}
def fatigue_warning(coding):#1921,byte.bit : 1.1
    return fatigue_dict[coding]

def binary_to_T(str):#4
    str_length = len(str)
    result = 0
    for i in range(str_length):
        result += int(str[i])*pow(2,str_length-1-i)
    return result
# create a bus instance
# many other interfaces are supported as well (see below)
bus = can.Bus(interface='socketcan',
              channel='can0',
              receive_own_messages=True)

# send a message
message = can.Message(arbitration_id=123, is_extended_id=True,
                      data=[0x11, 0x22, 0x33])
#0x780=1920
bus.send(message, timeout=0.2)
# iterate over received messages
for msg in bus:
    if msg.arbitration_id == 1921:
        # length = len(msg.data)
        # if length != 8:
        #     continue
        binary_num = "{:08b}".format(msg.data[0])[4:]
        # print(binary_num)
        coding = binary_to_T(binary_num)
        # print(coding)
        fatigue_info = fatigue_warning(str(coding))
        print(fatigue_info)
        print("###################")
