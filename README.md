# Simple_IR

Python을 활용한 간단한 정보검색 엔진입니다. 문서를 읽어 TF-IDF weight dictionary로 만들고, Querystring으로 들어온 데이터와의 유사도를 측정 후 상위 10개의 값을 출력합니다.

### 1. 프로젝트의 사용법은 다음과 같습니다.

```python
1. git clone
2. pip을 통해 konlpy를 다운받습니다. (pip install konlpy)
3. python을 통해 search.py를 실행시킵니다. (python3 search.py)
4. 검색할 QueryString을 작성합니다. (예시 : 독일 작곡가)
```

### 2. 예시 입/출력은 다음과 같습니다.

```python
Preprocessing Documents.. please wait...
Document Preprocessing finished!
Please input query : 독일 작곡가
input Query : ['독일', '작곡가']
49. 니콜로 파가니니
유사도 : 24%
83. 루트비히 베토벤
유사도 : 23%
54. 안톤 브루크너
유사도 : 21%
88. 게오르크 헨델
유사도 : 19%
14. 만프레트 아이겐
유사도 : 15%
7. 막스 플랑크
유사도 : 13%
3. 백남준 
유사도 : 12%
46. 안토니우 조빙
유사도 : 12%
94. 고틀로프 프레게
유사도 : 11%
61. 함부르크
유사도 : 11%
```

### 3. 파일 구조는 다음과 같습니다.

```python
1. document.txt : 예시로 만들어 둔 문서의 예시입니다.
<title></title> 사이에 문서 제목이 들어가고, 다음 줄에 한 줄로 문서 내용이 들어옵니다.

2. search.py : TF-IDF 기반의 간단한 검색 시스템 코드입니다.
구조 단순화를 위해 전처리와 검색을 동시에 진행하였지만, 실제 운영을 위해서는 전처리기를
분리해야 합니다.
```

### 4. 다음은 프로그램 작동 방식에 대한 간단한 설명입니다. [Search.py](http://Search.py) 내 주석에 더 자세한 내용이 적혀있으나, 읽기 편하도록 짧게 요약하였습니다.

```python
1. Document 파일을 읽어 데이터를 로드합니다.
2. 정규 표현식을 통해 한글과 숫자 이외의 문자를 제거합니다.
(예시 간단화를 위해, 숫자와 한글 데이터만을 처리하기로 하였습니다.)
3. konlpy의 tagger를 이용하여 각 단어를 tagging합니다.
4. 이후 조사를 제거합니다.
그가,그를,그에게,그와 같은 단어를 '그'라는 단어로 축소하기 위해 조사를 제거하였습니다.
5. 전처리가 끝난 단어를 통해 Inverted Index를 만듭니다.
6. TF-IDF Weight Dictionary를 계산하여 만듭니다.
7. 이후 각 Document별로 Length를 계산하여 Document Vector를 L2 Norm으로 Normalize합니다.
이는 코사인 유사도 계산 시 수식을 단순화하고, QueryString 입력 시 연산량을 줄이기 위함입니다.
--- 전처리 끝 ---

8. 이후 사용자에게 검색할 QueryString을 입력받습니다.
9. 해당 QueryString에서 전처리와 동일하게 한글,숫자 이외의 문자 제거, 조사 제거 등을 수행합니다.
10. 전처리가 끝났다면, QueryString을 하나의 Document로 볼 수 있습니다.
기존의 각 Document와 QueryString의 코사인 유사도를 구하여, 가장 유사한 Document를 찾습니다.
11. 이후 가장 유사한 Document를 출력합니다.
```
