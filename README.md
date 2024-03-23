
# 버스 데이터 수집 시스템

## 개요

버스 데이터 수집 시스템은 공공 교통 API에서 버스 위치 및 좌석 예약 가능 여부와 같은 실시간 데이터를 수집하고 이 시계열 데이터를 TimescaleDB에 저장하여 분석할 수 있게 설계된 시스템입니다. 이 시스템은 AWS EC2와 같은 클라우드 서비스에서의 배포를 최적화하여 지속적인 운영에 있어서의 확장성과 신뢰성을 보장합니다.

![버스 데이터 수집 시스템 개요](sandbox:/mnt/data/Create_an_image_that_visually_represents_a_bus_dat.png)

## 기능

- **실시간 데이터 수집**: 버스 위치, 좌석 예약 가능 여부 등의 생생한 정보를 수집합니다.
- **효율적인 데이터 저장**: 시계열 데이터에 최적화된 TimescaleDB를 사용하여 데이터를 저장합니다.
- **분석 준비**: 데이터 분석을 용이하게 하기 위해 구조화된 데이터 저장을 지원합니다.

## 시작하기

이 지침을 따라 개발 및 테스트 목적으로 로컬 머신에서 프로젝트를 실행할 수 있습니다.

### 필수 조건

- Python 3.6 이상
- pip 및 virtualenv
- PostgreSQL 및 TimescaleDB 확장
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
source venv/bin/activate  # Windows에서는 `venv\Scriptsctivate` 사용
```

3. **의존성 설치**

```bash
pip install -r requirements.txt
```

4. **환경 변수 설정**

`.env.example`을 `.env`로 복사하고 데이터베이스 연결 세부 정보 및 API 키를 입력하세요.

```bash
cp .env.example .env
```

5. **데이터베이스 초기화**

TimescaleDB에서 필요한 테이블 및 하이퍼테이블을 생성하는 스크립트를 실행합니다.

```bash
python init_db.py
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
