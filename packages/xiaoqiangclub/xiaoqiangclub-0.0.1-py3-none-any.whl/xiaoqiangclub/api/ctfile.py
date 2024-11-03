import asyncio
import csv
import hashlib
from typing import List, Dict, Optional
import httpx

# API URL 相关
BASE_URL = "https://api.ctfile.com/v1/"
GET_USER_INFO_ENDPOINT = "users/get_user_info"
GET_PUBLIC_FILES_LIST_ENDPOINT = "files/get_public_file_list"
GET_SHARE_LINK_ENDPOINT = "shares/get_file_share_info"
GET_SHORT_TIME_TOKEN_ENDPOINT = "tokens/get_short_time_token"

# CSV 输出模板
answer_template = {
    "问题": "获取城通网盘文件链接",
    "相似问题": "获取文件下载地址、文件分享链接",
    "回答": ""
}


class CtWPApi:
    def __init__(self, token: str):
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    async def get_short_time_token(self) -> Optional[str]:
        """ 获取有效期3天的临时 Token """
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL + GET_SHORT_TIME_TOKEN_ENDPOINT, headers=self.headers)
            if response.status_code == 200:
                return response.json().get("data", {}).get("token")
            return None

    async def get_user_info(self) -> Dict:
        """ 获取用户的基本信息 """
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL + GET_USER_INFO_ENDPOINT, headers=self.headers)
            if response.status_code == 200:
                return response.json().get("data", {})
            return {}

    async def get_public_files_list(self, folder_id: int = 0) -> List[Dict]:
        """ 列出文件夹下的文件信息 """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}{GET_PUBLIC_FILES_LIST_ENDPOINT}?folder_id={folder_id}", headers=self.headers
            )
            if response.status_code == 200:
                return response.json().get("data", {}).get("files", [])
            return []

    async def get_all_files_of_folder(self, folder_id: int = 0) -> List[Dict]:
        """ 递归地获取文件夹中的所有文件 """
        all_files = []
        files = await self.get_public_files_list(folder_id)
        for file_info in files:
            if file_info["type"] == "folder":
                sub_files = await self.get_all_files_of_folder(file_info["id"])
                all_files.extend(sub_files)
            else:
                all_files.append(file_info)
        return all_files

    async def get_share_link(self, file_id: int) -> str:
        """ 获取指定文件/文件夹的分享链接 """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}{GET_SHARE_LINK_ENDPOINT}?file_id={file_id}", headers=self.headers
            )
            if response.status_code == 200:
                return response.json().get("data", {}).get("share_url", "")
            return ""

    async def upload_file(self, file_path: str, folder_id: int = 0) -> Dict:
        """ 上传文件到城通网盘指定目录 """
        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as file:
                files = {'file': file}
                response = await client.post(
                    f"{BASE_URL}files/upload?folder_id={folder_id}",
                    headers=self.headers,
                    files=files
                )
            if response.status_code == 200:
                return response.json().get("data", {})
            return {}

    @staticmethod
    def calculate_checksum(file_path: str) -> str:
        """ 计算文件的 MD5 校验和 """
        md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()


async def get_ctwp_all_share_links(token: str) -> List[Dict[str, str]]:
    """ 获取指定 Token 下所有文件的分享链接 """
    ctwp_api = CtWPApi(token)
    all_files = await ctwp_api.get_all_files_of_folder()
    share_links = []
    for file_info in all_files:
        share_url = await ctwp_api.get_share_link(file_info["id"])
        share_links.append({"file_name": file_info["name"], "share_url": share_url})
    return share_links


async def get_all_data(token_list: List[str], save_to_csv_file: bool = False) -> List[Dict[str, str]]:
    """ 异步获取所有账户的数据并保存为 CSV 文件 """
    all_data = []
    tasks = [get_ctwp_all_share_links(token) for token in token_list]
    results = await asyncio.gather(*tasks)

    for result in results:
        all_data.extend(result)

    if save_to_csv_file:
        save_to_csv(all_data)
    return all_data


def save_to_csv(data: List[Dict[str, str]], filename: str = "ctwp_share_links.csv") -> None:
    """ 保存数据为 CSV 文件，格式适配微信对话平台 """
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=answer_template.keys())
        writer.writeheader()
        for row in data:
            answer = f"文件名：{row['file_name']}\n分享链接：{row['share_url']}"
            writer.writerow({**answer_template, "回答": answer})


# 示例执行
async def main():
    token_2270770463 = '56d20ce7b9094599c536d4e936674269'  # 2270770463@qq.com
    # token_464625642 = '430905def0be1cb63dbd1afdb9f21bfe'  # 464625642@qq.com
    # 账户 Token 列表（请替换为实际的 Token）
    ctwp = CtWPApi(token_2270770463)
    await ctwp.upload_file(r'D:\001_MyArea\SystemDirs\Downloads\test002\test\1.1MB_file.txt', 30252727)



if __name__ == '__main__':

    # # test = CtWPApi()z
    # # test.getAllPublicFilesShareLinks(token_2270770463)  # 464625642@qq.com
    # # test.getAllPublicFilesShareLinks(token_464625642)  # 2270770463@qq.com
    # tokens = [token_2270770463, token_464625642]
    # # 测试获取数据
    # # asyncio.xiaoqiangwol(get_all_data(tokens, True, save_to_csv_file=True))
    # # 测试向数据库插入数据
    # asyncio.run(
    #     manage_ctwp_data(tokens, db_path=r'D:\001_MyArea\002_MyCode\001_PythonProjects\my_fastapi\data\ctwp.sqlite3'))
    # # 测试结果搜索
    # print(asyncio.run(search_answers_from_ctwp(keyword='XHSD',
    #                                            db_path=r'D:\001_MyArea\002_MyCode\001_PythonProjects\my_fastapi\data\ctwp.sqlite3')))
    asyncio.run(main())
