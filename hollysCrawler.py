from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

# 크롤링 작업을 실행하는 크롤링 함수
def hollys_store(result):
    for page in range(1, 56):       # 1 ~ 55 페이지까지 반복해서 url 설정
        Hollys_url = 'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo=%d&sido=&gugun=&store=' % page
        print(Hollys_url)

        html = urllib.request.urlopen(Hollys_url)           # url 요청하여 응답받은 웹 페이지 저장
        soupHollys = BeautifulSoup(html, 'html.parser')     # HTML 파싱(1: 분석할 HTML을 저장한 문재열 객체[html], 2: 사용할 분석기['html.parser'])
        tag_tbody = soupHollys.find('tbody')                # 해당 페이지의 매장 정보 테이블 저장

        for store in tag_tbody.find_all('tr'):              # 매장 정보 테이블에서 <tr> 태그(한 행: 매장 1개) 찾기
            if len(store) <= 3:                             # 전체의 마지막 tr인 경우 매장 정보가 없으므로 크롤링 작업 중단
                break
            store_td = store.find_all('td')                 # tr 태그의 하위 태그인 td 태그 중에서 필요한 항목만 추출하여 result 리스트에 추가 저장
            store_name = store_td[1].string
            store_sido = store_td[0].string
            store_address = store_td[3].string
            store_phone = store_td[5].string
            result.append([store_name] + [store_sido] + [store_address] + [store_phone])
    return

# 작업 프로세스를 정의한 메인 함수
def main():
    result = []     # 작업 결과를 저장할 리스트
    print('Hollys store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    hollys_store(result)        # 크롤링 작업 함수 호출
    hollys_tbl = pd.DataFrame(result, columns=('store', 'sido_gu', 'address', 'phone'))     # 크롤링한 데이터를 2차원 배열 형식인 DataFrame 형식으로 저장
    hollys_tbl.to_csv('./data/hollys.csv', encoding='cp949', mode='w', index=True)          # DataFrame을 csv 파일로 저장
    del result[:]                                                                           # 작업 결과 비우기

# main 함수 호출
if __name__ == '__main__':
    main()



