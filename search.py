import re
import math
from konlpy.tag import Okt

import pprint

# 중간중간 Print는 Debug 를 위한 코드들입니다.
# 중간 과정이 이해되지 않거나 궁금하다면, print 부분의 주석을 풀어 중간 과정을 볼 수 있습니다.


print("Preprocessing Documents.. please wait...")

# document.txt 파일을 읽어 먼저 분석합니다.
# document 파일은 크롤러가 수집한 인터넷의 Document Data 등으로 치환될 수 있습니다.
readFile = open("document.txt", 'r')

#파일 전체 Read
lines = readFile.readlines()

#Okt -> Twitter 기반의 한글 Tokenizer 
okt = Okt()

# 정규표현식 이용하여 한글 제외한 나머지 문자들을 전부 제거하기 위해, korean_preprocessor를 정의합니다.
# 예시를 간단하게 하기 위해, 한글과 숫자를 제외한 문자는 무시하도록 처리하였습니다.
korean_preprocessor = re.compile('[^ ㄱ-ㅣ가-힣0-9]+')

title_list = []
term_dict = {}


docNumber = -1;

#읽은 Document들을 한줄씩 처리합니다.
for line in lines:
    if(line.find("<title>") != -1):
        #만약, <title> 있다면 Document의 Title이므로, <title> </title> 태그 제거하고 title_list에 보관합니다.
        # document.txt 파일을 참고하시면 구조를 이해하는데 도움이 될 수 있습니다.
        temp = line.replace("<title>","")
        temp = temp.replace("</title>","")
        title_list.append(temp)
        docNumber = docNumber +1
    else:
        #korean_line : 한글을 제외한 나머지 문자 전부 제거한 한 줄입니다.
        korean_line = korean_preprocessor.sub('',line)
        
        #Document 처리할 때, 만약 korean_line이 빈 문자열이라면 에러가 생기므로 빈 문자열이 아닌 경우만 처리해 줍니다.
        if(korean_line != "" or korean_line != ' '):
            #print(korean_line)
            
            #외부 Tokenizer 이용하여 각 문장을 분석합니다.
            word_list = okt.pos(korean_line)
            #print(word_list)
            
            # 이후, 품사가 조사인 것을 제거한 리스트를 만듭니다.
            # 한국어는 조사, 어미 등을 붙여 말을 만드는 교착어인데, 같은 단어임에도 서로 다른 조사가 붙어 다른 단어로 처리되는걸 방지하기 위함입니다.
            # 예를 들어, 그가, 그를, 그에게, 그와, 그는 이라는 단어를 '그'라는 단어 하나로 축소하기 위해 조사를 제거합니다.
            josa_delete_list = []
            for word in word_list:
                if word[1] != 'Josa':
                    josa_delete_list.append(word[0])
            
            #print(josa_delete_list)

            # 조사를 제거한 단어들을 이용하여 Inverted Index를 만듭니다.
            # Inverted Index는 마치 책 뒤의 단어 찾기와 비슷한 구조를 가집니다.
            # 검색엔진은 키워드를 바탕으로 유사한 문서를 찾아내는 시스템인데, Inverted Index 구조를 통해 효율적으로 문서를 찾을 수 있습니다.
            for word in josa_delete_list:
                if word not in term_dict:
                    term_dict[word] = {docNumber : 1}
                else:
                    if docNumber not in term_dict[word]:
                        term_dict[word][docNumber] = 1
                    else:
                        term_dict[word][docNumber] = term_dict[word][docNumber]+1              

#pprint.pprint(term_dict)
#print(len(term_dict))

#document_size 는 Title의 개수와 같습니다.
document_size = len(title_list)
tf_idf_weight_dict = {}

