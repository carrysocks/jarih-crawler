
# 버스 데이터 수집 시스템

## 개요

버스 데이터 수집 크롤러는 경기 버스 정보 Open API와 버스, 정류장 정보를 활용해 시간, 버스 좌석, 도착 정류장 정보 같은 실시간 데이터를 수집하고 이 시계열 데이터를 TimescaleDB에 저장하여 분석할 수 있게 설계되었습니다. 

## 기능

- **실시간 데이터 수집**: 현재 시간, 현재 버스 및 노선 정보, 현재 정류장 정보, 남은 좌석, 버스 타입 등을 수집합니다.
- **효율적인 데이터 저장**: 시계열 데이터에 최적화된 TimescaleDB를 사용하여 데이터를 저장합니다.
- **학습 및 추론에 활용**: 수집한 데이터는 예측 모델 학습과 추론 서버로 전달됩니다.

## 시작하기

이 지침을 따라 개발 및 테스트 목적으로 크롤러를 실행할 수 있습니다.

### 필수 조건

- Python 3.6 이상
- pip 및 virtualenv
- TimescaleDB 설치
- AWS EC2 인스턴스 (선택사항, 배포용)

### 설치

1. **레포지토리 클론**

```bash
git clone https://github.com/carrysocks/jarih-crawler.git
cd jarih-crawler
```

2. **가상 환경 설정**

```bash
virtualenv venv
source venv/bin/activate 
```

3. **의존성 설치**

```bash
pip install -r requirements.txt
```

4. **환경 변수 설정**

`.env.example`을 `.env`로 변경하고 데이터베이스 연결 세부 정보를 입력하세요.

```bash
cp .env_example .env
```

5. **데이터베이스 초기화**

TimescaleDB에서 필요한 테이블 및 하이퍼테이블을 생성하는 스크립트를 실행합니다.

```bash
python initialize_database.py
```

### 사용법

크롤러를 시작하여 데이터 수집 및 저장을 시작합니다:

```bash
python main.py
```

## 데이터 분석

이 프로젝트에는 수집된 데이터를 검색하고 시각화하는 방법을 보여주는 샘플 분석 스크립트가 포함되어 있습니다.

### 예시 분석

- **일별 평균 남은 좌석**

```bash
python analysis/daily_avg_seats.py
```
