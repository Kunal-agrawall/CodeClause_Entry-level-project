import pyaudio
import wave
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class AudioRecorder:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder")
        self.master.geometry("300x200")

        self.is_recording = False

        self.record_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)

        self.save_button = tk.Button(master, text="Save Recording", command=self.save_recording)
        self.save_button.pack(pady=10)
        self.save_button.config(state=tk.DISABLED)

        self.frames = []

        self.p = pyaudio.PyAudio()

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=1024)
        self.record_audio()

    def record_audio(self):
        if self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)
            self.master.after(1, self.record_audio)

    def stop_recording(self):
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

    def save_recording(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if file_path:
            wf = wave.open(file_path, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            messagebox.showinfo("Audio Recorder", "Recording saved successfully!")

    def on_closing(self):
        if self.is_recording:
            self.stop_recording()
        self.p.terminate()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorder(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
