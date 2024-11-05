import importlib.metadata
import subprocess
import sys
import os
import requests
from packaging import version
from mrjpacking import main as mrj_main

def install_package_if_missing(package_name):
    try:
        # Kiểm tra xem package đã được cài chưa
        importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        # Nếu chưa cài đặt thì tiến hành cài đặt
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def check_for_updates(): #gốc
    try:
        # Lấy phiên bản hiện tại của mrjpacking
        current_version = importlib.metadata.version("mrjpacking")
        
        # Lấy thông tin phiên bản mới nhất từ PyPI
        response = requests.get("https://pypi.org/pypi/mrjpacking/json", timeout=5)
        if response.status_code == 200:
            latest_version = response.json()["info"]["version"]
            
            # So sánh phiên bản
            if version.parse(latest_version) > version.parse(current_version):
                print(f"\nĐã có phiên bản mới {latest_version}.")
                choice = input("Bạn có muốn cập nhật không? (y/n): ").strip().lower()
                if choice == "y":
                    update_package(latest_version)  # Gọi hàm và truyền latest_version
                else:
                    run_mrjpacking()
                    clear_screen()
            else:
                print(f"Phiên bản hiện tại: {current_version}.")
                clear_screen()
                run_mrjpacking()
        # else:
        #     print("Không thể kiểm tra phiên bản mới.")
        #     clear_screen()
        #     run_mrjpacking()
    except Exception as e:
        print("Lỗi cập nhật:", e)
        clear_screen()
        run_mrjpacking()

def update_package(latest_version):  # Thêm đối số latest_version
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", f"mrjpacking=={latest_version}"])  # Sử dụng f-string
        print(f"\nĐã cập nhật phiên bản {latest_version} thành công!")
        clear_screen()
        run_mrjpacking()
    except Exception as e:
        print("Có lỗi khi cập nhật phiên bản {latest_version}:", e)
        run_mrjpacking()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_mrjpacking():
    try:
        mrj_main.main()  
    except ImportError:
        install_package_if_missing("mrjpacking")
        mrj_main.main()

def main():
    install_package_if_missing("mrjpacking")
    check_for_updates()

if __name__ == "__main__":
    main()
