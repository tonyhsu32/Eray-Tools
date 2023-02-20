import ast

# 轉換 frame number 為影片時間
# windows source path use raw string (r"")
source_path = r"C:\Users\eray\Desktop\AI-VISION_ppe-collect\already_cut\AI-VISION_192.168.100.167_0_20221024_144829\找人時間片段.txt"
save_path = r"C:\Users\eray\Desktop\AI-VISION_ppe-collect\already_cut\AI-VISION_192.168.100.167_0_20221024_144829\frame_to_time.txt"


def cal_frame_2_time(frame):
    if frame[0] == '0':
        frame = frame[1:]

    hour = int(frame) / 30 / 3600  # 轉成影片小時
    hour_first = str(round(hour, 1)).split('.')[0]
    hour_last = float(f"0.{str(round(hour, 3)).split('.')[1]}")
 
    minute = round(hour_last * 60, 3)  # 轉成影片分鐘
    minute_first = str(float(minute)).split('.')[0]
    minute_last = float(f"0.{str(round(minute, 3)).split('.')[1]}")

    second = int(round(minute_last * 60, 3))  # 轉成影片秒鐘
    
    time_list = [hour_first, minute_first, second]
    for i, t in enumerate([hour_first, minute_first, second], start=0):
    	if len(str(t)) < 2:
            time_list[i] = f"0{t}"
   
    #print(f"{time_list[0]}h{time_list[1]}m{time_list[2]}s")
    return time_list


def cal_video_time(frame):
    if frame[0] == '0':
        frame = frame[1:]
    
    total_second = round(int(frame) / 30)

    hour = str(round(total_second / 60 / 60, 3)).split('.')[0]
    minute = int(float(f"0.{str(total_second / 3600).split('.')[1]}") * 60)
    second = round(float(f"0.{str(total_second / 60).split('.')[1]}") * 60)

    time_space = [hour, minute, second]
    for i, t in enumerate([hour, minute, second], start=0):
    	if len(str(t)) < 2:
            time_space[i] = f"0{t}"
    
    return time_space


def read_file(path):
    frame_container = list()
    
    with open(path, "r") as f:
        frame_list = f.readlines()
        
    for idx, frame in enumerate(frame_list):
        if frame != "\n":
            frame_container.append(frame.split("_")[2].split("\n")[0])

    return frame_container


def save_file(file_path, frame_to_time):
    with open(file_path, "w") as f:
        f.write(str(frame_to_time))


def trans_str_of_list_to_list(path):
    with open(path, "r") as f:
        frame_list = f.readlines()

    transformat = ast.literal_eval(frame_list[0])
    return transformat


def time_format(frame_time):
    return f"{frame_time[0]}h{frame_time[1]}m{frame_time[2]}s"
    
    
if __name__ == '__main__':
    container = list()
    read_frame = read_file(source_path)
   
    for frame_idx, each_frame in enumerate(read_frame, start=1):
        #for frame_time in [last_frame_time, current_frame_time]:
            #print(f"{frame_time[0]}h{frame_time[1]}m{frame_time[2]}s")
        
        if frame_idx % 2 == 0:
            # method cal_frame_2_time
            #prev_frame_time = cal_frame_2_time(read_frame[frame_idx - 2])
            #current_frame_time = cal_frame_2_time(each_frame)
            
            # method cal_video_time
            prev_frame_time = cal_video_time(read_frame[frame_idx - 2])
            current_frame_time = cal_video_time(each_frame)

            container.append([time_format(prev_frame_time), time_format(current_frame_time)])
        
    print(container)
    save_file(save_path, container)
   
    # transform file content (type str of list) to (type list)
    #trans_str_of_list_to_list(save_path)
    
    


