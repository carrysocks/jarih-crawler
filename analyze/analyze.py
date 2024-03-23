import pandas as pd
import matplotlib.pyplot as plt
import os

root_path = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(root_path, "bus_mid_0617")

df = pd.read_csv(csv_file_path, parse_dates=['date_time'])

df['date_time'] = pd.to_datetime(df['date_time'])

# 9302, 잠실환승센터
target_route_id = 227000016
target_station_id = 123000611
target_date = pd.to_datetime('2023-06-09')

""" 하루당 시간대별 남은 좌석 """

filtered_df = df[(df['station_id'] == target_station_id)
                 & (df['route_id'] == target_route_id)
                 & (df['date_time'].dt.date == target_date.date())
                 & (df['plate_type'] == 3)
                 ]

filtered_df['time'] = filtered_df['date_time'].dt.time

avg_remaining_seats = filtered_df.groupby('time')['remaining_seats'].mean().reset_index()

avg_remaining_seats['time'] = pd.to_datetime(avg_remaining_seats['time'].astype(str))

plt.figure(figsize=(12, 6))
plt.plot(avg_remaining_seats['time'], avg_remaining_seats['remaining_seats'], marker='o')

plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))

plt.title(f'Remaining Seats on {target_date.date()} for route_id {target_route_id} and station_id {target_station_id}')
plt.xlabel('Time of Day')
plt.ylabel('Average Remaining Seats')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


""" 날짜별 평균 남은 좌석 """

df['date'] = df['date_time'].dt.date

# 필터링: 원하는 route_id와 station_id를 만족하는 데이터만 남깁니다.
filtered_df = df[(df['route_id'] == target_route_id)
               & (df['station_id'] == target_station_id)
               & (df['plate_type'] == 3)
                ]

# 날짜별로 그룹화하고 평균 남은 좌석 수를 계산합니다.
daily_avg_seats = filtered_df.groupby('date')['remaining_seats'].mean().reset_index()

# 그래프를 그립니다.
plt.figure(figsize=(12, 6))
plt.plot(daily_avg_seats['date'], daily_avg_seats['remaining_seats'], marker='o', linestyle='-')

plt.title(f'Daily Average Remaining Seats for route_id {target_route_id} and station_id {target_station_id}')
plt.xlabel('Date')
plt.ylabel('Average Remaining Seats')
plt.xticks(rotation=45)  # 날짜 레이블을 45도 회전하여 표시
plt.grid(True)  # 격자 표시
plt.tight_layout()  # 레이아웃 조정 및 그래프가 잘리지 않도록 함
plt.show()