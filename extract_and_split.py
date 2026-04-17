import os
import json
import subprocess
import re
import sys
import argparse
def sanitize_filename(filename):
    """파일명으로 사용할 수 없는 특수문자 제거"""
    return re.sub(r'[\\/*?:"<>|]', "", filename)
def time_to_seconds(t_str):
    """'1:20', '01:20:30' 등의 형식을 초 단위(float)로 변환"""
    try:
        parts = t_str.strip().split(':')
        if len(parts) == 1:
            return float(parts[0])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    except Exception:
        return None
    return None
def run_command(cmd):
    """외부 명령어 실행"""
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False
    return True
def download_audio(url, output_temp):
    """유튜브에서 전체 오디오를 임시로 다운로드"""
    print(f"Downloading audio from: {url}")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-check-certificate",
        "-x", "--audio-format", "mp3",
        "-o", output_temp,
        url
    ]
    return run_command(cmd)
def get_metadata(url):
    """유튜브 메타데이터(챕터 등) 가져오기"""
    cmd = [
        sys.executable, "-m", "yt_dlp", 
        "--no-check-certificate", 
        "-j", url
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Failed to get metadata: {e}")
        return None
def extract_section(input_file, start_time, end_time, output_name):
    """ffmpeg를 사용하여 특정 구간 추출"""
    duration = end_time - start_time
    if duration <= 0:
        print(f"Invalid duration: {duration}s")
        return False
    print(f"  Extracting: {output_name} ({start_time}s to {end_time}s)")
    cmd = [
        'ffmpeg', '-y',
        '-ss', str(start_time),
        '-t', str(duration),
        '-i', input_file,
        '-c', 'copy',
        output_name
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True
def main():
    parser = argparse.ArgumentParser(description="YouTube Audio Extractor & Splitter")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--range", help="Extract specific range (e.g. '1:20~2:24' or '00:30~01:45')")
    args = parser.parse_args()
    url = args.url
    audio_temp = "full_audio_temp.mp3"
    # 1. 오디오 다운로드
    if not download_audio(url, "full_audio_temp.%(ext)s"):
        return
    # 2. 추출 로직 선택
    if args.range:
        # 특정 구간 추출 모드
        try:
            start_str, end_str = args.range.replace(' ', '').split('~')
            start_sec = time_to_seconds(start_str)
            end_sec = time_to_seconds(end_str)
            if start_sec is None or end_sec is None:
                print("Invalid range format. Use 'MM:SS~MM:SS'")
            else:
                output_name = f"manual_clip_{start_str.replace(':','.')}_{end_str.replace(':','.')}.mp3"
                extract_section(audio_temp, start_sec, end_sec, output_name)
        except ValueError:
            print("Range must be in 'start~end' format (e.g., 1:20~2:24)")
    else:
        # 챕터 자동 분할 모드
        data = get_metadata(url)
        if not data: return
        chapters = data.get('chapters', [])
        if not chapters:
            print("No chapters found. Saved full audio as 'full_audio_temp.mp3'. Rename it if you want to keep it.")
            return
        print(f"Splitting into {len(chapters)} files based on chapters...")
        skip_keywords = ["playlist", "worship piano", "intro", "반복", "loop", "outro", "메들리", "repeat"]
        for i, chapter in enumerate(chapters, 1):
            title = chapter.get('title', f"Chapter_{i}")
            if any(key in title.lower() for key in skip_keywords):
                print(f"  Skipping: {title}")
                continue
            start = chapter['start_time']
            end = chapter['end_time']
            safe_title = sanitize_filename(title)
            output_name = f"{i:02d} - {safe_title}.mp3"
            extract_section(audio_temp, start, end, output_name)
    # 3. 정리
    if os.path.exists(audio_temp):
        os.remove(audio_temp)
    print("\nProcess finished successfully.")
if __name__ == "__main__":
    main()





