# Copyright 2023-2025 Jeongmin Kang, jarvisNim @ GitHub
# See LICENSE for details.


from datetime import datetime, timedelta
from pytz import timezone

from . import constant as cst


def find_Ndays_ago(to_date, n):
    # 'America/New_York' 타임존으로 설정
    ny_tz = timezone('America/New_York')
    # 현재 시간을 얻어옴
    now = datetime.now(ny_tz)  # 훗날 now 가 아닌 to_date 날짜로 적용하도록 개선이 필요함. 오늘은 아님, 20241105
    # 30일 전의 날짜를 계산
    nday_ago = now - timedelta(days=n)
    # day30_ago를 'UTC' 타임존으로 변환
    nday_ago_utc = nday_ago.astimezone(timezone('UTC'))
    
    return nday_ago_utc