## Eray Tools ##

**Python and Shell scripts:** 
   * xml_2_json_and_integration  
   Use Python package (**xml.etree.ElementTree**).
       - xml_2_json_and_integration_v2.py  
       
       
       1. ***PASCAL VOC dataset XML annotation format*** example: 
           ```
           <?xml version="1.0" encoding="utf-8"?>
           <annotation>
               <folder>VOC2007</folder>
               <filename>test100.mp4_3380.jpeg</filename>
               <size>
                   <width>1280</width>
                   <height>720</height>
                   <depth>3</depth>
               </size>
               <object>
                   <name>gemfield</name>
                   <bndbox>
                       <xmin>549</xmin>
                       <xmax>715</xmax>
                       <ymin>257</ymin>
                       <ymax>289</ymax>
                   </bndbox>
                   <truncated>0</truncated>
                   <difficult>0</difficult>
               </object>
               <object>
                   <name>civilnet</name>
                   <bndbox>
                       <xmin>842</xmin>
                       <xmax>1009</xmax>
                       <ymin>138</ymin>
                       <ymax>171</ymax>
                   </bndbox>
                   <truncated>0</truncated>
                   <difficult>0</difficult>
               </object>
               <segmented>0</segmented>
           </annotation>
           ```
       
       
       2. ***Our LabelImg XML annotation format*** example:
           ```
            <annotation>
                <folder>pic</folder>
                <filename>200311_145253_1_F14_P7_LB2_V_25.jpg</filename>
                <path>\\xx-MS-7B53\share2\xxx_0420\處理後\巡檢\200311_151028\pic\200311_145253_1_F14_P7_LB2_V_25.jpg</path>
                <source>
                    <database>Unknown</database>
                </source>
                <size>
                    <width>1280</width>
                    <height>720</height>
                    <depth>3</depth>
                </size>
                <segmented>0</segmented>
                <object>
                    <name>fence</name>
                    <pose>Unspecified</pose>
                    <truncated>0</truncated>
                    <difficult>0</difficult>
                    <bndbox>
                        <xmin>348</xmin>
                        <ymin>594</ymin>
                        <xmax>1012</xmax>
                        <ymax>712</ymax>
                    </bndbox>
                 </object>
                 <object>
                     <name>cones</name>
                     <pose>Unspecified</pose>
                     <truncated>0</truncated>
                     <difficult>0</difficult>
                     <bndbox>
                         <xmin>972</xmin>
                         <ymin>566</ymin>
                         <xmax>1074</xmax>
                         <ymax>715</ymax>
                     </bndbox>
                  </object>
                  <object>
                      <name>fence</name>
                      <pose>Unspecified</pose>
                      <truncated>0</truncated>
                      <difficult>0</difficult>
                      <bndbox>
                          <xmin>1048</xmin>
                          <ymin>530</ymin>
                          <xmax>1277</xmax>
                          <ymax>612</ymax>
                      </bndbox>
                   </object>
           </annotation>
           ```
       
       
       3. ***XML*** (Our LabelImg XML annotation format) ***to JSON*** (Format our training data annotations and MongoDB required json data) format example:
           ```
           {
                "id": 3822,
                "source": "xxx_環境物品",
                "filename": "\\\\xx-MS-7B53\\share2\\xxx_0420\\處理後\\巡檢\\200311_151028\\pic\\200311_145253_1_F14_P7_LB2_V_25.jpg",
                "import_Time": "2022-05-02 22:01:19",
                "remark": "xxx機器人拍攝的資料",
                "size": [
                    "1280",
                    "720",
                    "3"
                ],
                "object_detection": {
                    "fence": [
                        {
                            "xmin": "348",
                            "ymin": "594",
                            "xmax": "1012",
                            "ymax": "712"
                        },
                        {
                            "xmin": "1048",
                            "ymin": "530",
                            "xmax": "1277",
                            "ymax": "612"
                        }
                    ],
                    "cones": [
                        {
                            "xmin": "972",
                            "ymin": "566",
                            "xmax": "1074",
                            "ymax": "715"
                        }
                    ],
                    "負樣本": [
                        "shop_cart",
                        "basket",
                        "tree",
                        "car_rear",
                        "clampOnRear",
                        "plateBig",
                        "plate",
                        "vergenceTube",
                        "person"
                    ]
                }
            }
           ```
   
       4. ***Define your parameters and file path:***  
           ```
           # xml folder path 
             xml_init_path = "/home/xxx/Documents/xml_2_json/20220428_xx/xml"
             xml_des_path = "/home/xxx/Documents/xml_2_json/xx_20220428_xml_2_json/personal_json"
           ```
           
           ```
           ######## define required argments ########
           # 來源, (哪個專案 或 哪個公開資料集) and 備註說明
             project_source = "xxx_事件偵測"    # ["xxx_環境物品", "xxx_事件偵測", "xxx消防衣", "xxx_人身上的裝備"]
             remark_description = "xxx_事件偵測拍攝的資料"     # ["xxx機器人拍攝的資料", "xxx_事件偵測拍攝的資料", "xxx消防衣拍攝的資料", "xxx_人身上的裝備拍攝的資料"]


           # 給全部出現樣本 -> 會自動產生負樣本
           # total_sample = ['car_rear', 'clampOnRear', 'plateBig', 'plate', 'vergenceTube', 'person']
             total_sample = ['person', 'ladder']
           # total_sample = ['cones', 'fence', 'extinguisherCar', 'safeDoor', 'gutterHole', 'gutterCover', 'hydrant', 
           #                 'redBox', 'extinguisher', 'extinguisher_error', 'safeDoor_open', 'cardClose', 'personFall', 
           #                 'cones_error', 'capBlue', 'capWhite', 'capGreen', 'cardOpen', 'toolCabinet_open', 'cleaner', 'toolCabinet']
           ```
       
       5. ***XML to JSON sample:***  
          - xml_sample.png  
          
              ![XML sample](https://github.com/tonyhsu32/Eray-Tools/blob/main/xml_sample.png)  
          
          - xml_2_json_sample.png  
          
              ![XML to JSON sample](https://github.com/tonyhsu32/Eray-Tools/blob/main/xml_2_json_sample.png)
        
        
   * upload_download  
   Use **paramiko** package, select **SFTP protocol** method to **upload**, **download** and can support **compressed**, **decompressed** file.
     - paramiko使用ssh_改.py  
     
       ***define your parameters and file path:***
         ```
         # Define Server parameters  
           HostName = '192.168.33.240'  
           UserName = 'xxx'
           PassWord = 'xxx'  
           Port = 22
         ```  

         ```
         # 選擇方法 (4 methods): "upload", "download", "upload_compressed_file", "download_compressed_file"
           method = "download"  
         ```

         ```
         # 上傳and下載 (目前存放於Server: /home/xxx/projectDB/中)
         # 方法一： (資料夾)
         local_dir = "/home/xxx/Documents/xml_2_json/專案測試"
         remote_dir = "/home/xxx/projectDB/專案測試"

         # 方法二: (壓縮檔 ) (only support tar.xz to compress)
         # 注意: 只有下載的時候 server_folder 要是資料夾路徑  ex: "/home/eray/projectDB/專案測試"
         local_tar_path = "/home/xxx/Documents/xml_2_json/專案測試.tar.xz"
         server_folder = "/home/xxx/projectDB/專案測試.tar.xz"
         ```
   
   * test_mqtt  
     - test_mqtt_publisher.py  
     - test_mqtt_subsriber.py  
     - test_facedevice_rule.py
     
   * frame_to_time 
     - frame_to_time.py  
     - frame_to_time.txt  
     - 找人時間片段.txt
     
   * cut_frame  
     - videoToFrame.py
   
