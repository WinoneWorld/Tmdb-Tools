#Letterboxd export
#This script will export the tmdb database to a Letterboxd csv file
import os
import requests
import csv
import time
from pathlib import Path
from tqdm import tqdm  # 进度条库

# 获取 TMDb API 配置
TMDB_API_URL = "https://api.themoviedb.org/3"

# 获取 TMDb 上公开列表的所有条目
def get_list_items_from_tmdb(list_id, api_key):
    url = f"{TMDB_API_URL}/list/{list_id}?api_key={api_key}&language=en-US"
    
    items = []
    page = 1
    
    while True:
        response = requests.get(f"{url}&page={page}")
        if response.status_code == 200:
            data = response.json()
            results = data.get("items", [])
            
            if not results:
                break  # 如果没有更多数据，跳出循环
            
            for item in results:
                items.append(item)  # 获取所有条目（电影、电视节目等）
            
            page += 1
        else:
            print(f"错误：无法获取列表数据。HTTP 状态码：{response.status_code}")
            return None
    
    return items

# 获取条目（电影或电视节目）的详细信息
def get_item_info_from_tmdb(item_id, api_key, media_type="movie"):
    url = f"{TMDB_API_URL}/{media_type}/{item_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"错误：无法获取条目数据（ID: {item_id}，类型: {media_type}）。HTTP 状态码：{response.status_code}")
        return None

# 获取 IMDB ID（通过 TMDb ID）
def get_imdb_id(item_id, api_key, media_type="movie"):
    url = f"{TMDB_API_URL}/{media_type}/{item_id}/external_ids?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("imdb_id", None)
    else:
        print(f"错误：无法获取 IMDb ID（ID: {item_id}，类型: {media_type}）。HTTP 状态码：{response.status_code}")
        return None

# 导出到 Letterboxd 格式的 CSV
def export_to_letterboxd(items, api_key, output_file):
    # 打开 CSV 文件并写入数据
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # 写入表头
        writer.writerow(["LetterboxdURI", "tmdbID", "imdbID", "Title", "Year", "Directors", "Rating", "WatchedDate", "Rewatch", "Tags", "Review"])
        
        # 使用进度条显示导出进度
        for item in tqdm(items, desc="导出进度", unit="条目"):
            media_type = item.get("media_type", "movie")
            item_id = item.get("id")
            item_info = get_item_info_from_tmdb(item_id, api_key, media_type)
            if not item_info:
                continue  # 如果没有获取到数据，跳过该条
            
            title = item_info.get("title") or item_info.get("name", "")
            year = item_info.get("release_date", item_info.get("first_air_date", "")).split("-")[0]  # 获取年份
            directors = ", ".join([director["name"] for director in item_info.get("credits", {}).get("crew", []) if director["job"] == "Director"])
            imdb_id = get_imdb_id(item_id, api_key, media_type)
            rating = item_info.get("vote_average", 0) / 2  # 将 10 分制转换为 5 分制
            watched_date = time.strftime("%Y-%m-%d", time.gmtime(item_info.get("release_date", time.time())))  # 使用电影发布日期为观看日期
            rewatch = "false"  # 默认没有重看标志
            tags = ""  # 默认没有标签
            review = ""  # 默认没有评论

            # 写入每个条目的行数据
            writer.writerow([f"https://letterboxd.com/film/{item_id}", item_id, imdb_id, title, year, directors, rating, watched_date, rewatch, tags, review])
    
    print(f"数据成功导出到 {output_file}")

# 主程序
def main():
    print("欢迎使用 TMDb 到 Letterboxd 导出工具！")

    # 获取 TMDb API 密钥
    api_key = input("请输入 TMDb API 密钥：")
    
    while True:
        # 获取列表 ID
        list_id = input("请输入公开可见的 TMDb 列表 ID：")
        
        # 提示用户检查列表是否为公开可见
        print("请确保该列表为公开可见，否则无法获取数据。")
        check_list = input("您已确认该列表为公开可见吗？(y/n)：").strip().lower()
        
        if check_list != 'y':
            print("请确保列表设置为公开可见后再继续。")
            continue
        
        # 获取条目数据
        print("正在查找列表数据...")
        items = get_list_items_from_tmdb(list_id, api_key)
        if items:
            print(f"共找到 {len(items)} 个条目。")
            break  # 如果成功获取数据，跳出循环
        else:
            print("无法获取数据，请检查 TMDb 列表 ID 或 API 密钥。")

    # 获取脚本所在路径并指定输出文件
    script_path = Path(__file__).parent
    output_file = script_path / "Letterboxd_export.csv"

    # 导出为 Letterboxd 格式的 CSV
    try:
        print("开始导出 Letterboxd 格式的 CSV 文件...")
        export_to_letterboxd(items, api_key, output_file)
    except Exception as e:
        print(f"导出过程中发生错误：{e}")
        input("发生错误，按 Enter 键退出...")

    input(f"任务完成！按 Enter 键退出... 输出文件：{output_file}")

if __name__ == "__main__":
    main()