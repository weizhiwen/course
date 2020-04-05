# 导入requests库
import requests
# 导入beautifulsoup库
from bs4 import BeautifulSoup
# 导入openpyxl
from openpyxl import Workbook

# 1、获取数据
url_list = ['http://www.tianqihoubao.com/lishi/nanjing/month/2019{}.html'.format(str(i).zfill(2)) for i in range(1, 13)]
# 使用程序访问目标网站
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
excel_name = ""
data_dict = {}
for url in url_list:
	response = requests.get(url, headers=headers)
	# 将网站的HTML文件做成一碗汤
	bs = BeautifulSoup(response.text, 'lxml')
	# 缩小HTML内容范围
	content = bs.find(id="content")
	# 获取表格标题
	excel_name, title = content.h1.string.replace('\r', '').replace('\n', '').strip().split(' ')
	print("表格标题: {}".format(title))
	# 获取表格内容
	data_list = []
	tr_list = content.find_all('tr')
	for tr in tr_list:
		data_list.append([td.text.replace('\r', '').replace('\n', '').replace(' ', '') for td in tr.find_all('td')])
		# # 等价于下面的写法
		# for td in tr.find_all('td'):
		# 	row_data = []
		# 	data = td.text.replace('\r', '').replace('\n', '').replace(' ', '')
		# 	row_data.append(data)
	# 字典结构：{"2020年3月份": [[], []]}
	print('表格数据: {}'.format(data_list))
	data_dict[title] = data_list

# 2、保存数据
# 创建Excel工作薄对象
workbook = Workbook()
# 删除默认创建的Sheet工作表对象
worksheet = workbook.active
workbook.remove(worksheet)
for title, data_list in data_dict.items():
	# 创建自定义的Sheet工作表对象
	worksheet = workbook.create_sheet(title)
	for row_data in data_list:
		worksheet.append(row_data)
workbook.save('/tmp/{}.xlsx'.format(excel_name))
print('保存成功！')



