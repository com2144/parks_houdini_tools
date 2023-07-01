import hou
import os
import subprocess

class ImageConverting:
    def __init__(self):
        self.file_name = ''
        self.ext = ''
        self.mp4_file_path = ''
        self.render_path = '' 
        self.image_file_path = ''
        
        self.select_renderer()
        
    
    def select_renderer(self):
        select_node = hou.ui.selectNode()
        confirm_out = select_node.split('/')
            
        if select_node is not None and 'out' in confirm_out:
            self.node = hou.node(select_node)
        elif 'out' not in confirm_out:
            self.warning_message('Select Out network plz') 
        else:
            self.warning_message('Select Node plz!')
    
    def make_paths(self):
        image_path = self.node.parm('vm_picture').evalAsString()
        root_path = image_path.split('/')
        
        file_name = root_path[-1]
        element_dir_name = root_path[-2]
        jpg_dir_name = root_path[-3]
        
        
        for i in range(0,3):
            del root_path[-1]

        root_path = '/'.join(root_path)
        
        file_name_split = file_name.split('.')
        self.ext = file_name_split[-1]
        
        for i in range(0,2):
            del file_name_split[-1]        
        
        file_name = ''.join(file_name_split)

        mp4_path = f'{root_path}/mp4/{element_dir_name}'
        
        if not os.path.exists(mp4_path):
            os.makedirs(mp4_path)
                
        self.mp4_file_path = f'{mp4_path}/{file_name}.mp4'
        print(self.mp4_file_path)
        self.render_path = f'{root_path}/{jpg_dir_name}/{element_dir_name}'
        self.image_file_path = f'{self.render_path}/{self.file_name}.%04d.{self.ext}'
        
        
   
    def convert_action(self):
        start_frame = int(self.node.parm('f1').evalAsString())
        end_frame = int(self.node.parm('f2').evalAsString())
        
        render_dir_count = len(os.listdir(self.render_path))
        
        if self.ext not in ['jpg', 'exr']:
            self.warning_message('Wrong extension setup!')
            
        elif end_frame != render_dir_count or not os.path.exists(self.render_path):
            self.node.parm('execute').pressButton()
            if end_frame == len(os.listdir(self.render_path)):
                ffmpeg_cmd = f'ffmpeg -framerate 24 -start_number {start_frame} -i {self.image_file_path} -frames:v {end_frame} {self.mp4_file_path}'
                subprocess.run(ffmpeg_cmd, shell=True)
                self.warning_message('Converting is Done')
            else:
                self.warning_message('rendering not Complete')
            
        elif os.path.exists(self.mp4_file_path):
            self.warning_message('mp4 already exists!')
            
        else:
            ffmpeg_cmd = f'ffmpeg -framerate 24 -start_number {start_frame} -i {self.image_file_path} -frames:v {end_frame} {self.mp4_file_path}'
            subprocess.run(ffmpeg_cmd, shell=True)
            self.warning_message('Converting is Done')
  
    @staticmethod
    def warning_message(message):
        hou.ui.displayMessage(message, title='Warning', severity=hou.severityType.Message)
        
        
def main():
    test = ImageConverting()
    test.make_paths()
    test.convert_action()
    
main()
