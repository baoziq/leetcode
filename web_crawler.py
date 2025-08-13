# 根据url获取题目名称和描述
import os
import requests
from bs4 import BeautifulSoup
import re

def fetch_problem_description(problem_url):
    url = problem_url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch the problem: {problem_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('title')
    description_meta = soup.find('meta', {'name': 'description'})

    if title_tag and description_meta:
        title = title_tag.get_text().strip()
        description = description_meta.get('content', '').strip()
        title = re.sub(r" - 力扣（LeetCode）", "", title)
        description = re.sub(r'^\d+\..*? - ', '', description)
        return {"title": title, "description": description}
    else:
        print("Problem description or title not found.")
        return None


# 2. 保存题目描述到 Markdown 文件
def save_to_md(problem_name, description, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    md_content = f"### {problem_name}\n\n"
    md_content += f"\n\n{description}\n\n"

    md_filename = os.path.join(output_dir, f"{problem_name}.md")
    with open(md_filename, 'w', encoding='utf-8') as file:
        file.write(md_content)
    print(f"Markdown file saved as {md_filename}")


def main(problem_url, output_dir):
    res = fetch_problem_description(problem_url)
    if res:
        problem_name = res["title"]
        description = res["description"]
        save_to_md(problem_name, description, output_dir)


if __name__ == '__main__':
    problem_url = input("Enter the problem URL: ")
    output_dir = "/Users/baozi/leetcode"  
    main(problem_url, output_dir)

