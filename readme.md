# DOGDOGDOGDOGDOGDOGDOGDOGDOG

## 개인 맞춤형 구독 서비스

- 블로그, 공지사항, 커뮤니티 등 다양한 웹 문서를 구독하고, 개인화된 맞춤 추천을 받아보세요...


## 주요 기능

- **웹 문서 구독**: 사용자 관심사에 맞는 다양한 웹 문서를 구독하세요.
- **개인화된 추천**: 최신 AI 모델을 활용해 사용자 맞춤 콘텐츠를 추천합니다.
- **다양한 웹 문서 지원**: 블로그, 공지사항, 커뮤니티 게시글 등 다양한 웹 문서를 지원합니다.

## 설치 방법

이 프로젝트를 사용하기 위해서는 다음 의존성이 필요합니다.

### Dependencies

- Python >= 3.11
- FastAPI >= 0.65.2
- MariaDB >= 16
- OLlama >= 0.1.29
- BeautifulSoup4 >= 4.9.3

### 데이터베이스 설정

PostgreSQL을 설치하고, 다음의 SQL 명령어를 사용하여 필요한 데이터베이스와 사용자를 생성합니다.

```sql
CREATE DATABASE dogdogdb;
CREATE USER doguser WITH ENCRYPTED PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE dogdogdb TO doguser;
```
