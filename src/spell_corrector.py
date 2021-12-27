from hanspell import spell_checker
from hanspell.constants import CheckResult
from symspellpy import SymSpell

def hanspell(data):
    result = spell_checker.check(data)
    wrong_spell = CheckResult.WRONG_SPELLING
    return getattr(result, 'checked')

def symspell(data):
    sym_spell = SymSpell()
    # https://heegyukim.medium.com/symspell%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-%ED%95%9C%EA%B8%80-%EB%A7%9E%EC%B6%A4%EB%B2%95-%EA%B5%90%EC%A0%95-3def9ca00805


def selenium(data):
    pass
    #https://hong-yp-ml-records.tistory.com/99

if __name__ == '__main__':
    data = """
    특히 늦은 시간에 잠을 자는 것과 행야 할 일을 뒤로 미루는 것이 고치고 싶은 생활 습관이다. 
    밤에 늦게 잠을 자는 습관 때문에 자주 습업에 늦는다.
    그래서 수업 시간에 자주 지각하다. """

    print("RAW DATA")
    print(data)
    print("________________________")

    print("CORRECTED HANSPELL")
    hanspell_corrected = hanspell(data)
    print(hanspell_corrected)
    print("________________________")