import os
import subprocess

if __name__ == "__main__":
    # 定義 crawler 目錄的路徑
    crawler_dir = './crawler'

    # 遍歷 crawler 目錄中的所有檔案
    for filename in os.listdir(crawler_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(crawler_dir, filename)
            print(f"正在執行 {file_path}")
            # 使用 subprocess 執行每個 Python 檔案
            subprocess.run(['python', file_path], check=True)