# 이후 TF-IDF Weight Dictionary를 만듭니다.
# Term Frequency - Inverse Document Frequency (TF-IDF) 는 각 단어의 중요도를 계산하는 고전적이지만 중요한 방법입니다.
# TF는 특정 단어가 문서 내에서 등장하는 횟수를 나타냅니다.
# 만약 한 문서에서 "의약품" 이라는 단어가 여러번 나왔다면, 해당 단어가 해당 문서에서 중요한 단어라고 가정할 수 있을 것입니다.
# DF는 한 단어가 몇 개의 문서에서 나왔는지를 측정합니다. 예를 들어 "의약품" 이란 단어가 총 100개의 문서 중 2개의 문서에서만 나왔다면, DF는 2입니다.
# IDF는 Inverse-DF로서, DF의 역수입니다. 기본적으론 (문서의 수 / DF) 로 정의됩니다.
# 만약, "나는" 이란 단어가 여러 Document에서 많이 나왔다면 "나는" 이란 단어는 흔히 사용되는, 중요하지 않은 단어일 것입니다.
# 하지만, "의약품" 이란 단어가 딱 2개의 Document에서만 등장한다면, "의약품" 이란 단어는 중요한 단어로 취급할 수 있을 것입니다.
# 따라서, TF * IDF 값을 사용하여 각 단어의 중요도를 측정합니다.
# 이 때, log 값을 사용하는 이유는 값이 지나치게 커지지 않도록 하기 위해서입니다.
# 단, tf-idf 수식은 여러 variation이 있습니다. 여러 알려진 수식 중 적절한 것을 선택할 수 있습니다.

for term in term_dict:
    doc_freq = len(term_dict[term])
    
    for document_number in term_dict[term]:
        document_count = term_dict[term][document_number]

        if term not in tf_idf_weight_dict:
            tf_idf_weight_dict[term] = {}

        tf_idf_weight_dict[term][document_number] = (1 + math.log10(document_count)) * math.log10(document_size/doc_freq)

# pprint.pprint(tf_idf_weight_dict)


# 이후, 한 Document를 Legnth가 1인 Vector로 표현하기 위해 Normalize합니다.
# Cosine Similarity를 통해 이후 Document의 유사도를 구하는데, 미리 Vector를 Normalzie 할 경우 기존 (A * B / (len(A) * len(B))) 의 수식을 A * B로 단순화할 수 있습니다.
# 따라서, Query 입력 이후 검색 시간과 연산량을 단축할 수 있습니다.

# doc_length_list : 정규화 전 각 Document Vetor의 길이를 계산할 리스트입니다.
doc_length_list = list(0 for i in range(0,100))

for term in tf_idf_weight_dict:
    
    for document_number in tf_idf_weight_dict[term]:
        doc_length_list[document_number] += tf_idf_weight_dict[term][document_number] * tf_idf_weight_dict[term][document_number]

for i in range (0, len(doc_length_list)):
    doc_length_list[i] = math.sqrt(doc_length_list[i])

for term in tf_idf_weight_dict:
    
    # 각 단어를 Document Vector의 L2 Norm으로 나누어 정규화합니다.
    for document_number in tf_idf_weight_dict[term]:
        tf_idf_weight_dict[term].update({document_number : tf_idf_weight_dict[term][document_number] / doc_length_list[document_number]})

readFile.close()


print("Document Preprocessing finished!")
# 예시를 단순화하기 위해, 한 코드에서 데이터 전처리 이후 Query를 받았지만, 만약 실제 운영환경이라면 전처리 시스템을 분리해서 운영해야 할 것입니다.
# ----- 전처리 끝 ------

# answer_dict는 Document의 개수만큼, 입력 Query로 들어온 문서와의 유사도를 비교 후 값을 저장할 List입니다.
answer_dict = {}

for i in range(0,100):
    answer_dict[i] = 0

# 사용자로부터 검색어를 입력받습니다.
# 예시 : 독일 작곡가
query_str = input("Please input query : ")

# 검색어를 전처리 했을 때와 같이, 조사를 분리하고 하나의 Document Vector로 처리합니다.
preprocess_query = okt.pos(query_str)
query = []
for word in preprocess_query:
    if word[1] != 'Josa':
        query.append(word[0])

print(f"input Query : {query}")

# 입력된 각 단어에 대해 tf_idf weight dictionary를 순회하며 유사도를 계산합니다.
for word in query:
    if word in tf_idf_weight_dict:
        for document_number in tf_idf_weight_dict[word]:
            answer_dict[document_number] += tf_idf_weight_dict[word][document_number]

# 이후, Document 유사도를 내림차순으로 정리하여 Query와 가장 유사한 Document를 계산합니다.
sorted_answer_dict = sorted(answer_dict.items(), key=lambda x: x[1], reverse=True)

# 이후, 상위 10개의 문서를 출력합니다.
for i in range(0,10):
    print(f"{title_list[sorted_answer_dict[i][0]]}유사도 : {int(sorted_answer_dict[i][1]*100)}%")