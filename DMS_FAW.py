'''
connect device to your computer via usb_can
run sudo bash ./setup_can.sh can0 250000 in shell first
'''
import can
import json
import time
# b0 b1
Close_Eyes_Alarm_Dict = {'00': 'No Alarm','10': 'Alarm','01': 'Reserved','11': 'Not Available'}
Yawning_Alarm_Alarm_Dict = {'00': 'No Alarm','10': 'Alarm','01': 'Reserved','11': 'Not Available'}
Lower_Head_Alarm_Dict = {'00': 'No Alarm','10': 'Alarm','01': 'Reserved','11': 'Not Available'}
Wryneck_Alarm_Dict = {'00': 'No Alarm','10': 'Alarm','01': 'Reserved','11': 'Not Available'}
No_Face_Detected_Alert_Dict = {'00': 'No Alarm','10': 'Alarm','01': 'Reserved','11': 'Not Available'}

DMS_System_State_Dict = {'00': 'Not Active','10': 'Active','01': 'Error','11': 'Not Available'}

IRGlass_Detect_State_Dict = {'00': 'Unknown','10': 'Normal','01': 'Eye Shade by IR Glass','11': 'Not Available'}
Imager_Shade_State_Dict = {'00': 'Unknown','10': 'Normal','01': 'Shade','11': 'Not Available'}

Driver_Detect_State_Dict = {'00': 'Unknown','10': 'Normal','01': 'Can not find Driver','11': 'Not Available'}
Driver_Fatigue_State_Dict = {'000': 'Unknown','100': 'Attentive','010': 'Fatigue','110': 'HighFatigue','001': 'Reserved for future extensions','101': '......','011': 'Reserved for future extensions','111': 'Not Available'}
Driver_Attention_State_Dict = {'000': 'Unknown','100': 'Not Distractive','010': 'Distractive','110': 'High Distractive','001': 'Reserved for future extensions','101': '......','011': 'Reserved for future extensions','111': 'Not Available'}

#Message Class
class DMSInfo:
    def __init__(self):
        self.Close_Eyes_Alarm = "00"
        self.Yawning_Alarm_Alarm = "00"
        self.Lower_Head_Alarm = "00"
        self.Wryneck_Alarm = "00"
        self.No_Face_Detected_Alert = "00"

        self.DMS_System_State = "10"

        self.IRGlass_Detect_State = "10"
        self.Imager_Shade_State = "10"

        self.Driver_Detect_State = "10"
        self.Driver_Fatigue_State = "100"
        self.Driver_Attention_State = "100"

    # def LogInfo(self,log_file):
    def LogInfo(self):
        if self.Close_Eyes_Alarm != "00":
            print("Close_Eyes_Alarm:{}".format(Close_Eyes_Alarm_Dict[self.Close_Eyes_Alarm]))
        if self.Yawning_Alarm_Alarm != "00":
            print("Yawning_Alarm_Alarm:{}".format(Yawning_Alarm_Alarm_Dict[self.Yawning_Alarm_Alarm]))
        if self.Lower_Head_Alarm != "00":
            print("Lower_Head_Alarm:{}".format(Lower_Head_Alarm_Dict[self.Lower_Head_Alarm]))
        if self.Wryneck_Alarm != "00":
            print("Wryneck_Alarm:{}".format(Wryneck_Alarm_Dict[self.Wryneck_Alarm]))
        if self.No_Face_Detected_Alert != "00":
            print("No_Face_Detected_Alert:{}".format(No_Face_Detected_Alert_Dict[self.No_Face_Detected_Alert]))

        if self.DMS_System_State != "10":
            print("DMS_System_State:{}".format(DMS_System_State_Dict[self.DMS_System_State]))

        if self.IRGlass_Detect_State != "10":
            print("IRGlass_Detect_State:{}".format(IRGlass_Detect_State_Dict[self.IRGlass_Detect_State]))
        if self.Imager_Shade_State != "10":
            print("Imager_Shade_State:{}".format(Imager_Shade_State_Dict[self.Imager_Shade_State]))

        if self.Driver_Detect_State != "10":
            print("Driver_Detect_State:{}".format(Driver_Detect_State_Dict[self.Driver_Detect_State]))
            # log_file.write("Driver_Detect_State:{} \n".format(Driver_Detect_State_Dict[self.Driver_Detect_State]))
        if self.Driver_Fatigue_State != "100":
            print("Driver_Fatigue_State:{}".format(Driver_Fatigue_State_Dict[self.Driver_Fatigue_State]))
            # log_file.write("Driver_Fatigue_State:{} \n".format(Driver_Fatigue_State_Dict[self.Driver_Fatigue_State]))
        # if self.Driver_Attention_State != "100" or "101" or "000":
        if self.Driver_Attention_State not in ["000","100","101"]:
            print("Driver_Attention_State:{}".format(Driver_Attention_State_Dict[self.Driver_Attention_State]))
            # log_file.write("Driver_Attention_State:{} \n".format(Driver_Attention_State_Dict[self.Driver_Attention_State]))

