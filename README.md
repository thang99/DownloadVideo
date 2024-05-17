
# Phần mềm Download Video từ Youtube



+ Người dùng có thể tìm kiếm video và tải về
+ Người dùng có thể nhập URL để tải về
## Cách cài đặt:

1. clone repository

```bash
  git clone https://github.com/thang99/DownloadVideo.git
```
2. Navigate to the project directory:
```bash
  cd DownloadVideo
```
3. Create a virtual environment
```bash
  python3 -m venv env
```
4. Activate the virtual environment:
```bash
  env\Scripts\activate
```
5. Install required dependencies:
```bash
  pip install pytube
```
```bash
  pip install moviepy
```
```bash
  pip install pygame
```
```bash
  pip install google-api-python-client
```
6. run the application
```bash
  python download.py
```