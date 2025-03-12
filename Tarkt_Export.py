#Tarkt export
#This script will export the tmdb database to a trakt csv file
import requests
import csv
import sys
from datetime import datetime
from tqdm import tqdm  # 引入 tqdm 用于显示进度条

# 获取 TMDb API 密钥并验证连接
def get_tmdb_api_key():
    while True:
        api_key = input("请输入 TMDb API 密钥：")
        try:
            # 测试 API 密钥是否有效
            url = f'https://api.themoviedb.org/3/configuration?api_key={api_key}'
            response = requests.get(url)

            if response.status_code == 200:
                print("TMDb API 连接成功！")
                return api_key
            else:
                print(f"无法连接到 TMDb API，HTTP 状态码：{response.status_code}。请检查 API 密钥或网络连接。")
        except requests.exceptions.RequestException as e:
            print(f"请求异常：{e}。请检查网络连接和 API 密钥。")
        
        # 如果连接失败，要求用户重新输入
        input("按 Enter 键重新输入 API 密钥...")

# 获取 TMDb 列表并验证
def get_tmdb_list(list_id, api_key):
    movies = []
    page = 1

    while True:
        try:
            url = f'https://api.themoviedb.org/3/list/{list_id}?api_key={api_key}&language=en-US&page={page}'
            response = requests.get(url)

            # 检查 HTTP 请求是否成功
            if response.status_code != 200:
                print(f"错误：无法获取列表数据，HTTP 状态码 {response.status_code}")
                return []
            
            data = response.json()

            # 如果返回的数据没有 items 列表，则可能是列表 ID 错误
            if 'items' not in data:
                print("错误：无法找到电影列表，请检查列表 ID 是否正确，或列表是否为公开可见。")
                return []
            
            movies.extend(data['items'])  # 添加当前页面的电影到总列表

            # 如果没有更多页面，跳出循环
            if page >= data['total_pages']:
                break

            # 增加页面号，继续请求下一页
            page += 1

        except requests.exceptions.RequestException as e:
            print(f"请求异常：{e}")
            return []

    return movies  # 返回所有电影数据

# 获取 IMDb ID 或 TMDb ID
def get_movie_id(movie_id, api_key, use_imdb):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
        response = requests.get(url)

        if response.status_code != 200:
            print(f"错误：无法获取电影信息，HTTP 状态码 {response.status_code}")
            return ''
        
        movie_data = response.json()
        if use_imdb:
            return movie_data.get('imdb_id', '')
        else:
            return movie_data.get('id', '')  # 返回 TMDb ID

    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")
        return ''

# 将电影信息导出为 Trakt 格式的 CSV 文件
def export_to_csv(movies, api_key, use_imdb):
    try:
        file_path = 'trakt_import.csv'  # 默认文件路径

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'watched_at', 'watchlisted_at', 'rating', 'rated_at'])  # CSV 文件头

            # 使用 tqdm 显示进度条，遍历所有电影
            for movie in tqdm(movies, desc="导出中", unit="部电影"):
                # 获取选择的 ID
                movie_id = get_movie_id(movie['id'], api_key, use_imdb)
                if not movie_id:
                    print(f"电影 {movie['title']} 没有找到有效的 ID，跳过。")
                    continue

                # 设置时间格式
                watched_at = ''  # 省略
                watchlisted_at = ''  # 仅标记为 watched，省略
                rating = ''  # 省略
                rated_at = ''  # 省略

                # 写入 CSV 文件
                writer.writerow([movie_id, watched_at, watchlisted_at, rating, rated_at])

        print(f"CSV 文件已成功导出到 {file_path}")

    except Exception as e:
        print(f"导出 CSV 时发生错误：{e}")

# 主程序
def main():
    print("欢迎使用 TMDb 到 Trakt 导入工具！")

    # 获取 TMDb API 密钥并验证连接
    api_key = get_tmdb_api_key()

    # 让用户选择使用 imdb_id 还是 tmdb_id
    use_imdb = input("您希望导出的 ID 是 imdb_id 还是 tmdb_id？请输入 'imdb' 或 'tmdb'：").strip().lower() == 'imdb'

    while True:
        list_id = input("请输入公开可见的 TMDb 列表 ID：")
        # 提示用户检查列表是否为公开可见
        print("请确保该列表为公开可见，否则无法获取数据。")
        check_list = input("您已确认该列表为公开可见吗？(y/n)：").strip().lower()
        if check_list != 'y':
            print("请确保列表设置为公开可见后再继续。")
            continue

        # 获取电影列表数据
        print("正在查找列表数据...")
        movies = get_tmdb_list(list_id, api_key)
        if movies:
            print(f"共找到 {len(movies)} 部电影。")
            break  # 如果成功获取数据，跳出循环

    if movies:
        print(f"开始导出 Trakt 格式的 CSV 文件...")
        export_to_csv(movies, api_key, use_imdb)

    print("任务完成！按 Enter 键退出...")
    input()

if __name__ == '__main__':
    main()