# create a bus instance
bus = can.Bus(interface='socketcan',
              channel='can0',
              receive_own_messages=True)

# send a message
message = can.Message(arbitration_id=123, is_extended_id=True,
                      data=[0x11, 0x22, 0x33])

bus.send(message, timeout=0.2)

# create info instance
Warning_Info = DMSInfo()
#create log file
log_file = open("log.json","w")

# iterate over received messages
for msg in bus:
    #message id : 18ff4ef5 = hex(419385077)
    if msg.arbitration_id == 419385077:
        #transfer to binary
        byte_1 = "{:08b}".format(msg.data[0])
        #reverse
        byte_1 = byte_1[::-1]
        Warning_Info.Close_Eyes_Alarm = byte_1[0:2]
        Warning_Info.Yawning_Alarm_Alarm = byte_1[2:4]
        Warning_Info.Lower_Head_Alarm = byte_1[4:6]
        Warning_Info.Wryneck_Alarm = byte_1[6:8]

        byte_2 = "{:08b}".format(msg.data[1])
        # reverse
        byte_2 = byte_2[::-1]
        Warning_Info.No_Face_Detected_Alert = byte_2[0:2]

        #byte3:DMS_System_State,IRGlass_Detect_State,Imager_Shade_State,Driver_Detect_State
        byte_3 = "{:08b}".format(msg.data[2])
        #reverse
        byte_3 = byte_3[::-1]
        Warning_Info.DMS_System_State = byte_3[0:2]
        Warning_Info.IRGlass_Detect_State = byte_3[2:4]
        Warning_Info.Imager_Shade_State = byte_3[4:6]
        Warning_Info.Driver_Detect_State = byte_3[6:8]

        #byte4:Driver_Fatigue_State,Driver_Attention_State
        byte_4 = "{:08b}".format(msg.data[3])
        byte_4 = byte_4[::-1]
        Warning_Info.Driver_Fatigue_State = byte_4[0:3]
        Warning_Info.Driver_Attention_State = byte_4[3:6]

        #byte5-byte8 not used

        #print warnings
        Warning_Info.LogInfo()

        info_str = json.dumps({"byte1":byte_1,"byte2":byte_2,"byte3":byte_3,"byte4":byte_4,
                                "Close_Eyes_Alarm":Close_Eyes_Alarm_Dict[Warning_Info.Close_Eyes_Alarm],
                                "Yawning_Alarm_Alarm":Yawning_Alarm_Alarm_Dict[Warning_Info.Yawning_Alarm_Alarm],
                                "Lower_Head_Alarm": Lower_Head_Alarm_Dict[Warning_Info.Lower_Head_Alarm],
                                "Wryneck_Alarm": Wryneck_Alarm_Dict[Warning_Info.Wryneck_Alarm],
                                "No_Face_Detected_Alert": No_Face_Detected_Alert_Dict[Warning_Info.No_Face_Detected_Alert],
                                "DMS_System_State": DMS_System_State_Dict[Warning_Info.DMS_System_State],
                                "IRGlass_Detect_State": IRGlass_Detect_State_Dict[Warning_Info.IRGlass_Detect_State],
                                "Imager_Shade_State": Imager_Shade_State_Dict[Warning_Info.Imager_Shade_State],
                                "Driver_Detect_State": Driver_Detect_State_Dict[Warning_Info.Driver_Detect_State],
                                "Driver_Fatigue_State": Driver_Fatigue_State_Dict[Warning_Info.Driver_Fatigue_State],
                                "Driver_Attention_State": Driver_Attention_State_Dict[Warning_Info.Driver_Attention_State],
                                },sort_keys=True,indent=16)
        print('\n'.join([l.rstrip() for l in  info_str.splitlines()]))
        # str to dict
        info_dict = json.loads(info_str)
        #write to file
        json.dump(info_dict,log_file,sort_keys=True,indent=16)
        log_file.write("\n#######################################################################\n")
        print("################################################\n")
