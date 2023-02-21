## Eray Tools ##

**Python and Shell scripts:** 
   * xml_2_json_and_integration  
   
   * upload_download  
   Use paramiko package, select SFTP protocol method to upload, download and can support compressed, decompressed file.
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
   * frame_to_time  
   * cut_frame
