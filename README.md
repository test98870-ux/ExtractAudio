# YouTube Audio Extractor & Splitter (MakeClip Utility)
이 프로젝트는 유튜브 영상의 오디오를 추출하고, 자동 챕터 분할 또는 **사용자 지정 구간 추출**을 지원하는 도구입니다.
## 🚀 주요 기능
- 유튜브 URL에서 최고 음질 오디오 추출
- **자동 챕터 분할:** 영상의 챕터 정보를 분석하여 곡별로 자동 저장
- **수동 구간 추출:** 사용자가 지정한 특정 시간대(`--range`)만 추출 가능
- **스마트 필터링:** `intro`, `반복`, `loop`, `repeat` 등이 포함된 구간은 자동 제외
- 파일명 특수문자 제거 및 한글 인코딩 완벽 지원
## 🛠️ 사전 준비
1. **Python 3.10+**
2. **FFmpeg:** 설치 및 PATH 등록 필수
3. **yt-dlp:** `pip install yt-dlp`
## 📖 사용 방법
### 1. 챕터별 자동 분할 (전체 곡 저장)
```powershell
python extract_and_split.py "유튜브_URL"
```
### 2. 특정 구간만 수동 추출
```powershell
python extract_and_split.py "유튜브_URL" --range "시작시간~종료시간"
```
*   예시: `python extract_and_split.py "URL" --range "1:20~2:24"`
*   예시: `python extract_and_split.py "URL" --range "00:30~01:45:10"`
## 📂 작업 로그 (최근 작업 순)
### 2026-04-03 업데이트
- **신규 기능 추가:** 특정 구간 추출(`--range`) 기능 도입
- **코드 개선:** `argparse`를 통한 인자 처리 최적화 및 시간 파싱 로직 강화
- **작업 완료:** 3개 유튜브 영상의 오디오 추출 및 정밀 분할 작업 완료
