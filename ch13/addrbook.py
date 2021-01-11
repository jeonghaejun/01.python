import sys
import traceback


def load_config():
    config = {}
    with open('config.ini', 'rt') as f:
        entries = f.readlines()
        for entry in entries:
            key, value = entry.split('=')
            config[key.strip()] = value.strip()
    return config


def load(fpath, encoding):
    with open(fpath, 'rt', encoding=encoding) as f:
        return f.readlines()


def save(book, fpath, encoding):
    # 문자열.join(시퀸스)
    # 1=[1,2] : ','.join(1) ==> '1,2'
    with open(fpath, 'wt', encoding=encoding) as f:
        f.write('이름,전화번호,email,주소\n')
        for name, value in book.items():
            scores = ','.join(value)
            line = f'{name},{scores}\n'
            f.write(line)

# {
# 이름:[전화번호,EMAIL,주소]
# }


def make_book(lines):
    book = {}
    for line in lines[1:]:  # 헤더 제거
        name, phone, email, addr = line.split(',')
        addr = addr.strip()  # 주소 공백제거
        book[name] = [phone, email, addr]
    return book


def init():
    config = load_config()
    lines = load(config['FNAME'], config['ENCODING'])
    book = make_book(lines)
    return book, config


# 목록 보여            R
# 특정인 상세정보       R
# 추가                 C
# 수정                 U
# 삭제                 D
# CRUD 작업(연산)


def select_menu():
    print('1)목록, 2)상세보기, 3)추가, 4)수정, 5)삭제, 6)종료')
    menu = int(input('입력 : '))
    return menu


def print_book(book):     # 주소록 목록 출력
    # 정렬해서 출력
    names = list(book.keys())
    names.sort()
    print('='*50)
    print('주소록')
    print('='*50)
    # 실제 데이터 출력
    # for name, info in book.items():  # .keys(), .values(), .entries()
    for name in names:
        info = book[name]
        print(f'{name} : {info[0]}, {info[1]}, {info[2]}')
    print('-'*50)


def print_detail(book):
    name = input('이름: ')   # 검색
    if name not in book:
        print(f'{name}은 목록에 없습니다.')
    else:
        info = book[name]  # 이름없으면 오류 해결방안 2가지 get(),in
        print(f'{name} : {info[0]}, {info[1]}, {info[2]}')


def add_entry(book):
    name = input('이름: ')
    if name in book:
        print(f'{name}은 이미 존재합니다.')
        return

    phone = input('전화번호: ')
    email = input('email: ')
    addr = input('주소: ')
    book[name] = [phone, email, addr]


def delete_entry(book):
    name = input('이름: ')
    if name not in book:
        print(f'{name}은 목록에 없습니다.')
        return

    ans = input('삭제할까요?(Y/N)')
    if ans == 'Y' or 'y':
        del book[name]


def update_entry(book):
    name = input('이름: ')
    if name not in book:
        print(f'{name}은 존재하지 않습니다.')
        return

    old_phone, old_email, old_addr = book[name]
    print('변경이 없는 경우 그냥 엔터')
    phone = input(f'전화번호({old_phone}): ')
    print(old_phone, phone)
    if phone.strip() == '':  # 내용 없이 엔터를 친경우
        phone = old_phone
    email = input(f'email({old_email}): ')
    if email.strip() == '':  # 내용 없이 엔터를 친경우
        email = old_email
    addr = input(f'주소({old_addr}): ')
    if addr.strip() == '':  # 내용 없이 엔터를 친경우
        addr = old_addr

    print(phone, email, addr)
    book[name] = [phone, email, addr]


def exit(book, fpath, encoding):
    # 종료 여부 질의,
    # 업데이트된 주소록을 저장:book,저장할 파일의 경로
    ans = input('종료할까요?(Y/N)')
    if ans == 'N':
        return
    save(book, fpath, encoding)
    sys.exit(0)


def run(menu, book, config):
    if menu == 1:     # 목록
        print_book(book)
    elif menu == 2:   # 상세보기
        print_detail(book)
    elif menu == 3:   # 추가
        add_entry(book)
    elif menu == 4:   # 수정
        update_entry(book)
    elif menu == 5:   # 삭제
        delete_entry(book)
    elif menu == 6:   # 종료
        exit(book, config['FNAME'], config['ENCODING'])
    else:
        print('잘못 선택했습니다.')


def main():
    try:
        book, config = init()
        while True:
            menu = select_menu()
            run(menu, book, config)
    except Exception as e:
        print('예외', e)
        # traceback.print_stack()  # 예외 위치까지 오는데 거친 함수 목록을 출력
        # traceback.print_exc()    # 구체적인 예외 내용을 출력


main()

# refactorint

# 구조화(structure/계층화)/ tree 구조 <---> 평탄(평평)하다 flat