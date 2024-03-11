# github 이용하면서 숙지해야 할 사항
_팀단위 프로젝트를 진행하기에 앞서 파일 공유 철저한 및 관리를 해야한다.아래는 그러한 상황을 미리방지하고자 꼭 숙지 바란다._

* main과 개별  branch 구분하기
    
    _branch는 앞으로 개별로 관리하는 프로젝트이다. 개인의 branch에서 프로젝트를 진행하며 완성된 프로젝트는 main으로 옮겨 관리할 것이다._
    
```
    * 현재 branch 위치 확인

        __git branch__
        
    * branch 생성
    
        __git branch [branch명]__
    
    * branch 삭제

        __git branch -D [branch명]__

    * branch 이동

        __git checkout [branch명]__

    * 특정 branch push 및 pull

        __git push origin [branch명]__
        __git pull origin [branch명]__ 

        if) github에 commit하고 싶을떄
```
* 로그 남기기
    
    _각자 주기적인 commit과 README.md나 txt로 로그 작성을 자주 해주면 좋겠다. 세부적인 commit은 프로젝트를 수정하기에 용이하다. 또한 로그를 남기면 commit한 날에 어떠한 수정 및 작성을 했는지 알 수 있어서 좋다._
    
    __결론적으로 주기적인 github 업데이트와 그때마다 어떤 업데이트를 했는지 아직 어떤 문제를 해결 못했는지 써주면 다른 팀원이 보기 편하기에 작지만 작은 습관을 가졌으면한다.__

    ```
    [날짜][시간][commit명][할말]
    ex) 

    [03/11][2:25][Braille recognition AI design0]
    1.~~한 오류 수정 2.새로운 ~~한 오류 생성됨
    [03/11][3:21][Braille recognition ai design1]
    1. ~~한 오류 수정
    ...
    ```
- - - 
# 하이퍼링크 : README 작성법 및 branch 관련 링크
README.md 작성법:
https://velog.io/@gmlstjq123/README.md-%ED%8C%8C%EC%9D%BC-%EC%9E%91%EC%84%B1%EB%B2%95

branch 관련 코드 :
https://mylko72.gitbooks.io/git/content/branch/checkout.html