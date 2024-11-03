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
            else:
                print(f"Phiên bản hiện tại: {current_version}.")
                run_mrjpacking()
        else:
            print("Không thể kiểm tra phiên bản mới.")
            run_mrjpacking()
    except Exception as e:
        print("Lỗi cập nhật:", e)
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
        mrj_main.main()  # Gọi hàm chạy chính của mrjpacking
    except ImportError:
        install_package_if_missing("mrjpacking")
        mrj_main.main()

def main():
    install_package_if_missing("mrjpacking")
    check_for_updates()

if __name__ == "__main__":
    main()

# import os
# import subprocess
# from get_workflow import run_workflow, get_latest_workflow_run  # Nhập module mới tạo
# import mrjpacking  # Giả định rằng đây là module đã được cài đặt

# def check_for_updates():
#     latest_run = get_latest_workflow_run()
#     if latest_run:
#         latest_id = latest_run['id']
#         # Lấy ID của bản build hiện tại (có thể cần cách lấy ID bản build của bạn)
#         current_id = get_current_workflow_run_id()  # Hàm này cần được tạo để lấy ID của bản hiện tại

#         if latest_id != current_id:
#             response = input("Có phiên bản mới. Bạn có muốn cập nhật không? (y/n): ").strip().lower()
#             if response == 'y':
#                 download_and_install_new_version(latest_run)
#             elif response == 'n':
#                 print("Bỏ qua cập nhật. Chạy chương trình...")
#         else:
#             print("Bạn đã có phiên bản mới nhất.")
#     else:
#         print("Không tìm thấy workflow run mới nhất.")

# def get_current_workflow_run_id():
#     # Cần implement hàm này để lấy ID của workflow run hiện tại
#     return "ID_CỦA_BẢN_HIỆN_TẠI"  # Thay thế bằng cách lấy ID thực tế

# def download_and_install_new_version(latest_run):
#     print(f"Tải xuống phiên bản mới nhất với ID: {latest_run['id']}")
#     artifacts = get_artifacts(latest_run['id'])
#     if artifacts:
#         for artifact in artifacts:
#             if artifact['name'] == 'encrypted_mrjpacking':
#                 download_artifact(artifact)
#                 print("Cài đặt phiên bản mới...")
#                 # Cần thực hiện cài đặt module mới, có thể dùng pip hoặc setup.py
#                 subprocess.run(["pip", "install", "--upgrade", "encrypted_mrjpacking.zip"])
#                 print("Cài đặt hoàn tất.")
#                 break
#     else:
#         print("Không tìm thấy artifacts.")

# def main():
#     run_workflow()
#     # check_for_updates()  # Kiểm tra bản cập nhật khi khởi động
#     # mrjpacking.main()  # Thay đổi nếu cần thiết để chạy đúng

# if __name__ == "__main__":
#     main()
