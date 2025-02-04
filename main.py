import numpy as np
import wave
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import time
import sys
import os
from datetime import datetime
import ffmpeg  # 导入ffmpeg-python库

#刚学编程 我写的是屎山代码我写的是屎山代码我写的是屎山代码
# 限制递归深度
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

# 创建一个隐藏的主窗口
root = tk.Tk()
root.withdraw()  # 隐藏主窗口

# 时间戳
now = datetime.now()
timestamp = now.timestamp()
print("当前时间戳：", timestamp)

# 显示警告信息
messagebox.showwarning("警告！", "请不要在程序运行时删除本目录下的临时文件，否则会导致程序运行出错！")

# 循环直到用户确认文件选择正确
while True:
    file_path = filedialog.askopenfilename(
        title="请选择文件",
        filetypes=[("所有文件", "*.*")]
    )
    if file_path:
        result = messagebox.askyesno("确认", f"选中的文件路径是：\n{file_path}\n\n请确认是否正确")
        if result:
            print("文件选择已确认，继续后续操作...")
            break
        else:
            print("文件选择错误，重新选择文件...")
    else:
        print("没有选择文件，程序将在3秒后退出...")
        time.sleep(3)
        sys.exit()

print(f"选中的文件路径是：{file_path}")

while True:
    whatfps = simpledialog.askstring("帧率？", "请输入生成视频的帧率：")
    if whatfps == None:
        print("未输入帧率，程序将在3秒后退出...")
        time.sleep(3)
        sys.exit()
    elif whatfps.isdigit():
        break
    else:
        messagebox.showerror("错误", "请输入数字！")
        
whatpath = file_path

# 还未使用的功能.....
def bytes_to_image(data, width, height):
    image = np.frombuffer(data, dtype=np.uint8)
    image = image[:width * height * 3]
    image = image.reshape((height, width, 3))
    return image

messagebox.showinfo("提示","生成过程可能较为漫长，请耐心等待。可在控制台查看生成过程")

# 二进制文件转视频
def create_video_from_file(file_path, output_path, width=256, height=256, fps=int(whatfps)):
    with open(file_path, 'rb') as file:
        data = file.read()
    
    frame_size = width * height * 3
    num_frames = len(data) // frame_size
    
    frames = []
    for i in range(num_frames):
        start = i * frame_size
        end = start + frame_size
        frame_data = data[start:end]
        frame = bytes_to_image(frame_data, width, height)
        frames.append(frame)
    
    clip = ffmpeg.input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height), r=fps)
    process = (
        ffmpeg
        .output(clip, output_path, vcodec='libx264')
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )
    for frame in frames:
        process.stdin.write(frame.tobytes())
    process.stdin.close()
    process.wait()
    print(f"视频已生成，保存为{output_path}")

file_path = whatpath
video_output_path = 'video_temp_output.mp4'
create_video_from_file(file_path, video_output_path)
print(f"视频已生成，保存为{video_output_path}")

# 获取视频时长
def get_video_duration(output_path):
    probe = ffmpeg.probe(output_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    duration = float(video_stream['duration'])
    return duration

videolong = get_video_duration(video_output_path)

# 计算音频采样率
def calculate_audio_sample_rate(video_path, video_duration):
    probe = ffmpeg.probe(video_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    fps = float(video_stream['avg_frame_rate'].split('/')[0]) / float(video_stream['avg_frame_rate'].split('/')[1])
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    
    total_frames = int(video_duration * fps)
    frame_data_size = width * height * 3
    total_data_size = total_frames * frame_data_size
    sample_rate = total_data_size / video_duration / 2
    return sample_rate

sample_rate = calculate_audio_sample_rate(video_output_path, videolong)

# 将二进制数据转换为音频数据
def bytes_to_audio(data, sample_rate=int(sample_rate)):
    audio = np.frombuffer(data, dtype=np.int16)
    return audio

def create_audio_from_file(file_path, output_path, sample_rate=int(sample_rate)):
    with open(file_path, 'rb') as file:
        data = file.read()
    
    audio_data = bytes_to_audio(data, sample_rate)
    
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

file_path = whatpath
audio_output_path = 'audio_temp_output.wav'
create_audio_from_file(file_path, audio_output_path)
print(f"音频已生成，保存为{audio_output_path}")

# 合并视频和音频
def merge_video_audio(video_path, audio_path, output_path):
    video_input = ffmpeg.input(video_path)
    audio_input = ffmpeg.input(audio_path)
    ffmpeg.output(video_input, audio_input, output_path, vcodec='copy', acodec='aac').overwrite_output().run()
    print(f"合并完成，输出文件保存为{output_path}")

video_path = video_output_path
audio_path = audio_output_path
nozoom_output_path = "nozoomtemp_output.mp4"
merge_video_audio(video_path, audio_path, nozoom_output_path)

# 放大视频
def resize_video(input_file, output_file, width, height):
    video_input = ffmpeg.input(input_file)
    ffmpeg.output(video_input, output_file, vf=f"scale={width}:{height}:flags=neighbor", vcodec='libx264', crf=18, acodec='copy').overwrite_output().run()
    print(f"视频已成功放大并保存到 {output_file}")

input_file = nozoom_output_path
output_file = f"./output_{timestamp}.mp4"
resize_video(input_file, output_file, 768, 768)

# 安全删除临时文件
def safe_delete(file_path, retries=3, delay=2):
    for attempt in range(retries):
        try:
            os.remove(file_path)
            print(f"成功删除临时文件：{file_path}")
            return
        except PermissionError as e:
            print(f"删除文件时出错：{e}，尝试第 {attempt + 1} 次...")
            time.sleep(delay)
    print(f"无法删除文件：{file_path}，请手动删除。")

messagebox.showinfo("成功！", "视频已生成！")
time.sleep(1)

safe_delete(video_output_path)
safe_delete(audio_output_path)
safe_delete(nozoom_output_path)

print("已删除临时文件")

os._exit(0)
