class VideoFunction:
    @staticmethod
    def mp4_to_avi():
        return ['-c:v', 'mpeg4']

    @staticmethod
    def mp4_to_webm():
        return ['-c:v', 'libvpx', '-b:v', '1M', '-c:a', 'libvorbis']

    @staticmethod
    def mp4_to_mov():
        return ['-c:v', 'libx264', '-c:a', 'aac']

    @staticmethod
    def avi_to_mp4():
        return ['-c:v', 'libx264', '-c:a', 'aac']

    @staticmethod
    def webm_to_mp4():
        return ['-c:v', 'libx264', '-c:a', 'aac']

    @staticmethod
    def mov_to_mp4():
        return ['-c:v', 'libx264', '-c:a', 'aac']
