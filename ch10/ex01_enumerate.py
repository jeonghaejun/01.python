race = ['저그', '테란', '프로토스']

print(list(enumerate(race)))
# [(0, '저그'), (1, '테란'), (2, '프로토스')]


score = [88, 95, 70, 100, 99]

for no, s in enumerate(score, 1):
    print(str(no)+'번 학생의 성적 :', s)
    
# 1번 학생의 성적 : 88
# 2번 학생의 성적 : 95
# 3번 학생의 성적 : 70
# 4번 학생의 성적 : 100
# 5번 학생의 성적 : 99