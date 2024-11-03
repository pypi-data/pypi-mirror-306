# import requests
# import os
# import zipfile
# import importlib

# GITHUB_TOKEN = "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"
# GITHUB_API_URL = "https://api.github.com/repos/JustinNguyen9979/mrjpacking"

# def get_latest_workflow_run():
#     headers = {"Authorization": f"token {GITHUB_TOKEN}"}
#     response = requests.get(f"{GITHUB_API_URL}/actions/runs", headers=headers)
#     if response.status_code == 200:
#         return response.json()["workflow_runs"][0]  # Lấy run mới nhất
#     return None

# def get_artifacts(run_id):
#     headers = {"Authorization": f"token {GITHUB_TOKEN}"}
#     response = requests.get(f"{GITHUB_API_URL}/actions/runs/{run_id}/artifacts", headers=headers)
#     if response.status_code == 200:
#         return response.json()["artifacts"]
#     return None

# def download_artifact(artifact):
#     download_url = artifact["archive_download_url"]
#     headers = {
#         "Authorization": f"token {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json"  # Đảm bảo sử dụng đúng loại dữ liệu
#     }
    
#     response = requests.get(download_url, headers=headers)
#     if response.status_code == 200:
#         with open(f"{artifact['name']}.zip", "wb") as f:
#             f.write(response.content)
#         # print(f"Tải xuống thành công {artifact['name']}.zip")
#     else:
#         print("Có lỗi khi tải xuống artifact.")

# def run_workflow():
#     latest_run = get_latest_workflow_run()
#     if latest_run:
#         print(f"Workflow run mới nhất ID: {latest_run['id']}")
#         artifacts = get_artifacts(latest_run["id"])
#         if artifacts:
#             for artifact in artifacts:
#                 if artifact["name"] == "encrypted_mrjpacking":
#                     download_artifact(artifact)
#                     break

import requests
import os
import zipfile
import importlib
import sys
from glob import glob

GITHUB_TOKEN = "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"
GITHUB_API_URL = "https://api.github.com/repos/JustinNguyen9979/mrjpacking"
WORKFLOW_ID_FILE = "workflow_id.txt"  # File để lưu ID của lần tải về cuối cùng
ARTIFACT_NAME = "encrypted_mrjpacking"  # Tên artifact cần tải
EXTRACT_DIR = "encrypted_build"  # Thư mục giải nén

def get_latest_workflow_run():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(f"{GITHUB_API_URL}/actions/runs", headers=headers)
    if response.status_code == 200:
        return response.json()["workflow_runs"][0]  # Lấy run mới nhất
    return None

def load_last_run_id():
    if os.path.exists(WORKFLOW_ID_FILE):
        with open(WORKFLOW_ID_FILE, "r") as file:
            return file.read().strip()
    return None

def save_run_id(run_id):
    with open(WORKFLOW_ID_FILE, "w") as file:
        file.write(run_id)

def get_artifacts(run_id):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(f"{GITHUB_API_URL}/actions/runs/{run_id}/artifacts", headers=headers)
    if response.status_code == 200:
        return response.json()["artifacts"]
    return None

def download_artifact(artifact):
    download_url = artifact["archive_download_url"]
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(download_url, headers=headers)
    if response.status_code == 200:
        with open(f"{artifact['name']}.zip", "wb") as f:
            f.write(response.content)
    else:
        print("Có lỗi khi tải xuống artifact.")

def extract_artifact(artifact_name):
    zip_path = f"{artifact_name}.zip"
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
        print("Giải nén thành công.")
        os.remove(zip_path)  # Xóa file zip sau khi giải nén
    else:
        print("Không tìm thấy file zip để giải nén.")

def install_and_run_package():
    encrypted_path = os.path.abspath(EXTRACT_DIR)
    sys.path.insert(0, encrypted_path)

    try:
        # Xác định đường dẫn đến file .so có tên cụ thể
        so_file_path = os.path.join(encrypted_path, "main.cpython-312-x86_64-linux-gnu.so")
        
        # Kiểm tra nếu file tồn tại
        if not os.path.exists(so_file_path):
            print(f"Không tìm thấy file '{so_file_path}' trong thư mục encrypted_build.")
            return

        # Tạo spec và import module từ file .so
        spec = importlib.util.spec_from_file_location("mrjpacking", so_file_path)
        
        # Kiểm tra spec và loader
        if spec is None:
            print(f"Không thể tạo spec cho module từ '{so_file_path}'.")
            return
        
        if spec.loader is None:
            print(f"Loader cho spec là None. Không thể import module từ '{so_file_path}'.")
            return

        # Nếu spec và loader hợp lệ, thực hiện import
        mrjpacking = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mrjpacking)

        if hasattr(mrjpacking, "run"):
            mrjpacking.run()
        else:
            print("Không tìm thấy hàm 'run' trong module.")
    
    except Exception as e:
        print(f"Lỗi khi chạy module mã hóa: {e}")


def run_workflow():
    latest_run = get_latest_workflow_run()
    if not latest_run:
        print("Không thể lấy thông tin workflow run.")
        return

    last_run_id = load_last_run_id()
    latest_run_id = str(latest_run['id'])

    if latest_run_id == last_run_id:
        print("Workflow đã cập nhật với phiên bản mới nhất.")
        install_and_run_package()
        return

    # Cập nhật ID mới
    save_run_id(latest_run_id)
    print(f"Workflow mới nhất với ID: {latest_run_id}")

    # Tải artifact mới nhất nếu có
    artifacts = get_artifacts(latest_run_id)
    if artifacts:
        for artifact in artifacts:
            if artifact["name"] == ARTIFACT_NAME:
                download_artifact(artifact)
                extract_artifact(ARTIFACT_NAME)
                install_and_run_package()
                break
    else:
        print("Không tìm thấy artifact nào.")

if __name__ == "__main__":
    run_workflow()
