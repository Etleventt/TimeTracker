from flask import Flask, render_template, request, jsonify
import time
import json
from datetime import datetime
import csv

app = Flask(__name__)

# 存储活动记录
activity_log = []

# 定义CSV文件路径
csv_file_path = 'activity_log.csv'

# 初始化CSV文件，添加表头
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['活动名称', '活动时间(秒)', '开始时间', '结束时间', '日期'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_activity', methods=['POST'])
def log_activity():
    data = request.json
    data['start_time'] = time.time() - data['duration']  # 计算开始时间
    data['end_time'] = time.time()  # 记录结束时间
    data['date'] = datetime.now().strftime('%Y-%m-%d')  # 添加日期信息
    activity_log.append(data)
    
    # 将数据写入CSV文件
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([data['activity'], data['duration'], data['start_time'], data['end_time'], data['date']])

    return jsonify(success=True)

@app.route('/get_activity_log')
def get_activity_log():
    date = request.args.get('date')
    filtered_log = []
    
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, fieldnames=['活动名称', '活动时间(秒)', '开始时间', '结束时间', '日期'])
        next(reader)  # 跳过表头行
        for row in reader:
            if not date or row['日期'] == date:
                filtered_log.append({
                    'activity': row['活动名称'],
                    'duration': float(row['活动时间(秒)']),
                    'start_time': float(row['开始时间']),
                    'end_time': float(row['结束时间']),
                    'date': row['日期']
                })
    return jsonify(filtered_log)

if __name__ == '__main__':
    app.run(debug=True)